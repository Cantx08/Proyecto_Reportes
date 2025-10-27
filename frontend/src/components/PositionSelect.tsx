'use client';

import React, { useState, useRef, useEffect } from 'react';
import { usePositions } from '@/hooks/useNewPositions';
import type { PositionResponse } from '@/types/api';

interface PositionSelectProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
  className?: string;
  placeholder?: string;
}

const PositionSelect: React.FC<PositionSelectProps> = ({
  value,
  onChange,
  error,
  className = '',
  placeholder = 'Escriba o seleccione una posición'
}) => {
  const { positions, loading, error: fetchError } = usePositions();
  const [isOpen, setIsOpen] = useState(false);
  const [filteredPositions, setFilteredPositions] = useState<PositionResponse[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Filtrar posiciones basado en el texto ingresado
  useEffect(() => {
    if (!positions || !positions.length) return;
    
    if (!value.trim()) {
      setFilteredPositions(positions);
      return;
    }

    const filtered = positions.filter((position: PositionResponse) => 
      position.pos_name.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredPositions(filtered);
  }, [value, positions]);

  // Cerrar dropdown al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = event.target.value;
    onChange(newValue);
    if (!isOpen) {
      setIsOpen(true);
    }
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handleSelectPosition = (position: PositionResponse) => {
    onChange(position.pos_name);
    setIsOpen(false);
    inputRef.current?.blur();
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Escape') {
      setIsOpen(false);
      inputRef.current?.blur();
    }
  };

  const baseClassName = "w-full p-3 border rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors";
  const errorClassName = error ? "border-error-500 focus:ring-error-500 focus:border-error-500" : "border-neutral-300";

  return (
    <div className="relative" ref={dropdownRef}>
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={handleInputChange}
        onFocus={handleInputFocus}
        onKeyDown={handleKeyDown}
        disabled={loading}
        className={`${baseClassName} ${errorClassName} ${className}`}
        placeholder={loading ? 'Cargando posiciones...' : placeholder}
        aria-describedby={error ? "position-error" : undefined}
        autoComplete="off"
      />
      
      {loading && (
        <div className="absolute inset-y-0 right-0 flex items-center pr-3">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Dropdown de sugerencias */}
      {isOpen && !loading && !fetchError && filteredPositions.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
          {filteredPositions.map((position: PositionResponse, index: number) => (
            <div
              key={`${position.pos_id}-${index}`}
              onClick={() => handleSelectPosition(position)}
              className="px-3 py-2 cursor-pointer hover:bg-blue-50 hover:text-blue-700 border-b border-gray-100 last:border-b-0"
              title={position.pos_name}
            >
              <div className="font-medium">{position.pos_name}</div>
            </div>
          ))}
        </div>
      )}

      {/* Mensaje cuando no hay coincidencias */}
      {isOpen && !loading && !fetchError && value.trim() && filteredPositions.length === 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg p-3">
          <div className="text-gray-500 text-sm">
            No se encontraron posiciones que coincidan con "{value}".
          </div>
        </div>
      )}
      
      {fetchError && (
        <div className="mt-1 text-sm text-red-600" id="position-error">
          Error al cargar posiciones: {fetchError}
        </div>
      )}
      
      {error && (
        <div className="mt-1 text-sm text-red-600" id="position-error">
          {error}
        </div>
      )}
    </div>
  );
};

export default PositionSelect;