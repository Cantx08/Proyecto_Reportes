# Frontend - Análisis de Publicaciones Scopus

Esta es la interfaz de usuario para el sistema de análisis de publicaciones académicas de Scopus. Construida con **Next.js 14**, **React 18**, **TypeScript** y **Tailwind CSS**.

## 🚀 Características

- **Interfaz moderna y responsiva** con Tailwind CSS
- **Validación en tiempo real** de IDs de Scopus
- **Campos dinámicos** para múltiples IDs de autor
- **Visualizaciones interactivas** con Chart.js
- **Arquitectura modular** con componentes reutilizables
- **TypeScript** para desarrollo type-safe
- **Hooks personalizados** para manejo de estado

## 📋 Prerrequisitos

- Node.js 18.17 o superior
- npm o yarn
- Backend en funcionamiento en `http://localhost:8000`

## 🛠️ Instalación

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.local.example .env.local
   # Editar .env.local con la URL del backend
   ```

3. **Ejecutar en modo desarrollo:**
   ```bash
   npm run dev
   ```

4. **Abrir en el navegador:**
   ```
   http://localhost:3000
   ```

## 📁 Estructura del Proyecto

```
src/
├── app/                    # App Router de Next.js 14
│   ├── layout.tsx         # Layout principal
│   ├── page.tsx           # Página principal
│   └── globals.css        # Estilos globales
├── components/            # Componentes React
│   ├── ScopusIdInput.tsx  # Input de IDs con validación
│   ├── PublicacionesList.tsx # Lista de publicaciones
│   ├── AreasTematicas.tsx # Sidebar de áreas temáticas
│   ├── DocumentosPorAnio.tsx # Gráfico de publicaciones por año
│   └── ErrorNotification.tsx # Notificaciones de error
├── hooks/                 # Hooks personalizados
│   └── useScopusData.ts   # Hook principal para datos de Scopus
├── services/              # Servicios de API
│   └── scopusApi.ts       # Cliente HTTP para backend
├── types/                 # Definiciones TypeScript
│   └── api.ts             # Tipos de la API
└── utils/                 # Utilidades
    └── helpers.ts         # Funciones auxiliares
```

## 🎨 Componentes Principales

### ScopusIdInput
- Validación en tiempo real de IDs
- Campos dinámicos (agregar/remover)
- Estados de carga y error
- Botones de acción (buscar/limpiar)

### PublicacionesList
- Lista paginada de publicaciones
- Información detallada por publicación
- Enlaces a DOI cuando están disponibles
- Diseño responsivo

### AreasTematicas
- Sidebar con áreas temáticas únicas
- Scroll vertical para listas largas
- Badges con colores distintivos

### DocumentosPorAnio
- Gráfico de barras interactivo
- Datos agrupados por año
- Responsive design
- Tooltips informativos

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm run dev

# Construcción para producción
npm run build

# Ejecutar versión de producción
npm run start

# Linting
npm run lint

# Verificación de tipos
npm run type-check
```

## 🌐 API Integration

El frontend se comunica con el backend a través de tres endpoints:

1. **POST /api/publicaciones**
   - Obtiene publicaciones por IDs de autor
   - Respuesta: Lista de publicaciones con metadatos

2. **POST /api/documentos-por-anio**
   - Obtiene estadísticas por año
   - Respuesta: Objeto con conteos por año

3. **POST /api/areas-tematicas**
   - Obtiene áreas temáticas únicas
   - Respuesta: Array de áreas temáticas

## 📱 Diseño Responsivo

- **Desktop:** Layout de 3 columnas con sidebar
- **Tablet:** Layout de 2 columnas
- **Mobile:** Layout de 1 columna con elementos apilados

## 🎯 Características de UX

- **Validación en tiempo real** de IDs de Scopus
- **Estados de carga** con spinners y mensajes
- **Notificaciones de error** con auto-dismiss
- **Estados vacíos** informativos
- **Navegación intuitiva** y accesible

## 🔧 Configuración

### Variables de Entorno

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENV=development
NEXT_PUBLIC_API_TIMEOUT=30000
```

### Tailwind CSS

Configurado con:
- Tema personalizado con colores del proyecto
- Animaciones personalizadas
- Utilities extendidas
- Responsive breakpoints

## 🚀 Deployment

### Vercel (Recomendado)
```bash
npm run build
vercel --prod
```

### Docker
```bash
docker build -t scopus-frontend .
docker run -p 3000:3000 scopus-frontend
```

### Build Manual
```bash
npm run build
npm run start
```

## 🐛 Solución de Problemas

### Error de Conexión con Backend
- Verificar que el backend esté ejecutándose en el puerto 8000
- Comprobar la variable `NEXT_PUBLIC_API_URL`
- Revisar configuración de CORS en el backend

### Problemas de TypeScript
- Ejecutar `npm run type-check` para verificar errores
- Verificar versiones de dependencias en `package.json`

### Errores de Estilo
- Ejecutar `npm run build` para verificar compilación de Tailwind
- Revisar importación de `globals.css` en `layout.tsx`

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📞 Soporte

Para soporte y preguntas, crear un issue en el repositorio del proyecto.
