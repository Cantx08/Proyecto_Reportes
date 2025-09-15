'use client';

interface Step {
  id: number;
  title: string;
  description: string;
  path: string;
}

interface StepIndicatorProps {
  steps: Step[];
  currentStep: number;
}

export default function StepIndicator({ steps, currentStep }: StepIndicatorProps) {
  return (
    <nav aria-label="Progress" className="flex items-center">
      <ol className="flex items-center space-x-5">
        {steps.map((step, stepIdx) => (
          <li key={step.id} className="flex items-center">
            {stepIdx !== 0 && (
              <div className="flex items-center">
                <div
                  className={`w-12 h-0.5 ${
                    step.id <= currentStep ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                />
              </div>
            )}
            
            <div className="relative flex items-center">
              <div
                className={`
                  flex h-10 w-10 items-center justify-center rounded-full border-2
                  ${
                    step.id < currentStep
                      ? 'bg-blue-600 border-blue-600'
                      : step.id === currentStep
                      ? 'border-blue-600 bg-white'
                      : 'border-gray-300 bg-white'
                  }
                `}
              >
                {step.id < currentStep ? (
                  <svg className="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <span
                    className={`text-sm font-medium ${
                      step.id === currentStep ? 'text-blue-600' : 'text-gray-500'
                    }`}
                  >
                    {step.id}
                  </span>
                )}
              </div>
              
              <div className="ml-3 hidden sm:block">
                <div
                  className={`text-sm font-medium ${
                    step.id === currentStep ? 'text-blue-600' : 'text-gray-500'
                  }`}
                >
                  {step.title}
                </div>
                <div className="text-sm text-gray-500">{step.description}</div>
              </div>
            </div>
          </li>
        ))}
      </ol>
    </nav>
  );
}