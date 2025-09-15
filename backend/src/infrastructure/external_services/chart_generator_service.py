"""
Implementación del generador de gráficos para reportes.
"""

import io
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from ...domain.interfaces.external_services import ChartGeneratorInterface

# Configurar matplotlib para no mostrar gráficos en pantalla
matplotlib.use('Agg')


class ChartGeneratorService(ChartGeneratorInterface):
    """Implementación del generador de gráficos usando Matplotlib."""
    
    def __init__(self):
        self._configure_matplotlib()
    
    def _configure_matplotlib(self) -> None:
        """Configura matplotlib con ajustes por defecto."""
        plt.style.use('default')
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 10
    
    def generate_publications_by_year_chart(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un gráfico de publicaciones por año.
        
        Args:
            data: Datos con formato {'publications': [{'year': int, ...}, ...]}
            
        Returns:
            bytes: Imagen del gráfico en formato PNG
        """
        publications = data.get('publications', [])
        
        # Contar publicaciones por año
        year_counts = {}
        for pub in publications:
            year = pub.get('year')
            if year and isinstance(year, int):
                year_counts[year] = year_counts.get(year, 0) + 1
        
        if not year_counts:
            return self._generate_empty_chart("No hay datos de publicaciones por año")
        
        # Ordenar años
        years = sorted(year_counts.keys())
        counts = [year_counts[year] for year in years]
        
        # Crear gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(years, counts, marker='o', linewidth=2, markersize=8, color='#009ece')
        
        # Personalización
        plt.title('Publicaciones por Año', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Año', fontsize=12)
        plt.ylabel('Número de Publicaciones', fontsize=12)
        plt.grid(axis='y', alpha=0.3, color='#666666')
        
        # Configurar ejes
        plt.xlim(min(years) - 0.5, max(years) + 0.5)
        plt.ylim(0, max(counts) + 1)
        plt.xticks(years, rotation=45 if len(years) > 10 else 0)
        plt.yticks(range(0, max(counts) + 2))
        
        # Remover bordes
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        
        plt.tight_layout()
        
        # Guardar como bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer.getvalue()
    
    def generate_citations_distribution_chart(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un gráfico de distribución de citaciones.
        
        Args:
            data: Datos con publicaciones y citaciones
            
        Returns:
            bytes: Imagen del gráfico en formato PNG
        """
        publications = data.get('publications', [])
        
        # Extraer citaciones
        citations = []
        for pub in publications:
            cit_count = pub.get('citation_count', 0)
            if isinstance(cit_count, (int, float)) and cit_count >= 0:
                citations.append(cit_count)
        
        if not citations:
            return self._generate_empty_chart("No hay datos de citaciones")
        
        # Crear histograma
        plt.figure(figsize=(10, 6))
        
        # Definir bins automáticamente
        if max(citations) <= 10:
            bins = range(0, max(citations) + 2)
        else:
            bins = min(20, len(set(citations)))
        
        plt.hist(citations, bins=bins, color='#2e8b57', alpha=0.7, edgecolor='black')
        
        # Personalización
        plt.title('Distribución de Citaciones', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Número de Citaciones', fontsize=12)
        plt.ylabel('Número de Publicaciones', fontsize=12)
        plt.grid(axis='y', alpha=0.3, color='#666666')
        
        # Remover bordes
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        
        plt.tight_layout()
        
        # Guardar como bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer.getvalue()
    
    def generate_journal_quartiles_chart(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un gráfico de publicaciones por cuartil de revista.
        
        Args:
            data: Datos con publicaciones y información de SJR
            
        Returns:
            bytes: Imagen del gráfico en formato PNG
        """
        publications = data.get('publications', [])
        
        # Contar por cuartiles
        quartile_counts = {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Sin clasificar': 0}
        
        for pub in publications:
            quartile = pub.get('sjr_quartile', 'Sin clasificar')
            if quartile in quartile_counts:
                quartile_counts[quartile] += 1
            else:
                quartile_counts['Sin clasificar'] += 1
        
        # Filtrar cuartiles con datos
        filtered_quartiles = {k: v for k, v in quartile_counts.items() if v > 0}
        
        if not filtered_quartiles:
            return self._generate_empty_chart("No hay datos de cuartiles")
        
        # Crear gráfico de barras
        plt.figure(figsize=(10, 6))
        
        labels = list(filtered_quartiles.keys())
        values = list(filtered_quartiles.values())
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'][:len(labels)]
        
        bars = plt.bar(labels, values, color=colors, alpha=0.8, edgecolor='black')
        
        # Añadir valores encima de las barras
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center', va='bottom', fontweight='bold')
        
        # Personalización
        plt.title('Publicaciones por Cuartil SJR', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Cuartil', fontsize=12)
        plt.ylabel('Número de Publicaciones', fontsize=12)
        plt.grid(axis='y', alpha=0.3, color='#666666')
        
        # Ajustar límites del eje Y
        plt.ylim(0, max(values) * 1.2)
        
        # Remover bordes
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        
        plt.tight_layout()
        
        # Guardar como bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer.getvalue()
    
    def generate_collaboration_network_chart(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un gráfico de red de colaboración (simplificado).
        
        Args:
            data: Datos con publicaciones y coautores
            
        Returns:
            bytes: Imagen del gráfico en formato PNG
        """
        publications = data.get('publications', [])
        
        # Contar colaboraciones por coautor
        coauthor_counts = {}
        
        for pub in publications:
            coauthors = pub.get('coauthors', [])
            for coauthor in coauthors:
                if isinstance(coauthor, str) and coauthor.strip():
                    name = coauthor.strip()
                    coauthor_counts[name] = coauthor_counts.get(name, 0) + 1
        
        if not coauthor_counts:
            return self._generate_empty_chart("No hay datos de colaboración")
        
        # Tomar los top 10 colaboradores
        top_coauthors = sorted(coauthor_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if not top_coauthors:
            return self._generate_empty_chart("No hay suficientes datos de colaboración")
        
        # Crear gráfico de barras horizontales
        plt.figure(figsize=(12, 8))
        
        names = [item[0] for item in top_coauthors]
        counts = [item[1] for item in top_coauthors]
        
        # Truncar nombres largos
        truncated_names = [name[:30] + '...' if len(name) > 30 else name for name in names]
        
        y_pos = np.arange(len(truncated_names))
        
        bars = plt.barh(y_pos, counts, color='#ff6b6b', alpha=0.8, edgecolor='black')
        
        # Añadir valores al final de las barras
        for bar, count in zip(bars, counts):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    str(count), ha='left', va='center', fontweight='bold')
        
        # Personalización
        plt.title('Top 10 Colaboradores', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Número de Colaboraciones', fontsize=12)
        plt.ylabel('Colaboradores', fontsize=12)
        plt.yticks(y_pos, truncated_names)
        plt.grid(axis='x', alpha=0.3, color='#666666')
        
        # Ajustar límites
        plt.xlim(0, max(counts) * 1.2)
        
        # Remover bordes
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        
        plt.tight_layout()
        
        # Guardar como bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer.getvalue()
    
    def _generate_empty_chart(self, message: str) -> bytes:
        """
        Genera un gráfico vacío con un mensaje.
        
        Args:
            message: Mensaje a mostrar
            
        Returns:
            bytes: Imagen del gráfico vacío
        """
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, message, ha='center', va='center', 
                fontsize=14, transform=plt.gca().transAxes)
        plt.axis('off')
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return img_buffer.getvalue()
