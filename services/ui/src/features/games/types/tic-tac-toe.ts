import { z } from "zod"

export const MoveSchema = z.enum(["x", "o"])
export const TicTacToeStateSchema = z.object({
    board: z.array(z.array(MoveSchema.nullable()).length(3)).length(3),
    your_turn: z.boolean(),
    your_symbol: MoveSchema,
    is_draw: z.boolean(),
    winner: z.int().nullable(),
})

export type Move = z.infer<typeof MoveSchema>
export type CellValue = Move | null
export type TicTacToeState = z.infer<typeof TicTacToeStateSchema>
