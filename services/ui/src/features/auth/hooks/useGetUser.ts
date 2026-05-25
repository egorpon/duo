import { UserService } from "@/features/auth/services/user.service"
import type { User } from "@/features/auth/types/user"
import { useState } from "react"

export function useGetUser() {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [user, setUser] = useState<User | null>(null)

    const getUser = async (id: number): Promise<User | null> => {
        setError("")
        setLoading(true)
        const { result, error } = await UserService.get(id)
        setLoading(false)
        if (error) setError(error)
        setUser(result)
        return result
    }

    return { loading, error, user, getUser }
}
