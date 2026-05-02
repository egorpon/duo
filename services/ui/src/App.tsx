import { Button } from "@/components/ui/button"
import { useEffect } from "react"

const url = 'http://localhost:8000/ws/games/1/'

export default function App() {
    let websocket: WebSocket;
    useEffect(() => {
        websocket = new WebSocket(url)

        websocket.addEventListener('open', () => {
            console.log('ws open')
        })

        websocket.addEventListener('close', () => {
            console.log('ws closed')
        })
        websocket.addEventListener('message', (event: Event) => {
            console.log('received:', event)
        })
        return () => {
            websocket.close()
        }
    }, [])

    const handleClick = () => {
        websocket.send('Hello')
    }
    return (
        <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
            <Button onClick={handleClick}>Click</Button>
        </div>
    )
}
