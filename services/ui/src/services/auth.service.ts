import { api } from "@/lib/api"
import type { JWT } from "@/types/token"

const AuthService = {
    login: async (email: string, password: string): Promise<JWT> => {
        return await api<JWT>("/auth/login/", { body: { email, password } })
    },
    register: async (email: string, password: string): Promise<JWT> => {
        return await api<JWT>("/auth/register/", { body: { email, password } })
    },
}

export { AuthService }
