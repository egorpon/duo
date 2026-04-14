import { useRouteError, isRouteErrorResponse } from "react-router"

export function Error() {
    const error = useRouteError()
    if (!isRouteErrorResponse(error)) {
        return <div>Some error happend</div>
    }
    return <div>I know what happend: {error.statusText}</div>
}

export default Error
