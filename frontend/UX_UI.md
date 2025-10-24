# Paleta de Colores - Sistema de Certificaciones

Este documento define la paleta de colores oficial del Sistema de Certificaciones.

## 🎨 Paleta Principal

### Primary (Azul Institucional Navy)
Color principal

```
primary-50:  #e6eef5  (Fondos claros, hover states suaves)
primary-100: #ccdde8  (Hover states, bordes activos)
primary-200: #99bbce  (Bordes y divisores)
primary-300: #6699b5  (Elementos secundarios)
primary-400: #33779c  (Hover en botones)
primary-500: #042a53  ⭐ COLOR PRINCIPAL
primary-600: #032242  (Hover en elementos primarios, botones activos)
primary-700: #031a32  (Estados activos, navegación seleccionada)
primary-800: #021221  (Textos oscuros sobre fondos claros)
primary-900: #010911  (Fondos oscuros, footer)
```

**Uso recomendado:**
- `primary-500`: Botones principales, íconos destacados, títulos principales
- `primary-600`: Hover de botones principales
- `primary-50`: Fondos de filtros activos, highlights sutiles
- `primary-100`: Scrollbars, bordes de inputs activos

---

### Secondary (Dorado)
Color complementario

```
secondary-50:  #fffbeb  (Fondos claros de alertas/warnings)
secondary-100: #fef3c7  (Highlights, badges)
secondary-200: #fde68a  (Bordes suaves)
secondary-300: #fcd34d  (Hover states)
secondary-400: #fbbf24  (Elementos interactivos)
secondary-500: #f59e0b  ⭐ DORADO
secondary-600: #d97706  (Hover)
secondary-700: #b45309  (Activo)
secondary-800: #92400e  (Textos sobre fondos claros)
secondary-900: #78350f  (Fondos oscuros)
```

**Uso recomendado:**
- `secondary-500`: Acentos en módulos, bordes destacados (módulos home)
- `secondary-100`: Badges de facultad, chips
- Decoración en cards de módulos principales

---

### Success (Verde)
Para mensajes de éxito, confirmaciones y estados positivos.

```
success-50:  #f0fdf4
success-100: #dcfce7
success-200: #bbf7d0
success-300: #86efac
success-400: #4ade80
success-500: #22c55e  ⭐ VERDE SUCCESS
success-600: #16a34a  (Hover)
success-700: #15803d  (Activo)
success-800: #166534
success-900: #14532d
```

**Uso recomendado:**
- Botones de editar/guardar
- Mensajes de operación exitosa
- Badges de estado "Completado"
- Iconos de confirmación

---

### Warning (Naranja)
Para alertas, avisos y acciones que requieren atención.

```
warning-50:  #fff7ed
warning-100: #ffedd5
warning-200: #fed7aa
warning-300: #fdba74
warning-400: #fb923c
warning-500: #f97316  ⭐ NARANJA WARNING
warning-600: #ea580c  (Hover)
warning-700: #c2410c  (Activo)
warning-800: #9a3412
warning-900: #7c2d12
```

**Uso recomendado:**
- Alertas de precaución
- Badges de "Pendiente"
- Mensajes informativos importantes
- Tooltips de advertencia

---

### Error (Rojo)
Para errores, eliminaciones y acciones destructivas.

```
error-50:  #fef2f2
error-100: #fee2e2
error-200: #fecaca
error-300: #fca5a5
error-400: #f87171
error-500: #ef4444  ⭐ ROJO ERROR
error-600: #dc2626  (Hover)
error-700: #b91c1c  (Activo)
error-800: #991b1b
error-900: #7f1d1d
```

**Uso recomendado:**
- Botones de eliminar
- Mensajes de error
- Bordes de inputs con error
- Modales de confirmación destructiva

---

### Info (Azul Claro)
Para información general y tooltips.

```
info-50:  #f0f9ff
info-100: #e0f2fe
info-200: #bae6fd
info-300: #7dd3fc
info-400: #38bdf8
info-500: #0ea5e9  ⭐ AZUL INFO
info-600: #0284c7  (Hover)
info-700: #0369a1  (Activo)
info-800: #075985
info-900: #0c4a6e
```

**Uso recomendado:**
- Badges de departamento (filtros)
- Mensajes informativos
- Tooltips y ayudas
- Enlaces secundarios

---

### Neutral (Grises)
Para textos, fondos, bordes y elementos de interfaz general.

```
neutral-50:  #fafafa  (Fondo principal de la app)
neutral-100: #f5f5f5  (Fondos secundarios, cards)
neutral-200: #e5e5e5  (Bordes, divisores)
neutral-300: #d4d4d4  (Bordes de inputs)
neutral-400: #a3a3a3  (Iconos deshabilitados, placeholders)
neutral-500: #737373  (Textos secundarios)
neutral-600: #525252  (Textos normales)
neutral-700: #404040  (Textos importantes)
neutral-800: #262626  (Textos destacados)
neutral-900: #171717  (Textos principales, títulos)
```

