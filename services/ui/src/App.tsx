import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState } from "react"
import { Input } from "./components/ui/input"
import useAuthStore from "./stores/auth"

const url = "http://localhost:8000/ws/games/1/"

export default function App() {
    const wsRef = useRef<WebSocket | null>(null)
    const [messages, setMessages] = useState<string[]>([])
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
                console.error("no token, aborting")
                return
            }
            const payload = { token: token.access_token }
            ws.send(JSON.stringify(payload))
        })

        ws.addEventListener("close", () => {
            console.log("ws closed")
        })
        ws.addEventListener("message", (event: MessageEvent) => {
            console.log(event)
            setMessages((prev) => [...prev, event.data])
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
                        {idx}: {row}
                    </div>
                ))}
            </div>
        </div>
    )
}
