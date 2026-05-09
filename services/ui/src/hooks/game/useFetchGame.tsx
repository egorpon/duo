import { GameService } from "@/services/game.service"
import type { Game } from "@/types/game"
import { useState } from "react"

export function useFetchGame() {
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string>("")

    const fetch = async (id: number): Promise<Game | null> => {
        setError("")
        setLoading(true)

        const { result, error } = await GameService.get(id)
        setLoading(false)

        if (error) {
            setError(error)
        }

        return result
    }

    return { loading, fetch, error }
}
