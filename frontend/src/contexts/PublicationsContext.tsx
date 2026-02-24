'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Publication } from '@/features/publications/types';
import { AuthorResponse } from '@/features/authors/types';

/**
 * Datos de publicaciones para generar certificados
 */
interface PublicationsData {
    publications: Publication[];
    subjectAreas: string[];
    documentsByYear: Record<string, number>;
    authorIds: string[];
    selectedAuthor?: AuthorResponse;
}

/**
 * Estado del contexto de publicaciones
 */
interface PublicationsContextState {
    data: PublicationsData | null;
    hasData: boolean;
    setPublicationsData: (data: PublicationsData) => void;
    clearPublicationsData: () => void;
}

const defaultState: PublicationsContextState = {
    data: null,
    hasData: false,
    setPublicationsData: () => {},
    clearPublicationsData: () => {},
};

const PublicationsContext = createContext<PublicationsContextState>(defaultState);

/**
 * Provider para compartir datos de publicaciones entre páginas
 */
export const PublicationsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [data, setData] = useState<PublicationsData | null>(null);

    const setPublicationsData = useCallback((newData: PublicationsData) => {
        setData(newData);
    }, []);

    const clearPublicationsData = useCallback(() => {
        setData(null);
    }, []);

    const value: PublicationsContextState = {
        data,
        hasData: data !== null && data.publications.length > 0,
        setPublicationsData,
        clearPublicationsData,
    };

    return (
        <PublicationsContext.Provider value={value}>
            {children}
        </PublicationsContext.Provider>
    );
};

/**
 * Hook para acceder al contexto de publicaciones
 */
export const usePublicationsContext = () => {
    const context = useContext(PublicationsContext);
    if (!context) {
        throw new Error('usePublicationsContext debe usarse dentro de PublicationsProvider');
    }
    return context;
};

export default PublicationsContext;
