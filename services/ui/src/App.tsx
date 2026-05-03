import { Button } from "@/components/ui/button"
import { useEffect, useRef } from "react"

const url = "http://localhost:8000/ws/games/1/"

export default function App() {
    const wsRef = useRef<WebSocket | null>(null)
    useEffect(() => {
        const ws = new WebSocket(url)
        wsRef.current = new WebSocket(url)
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
            console.log("received:", event)
        })
        return () => {
            ws.close()
        }
    }, [])

    const handleClick = () => {
        if (!wsRef.current) {
            return
        }
        wsRef.current.send("Hello")
    }
    return (
        <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
            <Button onClick={handleClick}>Click</Button>
        </div>
    )
}
