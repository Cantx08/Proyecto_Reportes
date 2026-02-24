import axios, { AxiosResponse, AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 1. Crear la instancia única
export const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 2. Interceptor para agregar el token de autenticación
axiosInstance.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: AxiosError) => {
        // TODO: Agregar un toast notification global de error si quisieras
        console.error('API Error:', error?.response?.data || error.message);
        return Promise.reject(error);
    }
);
