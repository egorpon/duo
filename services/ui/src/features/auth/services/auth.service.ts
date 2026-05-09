import { makeRequest } from "@/shared/lib/api"
import type { ApiResponse } from "@/shared/types/api"
import type { JWT } from "@/features/auth/types/token"

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
