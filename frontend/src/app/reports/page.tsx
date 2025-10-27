'use client';

import React, { useState } from 'react';
import { 
  ClipboardCheck, 
  Download,
  Upload,
  FileText,
  AlertCircle
} from 'lucide-react';
import { scopusApi } from '@/services/scopusApi';

export default function CertificationPage() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setError(null);

    if (file) {
      // Validar tipo
      if (file.type !== 'application/pdf') {
        setError('Por favor seleccione un archivo PDF válido');
        return;
      }

      // Validar tamaño (10MB)
      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        setError('El archivo excede el tamaño máximo permitido (10MB)');
        return;
      }

      setUploadedFile(file);
    }
  };

  const handleProcessReport = async () => {
    if (!uploadedFile) {
      setError('Por favor seleccione un archivo PDF');
      return;
    }

    setIsProcessing(true);
    setError(null);
    
    try {
      // Llamar al backend para procesar el borrador
      const pdfBlob = await scopusApi.procesarBorrador(uploadedFile);
      
      // Crear URL del blob para descarga
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'certificado_final.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      // Reset form
      setUploadedFile(null);
      
      // Mostrar mensaje de éxito
      alert('Certificado generado y descargado exitosamente');
      
    } catch (error) {
      console.error('Error processing report:', error);
      const errorMessage = error instanceof Error 
        ? error.message 
        : 'Error desconocido al procesar el certificado';
      setError(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCancel = () => {
    setUploadedFile(null);
    setError(null);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-neutral-900 flex items-center">
              <ClipboardCheck className="h-6 w-6 mr-3 text-primary-500" />
              Generación de Certificaciones
            </h1>
            <p className="text-neutral-600 mt-1">
              Carga aquí el borrador para generar la certificación
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="bg-white rounded-lg border border-neutral-200 p-6">
        <div className="space-y-6">
          {/* Error Message */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
              <AlertCircle className="h-5 w-5 text-red-600 mr-3 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-red-800">Error</p>
                <p className="text-sm text-red-600 mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* File Upload */}
          <div>
            <div className="border-2 border-dashed border-neutral-300 rounded-lg p-8 text-center hover:border-neutral-400 transition-colors">
              <Upload className="mx-auto h-16 w-16 text-neutral-400 mb-4" />
              <div className="mb-2">
                <label className="cursor-pointer">
                  <span className="text-primary-500 hover:text-primary-400 font-medium text-lg">
                    Haz clic para subir un archivo
                  </span>
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileUpload}
                    className="hidden"
                    disabled={isProcessing}
                  />
                </label>
                <span className="text-neutral-600"> o arrastra y suelta aquí</span>
              </div>
              <p className="text-sm text-neutral-500">Solo archivos PDF hasta 10MB</p>
              
              {uploadedFile && (
                <div className="mt-6 p-4 bg-green-50 rounded-lg border border-green-200">
                  <div className="flex items-center justify-center text-green-800">
                    <FileText className="h-5 w-5 mr-2" />
                    <span className="font-medium">{uploadedFile.name}</span>
                  </div>
                  <p className="text-sm text-green-600 mt-2">
                    Tamaño: {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end space-x-4 pt-6 border-t border-neutral-200">
            <button
              onClick={handleCancel}
              disabled={isProcessing}
              className="px-6 py-2 border border-neutral-300 rounded-lg text-sm font-medium text-neutral-700 hover:bg-neutral-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancelar
            </button>
            <button
              onClick={handleProcessReport}
              disabled={isProcessing || !uploadedFile}
              className="px-6 py-2 bg-primary-500 text-white rounded-lg text-sm font-medium hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isProcessing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Procesando...
                </>
              ) : (
                <>
                  <Download className="h-4 w-4 mr-2" />
                  Generar Certificado
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
