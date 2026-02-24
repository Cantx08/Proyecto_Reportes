export interface AuthorCreateRequest {
    first_name: string;
    last_name: string;
    institutional_email?: string;
    title?: string;
    gender: string;
    job_position_id: string;
    department_id: string;
}

export interface AuthorUpdateRequest {
    first_name?: string;
    last_name?: string;
    title?: string;
    job_position_id?: string;
    department_id?: string;
}

export interface AuthorResponse {
    author_id: string;
    first_name: string;
    last_name: string;
    title: string;
    institutional_email?: string;
    gender: string;
    job_position_id: string;
    department_id: string;
}

export interface ImportAuthorsResponse {
    message: string;
    details: {
        created: number;
        updated: number;
        errors?: string[];
    };
}