/** @type {import('next').NextConfig} */
const nextConfig = {
  // ============================================================================
  // OPTIMIZACIONES DE PERFORMANCE
  // ============================================================================
  
  // Configuración de React
  reactStrictMode: true,
  swcMinify: true,
  
  // Compresión automática de assets
  compress: true,
  
  // Optimizaciones de webpack
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Optimizar el tamaño del bundle
    if (!dev && !isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            priority: 10,
            enforce: true,
          },
          common: {
            name: 'common',
            minChunks: 2,
            priority: 5,
            reuseExistingChunk: true,
          },
        },
      };
    }

    return config;
  },

  // ============================================================================
  // CONFIGURACIONES DE SEGURIDAD
  // ============================================================================
  
  // Headers de seguridad
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains; preload'
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()'
          }
        ],
      },
    ];
  },

  // ============================================================================
  // CONFIGURACIONES DE IMAGEN
  // ============================================================================
  
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    quality: 85,
  },

  // ============================================================================
  // CONFIGURACIONES EXPERIMENTALES
  // ============================================================================
  
  experimental: {
    optimizeCss: true,
  },

  // ============================================================================
  // CONFIGURACIONES DE OUTPUT
  // ============================================================================
  
  output: 'standalone',
  trailingSlash: false,

  // ============================================================================
  // CONFIGURACIONES DE PRODUCCIÓN
  // ============================================================================
  
  ...(process.env.NODE_ENV === 'production' && {
    compiler: {
      removeConsole: {
        exclude: ['error', 'warn'],
      },
    },
  }),

  // ============================================================================
  // REDIRECTS Y REWRITES
  // ============================================================================
  
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/:path*`,
      },
    ];
  },
}

module.exports = nextConfig
