export interface DepartmentCreateRequest {
    dep_name: string;
    dep_code: string;
    faculty_name: string;
}

export interface DepartmentUpdateRequest {
    dep_name?: string;
    dep_code?: string;
    faculty_name?: string;
}

export interface DepartmentResponse {
    dep_id: string;
    dep_name: string;
    dep_code: string;
    faculty_code: string;
    faculty_name: string;
}