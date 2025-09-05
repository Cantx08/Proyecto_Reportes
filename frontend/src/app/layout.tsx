import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Análisis de Publicaciones Scopus',
  description: 'Aplicación para analizar publicaciones académicas de Scopus, áreas temáticas y estadísticas por año',
  keywords: 'Scopus, publicaciones, análisis académico, investigación, estadísticas',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
