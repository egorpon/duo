import { Circle, X } from "lucide-react"

interface Props {
    value: "x" | "o" | null
}

export function TicTacToeCell({ value }: Props) {
    if (value === "x") return <X className="size-10 stroke-[3] text-rose-500" />
    if (value === "o")
        return <Circle className="size-10 stroke-[3] text-primary" />
    return null
}
