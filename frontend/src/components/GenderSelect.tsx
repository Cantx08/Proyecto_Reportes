'use client';

import React, { useState, useRef, useEffect } from 'react';

interface GenderSelectProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
  className?: string;
  placeholder?: string;
}

const GenderSelect: React.FC<GenderSelectProps> = ({
  value,
  onChange,
  error,
  className = '',
  placeholder = 'Escriba o seleccione un género'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filteredOptions, setFilteredOptions] = useState<Array<{value: string, label: string}>>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const genderOptions = [
    { value: 'M', label: 'Masculino' },
    { value: 'F', label: 'Femenino' }
  ];

  // Filtrar opciones basado en el texto ingresado
  useEffect(() => {
    if (!value.trim()) {
      setFilteredOptions(genderOptions);
      return;
    }

    const filtered = genderOptions.filter(option => 
      option.label.toLowerCase().includes(value.toLowerCase()) ||
      option.value.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredOptions(filtered);
  }, [value]);

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

  const handleSelectOption = (option: {value: string, label: string}) => {
    onChange(option.value);
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

  // Mostrar etiqueta completa si es una opción predefinida
  const displayValue = (() => {
    const option = genderOptions.find(opt => opt.value === value);
    return option ? option.label : value;
  })();
  
  return (
    <div className="relative" ref={dropdownRef}>
      <input
        ref={inputRef}
        type="text"
        value={displayValue}
        onChange={handleInputChange}
        onFocus={handleInputFocus}
        onKeyDown={handleKeyDown}
        className={`${baseClassName} ${errorClassName} ${className}`}
        placeholder={placeholder}
        aria-describedby={error ? "gender-error" : undefined}
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
      {isOpen && value.trim() && filteredOptions.length === 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg p-3">
          <div className="text-gray-500 text-sm">
            No se encontraron opciones que coincidan con "{value}".
          </div>
        </div>
      )}
      
      {error && (
        <div className="mt-1 text-sm text-red-600" id="gender-error">
          {error}
        </div>
      )}
    </div>
  );
};

export default GenderSelect;