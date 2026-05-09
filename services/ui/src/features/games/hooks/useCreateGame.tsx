import { GameService } from "@/features/games/services/game.service"
import type { Game, GameCreate } from "@/features/games/types/game"
import { useState } from "react"

export function useCreateGame() {
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string>("")

    const create = async (data: GameCreate): Promise<Game | null> => {
        setError("")
        setLoading(true)

        const { result, error } = await GameService.create(data)
        setLoading(false)

        if (error) {
            setError(error)
        }

        return result
    }

    return { loading, create, error }
}
