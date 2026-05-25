import { GameService } from "@/features/games/services/game.service"
import { useApiCall } from "@/shared/hooks/useApiCall"

export function useFetchGame() {
    const { loading, error, call: fetch } = useApiCall(GameService.get)
    return { loading, error, fetch }
}
