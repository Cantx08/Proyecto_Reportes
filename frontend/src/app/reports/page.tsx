'use client';

import React, { useState } from 'react';
import { 
  ClipboardCheck, 
  Download,
  Upload,
  FileText
} from 'lucide-react';

export default function InformesPage() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setUploadedFile(file);
    } else {
      alert('Por favor seleccione un archivo PDF válido');
    }
  };

  const handleProcessReport = async () => {
    if (!uploadedFile) {
      alert('Por favor seleccione un archivo PDF');
      return;
    }

    setIsProcessing(true);
    
    try {
      // Aquí se integraría con el backend para procesar el PDF
      // Simulación de procesamiento
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Simular descarga del archivo procesado
      alert('Certificado generado exitosamente');
      
      // Reset form
      setUploadedFile(null);
      
    } catch (error) {
      console.error('Error processing report:', error);
      alert('Error al procesar el certificado. Por favor intente nuevamente.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCancel = () => {
    setUploadedFile(null);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <ClipboardCheck className="h-6 w-6 mr-3 text-[#042a53]" />
              Generación de Certificaciones
            </h1>
            <p className="text-gray-600 mt-1">
              Carga el archivo PDF para generar el certificado oficial
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="space-y-6">
          {/* File Upload */}
          <div>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors">
              <Upload className="mx-auto h-16 w-16 text-gray-400 mb-4" />
              <div className="mb-2">
                <label className="cursor-pointer">
                  <span className="text-[#042a53] hover:text-[#1e7bb8] font-medium text-lg">
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
              <p className="text-sm text-gray-500">Solo archivos PDF hasta 10MB</p>
              
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
          <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200">
            <button
              onClick={handleCancel}
              disabled={isProcessing}
              className="px-6 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancelar
            </button>
            <button
              onClick={handleProcessReport}
              disabled={isProcessing || !uploadedFile}
              className="px-6 py-2 bg-[#5a8db3] text-white rounded-lg text-sm font-medium hover:bg-[#4a7d9f] disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isProcessing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Procesando...
                </>
              ) : (
                <>
                  <Download className="h-4 w-4 mr-2" />
                  Descargar PDF
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}