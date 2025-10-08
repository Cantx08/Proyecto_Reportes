'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useNewDepartments as useDepartments } from '@/hooks/useNewDepartments';
import type { DepartmentResponse } from '@/types/api';

interface DepartmentSelectProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
  className?: string;
  placeholder?: string;
}

const DepartmentSelect: React.FC<DepartmentSelectProps> = ({
  value,
  onChange,
  error,
  className = '',
  placeholder = 'Escriba o seleccione un departamento'
}) => {
  const { departments, loading, error: fetchError } = useDepartments();
  const [isOpen, setIsOpen] = useState(false);
  const [filteredDepartments, setFilteredDepartments] = useState<DepartmentResponse[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Filtrar departamentos basado en el texto ingresado
  useEffect(() => {
    if (!departments || !departments.length) return;
    
    if (!value.trim()) {
      setFilteredDepartments(departments);
      return;
    }

    const filtered = departments.filter((dept: DepartmentResponse) => 
      dept.dep_name.toLowerCase().includes(value.toLowerCase()) ||
      dept.fac_name.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredDepartments(filtered);
  }, [value, departments]);

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

  const handleSelectDepartment = (department: DepartmentResponse) => {
    onChange(department.dep_name);
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
        disabled={loading}
        className={`${baseClassName} ${errorClassName} ${className}`}
        placeholder={loading ? 'Cargando departamentos...' : placeholder}
        aria-describedby={error ? "department-error" : undefined}
        autoComplete="off"
      />
      
      {loading && (
        <div className="absolute inset-y-0 right-0 flex items-center pr-3">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Dropdown de sugerencias */}
      {isOpen && !loading && !fetchError && filteredDepartments.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
          {filteredDepartments.map((department: DepartmentResponse) => (
            <div
              key={department.dep_id}
              onClick={() => handleSelectDepartment(department)}
              className="px-3 py-2 cursor-pointer hover:bg-blue-50 hover:text-blue-700 border-b border-gray-100 last:border-b-0"
              title={`${department.dep_name} - ${department.fac_name}`}
            >
              <div className="font-medium">{department.dep_name}</div>
              <div className="text-xs text-gray-500">{department.fac_name}</div>
            </div>
          ))}
        </div>
      )}

      {/* Mensaje cuando no hay coincidencias */}
      {isOpen && !loading && !fetchError && value.trim() && filteredDepartments.length === 0 && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg p-3">
          <div className="text-gray-500 text-sm">
            No se encontraron departamentos que coincidan con "{value}".
          </div>
        </div>
      )}
      
      {fetchError && (
        <div className="mt-1 text-sm text-red-600" id="department-error">
          Error al cargar departamentos: {fetchError}
        </div>
      )}
      
      {error && (
        <div className="mt-1 text-sm text-red-600" id="department-error">
          {error}
        </div>
      )}
    </div>
  );
};

export default DepartmentSelect;