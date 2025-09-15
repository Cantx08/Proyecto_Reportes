/**
 * Servicio de Monitoreo de Performance - Frontend
 * Sistema de Reportes de Publicaciones Académicas
 */

'use client';

import { useEffect, useRef } from 'react';

// ============================================================================
// TIPOS Y INTERFACES
// ============================================================================

interface PerformanceMetric {
  name: string;
  value: number;
  timestamp: number;
  url?: string;
  userAgent?: string;
}

interface ErrorReport {
  message: string;
  stack?: string;
  url: string;
  line?: number;
  column?: number;
  timestamp: number;
  userAgent: string;
  userId?: string;
}

interface UserSession {
  sessionId: string;
  startTime: number;
  pageViews: number;
  actions: string[];
  errors: number;
}

// ============================================================================
// MONITOREO DE PERFORMANCE
// ============================================================================

export class FrontendMonitor {
  private static instance: FrontendMonitor;
  private metrics: PerformanceMetric[] = [];
  private errors: ErrorReport[] = [];
  private session: UserSession;
  private isEnabled: boolean = true;

  private constructor() {
    this.session = {
      sessionId: this.generateSessionId(),
      startTime: Date.now(),
      pageViews: 0,
      actions: [],
      errors: 0
    };

    this.initializeMonitoring();
  }

