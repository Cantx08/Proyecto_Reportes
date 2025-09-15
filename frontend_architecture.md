# Arquitectura Frontend - Next.js con Clean Architecture

## Estructura Propuesta para Frontend

```
frontend/
├── src/
│   ├── app/                        # App Router de Next.js 13+
│   │   ├── globals.css            # Estilos globales
│   │   ├── layout.tsx             # Layout raíz
│   │   ├── page.tsx               # Página principal
│   │   ├── loading.tsx            # Loading UI
│   │   ├── error.tsx              # Error UI
│   │   ├── not-found.tsx          # 404 UI
│   │   │
│   │   ├── autores/               # Páginas de autores
│   │   │   ├── page.tsx           # Lista de autores
│   │   │   ├── [id]/
│   │   │   │   ├── page.tsx       # Detalle de autor
│   │   │   │   └── editar/
│   │   │   │       └── page.tsx   # Editar autor
│   │   │   └── nuevo/
│   │   │       └── page.tsx       # Crear autor
│   │   │
│   │   ├── publicaciones/         # Páginas de publicaciones
│   │   │   ├── page.tsx           # Lista de publicaciones
│   │   │   ├── [id]/
│   │   │   │   ├── page.tsx       # Detalle de publicación
│   │   │   │   └── editar/
│   │   │   │       └── page.tsx   # Editar publicación
│   │   │   ├── buscar/
│   │   │   │   └── page.tsx       # Búsqueda en Scopus
│   │   │   └── sincronizar/
│   │   │       └── page.tsx       # Sincronizar con Scopus
│   │   │
│   │   ├── reportes/              # Páginas de reportes
│   │   │   ├── page.tsx           # Lista de reportes
│   │   │   ├── generar/
│   │   │   │   └── page.tsx       # Generar nuevo reporte
│   │   │   └── [id]/
│   │   │       └── page.tsx       # Ver reporte
│   │   │
│   │   └── api/                   # API Routes (opcional)
│   │       ├── auth/
│   │       └── health/
│   │
│   ├── components/                # Componentes reutilizables
│   │   ├── ui/                    # Componentes de UI básicos
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Table.tsx
│   │   │   ├── Chart.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   │
│   │   ├── forms/                 # Componentes de formularios
│   │   │   ├── AuthorForm.tsx
│   │   │   ├── PublicationForm.tsx
│   │   │   ├── ReportForm.tsx
│   │   │   └── ScopusSearchForm.tsx
│   │   │
│   │   ├── layout/                # Componentes de layout
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── Footer.tsx
│   │   │
│   │   ├── features/              # Componentes por funcionalidad
│   │   │   ├── author/
│   │   │   │   ├── AuthorList.tsx
│   │   │   │   ├── AuthorCard.tsx
│   │   │   │   ├── AuthorDetail.tsx
│   │   │   │   └── ScopusAccountManager.tsx
│   │   │   │
│   │   │   ├── publication/
│   │   │   │   ├── PublicationList.tsx
│   │   │   │   ├── PublicationCard.tsx
│   │   │   │   ├── PublicationDetail.tsx
│   │   │   │   ├── PublicationEditor.tsx
│   │   │   │   ├── ScopusImporter.tsx
│   │   │   │   └── CategoryMapper.tsx
│   │   │   │
│   │   │   ├── report/
│   │   │   │   ├── ReportGenerator.tsx
│   │   │   │   ├── ReportPreview.tsx
│   │   │   │   ├── ReportList.tsx
│   │   │   │   └── ReportConfiguration.tsx
│   │   │   │
│   │   │   └── charts/
│   │   │       ├── PublicationsByYear.tsx
│   │   │       ├── SubjectAreas.tsx
│   │   │       ├── QuartileDistribution.tsx
│   │   │       └── DocumentTypes.tsx
│   │   │
│   │   └── providers/             # Providers de contexto
│   │       ├── AuthProvider.tsx
│   │       ├── ThemeProvider.tsx
│   │       └── QueryProvider.tsx
│   │
│   ├── lib/                       # Lógica de negocio y utilidades
│   │   ├── api/                   # Cliente API
│   │   │   ├── client.ts          # Cliente HTTP base
│   │   │   ├── authors.ts         # API de autores
│   │   │   ├── publications.ts    # API de publicaciones
│   │   │   ├── reports.ts         # API de reportes
│   │   │   └── scopus.ts          # API de Scopus
│   │   │
│   │   ├── hooks/                 # Custom hooks
│   │   │   ├── useAuthor.ts
│   │   │   ├── usePublications.ts
│   │   │   ├── useScopusData.ts
│   │   │   ├── useReports.ts
│   │   │   └── useLocalStorage.ts
│   │   │
│   │   ├── stores/                # Estado global (Zustand)
│   │   │   ├── authStore.ts
│   │   │   ├── authorStore.ts
│   │   │   ├── publicationStore.ts
│   │   │   └── reportStore.ts
│   │   │
│   │   ├── utils/                 # Utilidades
│   │   │   ├── formatters.ts      # Formateo de datos
│   │   │   ├── validators.ts      # Validaciones
│   │   │   ├── constants.ts       # Constantes
│   │   │   ├── helpers.ts         # Funciones auxiliares
│   │   │   └── chartHelpers.ts    # Utilidades para gráficos
│   │   │
│   │   └── types/                 # Tipos TypeScript
│   │       ├── api.ts             # Tipos de API
│   │       ├── author.ts          # Tipos de autor
│   │       ├── publication.ts     # Tipos de publicación
│   │       ├── report.ts          # Tipos de reporte
│   │       └── common.ts          # Tipos comunes
│   │
│   └── styles/                    # Estilos
│       ├── globals.css           # Estilos globales
│       ├── components.css        # Estilos de componentes
│       └── themes/               # Temas
│           ├── light.css
│           └── dark.css
│
├── public/                        # Archivos estáticos
│   ├── images/
│   │   ├── logos/
│   │   └── icons/
│   ├── fonts/
│   └── favicon.ico
│
├── docs/                          # Documentación
│   ├── components.md
│   └── api.md
│
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── .env.local
├── .env.example
└── README.md
```

