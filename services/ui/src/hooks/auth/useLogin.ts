import { AuthService } from "@/services/auth.service"
import type { JWT } from "@/types/token"
import { useState } from "react"

export function useLogin() {
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string>("")

    const login = async (
        email: string,
        password: string
    ): Promise<JWT | null> => {
        setError("")
        setLoading(true)

        const { result, error } = await AuthService.login(email, password)
        setLoading(false)

        if (error) {
            setError(error)
        }

        return result
    }

    return { loading, login, error }
}
