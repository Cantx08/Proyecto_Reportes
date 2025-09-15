'use client';

import { createContext, useContext, useReducer, ReactNode } from 'react';

// Tipos para el estado del workflow
interface Author {
  id?: number;
  scopus_id?: string;
  first_name: string;
  last_name: string;
  email?: string;
  department_id?: number;
  title?: string;
  position?: string;
}

interface Publication {
  id?: number;
  title: string;
  journal?: string;
  year: number;
  doi?: string;
  scopus_id?: string;
  is_included_in_report: boolean;
  is_editable: boolean;
}

interface ReportConfig {
  report_type: 'draft' | 'final';
  include_headers: boolean;
  memo_number?: string;
  memo_date?: string;
  signatory?: string;
  title?: string;
}

interface WorkflowState {
  currentStep: number;
  author: Author | null;
  publications: Publication[];
  selectedPublications: number[];
  reportConfig: ReportConfig;
  searchResults: Author[];
  isLoading: boolean;
  error: string | null;
}

// Tipos de acciones
type WorkflowAction =
  | { type: 'SET_STEP'; payload: number }
  | { type: 'SET_AUTHOR'; payload: Author }
  | { type: 'SET_PUBLICATIONS'; payload: Publication[] }
  | { type: 'TOGGLE_PUBLICATION'; payload: number }
  | { type: 'SET_REPORT_CONFIG'; payload: Partial<ReportConfig> }
  | { type: 'SET_SEARCH_RESULTS'; payload: Author[] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'RESET_WORKFLOW' };

// Estado inicial
const initialState: WorkflowState = {
  currentStep: 1,
  author: null,
  publications: [],
  selectedPublications: [],
  reportConfig: {
    report_type: 'draft',
    include_headers: false,
  },
  searchResults: [],
  isLoading: false,
  error: null,
};

// Reducer
function workflowReducer(state: WorkflowState, action: WorkflowAction): WorkflowState {
  switch (action.type) {
    case 'SET_STEP':
      return { ...state, currentStep: action.payload };
    
    case 'SET_AUTHOR':
      return { ...state, author: action.payload };
    
    case 'SET_PUBLICATIONS':
      return { ...state, publications: action.payload };
    
    case 'TOGGLE_PUBLICATION':
      const publicationId = action.payload;
      const isSelected = state.selectedPublications.includes(publicationId);
      return {
        ...state,
        selectedPublications: isSelected
          ? state.selectedPublications.filter(id => id !== publicationId)
          : [...state.selectedPublications, publicationId],
      };
    
    case 'SET_REPORT_CONFIG':
      return {
        ...state,
        reportConfig: { ...state.reportConfig, ...action.payload },
      };
    
    case 'SET_SEARCH_RESULTS':
      return { ...state, searchResults: action.payload };
    
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    
    case 'RESET_WORKFLOW':
      return initialState;
    
    default:
      return state;
  }
}

// Contexto
const WorkflowContext = createContext<{
  state: WorkflowState;
  dispatch: React.Dispatch<WorkflowAction>;
} | undefined>(undefined);

// Provider
export default function WorkflowProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(workflowReducer, initialState);

  return (
    <WorkflowContext.Provider value={{ state, dispatch }}>
      {children}
    </WorkflowContext.Provider>
  );
}

// Hook personalizado
export function useWorkflow() {
  const context = useContext(WorkflowContext);
  if (!context) {
    throw new Error('useWorkflow must be used within a WorkflowProvider');
  }
  return context;
}

// Hooks de conveniencia
export function useWorkflowActions() {
  const { dispatch } = useWorkflow();

  return {
    setStep: (step: number) => dispatch({ type: 'SET_STEP', payload: step }),
    setAuthor: (author: Author) => dispatch({ type: 'SET_AUTHOR', payload: author }),
    setPublications: (publications: Publication[]) => 
      dispatch({ type: 'SET_PUBLICATIONS', payload: publications }),
    togglePublication: (id: number) => 
      dispatch({ type: 'TOGGLE_PUBLICATION', payload: id }),
    setReportConfig: (config: Partial<ReportConfig>) => 
      dispatch({ type: 'SET_REPORT_CONFIG', payload: config }),
    setSearchResults: (results: Author[]) => 
      dispatch({ type: 'SET_SEARCH_RESULTS', payload: results }),
    setLoading: (loading: boolean) => 
      dispatch({ type: 'SET_LOADING', payload: loading }),
    setError: (error: string | null) => 
      dispatch({ type: 'SET_ERROR', payload: error }),
    resetWorkflow: () => dispatch({ type: 'RESET_WORKFLOW' }),
  };
}