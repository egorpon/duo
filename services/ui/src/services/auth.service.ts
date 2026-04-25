import { makeRequest, type ApiResponse } from "@/lib/api"
import type { JWT } from "@/types/token"

const AuthService = {
    login: async (
        email: string,
        password: string
    ): Promise<ApiResponse<JWT>> => {
        return await makeRequest<JWT>("/auth/login/", {
            method: "post",
            body: { email, password },
        })
    },
    register: async (
        email: string,
        password: string
    ): Promise<ApiResponse<JWT>> => {
        return await makeRequest<JWT>("/auth/register/", {
            method: "post",
            body: { email, password },
        })
    },
}

export { AuthService }
