import type { TicTacToeState, Move } from "@/features/games/types/tic-tac-toe"

export function getStatusText(
    state: TicTacToeState,
    userId: number | undefined
): string {
    if (state.is_draw) return "It's a draw!"
    if (state.winner !== null)
        return state.winner === userId ? "You win!" : "Opponent wins!"
    return state.your_turn ? "Your turn" : "Opponent's turn"
}

export function getDialogTitle(
    state: TicTacToeState,
    userId: number | undefined
): string {
    if (state.is_draw) return "It's a draw!"
    if (state.winner !== null)
        return state.winner === userId ? "You win!" : "You lost!"
    return ""
}

export function opponentSymbol(yourSymbol: Move): Move {
    return yourSymbol === "x" ? "o" : "x"
}
