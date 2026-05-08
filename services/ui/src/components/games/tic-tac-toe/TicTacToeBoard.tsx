import type { GameMoveMessage } from "@/types/game"
import { z } from "zod"

const MoveSchema = z.enum(["x", "o"])
const TicTacToeStateSchema = z.object({
    board: z.array(z.array(MoveSchema.nullable()).length(3)).length(3),
    your_turn: z.boolean(),
    your_symbol: MoveSchema,
    is_draw: z.boolean(),
    winner: z.int().nullable(),
})
type TicTacToeState = z.infer<typeof TicTacToeStateSchema>

interface Props {
    gameState: any
    sendMoveHandler: (message: GameMoveMessage) => void
}
export function TicTacToe({ gameState, sendMoveHandler }: Props) {
    const { data } = TicTacToeStateSchema.safeParse(gameState)
    if (data === undefined) {
        return <div>Failed to parse game state</div>
    }
    const state: TicTacToeState = data!
    const handleClick = (i: number, j: number) => {
        console.log("clicked:", i, j)
        sendMoveHandler({
            type: "game_move",
            body: { game_move: { coordinate: [i, j] } },
        })
    }

    return (
        <div>
            <div>Your turn? {state.your_turn ? "yes" : "no"}</div>
            <div>Your symbol: {state.your_symbol}</div>
            <div>Is draw?: {state.is_draw ? "yes" : "no"}</div>
            <div>Winner: {state.winner ? "no winner" : state.winner}</div>
            <div>Board: ...</div>
            <div>
                {state.board.map((row, i) => (
                    <div className="flex" key={i}>
                        {row.map((value, j) => (
                            <div
                                className="m-4 cursor-pointer border border-white p-4"
                                key={`j_${j}`}
                                onClick={() => handleClick(i, j)}
                            >
                                {value}
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    )
}
