import useAuthStore from "@/stores/auth"
import { FetchError, ofetch } from "ofetch"
import type {
    ApiResponse,
    ApiOptions,
    ErrorResponseData,
    ErrorResponse,
} from "@/types/api"

const api = ofetch.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: { "Content-Type": "application/json" },
    retry: 0,
    timeout: 5000,
    onRequest: ({ options }) => {
        const token = useAuthStore.getState().token
        if (token !== null) {
            options.headers.set("Authorization", `Bearer ${token}`)
        }
    },
    onResponseError: ({ response }) => {
        if (response.status === 401) {
            useAuthStore.getState().logout()
        }
    },
})

const parseError = (err: any): ErrorResponse => {
    if (err instanceof FetchError) {
        const error: ErrorResponseData = err.data
        if (error.detail instanceof Object) {
            return {
                result: null,
                error: error.detail[0]["msg"] || "Something bad happened",
            }
        } else {
            return { result: null, error: error.detail }
        }
    }
    return { result: null, error: "Something bad happened" }
}

const makeRequest = async <T>(
    url: string,
    { method, body, query }: ApiOptions = { method: "get" }
): Promise<ApiResponse<T>> => {
    try {
        const result = await api<T>(url, { method, body, query })
        return { result, error: null }
    } catch (err) {
        return parseError(err)
    }
}

export { api, makeRequest }
