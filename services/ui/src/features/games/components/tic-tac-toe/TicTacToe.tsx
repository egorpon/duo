import useAuthStore from "@/features/auth/stores/auth"
import type { GameMoveMessage } from "@/features/games/types/game"
import { TicTacToeStateSchema } from "@/features/games/types/tic-tac-toe"
import type { TicTacToeState } from "@/features/games/types/tic-tac-toe"
import { GameBoard } from "./GameBoard"
import { GameOverDialog } from "./GameOverDialog"
import { GameStatus } from "./GameStatus"
import { TicTacToeCell } from "./TicTacToeCell"

interface Props {
    gameState: any
    sendMoveHandler: (message: GameMoveMessage) => void
}

export function TicTacToe({ gameState, sendMoveHandler }: Props) {
    const user = useAuthStore((state) => state.user)
    const { data } = TicTacToeStateSchema.safeParse(gameState)
    if (data === undefined) {
        return <div>Failed to parse game state</div>
    }
    const state: TicTacToeState = data!

    const isOver = state.winner !== null || state.is_draw

    const getStatusText = () => {
        if (state.is_draw) return "It's a draw!"
        if (state.winner !== null)
            return state.winner === user?.id ? "You win!" : "Opponent wins!"
        return state.your_turn ? "Your turn" : "Opponent's turn"
    }

    const getDialogTitle = () => {
        if (state.is_draw) return "It's a draw!"
        if (state.winner !== null)
            return state.winner === user?.id ? "You win!" : "You lost!"
        return ""
    }

    const handleClick = (i: number, j: number) => {
        sendMoveHandler({
            type: "game_move",
            body: { game_move: { coordinate: [i, j] } },
        })
    }

    return (
        <div className="flex flex-col items-center gap-6 p-8">
            <GameOverDialog isOver={isOver} title={getDialogTitle()} />

            <div className="flex flex-col items-center gap-2">
                <h2 className="text-2xl font-bold tracking-tight">
                    Tic Tac Toe
                </h2>
                <div className="flex items-center gap-2">
                    <p className="text-sm text-muted-foreground">You play as</p>
                    <TicTacToeCell value={state.your_symbol} />
                </div>
            </div>

            <GameStatus
                isOver={isOver}
                yourTurn={state.your_turn}
                text={getStatusText()}
            />

            <GameBoard
                board={state.board}
                yourTurn={state.your_turn}
                isOver={isOver}
                onCellClick={handleClick}
            />
        </div>
    )
}
