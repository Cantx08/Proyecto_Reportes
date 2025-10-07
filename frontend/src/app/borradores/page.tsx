'use client';

import React, { useState, useEffect } from 'react';
import { 
  FileEdit, 
  Search, 
  Plus,
  Eye,
  Download,
  Edit,
  Trash2,
  Calendar,
  User,
  Building,
  Clock,
  FileText
} from 'lucide-react';
import { scopusApi, ReportRequest } from '@/services/scopusApi';
import { formatDateToSpanish } from '@/utils/helpers';
import DepartmentSelect from '@/components/DepartmentSelectNew';
import CargoSelect from '@/components/PositionSelect';
import GenderSelect from '@/components/GenderSelect';
import FirmanteSelect from '@/components/SignatorySelect';

interface Draft {
  id: string;
  titulo: string;
  autor: string;
  departamento: string;
  cargo: string;
  fechaCreacion: string;
  fechaModificacion: string;
  estado: 'borrador' | 'revision' | 'aprobado';
  scopusIds: string[];
  preview: string;
}

const mockDrafts: Draft[] = [
  {
    id: '1',
    titulo: 'Reporte Dr. Juan Pérez - Q1 2025',
    autor: 'Dr. Juan Carlos Pérez',
    departamento: 'Ingeniería Civil',
    cargo: 'Profesor Principal',
    fechaCreacion: '2025-01-15',
    fechaModificacion: '2025-01-16',
    estado: 'borrador',
    scopusIds: ['12345678900'],
    preview: 'Reporte de publicaciones académicas para el período enero-marzo 2025...'
  },
  {
    id: '2',  
    titulo: 'Reporte Dra. María García - Anual 2024',
    autor: 'Dra. María García López',
    departamento: 'Ingeniería Química',
    cargo: 'Profesora Titular',
    fechaCreacion: '2025-01-10',
    fechaModificacion: '2025-01-14',
    estado: 'revision',
    scopusIds: ['98765432100'],
    preview: 'Análisis completo de productividad científica durante el año 2024...'
  }
];

