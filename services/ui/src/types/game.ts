type GameType = "tic_tac_toe"

type GameResult = "tbd" | "draw" | "p1_won" | "p2_won"

type GameStatus = "in_queue" | "in_progress" | "abandoned" | "finished"

type Game = {
    id: number
    type: GameType
    result: GameResult
    status: GameStatus
    player1: number
    player2: number | null
    current_player: number
    turn_number: number
    created_at: string
    updated_at: string
}

interface GameCreate {
    type: GameType
}

export type { Game, GameType, GameResult, GameStatus, GameCreate }
