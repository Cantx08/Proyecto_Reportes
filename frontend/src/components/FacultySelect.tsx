'use client';

import React, { useState, useEffect } from 'react';
import { Loader2 } from 'lucide-react';

interface Faculty {
  key: string;
  value: string;
}

interface FacultySelectProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
  disabled?: boolean;
  required?: boolean;
}

export const FacultySelect: React.FC<FacultySelectProps> = ({
  value,
  onChange,
  error,
  disabled = false,
  required = false
}) => {
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFaculties = async () => {
      try {
        const response = await fetch('http://localhost:8000/faculties');
        const data = await response.json();
        
        if (data.success) {
          setFaculties(data.data);
        }
      } catch (error) {
        console.error('Error loading faculties:', error);
      } finally {
        setLoading(false);
      }
    };

    loadFaculties();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-2">
        <Loader2 className="h-5 w-5 animate-spin text-gray-400" />
      </div>
    );
  }

  return (
    <div className="relative">
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className={`w-full px-3 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
          error ? 'border-red-500' : 'border-gray-300'
        } ${disabled ? 'bg-gray-100 cursor-not-allowed' : ''}`}
        required={required}
      >
        <option value="">Selecciona una facultad...</option>
        {faculties.map((faculty) => (
          <option key={faculty.key} value={faculty.value}>
            {faculty.value}
          </option>
        ))}
      </select>
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};
