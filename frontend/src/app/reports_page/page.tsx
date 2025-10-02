'use client';

import React, { useState } from 'react';
import { 
  ClipboardCheck, 
  Search, 
  Download,
  Eye,
  Calendar,
  Upload,
  FileText,
  CheckCircle,
  Clock,
  AlertCircle,
  Plus
} from 'lucide-react';

interface FinalReport {
  id: string;
  titulo: string;
  nombreArchivo: string;
  fechaCreacion: string;
  fechaProcesamiento: string;
  tipoReporte: 'trimestral' | 'semestral' | 'anual' | 'especial';
  estado: 'procesando' | 'completado' | 'error';
  archivoOriginal: string;
  archivoFinal?: string;
  numeroReporte: string;
}

const mockReports: FinalReport[] = [
  {
    id: '1',
    titulo: 'Informe Anual Dr. Juan Pérez - 2024',
    nombreArchivo: 'borrador_juan_perez_2024.pdf',
    fechaCreacion: '2025-01-15',
    fechaProcesamiento: '2025-01-15',
    tipoReporte: 'anual',
    estado: 'completado',
    archivoOriginal: 'borrador_juan_perez_2024.pdf',
    archivoFinal: 'informe_final_juan_perez_2024.pdf',
    numeroReporte: 'INF-2025-001'
  },
  {
    id: '2',
    titulo: 'Informe Trimestral Dra. María García - Q4 2024',
    nombreArchivo: 'borrador_maria_garcia_q4.pdf',
    fechaCreacion: '2025-01-10',
    fechaProcesamiento: '2025-01-12',
    tipoReporte: 'trimestral',
    estado: 'completado',
    archivoOriginal: 'borrador_maria_garcia_q4.pdf',
    archivoFinal: 'informe_final_maria_garcia_q4.pdf',
    numeroReporte: 'INF-2025-002'
  }
];

