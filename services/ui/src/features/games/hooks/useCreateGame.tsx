import { GameService } from "@/features/games/services/game.service"
import { useApiCall } from "@/shared/hooks/useApiCall"

export function useCreateGame() {
    const { loading, error, call: create } = useApiCall(GameService.create)
    return { loading, error, create }
}
