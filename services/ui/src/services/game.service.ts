import { makeRequest } from "@/lib/api"
import type { ApiResponse } from "@/types/api"
import type { Game, GameCreate } from "@/types/game"

const GameService = {
    create: async (data: GameCreate): Promise<ApiResponse<Game>> => {
        return await makeRequest<Game>("/games/create/", {
            method: "post",
            body: data,
        })
    },
    get: async (id: number): Promise<ApiResponse<Game>> => {
        return await makeRequest<Game>(`/games/${id}/`)
    },
}

export { GameService }
