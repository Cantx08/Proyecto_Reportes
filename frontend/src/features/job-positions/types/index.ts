export interface JobPositionCreateRequest {
    posName: string;
}

export interface JobPositionUpdateRequest {
    posName?: string;
}

export interface JobPositionResponse {
    posId: string;
    posName: string;
}