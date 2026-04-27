import { Spinner } from "../ui/spinner"

export function PageLoading() {
    return (
        <div style={{ display: "grid", placeItems: "center", height: "100vh" }}>
            <Spinner />
        </div>
    )
}
