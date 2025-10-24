'use client';

import React, { useState, useRef, useEffect } from 'react';

interface FirmanteSelectProps {
  cargoValue: number | string;
  nombreValue: string;
  onCargoChange: (value: number | string) => void;
  onNombreChange: (value: string) => void;
  error?: string;
  className?: string;
  placeholder?: string;
}

const FirmanteSelect: React.FC<FirmanteSelectProps> = ({
  cargoValue,
  nombreValue,
  onCargoChange,
  onNombreChange,
  error,
  className = '',
  placeholder = 'Escriba o seleccione un firmante'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filteredOptions, setFilteredOptions] = useState<Array<{value: number, label: string}>>([]);
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const firmanteOptions = [
    { value: 1, label: 'Directora de Investigación' },
    { value: 2, label: 'Vicerrectora de Investigación' }
  ];

  // Sincronizar el valor del input con el prop cargoValue
  useEffect(() => {
    if (typeof cargoValue === 'number') {
      const option = firmanteOptions.find(opt => opt.value === cargoValue);
      setInputValue(option ? option.label : '');
    } else {
      setInputValue(String(cargoValue));
    }
  }, [cargoValue]);

  // Filtrar opciones basado en el texto ingresado
  useEffect(() => {
    if (!inputValue.trim()) {
      setFilteredOptions(firmanteOptions);
      return;
    }

    const filtered = firmanteOptions.filter(option => 
      option.label.toLowerCase().includes(inputValue.toLowerCase())
    );
    setFilteredOptions(filtered);
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
    setInputValue(newValue);
    onCargoChange(newValue);
    setIsOpen(true);
  };

  const handleInputFocus = () => {
    setIsOpen(true);
  };

  const handleSelectOption = (option: {value: number, label: string}) => {
    setInputValue(option.label);
    onCargoChange(option.value); // Enviamos el número para opciones predefinidas
    // Limpiar el nombre cuando se selecciona una opción predefinida
    onNombreChange('');
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
    onNombreChange(event.target.value);
  };

  // Determinar si necesitamos mostrar el campo de nombre
  const showNombreField = typeof cargoValue === 'string' && cargoValue.trim() !== '';
  const isCustomFirmante = !firmanteOptions.some(opt => opt.value === cargoValue);

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
              No se encontraron opciones que coincidan con "{inputValue}".
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
            value={nombreValue}
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