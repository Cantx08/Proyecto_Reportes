export interface ReportRequest {
  author_ids: string[];
  docente_nombre: string;
  docente_genero: string; // Cambiado de 'M' | 'F' a string para permitir texto libre
  departamento: string;
  cargo: string;
  memorando?: string;
  firmante?: number | string; // Cambiado para permitir texto libre
  firmante_nombre?: string; // Nuevo campo para nombre de firmante personalizado
  fecha?: string;
  elaborador?: string; // Nombre de quien elaboró el reporte
}