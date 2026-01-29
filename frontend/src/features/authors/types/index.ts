import {Publication} from "@/types/api";

export interface Autor {
    author_id: string;
    publications_list: Publication[];
    error?: string;
}

// Autor
export interface Author {
    author_id: string;
    name: string;
    surname: string;
    dni: string;
    title: string;
    institutional_email?: string;
    gender: string;
    position: string;
    department: string;
}

export interface AuthorCreateRequest {
    author_id?: string;
    name: string;
    surname: string;
    dni: string;
    title: string;
    institutional_email?: string;
    gender: string;
    position: string;
    department: string;
}

export interface AuthorUpdateRequest {
    name?: string;
    surname?: string;
    dni?: string;
    title?: string;
    institutional_email?: string;
    gender?: string;
    position?: string;
    department?: string;
}

export interface AuthorResponse {
    author_id: string;
    name: string;
    surname: string;
    dni: string;
    title: string;
    institutional_email?: string;
    gender: string;
    position: string;
    department: string;
}

export interface AuthorsResponse {
    authors: AuthorResponse[];
}