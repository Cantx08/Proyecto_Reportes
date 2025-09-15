/**
 * Optimizaciones de Performance y Seguridad - Frontend
 * Sistema de Reportes de Publicaciones Académicas
 * Next.js + React + TypeScript
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

// ============================================================================
// SISTEMA DE CACHE CON LOCAL STORAGE Y SESSION STORAGE
// ============================================================================

export class ClientCacheManager {
  private static instance: ClientCacheManager;
  private readonly prefix = 'reportes_app_';
  
  public static getInstance(): ClientCacheManager {
    if (!ClientCacheManager.instance) {
      ClientCacheManager.instance = new ClientCacheManager();
    }
    return ClientCacheManager.instance;
  }

  /**
   * Obtener valor del cache con validación de TTL
   */
  get<T>(key: string, useSession: boolean = false): T | null {
    try {
      const storage = useSession ? sessionStorage : localStorage;
      const item = storage.getItem(this.prefix + key);
      
      if (!item) return null;
      
      const parsed = JSON.parse(item);
      
      // Verificar TTL
      if (parsed.expiry && Date.now() > parsed.expiry) {
        this.delete(key, useSession);
        return null;
      }
      
      return parsed.data;
    } catch (error) {
      console.warn('Cache get error:', error);
      return null;
    }
  }

  /**
   * Almacenar valor en cache con TTL opcional
   */
  set<T>(key: string, data: T, ttlMinutes: number = 60, useSession: boolean = false): boolean {
    try {
      const storage = useSession ? sessionStorage : localStorage;
      const item = {
        data,
        expiry: ttlMinutes > 0 ? Date.now() + (ttlMinutes * 60 * 1000) : null,
        timestamp: Date.now()
      };
      
      storage.setItem(this.prefix + key, JSON.stringify(item));
      return true;
    } catch (error) {
      console.warn('Cache set error:', error);
      return false;
    }
  }

  /**
   * Eliminar valor del cache
   */
  delete(key: string, useSession: boolean = false): boolean {
    try {
      const storage = useSession ? sessionStorage : localStorage;
      storage.removeItem(this.prefix + key);
      return true;
    } catch (error) {
      console.warn('Cache delete error:', error);
      return false;
    }
  }

  /**
   * Limpiar cache expirado
   */
  cleanup(): number {
    let cleaned = 0;
    try {
      [localStorage, sessionStorage].forEach(storage => {
        const keys = Object.keys(storage).filter(key => key.startsWith(this.prefix));
        
        keys.forEach(key => {
          const item = storage.getItem(key);
          if (item) {
            try {
              const parsed = JSON.parse(item);
              if (parsed.expiry && Date.now() > parsed.expiry) {
                storage.removeItem(key);
                cleaned++;
              }
            } catch (e) {
              storage.removeItem(key);
              cleaned++;
            }
          }
        });
      });
    } catch (error) {
      console.warn('Cache cleanup error:', error);
    }
    return cleaned;
  }

  /**
   * Invalidar cache por patrón
   */
  invalidatePattern(pattern: string): number {
    let invalidated = 0;
    try {
      [localStorage, sessionStorage].forEach(storage => {
        const keys = Object.keys(storage).filter(key => 
          key.startsWith(this.prefix) && key.includes(pattern)
        );
        
        keys.forEach(key => {
          storage.removeItem(key);
          invalidated++;
        });
      });
    } catch (error) {
      console.warn('Cache invalidation error:', error);
    }
    return invalidated;
  }
}

// ============================================================================
// HOOKS OPTIMIZADOS PARA FETCHING DE DATOS
// ============================================================================

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  lastFetch: number | null;
}

/**
 * Hook optimizado para fetching con cache, debounce y retry
 */
