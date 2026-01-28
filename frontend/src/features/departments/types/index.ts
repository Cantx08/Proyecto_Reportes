export interface Department {
    dep_code: string;
    dep_name: string;
    fac_name: string;
}

export interface DepartmentsResponse {
    success: boolean;
    data: Department[];
    message: string;
}

// Departamento (nuevo)
export interface NewDepartment {
    dep_id: string;
    dep_code: string;
    dep_name: string;
    fac_name: string;
}

export interface DepartmentCreateRequest {
    dep_id: string;
    dep_code: string;
    dep_name: string;
    fac_name: string;
}

export interface DepartmentUpdateRequest {
    dep_code?: string;
    dep_name?: string;
    fac_name?: string;
}

export interface DepartmentResponse {
    dep_id: string;
    dep_code: string;
    dep_name: string;
    fac_name: string;
}