import { useParams } from "react-router"

export function PlayGamePage() {
    const { id } = useParams()
    return <div>Play game {id}</div>
}
