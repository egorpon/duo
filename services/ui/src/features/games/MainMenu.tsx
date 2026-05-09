import { Button } from "@/components/ui/button"
import { useCreateGame } from "@/hooks/game/useCreateGame"
import type { GameType } from "@/types/game"
import { useNavigate } from "react-router"

export function MainMenu() {
    const navigate = useNavigate()
    const { loading, create, error } = useCreateGame()

    const handleCreateGame = async (type: GameType) => {
        const game = await create({ type })
        if (game === null) {
            console.error("Failed to create game:", error)
            return
        }
        navigate(`/game/${game.id}`)
    }
    return (
        <div>
            Main Menu
            <div>
                <Button
                    disabled={loading}
                    onClick={() => handleCreateGame("tic_tac_toe")}
                >
                    Tic Tac Toe
                </Button>
            </div>
        </div>
    )
}
