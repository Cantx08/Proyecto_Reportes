/**
 * Formatea un número agregando separadores de miles
 */
export const formatNumber = (num: number): string => {
  return new Intl.NumberFormat('es-ES').format(num);
};

/**
 * Trunca un texto a una longitud específica y agrega puntos suspensivos
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + '...';
};

/**
 * Capitaliza la primera letra de cada palabra
 */
export const capitalizeWords = (text: string): string => {
  return text
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

/**
 * Valida si una URL es válida
 */
export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

/**
 * Genera un ID único simple
 */
export const generateId = (): string => {
  return Math.random().toString(36).substr(2, 9);
};

/**
 * Debounce function para retrasar la ejecución de una función
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  waitFor: number
): (...args: Parameters<T>) => void => {
  let timeout: NodeJS.Timeout | null = null;
  
  return (...args: Parameters<T>): void => {
    if (timeout !== null) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => func(...args), waitFor);
  };
};

/**
 * Ordena un array de objetos por una propiedad específica
 */
export const sortBy = <T>(
  array: T[],
  key: keyof T,
  direction: 'asc' | 'desc' = 'asc'
): T[] => {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    
    if (aVal < bVal) return direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return direction === 'asc' ? 1 : -1;
    return 0;
  });
};

/**
 * Filtra valores únicos de un array
 */
export const unique = <T>(array: T[]): T[] => {
  return Array.from(new Set(array));
};

/**
 * Agrupa un array de objetos por una propiedad específica
 */
export const groupBy = <T, K extends keyof T>(
  array: T[],
  key: K
): Record<string, T[]> => {
  return array.reduce((groups, item) => {
    const group = String(item[key]);
    groups[group] = groups[group] || [];
    groups[group].push(item);
    return groups;
  }, {} as Record<string, T[]>);
};

/**
 * Convierte un texto a formato slug (URL-friendly)
 */
export const slugify = (text: string): string => {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '') // Remover caracteres especiales
    .replace(/[\s_-]+/g, '-') // Reemplazar espacios y guiones con un solo guión
    .replace(/^-+|-+$/g, ''); // Remover guiones al inicio y final
};

/**
 * Formatea una fecha del formato ISO (YYYY-MM-DD) al formato español (dd de mes de yyyy)
 */
export const formatDateToSpanish = (isoDate: string): string => {
  if (!isoDate) return '';
  
  const months = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
  ];
  
  // Dividir la fecha manualmente para evitar problemas de zona horaria
  const [year, month, day] = isoDate.split('-').map(num => parseInt(num, 10));
  
  // Los meses en JavaScript son 0-indexados, por eso restamos 1
  const monthName = months[month - 1];
  
  return `${day} de ${monthName} de ${year}`;
};
