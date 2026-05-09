import { TicTacToe } from "@/components/games/tic-tac-toe/TicTacToe"
import { useFetchGame } from "@/hooks/game/useFetchGame"
import useAuthStore from "@/stores/auth"
import type {
    Game,
    GameMessage,
    GameMoveMessage,
    TokenMessage,
} from "@/types/game"
import { GameMessageScheme } from "@/types/game"
import { useEffect, useRef, useState } from "react"
import { useNavigate, useParams } from "react-router"

const debug: boolean = true

export function PlayGamePage() {
    const navigate = useNavigate()
    const { id } = useParams()
    const [game, setGame] = useState<Game | null>(null)
    const { loading, fetch } = useFetchGame()
    const [messages, setMessages] = useState<GameMessage[]>([])

    const wsRef = useRef<WebSocket | null>(null)
    const token = useAuthStore((state) => state.token)
    const [gameState, setGameState] = useState<any | null>(null)

    const registerEventListeners = (ws: WebSocket): void => {
        ws.addEventListener("open", () => {
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
            console.debug("ws closed")
        })
        ws.addEventListener("message", (event: MessageEvent) => {
            const { success, data } = GameMessageScheme.safeParse(
                JSON.parse(JSON.parse(event.data))
            )
            if (!success) {
                console.debug("Failed to parse incoming message")
                console.debug("message was:", event.data)
                return
            }
            if (data!.type === "game_state") {
                setGameState(data.body.game_state)
            }

            setMessages((prev) => [...prev, data])
        })
    }
    useEffect(() => {
        const startup = async () => {
            const game = await fetch(Number(id))
            if (!game) {
                navigate("/")
                return
            }
            setGame(game)
        }
        startup()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [id])

    useEffect(() => {
        const ws = new WebSocket(`http://localhost:8000/ws/games/${id}/`)
        wsRef.current = ws
        if (wsRef === null) {
            return
        }
        registerEventListeners(ws)

        return () => ws.close()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [token, id])

    const sendMessage = (message: GameMoveMessage) => {
        if (!wsRef.current) {
            return
        }
        wsRef.current.send(JSON.stringify(message))
    }
    if (loading) {
        return <div>Loading</div>
    }
    if (!game) return
    if (!gameState) {
        return (
            <div>
                <div>Waiting for opponent</div>

                {debug && (
                    <div>
                        {messages.map((row, idx) => (
                            <div key={idx}>
                                {idx}: {JSON.stringify(row)}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        )
    }
    return (
        <div>
            <div>
                <div>ID: {game.id}</div>
                <div>Game: {game.type}</div>
                {game.type === "tic_tac_toe" && (
                    <TicTacToe
                        gameState={gameState}
                        sendMoveHandler={sendMessage}
                    />
                )}
            </div>
            {debug && (
                <div>
                    {messages.map((row, idx) => (
                        <div key={idx}>
                            {idx}: {JSON.stringify(row)}
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
