'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useCargos } from '@/hooks/useCargos';
import type { Cargo } from '@/types/api';

interface CargoSelectProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
  className?: string;
  placeholder?: string;
}

const CargoSelect: React.FC<CargoSelectProps> = ({
  value,
  onChange,
  error,
  className = '',
  placeholder = 'Escriba o seleccione un cargo'
}) => {
  const { cargos, isLoading, error: fetchError } = useCargos();
  const [isOpen, setIsOpen] = useState(false);
  const [filteredCargos, setFilteredCargos] = useState<Cargo[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Filtrar cargos basado en el texto ingresado
  useEffect(() => {
    if (!cargos.length) return;
    
    if (!value.trim()) {
      setFilteredCargos(cargos);
      return;
    }

    const filtered = cargos.filter(cargo => 
      cargo.cargo.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredCargos(filtered);
  }, [value, cargos]);

  // Cerrar dropdown al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = event.target.value;
    onChange(newValue);
    setIsOpen(true);
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handleSelectCargo = (cargo: Cargo) => {
    onChange(cargo.cargo);
    setIsOpen(false);
    inputRef.current?.blur();
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Escape') {
      setIsOpen(false);
      inputRef.current?.blur();
    }
  };

  const baseClassName = "w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500";
  const errorClassName = error ? "border-red-500 focus:ring-red-500 focus:border-red-500" : "";
  
  return (
    <div className="relative" ref={dropdownRef}>
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={handleInputChange}
        onFocus={handleInputFocus}
        onKeyDown={handleKeyDown}
        disabled={isLoading}
        className={`${baseClassName} ${errorClassName} ${className}`}
        placeholder={isLoading ? 'Cargando cargos...' : placeholder}
        aria-describedby={error ? "cargo-error" : undefined}
        autoComplete="off"
      />
      
      {isLoading && (
        <div className="absolute inset-y-0 right-0 flex items-center pr-3">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Dropdown de sugerencias */}
      {isOpen && !isLoading && !fetchError && filteredCargos.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
          {filteredCargos.map((cargo: Cargo, index: number) => (
            <div
              key={`${cargo.cargo}-${index}`}
              onClick={() => handleSelectCargo(cargo)}
              className="px-3 py-2 cursor-pointer hover:bg-blue-50 hover:text-blue-700 border-b border-gray-100 last:border-b-0"
              title={`${cargo.cargo} - ${cargo.tiempo === 'TC' ? 'Tiempo Completo' : 'Tiempo Parcial'}`}
            >
              <div className="font-medium">{cargo.cargo}</div>
              <div className="text-xs text-gray-500">
                {cargo.tiempo === 'TC' ? 'Tiempo Completo' : 'Tiempo Parcial'}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Mensaje cuando no hay coincidencias */}
      {isOpen && !isLoading && !fetchError && value.trim() && filteredCargos.length === 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg p-3">
          <div className="text-gray-500 text-sm">
            No se encontraron cargos que coincidan con "{value}".
            <br />
            <span className="text-blue-600 font-medium">Puede escribir el nombre personalizado.</span>
          </div>
        </div>
      )}
      
      {fetchError && (
        <div className="mt-1 text-sm text-red-600" id="cargo-error">
          Error al cargar cargos: {fetchError}
        </div>
      )}
      
      {error && (
        <div className="mt-1 text-sm text-red-600" id="cargo-error">
          {error}
        </div>
      )}
    </div>
  );
};

export default CargoSelect;