export function useOptimizedFetch<T>(
  url: string,
  options: {
    cacheKey?: string;
    cacheTTL?: number;
    dependencies?: any[];
    debounceMs?: number;
    retryAttempts?: number;
    retryDelay?: number;
  } = {}
) {
  const {
    cacheKey = url,
    cacheTTL = 5,
    dependencies = [],
    debounceMs = 300,
    retryAttempts = 3,
    retryDelay = 1000
  } = options;

  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: false,
    error: null,
    lastFetch: null
  });

  const cache = ClientCacheManager.getInstance();

  const fetchData = useCallback(async (attempt = 0): Promise<void> => {
    // Verificar cache primero
    const cachedData = cache.get<T>(cacheKey);
    if (cachedData && state.lastFetch && Date.now() - state.lastFetch < cacheTTL * 60 * 1000) {
      setState(prev => ({ ...prev, data: cachedData, loading: false }));
      return;
    }

    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
        // Timeout de 30 segundos
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Cachear resultado
      cache.set(cacheKey, data, cacheTTL);
      
      setState({
        data,
        loading: false,
        error: null,
        lastFetch: Date.now()
      });

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      
      // Retry logic
      if (attempt < retryAttempts) {
        setTimeout(() => {
          fetchData(attempt + 1);
        }, retryDelay * Math.pow(2, attempt)); // Exponential backoff
        return;
      }

      setState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage
      }));
    }
  }, [url, cacheKey, cacheTTL, retryAttempts, retryDelay]);

  // Debounced fetch
  const debouncedFetch = useMemo(() => {
    let timeoutId: NodeJS.Timeout;
    return () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(fetchData, debounceMs);
    };
  }, [fetchData, debounceMs]);

  useEffect(() => {
    debouncedFetch();
    return () => {
      // Cleanup timeout on unmount
    };
  }, dependencies);

  const refetch = useCallback(() => {
    cache.delete(cacheKey);
    fetchData();
  }, [fetchData, cacheKey, cache]);

  return {
    ...state,
    refetch
  };
}

// ============================================================================
// VALIDACIONES DE ENTRADA DEL CLIENTE
// ============================================================================

export class ClientValidator {
  // Schemas de validación con Zod
  static readonly scopusIdSchema = z.string()
    .regex(/^\d{10,11}$/, 'Scopus ID debe tener 10-11 dígitos numéricos');

  static readonly emailSchema = z.string()
    .email('Formato de email inválido')
    .max(255, 'Email demasiado largo');

  static readonly authorSchema = z.object({
    first_name: z.string()
      .min(1, 'Nombre es requerido')
      .max(255, 'Nombre demasiado largo')
      .regex(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/, 'Nombre contiene caracteres inválidos'),
    last_name: z.string()
      .min(1, 'Apellido es requerido')
      .max(255, 'Apellido demasiado largo')
      .regex(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/, 'Apellido contiene caracteres inválidos'),
    email: ClientValidator.emailSchema.optional(),
    title: z.string().max(50, 'Título demasiado largo').optional(),
    position: z.string().max(255, 'Posición demasiado larga').optional()
  });

  static readonly publicationYearSchema = z.number()
    .int('Año debe ser un número entero')
    .min(1900, 'Año debe ser mayor a 1900')
    .max(new Date().getFullYear() + 1, 'Año no puede ser futuro');

  /**
   * Sanitizar string eliminando caracteres peligrosos
   */
  static sanitizeString(input: string): string {
    return input
      .replace(/[<>]/g, '') // Remover < y >
      .replace(/javascript:/gi, '') // Remover javascript:
      .replace(/on\w+=/gi, '') // Remover event handlers
      .trim();
  }

  /**
   * Validar Scopus ID
   */
  static validateScopusId(scopusId: string): { isValid: boolean; error?: string } {
    try {
      ClientValidator.scopusIdSchema.parse(scopusId);
      return { isValid: true };
    } catch (error) {
      if (error instanceof z.ZodError) {
        return { isValid: false, error: error.errors[0]?.message || 'Error de validación' };
      }
      return { isValid: false, error: 'Error de validación' };
    }
  }

  /**
   * Validar datos de autor
   */
  static validateAuthor(authorData: any): { isValid: boolean; errors?: Record<string, string> } {
    try {
      ClientValidator.authorSchema.parse(authorData);
      return { isValid: true };
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errors: Record<string, string> = {};
        error.errors.forEach((err: z.ZodIssue) => {
          if (err.path.length > 0) {
            errors[err.path[0] as string] = err.message;
          }
        });
        return { isValid: false, errors };
      }
      return { isValid: false, errors: { general: 'Error de validación' } };
    }
  }
}

// ============================================================================
// RATE LIMITING DEL CLIENTE
// ============================================================================

export class ClientRateLimiter {
  private static requests: Map<string, number[]> = new Map();

  /**
   * Verificar si una acción está permitida según rate limiting
   */
  static isAllowed(action: string, maxRequests: number = 10, windowMs: number = 60000): boolean {
    const now = Date.now();
    const windowStart = now - windowMs;
    
    // Obtener requests previos para esta acción
    const prevRequests = this.requests.get(action) || [];
    
    // Filtrar requests dentro de la ventana de tiempo
    const recentRequests = prevRequests.filter(time => time > windowStart);
    
    // Verificar si se excede el límite
    if (recentRequests.length >= maxRequests) {
      return false;
    }
    
    // Agregar el request actual
    recentRequests.push(now);
    this.requests.set(action, recentRequests);
    
    return true;
  }

