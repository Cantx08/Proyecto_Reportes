export interface ScopusAccountCreateRequest {
    scopus_id: string;
    author_id: string;
}

export interface ScopusAccountResponse {
    account_id: string;
    scopus_id: string;
    author_id: string;
}
