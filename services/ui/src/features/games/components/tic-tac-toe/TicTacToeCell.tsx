import { Circle, X } from "lucide-react"

interface Props {
    value: "x" | "o" | null
    className?: string
}

export function TicTacToeCell({
    value,
    className = "size-10 stroke-[3]",
}: Props) {
    if (value === "x") return <X className={`${className} text-rose-500`} />
    if (value === "o") return <Circle className={`${className} text-primary`} />
    return null
}
