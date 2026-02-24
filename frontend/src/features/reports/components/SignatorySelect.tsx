'use client';

import React, { useState, useRef, useEffect, useMemo } from 'react';

interface SignatorySelectProps {
  positionValue: number | string;
  nameValue: string;
  onPositionChange: (value: number | string) => void;
  onNameChange: (value: string) => void;
  error?: string;
  className?: string;
  placeholder?: string;
}

const FIRMANTE_OPTIONS = [
  { value: 1, label: 'Director de Investigación' },
  { value: 2, label: 'Vicerrectora de Investigación' }
];

const FirmanteSelect: React.FC<SignatorySelectProps> = ({
  positionValue,
  nameValue,
  onPositionChange,
  onNameChange,
  error,
  className = '',
  placeholder = 'Escriba o seleccione un firmante'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Calcular el valor del input basado en positionValue usando useMemo
  const inputValue = useMemo(() => {
    if (typeof positionValue === 'number') {
      const option = FIRMANTE_OPTIONS.find(opt => opt.value === positionValue);
      return option ? option.label : '';
    }
    return String(positionValue);
  }, [positionValue]);

  // Filtrar opciones según el texto ingresado usando useMemo
  const filteredOptions = useMemo(() => {
    if (!inputValue.trim()) {
      return FIRMANTE_OPTIONS;
    }

    return FIRMANTE_OPTIONS.filter(option =>
      option.label.toLowerCase().includes(inputValue.toLowerCase())
    );
  }, [inputValue]);

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
    onPositionChange(newValue);
    setIsOpen(true);
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handleSelectOption = (option: {value: number, label: string}) => {
    onPositionChange(option.value); // Enviamos el número para opciones predefinidas
    // Limpiar el nombre cuando se selecciona una opción predefinida
    onNameChange('');
    setIsOpen(false);
    inputRef.current?.blur();
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Escape') {
      setIsOpen(false);
      inputRef.current?.blur();
    }
  };

  const handleNombreChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onNameChange(event.target.value);
  };

  // Determinar si necesitamos mostrar el campo de nombre
  const showNombreField = typeof positionValue === 'string' && positionValue.trim() !== '';
  const isCustomFirmante = !FIRMANTE_OPTIONS.some(opt => opt.value === positionValue);

  const baseClassName = "w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500";
  const errorClassName = error ? "border-red-500 focus:ring-red-500 focus:border-red-500" : "";
  
  return (
    <div className="space-y-3">
      {/* Campo para cargo/título del firmante */}
      <div className="relative" ref={dropdownRef}>
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onKeyDown={handleKeyDown}
          className={`${baseClassName} ${errorClassName} ${className}`}
          placeholder={placeholder}
          aria-describedby={error ? "firmante-error" : undefined}
          autoComplete="off"
        />

        {/* Dropdown de sugerencias */}
        {isOpen && filteredOptions.length > 0 && (
          <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
            {filteredOptions.map((option) => (
              <div
                key={option.value}
                onClick={() => handleSelectOption(option)}
                className="px-3 py-2 cursor-pointer hover:bg-blue-50 hover:text-blue-700 border-b border-gray-100 last:border-b-0"
              >
                <div className="font-medium">{option.label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Mensaje cuando no hay coincidencias */}
        {isOpen && inputValue.trim() && filteredOptions.length === 0 && (
          <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg p-3">
            <div className="text-gray-500 text-sm">
              No se encontraron opciones que coincidan con &quot;{inputValue}&quot;.
              <br />
              <span className="text-blue-600 font-medium">Puede escribir el cargo personalizado.</span>
            </div>
          </div>
        )}
      </div>

      {/* Campo adicional para nombre del firmante (solo para firmantes personalizados) */}
      {showNombreField && isCustomFirmante && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Nombre del Firmante *
          </label>
          <input
            type="text"
            value={nameValue}
            onChange={handleNombreChange}
            className={`${baseClassName} ${className}`}
            placeholder="Ej: Dr. Juan Pérez Rodríguez"
            autoComplete="off"
          />
          <p className="mt-1 text-xs text-gray-500">
            Ingrese el nombre completo de la persona que firmará el documento
          </p>
        </div>
      )}
      
      {error && (
        <div className="mt-1 text-sm text-red-600" id="firmante-error">
          {error}
        </div>
      )}
    </div>
  );
};

export default FirmanteSelect;