  /**
   * Limpiar requests antiguos
   */
  static cleanup(): void {
    const now = Date.now();
    this.requests.forEach((requests, action) => {
      const filtered = requests.filter(time => now - time < 300000); // 5 minutos
      if (filtered.length === 0) {
        this.requests.delete(action);
      } else {
        this.requests.set(action, filtered);
      }
    });
  }
}

// ============================================================================
// OPTIMIZACIONES DE PERFORMANCE DE COMPONENTES
// ============================================================================

/**
 * Hook para virtualización de listas grandes
 */
export function useVirtualization(
  itemCount: number,
  itemHeight: number,
  containerHeight: number
) {
  const [scrollTop, setScrollTop] = useState(0);
  
  const visibleStart = Math.floor(scrollTop / itemHeight);
  const visibleEnd = Math.min(
    itemCount - 1,
    Math.floor((scrollTop + containerHeight) / itemHeight)
  );
  
  const offsetY = visibleStart * itemHeight;
  const visibleItems = Math.max(0, visibleEnd - visibleStart + 1);
  
  return {
    visibleStart,
    visibleEnd,
    offsetY,
    visibleItems,
    setScrollTop
  };
}

/**
 * Hook para debouncing de inputs
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook para lazy loading de imágenes
 */
export function useLazyLoad(ref: React.RefObject<HTMLElement>) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(element);

    return () => observer.disconnect();
  }, [ref]);

  return isVisible;
}

// ============================================================================
// MIDDLEWARE DE SEGURIDAD PARA NEXT.JS
// ============================================================================

export function securityMiddleware(request: NextRequest) {
  const response = NextResponse.next();

  // Headers de seguridad
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;"
  );

  // CORS para desarrollo
  if (process.env.NODE_ENV === 'development') {
    response.headers.set('Access-Control-Allow-Origin', 'http://localhost:3000');
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  }

  return response;
}

// ============================================================================
// UTILIDADES DE PERFORMANCE
// ============================================================================

export class PerformanceUtils {
  /**
   * Medir tiempo de ejecución de una función
   */
  static async measureAsync<T>(
    name: string,
    fn: () => Promise<T>
  ): Promise<{ result: T; duration: number }> {
    const start = performance.now();
    try {
      const result = await fn();
      const duration = performance.now() - start;
      console.log(`⚡ ${name}: ${duration.toFixed(2)}ms`);
      return { result, duration };
    } catch (error) {
      const duration = performance.now() - start;
      console.error(`❌ ${name} failed after ${duration.toFixed(2)}ms:`, error);
      throw error;
    }
  }

  /**
   * Throttle function
   */
  static throttle<T extends (...args: any[]) => any>(
    func: T,
    delay: number
  ): (...args: Parameters<T>) => void {
    let lastCall = 0;
    return (...args: Parameters<T>) => {
      const now = Date.now();
      if (now - lastCall >= delay) {
        lastCall = now;
        func(...args);
      }
    };
  }

  /**
   * Preload critical resources
   */
  static preloadResource(href: string, as: string = 'fetch'): void {
    if (typeof window !== 'undefined') {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = href;
      link.as = as;
      document.head.appendChild(link);
    }
  }

  /**
   * Lazy load non-critical resources
   */
  static lazyLoadScript(src: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (typeof window === 'undefined') {
        resolve();
        return;
      }

      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve();
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }
}

// ============================================================================
// CONFIGURACIÓN DE OPTIMIZACIONES AUTOMÁTICAS
// ============================================================================

// Limpiar cache automáticamente cada 5 minutos
if (typeof window !== 'undefined') {
  setInterval(() => {
    const cache = ClientCacheManager.getInstance();
    const cleaned = cache.cleanup();
    if (cleaned > 0) {
      console.log(`🧹 Cleaned ${cleaned} expired cache entries`);
    }
    
    ClientRateLimiter.cleanup();
  }, 5 * 60 * 1000);
}

// Preload critical API endpoints
if (typeof window !== 'undefined') {
  window.addEventListener('load', () => {
    PerformanceUtils.preloadResource('/api/v1/health');
    PerformanceUtils.preloadResource('/api/v1/authors/search');
  });
}