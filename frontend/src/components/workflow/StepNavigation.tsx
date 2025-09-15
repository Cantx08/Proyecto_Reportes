'use client';

import { useRouter } from 'next/navigation';
import { useWorkflow } from './WorkflowProvider';

interface Step {
  id: number;
  title: string;
  description: string;
  path: string;
}

interface StepNavigationProps {
  currentStep: number;
  totalSteps: number;
  steps: Step[];
}

export default function StepNavigation({ currentStep, totalSteps, steps }: StepNavigationProps) {
  const router = useRouter();
  const { state } = useWorkflow();

  const handlePrevious = () => {
    if (currentStep > 1) {
      const previousStep = steps.find(s => s.id === currentStep - 1);
      if (previousStep) {
        router.push(previousStep.path);
      }
    }
  };

  const handleNext = () => {
    if (currentStep < totalSteps) {
      const nextStep = steps.find(s => s.id === currentStep + 1);
      if (nextStep) {
        router.push(nextStep.path);
      }
    }
  };

  const canProceedToNext = () => {
    switch (currentStep) {
      case 1: // Búsqueda
        return state.author !== null || state.searchResults.length > 0;
      case 2: // Autor
        return state.author !== null && state.author.first_name && state.author.last_name;
      case 3: // Publicaciones
        return state.publications.length > 0;
      case 4: // Vista previa
        return state.selectedPublications.length > 0;
      default:
        return true;
    }
  };

  const getNextButtonText = () => {
    switch (currentStep) {
      case 1:
        return state.author ? 'Continuar con Autor' : 'Buscar Autor';
      case 2:
        return 'Gestionar Publicaciones';
      case 3:
        return 'Vista Previa del Reporte';
      case 4:
        return 'Generar PDF';
      case 5:
        return 'Finalizar';
      default:
        return 'Siguiente';
    }
  };

  return (
    <div className="flex justify-between items-center">
      <button
        type="button"
        onClick={handlePrevious}
        disabled={currentStep === 1}
        className={`
          inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md
          ${
            currentStep === 1
              ? 'text-gray-300 bg-white cursor-not-allowed'
              : 'text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
          }
        `}
      >
        <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
        </svg>
        Anterior
      </button>

      <div className="flex-1 flex justify-center">
        <span className="text-sm text-gray-500">
          Paso {currentStep} de {totalSteps}
        </span>
      </div>

      <button
        type="button"
        onClick={handleNext}
        disabled={currentStep === totalSteps || !canProceedToNext()}
        className={`
          inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white
          ${
            currentStep === totalSteps || !canProceedToNext()
              ? 'bg-gray-300 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
          }
        `}
      >
        {getNextButtonText()}
        <svg className="w-5 h-5 ml-2" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
        </svg>
      </button>
    </div>
  );
}