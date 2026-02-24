// Types
export * from './types';

// Services
export { publicationService } from './services/publicationService';

// Hooks
export { usePublications } from './hooks/usePublications';
export type { UsePublicationsState, UsePublicationsActions } from './hooks/usePublications';

// Components
export { PublicationsList } from './components/PublicationsList';
export { DocumentsByYear } from './components/DocumentsByYearChart';
export { SubjectAreas } from './components/SubjectAreas';
