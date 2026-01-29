export interface JobPositionCreateRequest {
    pos_name: string;
}

export interface JobPositionUpdateRequest {
    pos_name?: string;
}

export interface JobPositionResponse {
    pos_id: string;
    pos_name: string;
}