## Principios de Arquitectura Frontend

### 1. **Separación de Responsabilidades**
- **Pages**: Solo routing y composición de componentes
- **Components**: UI reutilizable sin lógica de negocio
- **Hooks**: Lógica de negocio y estado
- **Services**: Comunicación con APIs
- **Utils**: Funciones puras auxiliares

### 2. **Component Architecture**
```typescript
// Ejemplo de estructura de componente
interface AuthorCardProps {
  author: Author;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export function AuthorCard({ author, onEdit, onDelete }: AuthorCardProps) {
  // Solo lógica de presentación
  return (
    // JSX
  );
}
```

### 3. **Custom Hooks Pattern**
```typescript
// Hook para manejo de autores
export function useAuthor(id: string) {
  const [author, setAuthor] = useState<Author | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Lógica de negocio
  const updateAuthor = async (data: Partial<Author>) => {
    // Implementación
  };

  return { author, loading, error, updateAuthor };
}
```

### 4. **API Client Pattern**
```typescript
// Cliente API tipado
class AuthorAPI {
  static async getAll(): Promise<Author[]> {
    // Implementación
  }
  
  static async getById(id: string): Promise<Author> {
    // Implementación
  }
  
  static async create(data: CreateAuthorRequest): Promise<Author> {
    // Implementación
  }
}
```

### 5. **State Management**
- **Local State**: useState, useReducer para estado de componente
- **Server State**: TanStack Query para cache y sincronización
- **Global State**: Zustand para estado global simple
- **Forms**: React Hook Form para formularios complejos

### 6. **Error Handling**
```typescript
// Error Boundary para captura de errores
export function ErrorBoundary({ children }: { children: ReactNode }) {
  // Implementación de error boundary
}

// Hook para manejo de errores
export function useErrorHandler() {
  const handleError = useCallback((error: Error) => {
    // Log error, show notification, etc.
  }, []);
  
  return { handleError };
}
```

## Flujo de Datos

```
User Interaction → Component → Hook → API Client → Backend
                ↓
              State Update → Component Re-render
```

## Beneficios de esta Arquitectura

1. **Mantenibilidad**: Código organizado y fácil de entender
2. **Testabilidad**: Cada pieza se puede testear independientemente
3. **Reutilización**: Componentes y hooks reutilizables
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades
5. **Performance**: Optimizaciones de React y Next.js
6. **Developer Experience**: TypeScript, hot reload, dev tools

## Tecnologías Recomendadas

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand + TanStack Query
- **Forms**: React Hook Form + Zod
- **Charts**: Chart.js o Recharts
- **Testing**: Jest + React Testing Library
- **Linting**: ESLint + Prettier