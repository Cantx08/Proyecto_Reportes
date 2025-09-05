'use client';

import React, { useEffect, useRef } from 'react';

interface DocumentosPorAnioProps {
  documentosPorAnio: Record<string, number>;
}

export const DocumentosPorAnio: React.FC<DocumentosPorAnioProps> = ({
  documentosPorAnio
}) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<any>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    // Importar Chart.js dinámicamente para evitar errores de SSR
    import('chart.js').then((Chart) => {
      const {
        Chart: ChartJS,
        CategoryScale,
        LinearScale,
        LineElement,
        LineController,
        PointElement,
        Title,
        Tooltip,
        Legend,
      } = Chart;

      ChartJS.register(
        CategoryScale,
        LinearScale,
        LineElement,
        LineController,
        PointElement,
        Title,
        Tooltip,
        Legend
      );

      // Destruir gráfico anterior si existe
      if (chartInstance.current) {
        chartInstance.current.destroy();
        chartInstance.current = null;
      }

      const canvas = chartRef.current;
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      // Preparar datos
      const years = Object.keys(documentosPorAnio).sort();
      const counts = years.map(year => documentosPorAnio[year]);

      chartInstance.current = new ChartJS(ctx, {
        type: 'line',
        data: {
          labels: years,
          datasets: [
            {
              label: 'Documentos publicados',
              data: counts,
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              borderColor: 'rgba(59, 130, 246, 1)',
              borderWidth: 3,
              fill: true,
              tension: 0,
              pointBackgroundColor: 'rgba(59, 130, 246, 1)',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointRadius: 6,
              pointHoverRadius: 8,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: 'Publicaciones por Año',
              font: {
                size: 16,
                weight: 'bold',
              },
            },
            legend: {
              display: false,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
              },
              title: {
                display: true,
                text: 'Documents',
              },
            },
            x: {
              title: {
                display: true,
                text: 'Year',
              },
            },
          },
        },
      });
    });

    // Cleanup
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
        chartInstance.current = null;
      }
    };
  }, [documentosPorAnio]);

  if (Object.keys(documentosPorAnio).length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Publicaciones por Año
        </h3>
        <p className="text-gray-500 text-center py-8">
          No hay datos para mostrar
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="relative h-80">
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
  );
};
