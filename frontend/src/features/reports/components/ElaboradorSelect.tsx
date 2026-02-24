'use client';

import React, { useState, useEffect, useRef } from 'react';
import { ELABORADOR_OPTIONS } from '@/src/features/reports/types';

interface ElaboradorSelectProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

/**
 * Componente selector de elaborador con opción de entrada manual
 * Permite seleccionar de opciones predefinidas o ingresar un valor personalizado
 */
const ElaboradorSelect: React.FC<ElaboradorSelectProps> = ({
  value,
  onChange,
  placeholder = "Seleccione o escriba el elaborador"
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);


  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
    setIsOpen(true);
  };

  const handleOptionSelect = (optionValue: string) => {
    onChange(optionValue);
    setIsOpen(false);
  };

  const filteredOptions = ELABORADOR_OPTIONS.filter(option =>
    option.label.toLowerCase().includes((value || '').toLowerCase())
  );

  return (
    <div ref={wrapperRef} className="relative">
      <input
        type="text"
        className="w-full p-3 border border-neutral-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
        placeholder={placeholder}
        value={value || ''}
        onChange={handleInputChange}
        onFocus={() => setIsOpen(true)}
      />
      
      {isOpen && (
        <ul className="absolute z-10 w-full mt-1 bg-white border border-neutral-300 rounded-md shadow-lg max-h-60 overflow-auto">
          {filteredOptions.length > 0 ? (
            filteredOptions.map((option) => (
              <li
                key={option.value}
                className={`px-4 py-2 cursor-pointer hover:bg-primary-50 transition-colors ${
                  option.value === value ? 'bg-primary-100 text-primary-700' : ''
                }`}
                onClick={() => handleOptionSelect(option.value)}
              >
                {option.label}
              </li>
            ))
          ) : (
            <li className="px-4 py-2 text-neutral-500 italic">
              {value ? `Usar: "${value}"` : 'No hay opciones disponibles'}
            </li>
          )}
          {value && !ELABORADOR_OPTIONS.some(opt => opt.value === value) && (
            <li
              className="px-4 py-2 cursor-pointer hover:bg-primary-50 text-primary-600 border-t"
              onClick={() => handleOptionSelect(value)}
            >
              ✓ Usar valor personalizado: &quot;{value}&quot;
            </li>
          )}
        </ul>
      )}
    </div>
  );
};

export default ElaboradorSelect;
