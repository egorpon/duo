import { createBrowserRouter, redirect } from "react-router"
import App from "@/App"
import Error from "@/components/Error"
import Register from "@/features/auth/Register"
import Login from "@/features/auth/Login"
import VerticalLayout from "@/components/layout/VerticalLayout"

const router = createBrowserRouter([
    {
        path: "/",
        errorElement: <Error />,
        Component: VerticalLayout,
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
                index: true,
                loader: () => redirect("/auth/login"),
            },
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
