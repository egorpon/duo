import { z } from "zod"

export const TicTacToeStateScheme = z.object()
export type TicTacToeState = z.infer<typeof TicTacToeStateScheme>
