/**
 * Middleware de Next.js para Optimizaciones de Seguridad y Performance
 * Sistema de Reportes de Publicaciones Académicas
 */

import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // ============================================================================
  // HEADERS DE SEGURIDAD
  // ============================================================================

  // Prevenir MIME type sniffing
  response.headers.set('X-Content-Type-Options', 'nosniff');
  
  // Prevenir embedding en iframes
  response.headers.set('X-Frame-Options', 'DENY');
  
  // Habilitar protección XSS del navegador
  response.headers.set('X-XSS-Protection', '1; mode=block');
  
  // Controlar información de referrer
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Content Security Policy restrictiva
  const csp = [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    "font-src 'self' data:",
    "connect-src 'self' http://localhost:8000",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'"
  ].join('; ');
  
  response.headers.set('Content-Security-Policy', csp);

  // ============================================================================
  // HEADERS DE PERFORMANCE
  // ============================================================================

  // Cache estático para assets
  if (request.nextUrl.pathname.startsWith('/_next/static/')) {
    response.headers.set('Cache-Control', 'public, max-age=31536000, immutable');
  }
  
  // Cache para imágenes
  if (request.nextUrl.pathname.match(/\.(jpg|jpeg|png|gif|ico|svg|webp)$/)) {
    response.headers.set('Cache-Control', 'public, max-age=86400');
  }

  // ============================================================================
  // RATE LIMITING BÁSICO
  // ============================================================================

  const ip = request.ip || request.headers.get('x-forwarded-for') || 'unknown';
  
  // Rate limiting para rutas API
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const rateLimitKey = `rate_limit_${ip}`;
    
    // En producción, esto debería usar Redis o una base de datos
    // Para desarrollo, usamos headers para tracking básico
    const requests = parseInt(request.headers.get('x-request-count') || '0');
    
    if (requests > 100) { // 100 requests por período
      return new NextResponse('Too Many Requests', { status: 429 });
    }
    
    response.headers.set('x-request-count', String(requests + 1));
  }

  // ============================================================================
  // CORS PARA DESARROLLO
  // ============================================================================

  if (process.env.NODE_ENV === 'development') {
    response.headers.set('Access-Control-Allow-Origin', 'http://localhost:3000');
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  }

  // ============================================================================
  // PREVENCIÓN DE HOTLINKING
  // ============================================================================

  const referer = request.headers.get('referer');
  const host = request.headers.get('host');
  
  if (referer && host && !referer.includes(host) && 
      request.nextUrl.pathname.match(/\.(jpg|jpeg|png|gif|svg|webp)$/)) {
    return new NextResponse('Hotlinking not allowed', { status: 403 });
  }

  // ============================================================================
  // REDIRECCIONES DE SEGURIDAD
  // ============================================================================

  // Forzar HTTPS en producción
  if (process.env.NODE_ENV === 'production' && 
      request.headers.get('x-forwarded-proto') !== 'https') {
    return NextResponse.redirect(
      `https://${request.headers.get('host')}${request.nextUrl.pathname}${request.nextUrl.search}`,
      301
    );
  }

  return response;
}

// Configurar rutas donde aplicar el middleware
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};