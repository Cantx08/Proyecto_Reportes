'use client';

import React from 'react'; // Ya no necesitamos useState
import Sidebar from './Sidebar';
import Header from './Header';
import { SidebarProvider } from '@/src/contexts/SidebarContext';

interface MainLayoutProps {
    children: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
    return (
        <SidebarProvider>
            <div className="flex h-screen bg-neutral-50 overflow-hidden">
                <Sidebar />

                <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
                    {/* HEADER */}
                    <Header />

                    <main>
                        <div className="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
                            {children}
                        </div>
                    </main>
                </div>
            </div>
        </SidebarProvider>
    );
}