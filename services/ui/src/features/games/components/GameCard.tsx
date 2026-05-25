const GRID_MARKS = [
    { x: true },
    { o: true },
    {},
    {},
    { x: true },
    { o: true },
    { o: true },
    {},
    { x: true },
] as const

function MiniGrid() {
    return (
        <div className="relative mx-auto grid aspect-square w-48 grid-cols-3 grid-rows-3 gap-[3px] sm:w-36">
            {GRID_MARKS.map((cell, i) => (
                <div
                    key={i}
                    className="flex items-center justify-center rounded-[3px] bg-white/5"
                >
                    {"x" in cell && (
                        <svg
                            viewBox="0 0 16 16"
                            className="h-9 w-9 sm:h-7 sm:w-7"
                        >
                            <line
                                x1="3"
                                y1="3"
                                x2="13"
                                y2="13"
                                stroke="oklch(0.696 0.17 162.48)"
                                strokeWidth="2.5"
                                strokeLinecap="round"
                            />
                            <line
                                x1="13"
                                y1="3"
                                x2="3"
                                y2="13"
                                stroke="oklch(0.696 0.17 162.48)"
                                strokeWidth="2.5"
                                strokeLinecap="round"
                            />
                        </svg>
                    )}
                    {"o" in cell && (
                        <svg
                            viewBox="0 0 16 16"
                            className="h-9 w-9 sm:h-7 sm:w-7"
                        >
                            <circle
                                cx="8"
                                cy="8"
                                r="4.5"
                                fill="none"
                                stroke="oklch(0.75 0.05 220)"
                                strokeWidth="2.5"
                            />
                        </svg>
                    )}
                </div>
            ))}
            <div className="pointer-events-none absolute inset-0 rounded-sm ring-1 ring-white/10" />
        </div>
    )
}

interface GameCardProps {
    title: string
    loading?: boolean
    onClick: () => void
}

export function GameCard({ title, loading, onClick }: GameCardProps) {
    return (
        <button
            disabled={loading}
            onClick={onClick}
            className="group relative flex w-72 cursor-pointer flex-col gap-5 overflow-hidden rounded-xl border border-white/10 bg-card p-6 text-left transition-all duration-200 hover:border-primary/50 hover:shadow-[0_0_24px_oklch(0.696_0.17_162.48/0.15)] active:scale-[0.98] disabled:pointer-events-none disabled:opacity-50 sm:w-64"
        >
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-transparent opacity-0 transition-opacity duration-200 group-hover:opacity-100" />
            <MiniGrid />
            <div className="relative flex flex-col gap-1 text-center">
                <span className="text-base font-semibold tracking-tight text-foreground sm:text-lg">
                    {title}
                </span>
            </div>
            <div className="relative mt-auto w-full rounded-lg bg-primary px-3 py-2 text-center text-sm font-medium text-primary-foreground transition-colors duration-150 group-hover:brightness-110">
                {loading ? "Creating…" : "Play"}
            </div>
        </button>
    )
}
