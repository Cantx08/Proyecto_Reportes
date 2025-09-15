'use client';

import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import StepIndicator from '@/components/workflow/StepIndicator';
import StepNavigation from '@/components/workflow/StepNavigation';
import WorkflowProvider from '@/components/workflow/WorkflowProvider';

const steps = [
  { id: 1, title: 'Búsqueda', description: 'Buscar autor por ID o nombre', path: '/step-1-search' },
  { id: 2, title: 'Autor', description: 'Gestionar datos del autor', path: '/step-2-author' },
  { id: 3, title: 'Publicaciones', description: 'Sincronizar y editar publicaciones', path: '/step-3-publications' },
  { id: 4, title: 'Vista Previa', description: 'Configurar y previsualizar reporte', path: '/step-4-preview' },
  { id: 5, title: 'Generar PDF', description: 'Generar documento final', path: '/step-5-generate' },
];

export default function WorkflowLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    // Determinar el paso actual basado en la ruta
    const step = steps.find(s => pathname.includes(s.path));
    if (step) {
      setCurrentStep(step.id);
    }
  }, [pathname]);

  return (
    <WorkflowProvider>
      <div className="min-h-screen bg-gray-50">
        {/* Header con indicador de pasos */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="py-6">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">
                Generador de Reportes Académicos
              </h1>
              <StepIndicator 
                steps={steps} 
                currentStep={currentStep} 
              />
            </div>
          </div>
        </div>

        {/* Contenido principal */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
            {children}
          </div>

          {/* Navegación entre pasos */}
          <StepNavigation 
            currentStep={currentStep}
            totalSteps={steps.length}
            steps={steps}
          />
        </div>
      </div>
    </WorkflowProvider>
  );
}