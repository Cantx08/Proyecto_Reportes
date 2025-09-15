"""
Optimizaciones de Performance y Seguridad - Backend
Sistema de Reportes de Publicaciones Académicas
"""

from functools import wraps
from typing import Optional, Dict, Any, List
import time
import hashlib
import redis
import logging
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from ratelimit import limits, sleep_and_retry
import asyncio

# Configuración de logging estructurado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(extra)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# SISTEMA DE CACHE CON REDIS
# ============================================================================

class CacheManager:
    """Gestor de cache Redis con TTL y invalidación inteligente"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = 3600  # 1 hora
        
    def get_cache_key(self, prefix: str, **kwargs) -> str:
        """Genera una clave de cache única basada en parámetros"""
        key_parts = [prefix]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        return ":".join(key_parts)
    
    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Almacena un valor en el cache"""
        try:
            ttl = ttl or self.default_ttl
            self.redis_client.setex(key, ttl, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    def delete(self, pattern: str) -> int:
        """Elimina claves que coincidan con un patrón"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
        return 0
    
    def invalidate_author_cache(self, author_id: int):
        """Invalida cache relacionado con un autor específico"""
        patterns = [
            f"author:{author_id}:*",
            f"publications:author:{author_id}:*",
            f"reports:author:{author_id}:*"
        ]
        for pattern in patterns:
            self.delete(pattern)

# Instancia global del cache
cache_manager = CacheManager()

# ============================================================================
# DECORADORES DE CACHE
# ============================================================================

def cached(prefix: str, ttl: Optional[int] = None):
    """Decorador para cachear resultados de funciones"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generar clave de cache
            cache_key = cache_manager.get_cache_key(prefix, **kwargs)
            
            # Intentar obtener del cache
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit: {cache_key}")
                return cached_result
            
            # Ejecutar función y cachear resultado
            result = await func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            logger.info(f"Cache miss, stored: {cache_key}")
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = cache_manager.get_cache_key(prefix, **kwargs)
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# ============================================================================
# SISTEMA DE RATE LIMITING
# ============================================================================

class RateLimiter:
    """Rate limiter con diferentes límites por endpoint"""
    
    def __init__(self):
        self.redis_client = redis.from_url("redis://localhost:6379")
    
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        """Verifica si una solicitud está dentro del límite"""
        try:
            current = self.redis_client.get(key)
            if current is None:
                self.redis_client.setex(key, window, 1)
                return True
            
            if int(current) < limit:
                self.redis_client.incr(key)
                return True
            
            return False
        except Exception as e:
            logger.warning(f"Rate limiter error: {e}")
            return True  # Fallar abierto en caso de error

rate_limiter = RateLimiter()

def rate_limit(requests_per_minute: int = 60):
    """Decorador para rate limiting"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host
            key = f"rate_limit:{client_ip}:{func.__name__}"
            
            if not rate_limiter.is_allowed(key, requests_per_minute, 60):
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# ============================================================================
# SISTEMA DE AUTENTICACIÓN Y AUTORIZACIÓN
# ============================================================================

class SecurityManager:
    """Gestor de seguridad con JWT y validaciones"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
    
    def hash_password(self, password: str) -> str:
        """Hash de contraseña con bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verificar contraseña"""
        return self.pwd_context.verify(password, hashed)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None):
        """Crear token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Obtener usuario actual desde token"""
        payload = self.verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )
        return payload

# ============================================================================
# VALIDACIONES DE ENTRADA
# ============================================================================

