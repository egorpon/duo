import { AuthService } from "@/features/auth/services/auth.service"
import type { JWT } from "@/features/auth/types/token"
import { useState } from "react"

export function useRegister() {
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string>("")

    const register = async (
        email: string,
        password: string
    ): Promise<JWT | null> => {
        setError("")
        setLoading(true)

        const { result, error } = await AuthService.register(email, password)
        setLoading(false)

        if (error) {
            setError(error)
        }

        return result
    }

    return { loading, register, error }
}
