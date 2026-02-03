'use client';

import React, { useEffect, useRef } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LineElement,
  LineController,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Registrar componentes de Chart.js
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

interface DocumentsByYearProps {
  documentsByYear: Record<string, number>;
}

export const DocumentsByYear: React.FC<DocumentsByYearProps> = ({
  documentsByYear
}) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<any>(null);

  useEffect(() => {
    if (!chartRef.current) return;

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
    const years = Object.keys(documentsByYear).sort();
    const counts = years.map(year => documentsByYear[year]);
    
    // Calcular el máximo dinámico para el eje Y y el stepSize
    const maxPublications = Math.max(...counts);
    let dynamicMax: number;
    let stepSize: number;
    
    if (maxPublications <= 5) {
      // Para 1-5 publicaciones: límite +1, stepSize de 1
      dynamicMax = maxPublications + 1;
      stepSize = 1;
    } else if (maxPublications <= 10) {
      // Para 6-10 publicaciones: límite +2, stepSize de 2
      dynamicMax = maxPublications + 2;
      stepSize = 2;
    } else if (maxPublications <= 20) {
      // Para 11-20 publicaciones: límite +4, stepSize de 4
      dynamicMax = maxPublications + 4;
      stepSize = 4;
    } else {
      // Para más de 20: límite +10% redondeado, stepSize de 5
      dynamicMax = Math.ceil(maxPublications * 1.1);
      stepSize = 5;
    }

    chartInstance.current = new ChartJS(ctx, {
      type: 'line',
      data: {
        labels: years,
        datasets: [
          {
            label: 'Documentos publicados',
            data: counts,
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderColor: 'rgba(0, 158, 206, 1)',
            borderWidth: 3,
            fill: true,
            tension: 0,
            pointBackgroundColor: 'rgba(0, 158, 206, 1)',
            pointRadius: 6,
            pointHoverRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            top: 20,
            right: 20,
            bottom: 20,
            left: 20
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Documents by year',
            font: {
              family: 'ElsevierSans, Arial, Georgia, sans-serif, serif',
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
            max: dynamicMax,
            ticks: {
              stepSize: stepSize,
              color: '#666666',
              callback: function(value: any) {
                return value;
              }
            },
            title: {
              display: true,
              text: 'Documents',
              color: '#666666',
              font: {
                family: 'ElsevierSans, Arial, Georgia, sans-serif, serif',
                size: 12,
              }
            },
            grid: {
              color: '#e5e5e5',
              lineWidth: 1,
            }
          },
          x: {
            ticks: {
              color: '#666666',
            },
            title: {
              display: true,
              text: 'Year',
              color: '#666666',
              font: {
                family: 'ElsevierSans, Arial, Georgia, sans-serif, serif',
                size: 12,
              }
            },
            grid: {
              display: false,
            }
          },
        },
      },
    });

    // Cleanup
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
        chartInstance.current = null;
      }
    };
  }, [documentsByYear]);

  if (Object.keys(documentsByYear).length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Documents by year
        </h3>
        <p className="text-gray-500 text-center py-8">
          No hay datos para mostrar
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div 
        className="relative"
        style={{
          width: 'clamp(695px, 100%, 875px)',
          height: '498px'
        }}
      >
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
  );
};
