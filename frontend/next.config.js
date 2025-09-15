/** @type {import('next').NextConfig} */
const nextConfig = {
  // Configuración de Next.js 14
  reactStrictMode: true,
  swcMinify: true,
  
  // Configuración de imágenes
  images: {
    domains: [],
  },

  // Configuración experimental (solo funciones estables)
  experimental: {
    // serverComponentsExternalPackages: ['@scope/package'],
  },
}

module.exports = nextConfig
