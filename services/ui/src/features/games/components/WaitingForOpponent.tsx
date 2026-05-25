import { Check, Copy, Link } from "lucide-react"
import { useState } from "react"
import { toast } from "sonner"

export function WaitingForOpponent() {
    const [copied, setCopied] = useState(false)
    const url = window.location.href

    const handleCopy = async () => {
        await navigator.clipboard.writeText(url)
        setCopied(true)
        toast.success("Link copied!")
        setTimeout(() => setCopied(false), 2000)
    }

    return (
        <div className="flex w-full items-start justify-center p-4 sm:p-10">
            <div className="flex w-full max-w-md flex-col gap-5 rounded-xl border border-white/10 bg-card p-8 text-center">
                <div className="flex flex-col items-center gap-2">
                    <Link className="size-6 text-primary" />
                    <p className="text-lg font-semibold text-foreground">
                        Invite your opponent
                    </p>
                </div>
                <button
                    onClick={handleCopy}
                    className="group flex items-center gap-3 rounded-lg border border-white/10 bg-background px-4 py-3 transition-colors hover:border-primary/50 hover:bg-primary/5"
                    aria-label="Copy link"
                >
                    <span className="flex-1 truncate text-sm text-muted-foreground group-hover:text-foreground">
                        {url}
                    </span>
                    {copied ? (
                        <Check className="size-4 shrink-0 text-primary" />
                    ) : (
                        <Copy className="size-4 shrink-0 text-muted-foreground" />
                    )}
                </button>
                <p className="text-sm text-muted-foreground">
                    Waiting for opponent to join…
                </p>
            </div>
        </div>
    )
}