export default function BorradoresPage() {
  const [activeTab, setActiveTab] = useState<'lista' | 'nuevo'>('lista');
  const [drafts, setDrafts] = useState<Draft[]>(mockDrafts);
  const [searchTerm, setSearchTerm] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  
  // Form data for new draft
  const [formData, setFormData] = useState<Partial<ReportRequest>>({
    docente_nombre: '',
    docente_genero: 'M',
    departamento: '',
    cargo: '',
    memorando: '',
    firmante: 1,
    firmante_nombre: '',
    fecha: '',
    es_borrador: true,
  });
  const [authorIds, setAuthorIds] = useState<string[]>(['']);

  const filteredDrafts = drafts.filter(draft =>
    draft.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    draft.autor.toLowerCase().includes(searchTerm.toLowerCase()) ||
    draft.departamento.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleInputChange = (field: keyof ReportRequest, value: string | number | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addAuthorId = () => {
    setAuthorIds(prev => [...prev, '']);
  };

  const removeAuthorId = (index: number) => {
    setAuthorIds(prev => prev.filter((_, i) => i !== index));
  };

  const updateAuthorId = (index: number, value: string) => {
    setAuthorIds(prev => prev.map((id, i) => i === index ? value : id));
  };

  const handleGenerateDraft = async () => {
    const validAuthorIds = authorIds.filter(id => id.trim() !== '');
    
    if (!formData.docente_nombre || !formData.departamento || !formData.cargo) {
      alert('Por favor complete todos los campos requeridos');
      return;
    }

    if (validAuthorIds.length === 0) {
      alert('Debe ingresar al menos un ID de autor');
      return;
    }

    setIsGenerating(true);
    
    try {
      const reportData: ReportRequest = {
        author_ids: validAuthorIds,
        docente_nombre: formData.docente_nombre!,
        docente_genero: formData.docente_genero!,
        departamento: formData.departamento!,
        cargo: formData.cargo!,
        memorando: formData.memorando || '',
        firmante: formData.firmante!,
        firmante_nombre: formData.firmante_nombre || '',
        fecha: formData.fecha || new Date().toISOString().split('T')[0],
        es_borrador: true,
      };

      const response = await scopusApi.generarReporte(reportData);
      
      // Create new draft entry
      const newDraft: Draft = {
        id: Date.now().toString(),
        titulo: `Borrador ${formData.docente_nombre} - ${new Date().toLocaleDateString('es-ES')}`,
        autor: formData.docente_nombre!,
        departamento: formData.departamento!,
        cargo: formData.cargo!,
        fechaCreacion: new Date().toISOString().split('T')[0],
        fechaModificacion: new Date().toISOString().split('T')[0],
        estado: 'borrador',
        scopusIds: validAuthorIds,
        preview: `Borrador generado automáticamente para ${formData.docente_nombre}...`
      };

      setDrafts(prev => [newDraft, ...prev]);
      setActiveTab('lista');
      
      // Reset form
      setFormData({
        docente_nombre: '',
        docente_genero: 'M',
        departamento: '',
        cargo: '',
        memorando: '',
        firmante: 1,
        firmante_nombre: '',
        fecha: '',
        es_borrador: true,
      });
      setAuthorIds(['']);
      
    } catch (error) {
      console.error('Error generating draft:', error);
      alert('Error al generar el borrador. Por favor intente nuevamente.');
    } finally {
      setIsGenerating(false);
    }
  };

  const stats = {
    total: drafts.length,
    borradores: drafts.filter(d => d.estado === 'borrador').length,
    revision: drafts.filter(d => d.estado === 'revision').length,
    aprobados: drafts.filter(d => d.estado === 'aprobado').length
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <FileEdit className="h-6 w-6 mr-3 text-[#042a53]" />
              Generación de Borradores
            </h1>
            <p className="text-gray-600 mt-1">
              Crea y gestiona versiones preliminares de reportes para revisión
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('lista')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'lista'
                  ? 'border-[#042a53] text-[#042a53]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Lista de Borradores
            </button>
            <button
              onClick={() => setActiveTab('nuevo')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'nuevo'
                  ? 'border-[#042a53] text-[#042a53]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Crear Nuevo Borrador
            </button>
          </nav>
        </div>

        {/* Stats Cards */}
        {activeTab === 'lista' && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
              <div className="text-sm text-gray-600">Total Borradores</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-orange-600">{stats.borradores}</div>
              <div className="text-sm text-gray-600">En Borrador</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold" style={{ color: '#042a53' }}>{stats.revision}</div>
              <div className="text-sm text-gray-600">En Revisión</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-green-600">{stats.aprobados}</div>
              <div className="text-sm text-gray-600">Aprobados</div>
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      {activeTab === 'lista' ? (
        <div className="space-y-6">
          {/* Search Bar */}
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar borradores por título, autor o departamento..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Drafts List */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredDrafts.map((draft) => (
              <div key={draft.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {draft.titulo}
                    </h3>
                    <div className="space-y-1">
                      <div className="flex items-center text-sm text-gray-600">
                        <User className="h-4 w-4 mr-2 text-gray-400" />
                        {draft.autor}
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Building className="h-4 w-4 mr-2 text-gray-400" />
                        {draft.departamento} - {draft.cargo}
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar className="h-4 w-4 mr-2 text-gray-400" />
                        Creado: {new Date(draft.fechaCreacion).toLocaleDateString('es-ES')}
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Clock className="h-4 w-4 mr-2 text-gray-400" />
                        Modificado: {new Date(draft.fechaModificacion).toLocaleDateString('es-ES')}
                      </div>
                    </div>
                  </div>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    draft.estado === 'borrador' ? 'bg-orange-100 text-orange-800' :
                    draft.estado === 'revision' ? 'bg-blue-100 text-blue-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {draft.estado}
                  </span>
                </div>

                <div className="mb-4">
                  <p className="text-sm text-gray-600 line-clamp-2">
                    {draft.preview}
                  </p>
                </div>

                <div className="mb-4">
                  <div className="text-xs text-gray-500 mb-1">Scopus IDs:</div>
                  <div className="flex flex-wrap gap-1">
                    {draft.scopusIds.map((id, index) => (
                      <span key={index} className="inline-flex px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                        {id}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <div className="flex items-center text-xs text-gray-500">
                    <FileText className="h-3 w-3 mr-1" />
                    Borrador
                  </div>
                  <div className="flex space-x-2">
                    <button className="text-blue-600 hover:text-blue-900 p-1">
                      <Eye className="h-4 w-4" />
                    </button>
                    <button className="text-green-600 hover:text-green-900 p-1">
                      <Edit className="h-4 w-4" />
                    </button>
                    <button className="text-purple-600 hover:text-purple-900 p-1">
                      <Download className="h-4 w-4" />
                    </button>
                    <button className="text-red-600 hover:text-red-900 p-1">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredDrafts.length === 0 && (
            <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
              <FileEdit className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                No se encontraron borradores
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Crea tu primer borrador para comenzar
              </p>
              <button
                onClick={() => setActiveTab('nuevo')}
                className="mt-4 px-4 py-2 bg-orange-600 text-white rounded-lg text-sm font-medium hover:bg-orange-700"
              >
                Crear Borrador
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Crear Nuevo Borrador
            </h2>
            <p className="text-gray-600">
              Complete la información del reporte para generar un borrador preliminar
            </p>
          </div>

          <div className="space-y-6">
            {/* Author IDs Section */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                IDs de Scopus de los Autores *
              </label>
              <div className="space-y-3">
                {authorIds.map((id, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={id}
                      onChange={(e) => updateAuthorId(index, e.target.value)}
                      placeholder="Ej: 12345678900"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                    />
                    {authorIds.length > 1 && (
                      <button
                        onClick={() => removeAuthorId(index)}
                        className="p-2 text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                ))}
                <button
                  onClick={addAuthorId}
                  className="flex items-center text-sm text-[#042a53] hover:text-[#042a53]/60"
                >
                  <Plus className="h-4 w-4 mr-1" />
                  Agregar otro ID
                </button>
              </div>
            </div>

            {/* Basic Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Docente *
                </label>
                <input
                  type="text"
                  value={formData.docente_nombre || ''}
                  onChange={(e) => handleInputChange('docente_nombre', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                  placeholder="Dr. Juan Pérez"
                />
              </div>

              <div className="space-y-1">
                <label className="block text-sm font-medium text-gray-700">
                  Género *
                </label>
                <GenderSelect
                  value={formData.docente_genero || 'M'}
                  onChange={(value) => handleInputChange('docente_genero', value)}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-1">
                <label className="block text-sm font-medium text-gray-700">
                  Departamento *
                </label>
                <DepartmentSelect
                  value={formData.departamento || ''}
                  onChange={(value) => handleInputChange('departamento', value)}
                />
              </div>

              <div className="space-y-1">
                <label className="block text-sm font-medium text-gray-700">
                  Cargo *
                </label>
                <CargoSelect
                  value={formData.cargo || ''}
                  onChange={(value) => handleInputChange('cargo', value)}
                />
              </div>
            </div>

            {/* Additional Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Número de Memorando
                </label>
                <input
                  type="text"
                  value={formData.memorando || ''}
                  onChange={(e) => handleInputChange('memorando', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                  placeholder="EPN-2025-001"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Fecha del Reporte
                </label>
                <input
                  type="date"
                  value={formData.fecha || new Date().toISOString().split('T')[0]}
                  onChange={(e) => handleInputChange('fecha', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
            </div>

            {/* Signatory */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Información del Firmante
              </label>
              <FirmanteSelect
                cargoValue={formData.firmante || 1}
                nombreValue={formData.firmante_nombre || ''}
                onCargoChange={(value: number | string) => handleInputChange('firmante', value)}
                onNombreChange={(value: string) => handleInputChange('firmante_nombre', value)}
              />
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
              <button
                onClick={() => setActiveTab('lista')}
                className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                onClick={handleGenerateDraft}
                disabled={isGenerating}
                className="px-6 py-2 bg-[#5a8db3] text-white rounded-lg text-sm font-medium hover:bg-[#4a7d9f] disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Generando...
                  </>
                ) : (
                  <>
                    <FileEdit className="h-4 w-4 mr-2" />
                    Generar Borrador
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}