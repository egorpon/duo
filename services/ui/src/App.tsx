import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState } from "react"
import { Input } from "./components/ui/input"
import useAuthStore from "./stores/auth"
import { z } from "zod"

const url = "http://localhost:8000/ws/games/1/"

const GameMessageScheme = z.discriminatedUnion("type", [
    z.object({
        type: z.literal("authenticated"),
        body: z.object({ success: z.boolean(), message: z.string() }),
    }),
    z.object({
        type: z.literal("game_move"),
        body: z.object({ game_move: z.record(z.any(), z.any()) }),
    }),
    z.object({
        type: z.literal("game_state"),
        body: z.object({ game_state: z.record(z.any(), z.any()) }),
    }),
    z.object({
        type: z.literal("game_created"),
        body: z.object({ message: z.string() }),
    }),
    z.object({
        type: z.literal("connected"),
        body: z.object({ message: z.string() }),
    }),
    z.object({
        type: z.literal("disconnected"),
        body: z.object({ message: z.string() }),
    }),
    z.object({
        type: z.literal("invalid_move"),
        body: z.object({ message: z.string() }),
    }),
])
type GameMessage = z.infer<typeof GameMessageScheme>

export default function App() {
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

        ws.addEventListener("open", () => {
            console.log("ws open")
            if (!token) {
                return
            }
            const payload = { token: token.access_token }
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
                return
            }
            setMessages((prev) => [...prev, data])
        })
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
