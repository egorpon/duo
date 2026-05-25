import { TicTacToe } from "@/features/games/components/tic-tac-toe/TicTacToe"
import { useFetchGame } from "@/features/games/hooks/useFetchGame"
import { useGameWebSocket } from "@/features/games/hooks/useGameWebSocket"
import useAuthStore from "@/features/auth/stores/auth"
import { PageLoading } from "@/shared/components/layout/PageLoading"
import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router"
import type { Game } from "@/features/games/types/game"

export function PlayGamePage() {
    const navigate = useNavigate()
    const { id } = useParams()
    const [game, setGame] = useState<Game | null>(null)
    const { loading, fetch } = useFetchGame()
    const token = useAuthStore((state) => state.token)

    const { gameState, sendMessage } = useGameWebSocket(id!, token)

    useEffect(() => {
        const startup = async () => {
            const game = await fetch(Number(id))
            if (!game) {
                navigate("/")
                return
            }
            setGame(game)
        }
        startup()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [id])

    if (loading) return <PageLoading />
    if (!game) return null
    if (!gameState) {
        return (
            <div className="flex h-full items-center justify-center text-muted-foreground">
                Waiting for opponent...
            </div>
        )
    }

    return (
        <div className="flex w-full items-start justify-center">
            {game.type === "tic_tac_toe" && (
                <TicTacToe
                    gameState={gameState}
                    sendMoveHandler={sendMessage}
                />
            )}
        </div>
    )
}
