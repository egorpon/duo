import { useRouteError, isRouteErrorResponse, Link } from "react-router"
import { Button } from "./ui/button"

export function Error() {
    const error = useRouteError()
    if (!isRouteErrorResponse(error)) {
        return <div>Some error happend</div>
    }
    return (
        <div>
            <div>I know what happend: {error.statusText}</div>
            <Button>
                <Link to="/">Back to home</Link>
            </Button>
        </div>
    )
}

export default Error
