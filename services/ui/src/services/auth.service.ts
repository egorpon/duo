import { api, makeRequest } from "@/lib/api"
import type { JWT } from "@/types/token"

const AuthService = {
    login: async (email: string, password: string): Promise<JWT | null> => {
        const { result } = await makeRequest<JWT>({ url: "/auth/login/", method: "POST", data: { email, password } })
        return result
    },
    register: async (email: string, password: string): Promise<JWT> => {
        return await api<JWT>("/auth/register/", { method: "POST", body: { email, password } })
    },
}

export { AuthService }
