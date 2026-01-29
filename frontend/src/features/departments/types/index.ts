export interface DepartmentCreateRequest {
    depName: string;
    depCode: string;
    facultyName: string;
}

export interface DepartmentUpdateRequest {
    depName?: string;
    depCode?: string;
    facultyName?: string;
}

export interface DepartmentResponse {
    depId: string;
    depName: string;
    depCode: string;
    facultyCode: string;
    facultyName: string;
}