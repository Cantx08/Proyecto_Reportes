'use client';

import React, { useState, useRef, useCallback } from 'react';
import { Upload, FileText, X, CheckCircle } from 'lucide-react';
import { reportService } from '@/src/features/reports/services/reportService';

interface PdfDropZoneProps {
  onError: (error: string) => void;
}

const PdfDropZone: React.FC<PdfDropZoneProps> = ({ onError }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processSuccess, setProcessSuccess] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = useCallback((file: File): boolean => {
    if (file.type !== 'application/pdf') {
      onError('Solo se aceptan archivos PDF.');
      return false;
    }
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      onError('El archivo excede el tamaño máximo permitido (10MB).');
      return false;
    }
    return true;
  }, [onError]);

  const handleFile = useCallback((file: File) => {
    if (validateFile(file)) {
      setSelectedFile(file);
      setProcessSuccess(false);
    }
  }, [validateFile]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  }, [handleFile]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
    // Reset input para permitir seleccionar el mismo archivo
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [handleFile]);

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setProcessSuccess(false);
  };

  const handleProcessDraft = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setProcessSuccess(false);

    try {
      const blob = await reportService.processDraft(selectedFile);

      // Descargar el PDF final
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'certificado_final.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setProcessSuccess(true);
    } catch (error) {
      onError(error instanceof Error ? error.message : 'Error al procesar el borrador');
    } finally {
      setIsProcessing(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-all duration-200 ease-in-out
          ${isDragOver
            ? 'border-primary-500 bg-primary-50 scale-[1.01]'
            : selectedFile
              ? 'border-success-300 hover:border-success-400'
              : 'border-neutral-300 hover:border-primary-400'
          }
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileSelect}
          className="hidden"
        />

        {!selectedFile ? (
          <div className="flex flex-col items-center space-y-3">
            <div className={`
              p-3 rounded-full transition-colors
              ${isDragOver ? 'bg-primary-100 text-primary-600' : 'bg-neutral-100 text-neutral-400'}
            `}>
              <Upload className="h-8 w-8" />
            </div>
            <div>
              <p className="text-sm font-medium text-neutral-700">
                {isDragOver ? 'Suelte el archivo aquí' : 'Arrastre el archivo PDF aquí'}
              </p>
              <p className="text-xs text-neutral-500 mt-1">
                o haga clic para seleccionar un archivo (máx. 10MB)
              </p>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-between" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-lg">
                <FileText className="h-6 w-6 text-success-500" />
              </div>
              <div className="text-left">
                <p className="text-sm font-medium text-neutral-800 truncate max-w-xs">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-neutral-500">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {processSuccess && (
                <CheckCircle className="h-5 w-5 text-success-500" />
              )}
              <button
                onClick={handleRemoveFile}
                className="p-1 hover:bg-neutral-200 rounded-full transition-colors"
                title="Quitar archivo"
              >
                <X className="h-4 w-4 text-neutral-500" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Process Button */}
      {selectedFile && (
        <div className="flex flex-col items-center space-y-3">
          <button
            onClick={handleProcessDraft}
            disabled={isProcessing}
            className="w-full sm:w-auto bg-success-600 hover:bg-success-700 disabled:bg-neutral-400 disabled:cursor-not-allowed text-white font-medium py-3 px-8 rounded-md transition-colors duration-200 shadow-sm flex items-center justify-center"
          >
            {isProcessing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Aplicando plantilla...
              </>
            ) : (
              <>
                <FileText className="h-4 w-4 mr-2" />
                Generar Certificado
              </>
            )}
          </button>

          {processSuccess && (
            <div className="flex items-center space-x-2 text-success-700 rounded-lg px-4 py-2">
              <CheckCircle className="h-4 w-4" />
              <span className="text-sm font-medium">
                Certificado generado exitosamente
              </span>
            </div>
          )}

          {/* Loading state */}
          {isProcessing && (
            <div className="w-full bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center flex-col">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-3"></div>
                <span className="text-sm font-medium text-blue-900">
                  Aplicando plantilla institucional al borrador...
                </span>
                <span className="text-xs text-blue-600 mt-1">
                  Esto puede tomar unos segundos
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PdfDropZone;
