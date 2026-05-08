import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState } from "react"
import { Input } from "./components/ui/input"
import useAuthStore from "./stores/auth"
import { type GameMessage, GameMessageScheme } from "./types/game"
import type { TokenMessage } from "@/types/game"

const url = "http://localhost:8000/ws/games/1/"

export default function App() {

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
            setMessages((prev) => [...prev, data])
        })

    }
    const wsRef = useRef<WebSocket | null>(null)
    const [messages, setMessages] = useState<GameMessage[]>([])
    const [message, setMessage] = useState<string>("")
    const token = useAuthStore((state) => state.token)
    useEffect(() => {
        const ws = new WebSocket(url)
        wsRef.current = ws
        if (wsRef === null) {
            return
        }
        registerEventListeners(ws)

        return () => ws.close()
    }, [token])

    const handleMessage = () => {
        if (!wsRef.current) {
            console.log("no current ws", wsRef.current)
            return
        }
        wsRef.current.send(JSON.stringify({ message }))
        setMessage("")
    }
    const handleDisconnect = () => {
        if (!wsRef.current) {
            console.log("no current ws", wsRef.current)
            return
        }
        wsRef.current.close()
    }
    return (
        <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
            <Button onClick={handleMessage}>Message</Button>
            <Button onClick={handleDisconnect}>Disconnect</Button>
            <Input
                name="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
            />
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
