import { describe, expect, it } from "vitest"
import { TicTacToeStateSchema } from "@/features/games/types/tic-tac-toe"

const validState = {
    board: [
        ["x", null, "o"],
        [null, "x", null],
        ["o", null, null],
    ],
    your_turn: true,
    your_symbol: "x",
    is_draw: false,
    winner: null,
}

describe("TicTacToeStateSchema", () => {
    it("parses valid state", () => {
        const { success, data } = TicTacToeStateSchema.safeParse(validState)
        expect(success).toBe(true)
        expect(data?.your_symbol).toBe("x")
    })

    it("fails on invalid symbol", () => {
        const { success } = TicTacToeStateSchema.safeParse({
            ...validState,
            your_symbol: "z",
        })
        expect(success).toBe(false)
    })

    it("fails on wrong board size", () => {
        const { success } = TicTacToeStateSchema.safeParse({
            ...validState,
            board: [
                [null, null],
                [null, null],
            ],
        })
        expect(success).toBe(false)
    })

    it("fails on missing field", () => {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        const { board, ...withoutBoard } = validState
        const { success } = TicTacToeStateSchema.safeParse(withoutBoard)
        expect(success).toBe(false)
    })

    it("parses winner as number", () => {
        const { success, data } = TicTacToeStateSchema.safeParse({
            ...validState,
            winner: 42,
        })
        expect(success).toBe(true)
        expect(data?.winner).toBe(42)
    })
})
