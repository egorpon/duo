import { makeRequest } from "@/shared/lib/api"
import type { ApiResponse } from "@/shared/types/api"
import type { JWT } from "@/features/auth/types/token"
import type { User } from "@/features/auth/types/user"

const UserService = {
    me: async (): Promise<ApiResponse<User>> => {
        return await makeRequest<User>("/users/me/")
    },
    get: async (id: number): Promise<ApiResponse<User>> => {
        return await makeRequest<User>(`/users/${id}/`)
    },
    updateEmail: async (email: string): Promise<ApiResponse<User>> => {
        return await makeRequest<User>(`/users/update/email/`, {
            method: "post",
            body: { email },
        })
    },
    updatePassword: async (password: string): Promise<ApiResponse<JWT>> => {
        return await makeRequest<JWT>(`/users/update/password/`, {
            method: "post",
            body: { password },
        })
    },
}

export { UserService }
