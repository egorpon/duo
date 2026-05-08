import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState } from "react"
import useAuthStore from "./stores/auth"
import { type GameMessage, GameMessageScheme } from "./types/game"
import type { TokenMessage, GameMoveMessage } from "@/types/game"
import { TicTacToe } from "./components/games/tic-tac-toe/TicTacToeBoard"

const url = "http://localhost:8000/ws/games/1/"

export default function App() {
    const wsRef = useRef<WebSocket | null>(null)
    const [messages, setMessages] = useState<GameMessage[]>([])
    const token = useAuthStore((state) => state.token)
    const [gameState, setGameState] = useState<any | null>(null)
    useEffect(() => {
        const registerEventListeners = (ws: WebSocket): void => {
            ws.addEventListener("open", () => {
                console.log("ws open")
                if (!token) {
                    return
                }
                const payload: TokenMessage = {
                    type: "token",
                    body: { token: token.access_token },
                }
                ws.send(JSON.stringify(payload))
            })

            ws.addEventListener("close", () => {
                console.log("ws closed")
            })
            ws.addEventListener("message", (event: MessageEvent) => {
                const { success, data } = GameMessageScheme.safeParse(
                    JSON.parse(JSON.parse(event.data))
                )
                if (!success) {
                    console.log("Failed to parse incoming message")
                    console.log("message was:", event.data)
                    return
                }
                if (data!.type === "game_state") {
                    setGameState(data.body.game_state)
                }
                setMessages((prev) => [...prev, data])
            })
        }
        const ws = new WebSocket(url)
        wsRef.current = ws
        if (wsRef === null) {
            return
        }
        registerEventListeners(ws)

        return () => ws.close()
    }, [token])

    const handleDisconnect = () => {
        if (!wsRef.current) {
            console.log("no current ws", wsRef.current)
            return
        }
        wsRef.current.close()
    }
    const handleSendMove = (message: GameMoveMessage) => {
        if (!wsRef.current) {
            return
        }
        wsRef.current.send(JSON.stringify(message))
    }
    return (
        <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
            <Button onClick={handleDisconnect}>Disconnect</Button>
            {gameState && (
                <TicTacToe
                    sendMoveHandler={handleSendMove}
                    gameState={gameState}
                />
            )}
            <div>
                {messages.map((row, idx) => (
                    <div key={idx}>
                        {idx}: {JSON.stringify(row)}
                    </div>
                ))}
            </div>
        </div>
    )
}
