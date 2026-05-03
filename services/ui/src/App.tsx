import { Button } from "@/components/ui/button"
import { useEffect, useRef, useState } from "react"
import { Input } from "./components/ui/input"

const url = "http://localhost:8000/ws/games/1/"

export default function App() {
    const wsRef = useRef<WebSocket | null>(null)
    const [messages, setMessages] = useState<string[]>([])
    const [message, setMessage] = useState<string>("")
    useEffect(() => {
        const ws = new WebSocket(url)
        wsRef.current = ws
        if (wsRef === null) {
            return
        }

        ws.addEventListener("open", () => {
            console.log("ws open")
        })

        ws.addEventListener("close", () => {
            console.log("ws closed")
        })
        ws.addEventListener("message", (event: MessageEvent) => {
            setMessages((prev) => [...prev, event.data])
        })
        return () => ws.close()
    }, [])

    const handleClick = () => {
        if (!wsRef.current) {
            console.log("no current ws", wsRef.current)
            return
        }
        wsRef.current.send(message)
        setMessage('')
    }
    return (
        <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
            <Button onClick={handleClick}>Click</Button>
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
