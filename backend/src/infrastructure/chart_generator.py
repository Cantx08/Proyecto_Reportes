"""
Generador de gráficos usando matplotlib.
"""
import io
from typing import Dict
from matplotlib import pyplot as plt
import matplotlib

from ..domain.interfaces import IChartGenerator

matplotlib.use('Agg')  # Use non-interactive backend


class MatplotlibChartGenerator(IChartGenerator):
    """Implementación de generador de gráficos usando matplotlib."""
    
    def __init__(self):
        self._configure_matplotlib()
    
    def _configure_matplotlib(self) -> None:
        """Configura matplotlib con ajustes por defecto."""
        plt.style.use('default')
    
    def generar_grafico_tendencias(self, documentos_por_anio: Dict[str, int], docente_nombre: str) -> bytes:
        """Genera un gráfico de tendencias por año."""
        # Crear figura
        plt.figure(figsize=(8, 4))
        
        # Preparar datos
        years = sorted([int(year) for year in documentos_por_anio.keys()])
        counts = [documentos_por_anio[str(year)] for year in years]
        
        # Crear gráfico de línea con colores personalizados
        plt.plot(years, counts, marker='o', linewidth=2, markersize=6, color='#009ece')
        
        # Configurar etiquetas y título
        plt.xlabel('Año', fontsize=10, ha='center', color='#333366')
        plt.ylabel('Documentos', fontsize=10, ha='center', color='#333366')
        plt.title('Documentos por año', fontsize=12, pad=15, color='#333366', loc='center')
        
        # Configurar grid - solo líneas horizontales
        plt.grid(axis='y', alpha=0.3, color='#cccccc')
        
        # Hacer transparentes los bordes de la gráfica
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        
        # Eliminar márgenes
        plt.margins(0)
        plt.tight_layout(pad=0)
        
        # Configurar límites de ejes
        plt.xlim(min(years) - 0.5, max(years) + 0.5)
        plt.ylim(0, max(counts) + 1)
        
        # Configurar ticks
        plt.xticks(years, color='#333366')
        plt.yticks(range(0, max(counts) + 2), color='#333366')
        
        # Guardar como imagen
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer.getvalue()
