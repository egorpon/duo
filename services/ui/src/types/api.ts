type Method = "get" | "post" | "patch" | "put" | "delete"
type ApiOptions = {
    method: Method
    body?: Record<string, any>
    query?: Record<string, any>
}

type SuccessResponse<T> = {
    result: T
    error: null
}
type ErrorResponse = {
    result: null
    error: string
}
type ApiResponse<T> = SuccessResponse<T> | ErrorResponse

type ErrorResponseData = {
    detail: string | Record<string, string>[]
}

export type {
    ApiOptions,
    ApiResponse,
    ErrorResponse,
    ErrorResponseData,
    Method,
    SuccessResponse,
}
