import './globals.css'
import type {Metadata} from 'next'
import {Inter} from 'next/font/google'
import {SidebarProvider} from '@/contexts/SidebarContext'
import {PublicationsProvider} from '@/contexts/PublicationsContext'
import MainLayout from '@/components/layout/MainLayout'
import React from "react";

const inter = Inter({subsets: ['latin']})

export const metadata: Metadata = {
    title: 'Sistema de Certificaciones EPN',
    description: 'Sistema para obtención de publicaciones y generación de certificados para los docentes de la Escuela Politécnica Nacional',
    keywords: 'Scopus, publicaciones, análisis académico, investigación, estadísticas, reportes',
    icons: {
        icon: '/logo_viiv.png',
        shortcut: '/logo_viiv.png',
        apple: '/logo_viiv.png',
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
            <link rel="icon" href="/logo_viiv.png" type="image/png"/>
            <link rel="shortcut icon" href="/logo_viiv.png" type="image/png"/>
            <link rel="apple-touch-icon" href="/logo_viiv.png"/>
            <title>Sistema de Certificaciones DI</title>
        </head>
        <body className={inter.className}>
            <SidebarProvider>
                <PublicationsProvider>
                    <MainLayout>
                        {children}
                    </MainLayout>
                </PublicationsProvider>
            </SidebarProvider>
        </body>
        </html>
    )
}