**Uso recomendado:**
- `neutral-50`: Background general de la aplicación
- `neutral-100`: Background de cards, tablas
- `neutral-200`: Bordes sutiles, divisores
- `neutral-300`: Bordes de inputs, separadores
- `neutral-500-700`: Textos secundarios y normales
- `neutral-900`: Títulos, textos importantes

---

## 📋 Guía de Uso por Componente

### Botones

```tsx
// Botón Principal
className="bg-primary-500 hover:bg-primary-600 text-white"

// Botón Secundario
className="border border-neutral-300 text-neutral-700 hover:bg-neutral-50"

// Botón Success (Guardar/Editar)
className="bg-success-600 hover:bg-success-700 text-white"

// Botón Error (Eliminar)
className="bg-error-600 hover:bg-error-700 text-white"
```

### Inputs y Filtros

```tsx
// Input normal
className="border-neutral-300 focus:border-primary-500 focus:ring-primary-500"

// Input con valor (activo)
className="border-primary-400 bg-primary-50"

// Input con error
className="border-error-400 bg-error-50"
```

### Badges y Chips

```tsx
// Badge de búsqueda
className="bg-primary-100 text-primary-800"

// Badge de facultad
className="bg-secondary-100 text-secondary-800"

// Badge de departamento
className="bg-info-100 text-info-800"

// Badge de éxito
className="bg-success-100 text-success-800"
```

### Tablas

```tsx
// Header de tabla
className="bg-neutral-50 text-neutral-500"

// Fila normal
className="bg-white hover:bg-primary-50"

// Bordes
className="border-neutral-200 divide-neutral-200"
```

### Modales y Cards

```tsx
// Modal
className="bg-white border border-neutral-200 shadow-xl"

// Card
className="bg-white border border-neutral-200 rounded-lg shadow-sm"

// Card hover
className="hover:shadow-lg transition-shadow"
```

---

## 🎯 Principios de Diseño

### 1. Jerarquía Visual
- **Primary (Navy)**: Acciones principales, navegación, branding
- **Secondary (Gold)**: Acentos, decoración
- **Semantic Colors**: Success/Warning/Error/Info según contexto

### 2. Contraste y Accesibilidad
- Usar `neutral-900` para textos principales sobre fondos claros
- Usar `white` para textos sobre fondos `primary-500` o más oscuros
- Ratios de contraste WCAG AA cumplidos en todas las combinaciones principales

### 3. Consistencia
- Usar siempre los mismos tonos para los mismos propósitos
- `primary-500` para todos los elementos de marca
- `neutral-50` como background principal de la app

### 4. Estados Interactivos
- **Normal**: Tono base (ej: `primary-500`)
- **Hover**: Tono +100 más oscuro (ej: `primary-600`)
- **Active/Pressed**: Tono +200 más oscuro (ej: `primary-700`)
- **Disabled**: `neutral-300` o `neutral-400`

---

## 🔧 Variables CSS

Las variables CSS están definidas en `globals.css`:

```css
:root {
  /* Colores institucionales */
  --color-primary: #042a53;
  --color-primary-light: #ccdde8;
  --color-primary-dark: #021221;
  
  --color-secondary: #f59e0b;
  --color-secondary-light: #fef3c7;
  
  --color-success: #22c55e;
  --color-warning: #f97316;
  --color-error: #ef4444;
  --color-info: #0ea5e9;
  
  /* Backgrounds */
  --bg-primary: #ffffff;
  --bg-secondary: #fafafa;
  --bg-tertiary: #f5f5f5;
  
  /* Text colors */
  --text-primary: #171717;
  --text-secondary: #525252;
  --text-tertiary: #a3a3a3;
}
```

---

## 📱 Ejemplos de Implementación

### Página de Módulos (Home)
```tsx
// Cards de módulos con borde dorado
<div className="bg-primary-500 border-b-4 border-secondary-500 hover:bg-primary-600">
  <Icon className="text-white" />
  <h3 className="text-white">Módulo</h3>
</div>
```

### Filtros y Búsqueda
```tsx
// Barra de búsqueda activa
<input className={`
  ${searchTerm 
    ? 'border-primary-400 bg-primary-50' 
    : 'border-neutral-300'
  }
  focus:ring-primary-500
`} />

// Filtro de facultad activo
<select className={`
  ${selectedFaculty !== 'all'
    ? 'border-secondary-400 bg-secondary-50'
    : 'border-neutral-300'
  }
`} />
```

### Tabla con Hover
```tsx
<tr className="hover:bg-primary-50">
  <td className="text-neutral-900">{data}</td>
  <td>
    <button className="text-success-600 hover:bg-success-50">
      <Edit />
    </button>
    <button className="text-error-600 hover:bg-error-50">
      <Trash2 />
    </button>
  </td>
</tr>
```
