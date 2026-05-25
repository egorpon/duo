import type { CellValue } from "@/features/games/types/tic-tac-toe"
import clsx from "clsx"
import { TicTacToeCell } from "./TicTacToeCell"

interface Props {
    board: CellValue[][]
    yourTurn: boolean
    isOver: boolean
    onCellClick: (i: number, j: number) => void
}

const styles = {
    cell: {
        base: "flex h-24 w-24 items-center justify-center rounded-xl border bg-card transition-all sm:h-32 sm:w-32",
        interactive:
            "cursor-pointer hover:border-primary/60 hover:bg-primary/10 active:scale-95",
        static: "cursor-default",
    },
}

export function GameBoard({ board, yourTurn, isOver, onCellClick }: Props) {
    return (
        <div className="grid grid-cols-3 gap-2">
            {board.map((row, i) =>
                row.map((value, j) => (
                    <button
                        key={`${i}_${j}`}
                        onClick={() => onCellClick(i, j)}
                        disabled={!yourTurn || value !== null || isOver}
                        className={clsx(
                            styles.cell.base,
                            value === null && yourTurn && !isOver
                                ? styles.cell.interactive
                                : styles.cell.static
                        )}
                    >
                        <TicTacToeCell value={value} />
                    </button>
                ))
            )}
        </div>
    )
}