class InputValidator:
    """Validador de entrada con sanitización"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """Sanitizar string de entrada"""
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        
        # Remover caracteres peligrosos
        sanitized = value.strip()
        sanitized = sanitized.replace('<', '&lt;').replace('>', '&gt;')
        
        if len(sanitized) > max_length:
            raise ValueError(f"String too long. Max length: {max_length}")
        
        return sanitized
    
    @staticmethod
    def validate_scopus_id(scopus_id: str) -> str:
        """Validar formato de Scopus ID"""
        if not scopus_id.isdigit() or len(scopus_id) not in [10, 11]:
            raise ValueError("Scopus ID must be 10-11 digits")
        return scopus_id
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validar formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()
    
    @staticmethod
    def validate_year(year: int) -> int:
        """Validar año de publicación"""
        current_year = datetime.now().year
        if year < 1900 or year > current_year + 1:
            raise ValueError(f"Year must be between 1900 and {current_year + 1}")
        return year

# ============================================================================
# OPTIMIZACIONES DE BASE DE DATOS
# ============================================================================

class DatabaseOptimizer:
    """Optimizador de consultas de base de datos"""
    
    @staticmethod
    def get_optimized_author_query() -> str:
        """Query optimizada para obtener autores con información completa"""
        return """
        SELECT 
            a.id,
            a.full_name,
            a.email,
            d.name as department_name,
            COUNT(DISTINCT sa.id) as scopus_accounts_count,
            COUNT(DISTINCT p.id) as publications_count,
            COALESCE(SUM(p.citation_count), 0) as total_citations
        FROM authors a
        LEFT JOIN departments d ON a.department_id = d.id
        LEFT JOIN scopus_accounts sa ON a.id = sa.author_id AND sa.is_active = true
        LEFT JOIN publication_authors pa ON a.id = pa.author_id
        LEFT JOIN publications p ON pa.publication_id = p.id
        WHERE a.is_active = true
        GROUP BY a.id, a.full_name, a.email, d.name
        ORDER BY a.full_name
        """
    
    @staticmethod
    def get_optimized_publications_query(author_id: int, year: Optional[int] = None) -> str:
        """Query optimizada para publicaciones de un autor"""
        base_query = """
        SELECT 
            p.id,
            p.title,
            p.publication_year,
            j.title as journal_title,
            p.citation_count,
            p.doi,
            p.is_included_in_report
        FROM publications p
        LEFT JOIN journals j ON p.journal_id = j.id
        JOIN publication_authors pa ON p.id = pa.publication_id
        WHERE pa.author_id = :author_id
        """
        
        if year:
            base_query += " AND p.publication_year = :year"
        
        base_query += " ORDER BY p.publication_year DESC, p.title"
        return base_query
    
    @staticmethod
    async def execute_with_connection_pool(query: str, params: Dict[str, Any], session: Session):
        """Ejecutar query con pool de conexiones optimizado"""
        try:
            result = session.execute(text(query), params)
            return result.fetchall()
        except Exception as e:
            logger.error(f"Database query error: {e}")
            raise HTTPException(status_code=500, detail="Database query failed")

# ============================================================================
# MONITOREO Y MÉTRICAS
# ============================================================================

class PerformanceMonitor:
    """Monitor de performance de la aplicación"""
    
    def __init__(self):
        self.metrics = {}
    
    def time_function(self, func_name: str):
        """Decorador para medir tiempo de ejecución"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self.record_metric(func_name, execution_time, "success")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self.record_metric(func_name, execution_time, "error")
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self.record_metric(func_name, execution_time, "success")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self.record_metric(func_name, execution_time, "error")
                    raise
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator
    
    def record_metric(self, name: str, execution_time: float, status: str):
        """Registrar métrica de performance"""
        if name not in self.metrics:
            self.metrics[name] = {"count": 0, "total_time": 0, "errors": 0}
        
        self.metrics[name]["count"] += 1
        self.metrics[name]["total_time"] += execution_time
        
        if status == "error":
            self.metrics[name]["errors"] += 1
        
        logger.info(f"Performance metric: {name} took {execution_time:.3f}s status:{status}")
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Obtener resumen de métricas"""
        summary = {}
        for name, data in self.metrics.items():
            avg_time = data["total_time"] / data["count"] if data["count"] > 0 else 0
            error_rate = (data["errors"] / data["count"] * 100) if data["count"] > 0 else 0
            
            summary[name] = {
                "call_count": data["count"],
                "average_time": round(avg_time, 3),
                "error_rate": round(error_rate, 2),
                "total_errors": data["errors"]
            }
        
        return summary

# Instancia global del monitor
performance_monitor = PerformanceMonitor()

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD PARA FASTAPI
# ============================================================================

def get_security_headers_middleware():
    """Middleware para agregar headers de seguridad"""
    async def security_headers_middleware(request: Request, call_next):
        response = await call_next(request)
        
        # Headers de seguridad
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
    
    return security_headers_middleware

# ============================================================================
# EJEMPLO DE USO EN ENDPOINTS
# ============================================================================

"""
# Ejemplo de uso en un endpoint de FastAPI:

from .optimizations import cached, rate_limit, performance_monitor, InputValidator

@router.get("/authors/{author_id}")
@rate_limit(requests_per_minute=100)
@performance_monitor.time_function("get_author")
@cached("author", ttl=1800)  # Cache por 30 minutos
async def get_author(
    author_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    # Validar entrada
    if author_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid author ID")
    
    # Ejecutar query optimizada
    query = DatabaseOptimizer.get_optimized_author_query()
    result = await DatabaseOptimizer.execute_with_connection_pool(
        query, 
        {"author_id": author_id}, 
        db
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return result[0]

@router.post("/authors")
@rate_limit(requests_per_minute=30)  # Límite más estricto para creación
@performance_monitor.time_function("create_author")
async def create_author(
    author_data: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    # Validar y sanitizar entrada
    try:
        author_data["first_name"] = InputValidator.sanitize_string(author_data["first_name"])
        author_data["last_name"] = InputValidator.sanitize_string(author_data["last_name"])
        if "email" in author_data:
            author_data["email"] = InputValidator.validate_email(author_data["email"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Crear autor
    # ... lógica de creación ...
    
    # Invalidar cache relacionado
    cache_manager.delete("authors:*")
    
    return {"message": "Author created successfully"}
"""