import type { GameMoveMessage } from "@/features/games/types/game"
import { GameMessageScheme } from "@/features/games/types/game"
import type { JWT } from "@/features/auth/types/token"
import { useEffect, useRef, useState } from "react"
import { toast } from "sonner"

const WS_BASE_URL = import.meta.env.VITE_WS_URL

export function useGameWebSocket(id: string, token: JWT | null) {
    const wsRef = useRef<WebSocket | null>(null)
    const [gameState, setGameState] = useState<unknown>(null)

    useEffect(() => {
        const ws = new WebSocket(`${WS_BASE_URL}games/${id}/`)
        wsRef.current = ws

        ws.addEventListener("open", () => {
            console.debug("ws open")
            if (!token) return
            ws.send(
                JSON.stringify({
                    type: "token",
                    body: { token: token.access_token },
                })
            )
        })

        ws.addEventListener("close", () => {
            console.debug("ws closed")
        })

        ws.addEventListener("message", (event: MessageEvent) => {
            const { success, data } = GameMessageScheme.safeParse(
                JSON.parse(event.data)
            )
            if (!success) {
                console.debug("Failed to parse incoming message", event.data)
                return
            }
            if (data!.type === "game_state") {
                setGameState(data.body.game_state)
            }
            if (data!.type === "connected") {
                toast.info("Opponent connected")
            }
            if (data!.type === "disconnected") {
                toast.info("Opponent disconnected")
            }
            console.debug("message received:", data)
        })

        return () => ws.close()
    }, [id, token])

    const sendMessage = (message: GameMoveMessage) => {
        wsRef.current?.send(JSON.stringify(message))
    }

    return { gameState, sendMessage }
}
