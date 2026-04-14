import { createBrowserRouter } from "react-router"
import App from "@/App"
import Error from "@/Error"
import Register from "@/features/auth/Register"
import Login from "@/features/auth/Login"

const router = createBrowserRouter([
    {
        path: "/",
        errorElement: <Error />,
        children: [
            {
                index: true,
                Component: App,
            },
        ],
    },
    {
        path: "/auth",
        errorElement: <Error />,
        children: [
            {
                path: "register",
                Component: Register,
            },
            {
                path: "login",
                Component: Login,
            },
        ],
    },
])

export default router
