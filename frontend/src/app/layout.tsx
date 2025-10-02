import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Sidebar from '@/components/layout/Sidebar'
import Header from '@/components/layout/Header'
import Breadcrumb from '@/components/layout/Breadcrumb'
import { SidebarProvider } from '@/contexts/SidebarContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Sistema de Certificaciones EPN',
  description: 'Sistema para obtención de publicaciones y generación de certificados para los docentes de la Escuela Politécnica Nacional',
  keywords: 'Scopus, publicaciones, análisis académico, investigación, estadísticas, reportes',
  icons: {
    icon: '/logo viiv.png',
    shortcut: '/logo viiv.png',
    apple: '/logo viiv.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <head>
        <link rel="icon" href="/logo viiv.png" type="image/png" />
        <link rel="shortcut icon" href="/logo viiv.png" type="image/png" />
        <link rel="apple-touch-icon" href="/logo viiv.png" />
      </head>
      <body className={inter.className}>
        <SidebarProvider>
          <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <Sidebar />
            
            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
              {/* Header */}
              <Header />
              
              {/* Page Content */}
              <main className="flex-1 overflow-x-hidden overflow-y-auto px-6 py-4">
                <Breadcrumb />
                {children}
              </main>
            </div>
          </div>
        </SidebarProvider>
      </body>
    </html>
  )
}
