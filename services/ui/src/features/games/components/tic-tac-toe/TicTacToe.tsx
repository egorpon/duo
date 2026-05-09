import useAuthStore from "@/features/auth/stores/auth"
import type { GameMoveMessage } from "@/features/games/types/game"
import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import clsx from "clsx"
import { z } from "zod"
import { useNavigate } from "react-router"
import { TicTacToeCell } from "./TicTacToeCell"

const MoveSchema = z.enum(["x", "o"])
const TicTacToeStateSchema = z.object({
    board: z.array(z.array(MoveSchema.nullable()).length(3)).length(3),
    your_turn: z.boolean(),
    your_symbol: MoveSchema,
    is_draw: z.boolean(),
    winner: z.int().nullable(),
})
type TicTacToeState = z.infer<typeof TicTacToeStateSchema>

const styles = {
    status: {
        base: "rounded-full px-5 py-1.5 text-sm font-semibold transition-all",
        over: "bg-primary/20 text-primary",
        yourTurn: "bg-primary text-primary-foreground shadow-md",
        waiting: "bg-muted text-muted-foreground",
    },
    cell: {
        base: "flex h-24 w-24 items-center justify-center rounded-xl border bg-card transition-all",
        interactive:
            "cursor-pointer hover:border-primary/60 hover:bg-primary/10 active:scale-95",
        static: "cursor-default",
    },
}

interface Props {
    gameState: any
    sendMoveHandler: (message: GameMoveMessage) => void
}
export function TicTacToe({ gameState, sendMoveHandler }: Props) {
    const user = useAuthStore((state) => state.user)
    const navigate = useNavigate()
    const { data } = TicTacToeStateSchema.safeParse(gameState)
    if (data === undefined) {
        return <div>Failed to parse game state</div>
    }
    const state: TicTacToeState = data!
    const handleClick = (i: number, j: number) => {
        sendMoveHandler({
            type: "game_move",
            body: { game_move: { coordinate: [i, j] } },
        })
    }

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
            return state.winner === user?.id ? "You win! 🎉" : "You lost!"
        return ""
    }

    return (
        <div className="flex flex-col items-center gap-6 p-8">
            <Dialog open={isOver}>
                <DialogContent showCloseButton={false}>
                    <DialogHeader>
                        <DialogTitle className="text-center text-2xl">
                            {getDialogTitle()}
                        </DialogTitle>
                    </DialogHeader>
                    <DialogDescription className="sr-only">
                        Game over
                    </DialogDescription>
                    <DialogFooter className="sm:justify-center">
                        <Button onClick={() => navigate("/")}>
                            Back to main menu
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            {/* Header */}
            <div className="flex flex-col items-center gap-2">
                <h2 className="text-2xl font-bold tracking-tight">
                    Tic Tac Toe
                </h2>
                <div className="flex items-center gap-2">
                    <p className="text-sm text-muted-foreground">You play as</p>
                    <TicTacToeCell value={state.your_symbol} />
                </div>
            </div>

            {/* Status banner */}
            <div
                className={clsx(
                    styles.status.base,
                    isOver && styles.status.over,
                    !isOver && state.your_turn && styles.status.yourTurn,
                    !isOver && !state.your_turn && styles.status.waiting
                )}
            >
                {getStatusText()}
            </div>

            {/* Board */}
            <div className="grid grid-cols-3 gap-2">
                {state.board.map((row, i) =>
                    row.map((value, j) => (
                        <button
                            key={`${i}_${j}`}
                            onClick={() => handleClick(i, j)}
                            disabled={
                                !state.your_turn || value !== null || isOver
                            }
                            className={clsx(
                                styles.cell.base,
                                value === null && state.your_turn && !isOver
                                    ? styles.cell.interactive
                                    : styles.cell.static
                            )}
                        >
                            <TicTacToeCell value={value} />
                        </button>
                    ))
                )}
            </div>
        </div>
    )
}