  public static getInstance(): FrontendMonitor {
    if (!FrontendMonitor.instance) {
      FrontendMonitor.instance = new FrontendMonitor();
    }
    return FrontendMonitor.instance;
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substring(2)}`;
  }

  private initializeMonitoring(): void {
    if (typeof window === 'undefined') return;

    // Monitorear errores JavaScript
    window.addEventListener('error', (event) => {
      this.reportError({
        message: event.message,
        stack: event.error?.stack,
        url: event.filename || window.location.href,
        line: event.lineno,
        column: event.colno,
        timestamp: Date.now(),
        userAgent: navigator.userAgent
      });
    });

    // Monitorear errores de promesas no manejadas
    window.addEventListener('unhandledrejection', (event) => {
      this.reportError({
        message: `Unhandled Promise Rejection: ${event.reason}`,
        stack: event.reason?.stack,
        url: window.location.href,
        timestamp: Date.now(),
        userAgent: navigator.userAgent
      });
    });

    // Monitorear performance al cargar la página
    window.addEventListener('load', () => {
      this.measurePageLoad();
    });

    // Monitorear cambios de página
    this.trackPageViews();

    // Reportar métricas periódicamente
    setInterval(() => {
      this.sendMetrics();
    }, 30000); // Cada 30 segundos
  }

  /**
   * Medir performance de carga de página
   */
  private measurePageLoad(): void {
    if (!window.performance) return;

    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    
    if (navigation) {
      // Time to First Byte
      this.recordMetric('TTFB', navigation.responseStart - navigation.requestStart);
      
      // DOM Content Loaded
      this.recordMetric('DOMContentLoaded', navigation.domContentLoadedEventEnd - navigation.fetchStart);
      
      // Load Complete
      this.recordMetric('LoadComplete', navigation.loadEventEnd - navigation.fetchStart);
      
      // DNS Lookup
      this.recordMetric('DNSLookup', navigation.domainLookupEnd - navigation.domainLookupStart);
      
      // TCP Connection
      this.recordMetric('TCPConnection', navigation.connectEnd - navigation.connectStart);
    }

    // Core Web Vitals
    this.measureCoreWebVitals();
  }

  /**
   * Medir Core Web Vitals
   */
  private measureCoreWebVitals(): void {
    // Largest Contentful Paint (LCP)
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.recordMetric('LCP', lastEntry.startTime);
    }).observe({ entryTypes: ['largest-contentful-paint'] });

    // First Input Delay (FID)
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry: any) => {
        this.recordMetric('FID', entry.processingStart - entry.startTime);
      });
    }).observe({ entryTypes: ['first-input'] });

    // Cumulative Layout Shift (CLS)
    let clsValue = 0;
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      entries.forEach((entry: any) => {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      });
      this.recordMetric('CLS', clsValue);
    }).observe({ entryTypes: ['layout-shift'] });
  }

  /**
   * Registrar métrica de performance
   */
  public recordMetric(name: string, value: number): void {
    if (!this.isEnabled) return;

    const metric: PerformanceMetric = {
      name,
      value,
      timestamp: Date.now(),
      url: typeof window !== 'undefined' ? window.location.href : undefined,
      userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : undefined
    };

    this.metrics.push(metric);

    // Limitar cantidad de métricas en memoria
    if (this.metrics.length > 1000) {
      this.metrics = this.metrics.slice(-500);
    }

    console.log(`📊 Performance Metric - ${name}: ${value.toFixed(2)}ms`);
  }

  /**
   * Reportar error
   */
  private reportError(error: ErrorReport): void {
    if (!this.isEnabled) return;

    this.errors.push(error);
    this.session.errors++;

    // Limitar cantidad de errores en memoria
    if (this.errors.length > 100) {
      this.errors = this.errors.slice(-50);
    }

    console.error('🚨 Frontend Error:', error);
  }

  /**
   * Trackear vistas de página
   */
  private trackPageViews(): void {
    this.session.pageViews++;
    
    // En aplicaciones SPA, monitorear cambios de ruta
    if (typeof window !== 'undefined' && window.history) {
      const originalPushState = window.history.pushState;
      const originalReplaceState = window.history.replaceState;

      window.history.pushState = function(...args) {
        originalPushState.apply(window.history, args);
        FrontendMonitor.getInstance().session.pageViews++;
      };

      window.history.replaceState = function(...args) {
        originalReplaceState.apply(window.history, args);
        FrontendMonitor.getInstance().session.pageViews++;
      };

      window.addEventListener('popstate', () => {
        this.session.pageViews++;
      });
    }
  }

  /**
   * Trackear acción del usuario
   */
  public trackAction(action: string): void {
    if (!this.isEnabled) return;

    this.session.actions.push(`${Date.now()}:${action}`);
    
    // Limitar cantidad de acciones
    if (this.session.actions.length > 100) {
      this.session.actions = this.session.actions.slice(-50);
    }

    console.log(`👤 User Action: ${action}`);
  }

  /**
   * Medir tiempo de ejecución de función
   */
  public async measureFunction<T>(
    name: string,
    fn: () => Promise<T> | T
  ): Promise<T> {
    const start = performance.now();
    
    try {
      const result = await fn();
      const duration = performance.now() - start;
      this.recordMetric(`Function_${name}`, duration);
      return result;
    } catch (error) {
      const duration = performance.now() - start;
      this.recordMetric(`Function_${name}_Error`, duration);
      throw error;
    }
  }

  /**
   * Enviar métricas al backend
   */
  private async sendMetrics(): Promise<void> {
    if (this.metrics.length === 0 && this.errors.length === 0) return;

    try {
      const payload = {
        session: this.session,
        metrics: [...this.metrics],
        errors: [...this.errors],
        timestamp: Date.now()
      };

      // En desarrollo, solo loggear
      if (process.env.NODE_ENV === 'development') {
        console.log('📈 Performance Report:', payload);
        return;
      }

      // En producción, enviar al backend
      await fetch('/api/v1/monitoring/frontend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      // Limpiar métricas enviadas
      this.metrics = [];
      this.errors = [];

    } catch (error) {
      console.warn('Failed to send performance metrics:', error);
    }
  }

  /**
   * Obtener resumen de performance
   */
  public getPerformanceSummary(): {
    session: UserSession;
    metricsCount: number;
    errorsCount: number;
    avgMetrics: Record<string, number>;
  } {
    const avgMetrics: Record<string, number> = {};
    
    // Calcular promedios por tipo de métrica
    const metricGroups = this.metrics.reduce((acc, metric) => {
      if (!acc[metric.name]) {
        acc[metric.name] = [];
      }
      acc[metric.name].push(metric.value);
      return acc;
    }, {} as Record<string, number[]>);

    Object.entries(metricGroups).forEach(([name, values]) => {
      avgMetrics[name] = values.reduce((sum, val) => sum + val, 0) / values.length;
    });

    return {
      session: this.session,
      metricsCount: this.metrics.length,
      errorsCount: this.errors.length,
      avgMetrics
    };
  }

  /**
   * Habilitar/deshabilitar monitoreo
   */
  public setEnabled(enabled: boolean): void {
    this.isEnabled = enabled;
  }
}

// ============================================================================
// HOOK PARA USAR EN COMPONENTES REACT
// ============================================================================

export function usePerformanceMonitoring(componentName: string) {
  const monitor = FrontendMonitor.getInstance();
  const mountTime = useRef<number>(Date.now());

  useEffect(() => {
    const start = Date.now();
    monitor.trackAction(`Component_${componentName}_Mount`);

    return () => {
      const duration = Date.now() - start;
      monitor.recordMetric(`Component_${componentName}_Lifetime`, duration);
      monitor.trackAction(`Component_${componentName}_Unmount`);
    };
  }, [componentName, monitor]);

  const trackAction = (action: string) => {
    monitor.trackAction(`${componentName}_${action}`);
  };

  const measureFunction = <T>(name: string, fn: () => Promise<T> | T) => {
    return monitor.measureFunction(`${componentName}_${name}`, fn);
  };

  return {
    trackAction,
    measureFunction,
    recordMetric: monitor.recordMetric.bind(monitor)
  };
}

// ============================================================================
// INITIALIZACIÓN AUTOMÁTICA
// ============================================================================

// Inicializar automáticamente cuando se carga el módulo
if (typeof window !== 'undefined') {
  FrontendMonitor.getInstance();
}

export default FrontendMonitor;