export default function InformesPage() {
  const [activeTab, setActiveTab] = useState<'lista' | 'nuevo'>('lista');
  const [finalReports, setFinalReports] = useState<FinalReport[]>(mockReports);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterEstado, setFilterEstado] = useState<string>('');
  const [filterTipo, setFilterTipo] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  
  // Form data for new final report
  const [uploadData, setUploadData] = useState({
    titulo: '',
    tipoReporte: 'anual' as 'trimestral' | 'semestral' | 'anual' | 'especial',
    archivo: null as File | null,
    incluirEncabezados: true,
    incluirLogo: true,
    incluirPiesPagina: true
  });

  const filteredReports = finalReports.filter(report => {
    const matchesSearch = report.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.nombreArchivo.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.numeroReporte.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesEstado = !filterEstado || report.estado === filterEstado;
    const matchesTipo = !filterTipo || report.tipoReporte === filterTipo;
    
    return matchesSearch && matchesEstado && matchesTipo;
  });

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setUploadData(prev => ({
        ...prev,
        archivo: file,
        titulo: file.name.replace('.pdf', '')
      }));
    } else {
      alert('Por favor seleccione un archivo PDF válido');
    }
  };

  const handleProcessReport = async () => {
    if (!uploadData.archivo || !uploadData.titulo) {
      alert('Por favor complete todos los campos requeridos y seleccione un archivo');
      return;
    }

    setIsProcessing(true);
    
    try {
      // Simulación de procesamiento - aquí se integraría con el backend
      const newReport: FinalReport = {
        id: Date.now().toString(),
        titulo: uploadData.titulo,
        nombreArchivo: uploadData.archivo.name,
        fechaCreacion: new Date().toISOString().split('T')[0],
        fechaProcesamiento: new Date().toISOString().split('T')[0],
        tipoReporte: uploadData.tipoReporte,
        estado: 'procesando',
        archivoOriginal: uploadData.archivo.name,
        numeroReporte: `INF-${new Date().getFullYear()}-${String(finalReports.length + 1).padStart(3, '0')}`
      };

      setFinalReports(prev => [newReport, ...prev]);
      
      // Simular procesamiento completado después de 3 segundos
      setTimeout(() => {
        setFinalReports(prev => prev.map(report => 
          report.id === newReport.id 
            ? { ...report, estado: 'completado' as const, archivoFinal: `final_${report.archivoOriginal}` }
            : report
        ));
      }, 3000);
      
      setActiveTab('lista');
      
      // Reset form
      setUploadData({
        titulo: '',
        tipoReporte: 'anual',
        archivo: null,
        incluirEncabezados: true,
        incluirLogo: true,
        incluirPiesPagina: true
      });
      
    } catch (error) {
      console.error('Error processing report:', error);
      alert('Error al procesar el informe. Por favor intente nuevamente.');
    } finally {
      setIsProcessing(false);
    }
  };

  const stats = {
    total: finalReports.length,
    procesando: finalReports.filter(r => r.estado === 'procesando').length,
    completados: finalReports.filter(r => r.estado === 'completado').length,
    errores: finalReports.filter(r => r.estado === 'error').length
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <ClipboardCheck className="h-6 w-6 mr-3 text-[#042a53]']" />
              Informes Finales
            </h1>
            <p className="text-gray-600 mt-1">
              Procesa borradores de reportes para generar informes oficiales con encabezados institucionales
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
              Lista de Informes
            </button>
            <button
              onClick={() => setActiveTab('nuevo')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'nuevo'
                  ? 'border-[#042a53] text-[#042a53]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Generar Informe
            </button>
          </nav>
        </div>

        {/* Stats Cards */}
        {activeTab === 'lista' && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
              <div className="text-sm text-gray-600">Total Informes</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold" style={{ color: '#042a53' }}>{stats.procesando}</div>
              <div className="text-sm text-gray-600">Procesando</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-green-600">{stats.completados}</div>
              <div className="text-sm text-gray-600">Completados</div>
            </div>
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <div className="text-2xl font-bold text-red-600">{stats.errores}</div>
              <div className="text-sm text-gray-600">Con Errores</div>
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      {activeTab === 'lista' ? (
        <div className="space-y-6">
          {/* Search and Filters */}
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Buscar por título, archivo o número de informe..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              <select
                value={filterEstado}
                onChange={(e) => setFilterEstado(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">Todos los estados</option>
                <option value="procesando">Procesando</option>
                <option value="completado">Completado</option>
                <option value="error">Error</option>
              </select>
              <select
                value={filterTipo}
                onChange={(e) => setFilterTipo(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">Todos los tipos</option>
                <option value="trimestral">Trimestral</option>
                <option value="semestral">Semestral</option>
                <option value="anual">Anual</option>
                <option value="especial">Especial</option>
              </select>
            </div>
          </div>

          {/* Reports List */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredReports.map((report) => (
              <div key={report.id} className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {report.titulo}
                      </h3>
                      <span className={`ml-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        report.tipoReporte === 'anual' ? 'bg-purple-100 text-purple-800' :
                        report.tipoReporte === 'semestral' ? 'bg-blue-100 text-blue-800' :
                        report.tipoReporte === 'trimestral' ? 'bg-green-100 text-green-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {report.tipoReporte}
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 mb-2">
                      <strong>No. Informe:</strong> {report.numeroReporte}
                    </div>
                    <div className="space-y-1 mb-3">
                      <div className="flex items-center text-sm text-gray-600">
                        <FileText className="h-4 w-4 mr-2 text-gray-400" />
                        {report.nombreArchivo}
                      </div>
                      <div className="flex items-center text-sm text-gray-600">
                        <Calendar className="h-4 w-4 mr-2 text-gray-400" />
                        Procesado: {new Date(report.fechaProcesamiento).toLocaleDateString('es-ES')}
                      </div>
                    </div>
                  </div>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    report.estado === 'procesando' ? 'bg-blue-100 text-blue-800' :
                    report.estado === 'completado' ? 'bg-green-100 text-green-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {report.estado === 'procesando' ? (
                      <div className="flex items-center">
                        <Clock className="h-3 w-3 mr-1" />
                        Procesando
                      </div>
                    ) : report.estado === 'completado' ? (
                      <div className="flex items-center">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Completado
                      </div>
                    ) : (
                      <div className="flex items-center">
                        <AlertCircle className="h-3 w-3 mr-1" />
                        Error
                      </div>
                    )}
                  </span>
                </div>

                <div className="border-t pt-4">
                  <div className="flex items-center justify-between">
                    <div className="text-xs text-gray-500">
                      Archivo original: {report.archivoOriginal}
                    </div>
                    <div className="flex space-x-2">
                      <button className="text-blue-600 hover:text-blue-900 p-1">
                        <Eye className="h-4 w-4" />
                      </button>
                      {report.estado === 'completado' && (
                        <button className="text-green-600 hover:text-green-900 p-1">
                          <Download className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredReports.length === 0 && (
            <div className="text-center py-12 bg-white rounded-lg border border-gray-200">
              <ClipboardCheck className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                No se encontraron informes finales
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Procesa tu primer borrador para crear un informe final
              </p>
              <button
                onClick={() => setActiveTab('nuevo')}
                className="mt-4 px-4 py-2 bg-[#042a53] text-white rounded-lg text-sm font-medium hover:bg-[#1e7bb8]"
              >
                Generar Informe
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Generación de Certificado
            </h2>
            <p className="text-gray-600">
              Carga el archivo PDF del borrador para generar el certificado final
            </p>
          </div>

          <div className="space-y-6">
            {/* File Upload */}
            <div>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <div className="mb-2">
                  <label className="cursor-pointer">
                    <span className="text-[#042a53] hover:text-[#1e7bb8] font-medium">
                      Haz clic para subir un archivo
                    </span>
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </label>
                  <span className="text-gray-600"> o arrastra y suelta aquí</span>
                </div>
                <p className="text-xs text-gray-500">Solo archivos PDF hasta 10MB</p>
                {uploadData.archivo && (
                  <div className="mt-4 p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center text-sm text-green-800">
                      <FileText className="h-4 w-4 mr-2" />
                      {uploadData.archivo.name}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Basic Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Título del Informe *
                </label>
                <input
                  type="text"
                  value={uploadData.titulo}
                  onChange={(e) => setUploadData(prev => ({...prev, titulo: e.target.value}))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Informe Anual Dr. Juan Pérez - 2024"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tipo de Reporte *
                </label>
                <select
                  value={uploadData.tipoReporte}
                  onChange={(e) => setUploadData(prev => ({...prev, tipoReporte: e.target.value as any}))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="trimestral">Trimestral</option>
                  <option value="semestral">Semestral</option>
                  <option value="anual">Anual</option>
                  <option value="especial">Especial</option>
                </select>
              </div>
            </div>

            {/* Processing Options */}
            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="text-md font-semibold text-gray-900 mb-4">Opciones de Procesamiento</h3>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={uploadData.incluirEncabezados}
                    onChange={(e) => setUploadData(prev => ({...prev, incluirEncabezados: e.target.checked}))}
                    className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Incluir encabezados institucionales</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={uploadData.incluirLogo}
                    onChange={(e) => setUploadData(prev => ({...prev, incluirLogo: e.target.checked}))}
                    className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Incluir logo institucional</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={uploadData.incluirPiesPagina}
                    onChange={(e) => setUploadData(prev => ({...prev, incluirPiesPagina: e.target.checked}))}
                    className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">Incluir pies de página oficiales</span>
                </label>
              </div>
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
                onClick={handleProcessReport}
                disabled={isProcessing || !uploadData.archivo || !uploadData.titulo}
                className="px-6 py-2 bg-[#5a8db3] text-white rounded-lg text-sm font-medium hover:bg-[#4a7d9f] disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {isProcessing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Procesando...
                  </>
                ) : (
                  <>
                    <ClipboardCheck className="h-4 w-4 mr-2" />
                    Descargar PDF
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