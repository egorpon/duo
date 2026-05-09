import Error from "@/shared/components/Error"
import { PageLoading } from "@/shared/components/layout/PageLoading"
import VerticalLayout from "@/shared/components/layout/VerticalLayout"
import Login from "@/features/auth/components/Login"
import Register from "@/features/auth/components/Register"
import { MainMenu } from "@/features/games/components/MainMenu"
import { PlayGamePage } from "@/features/games/components/PlayGamePage"
import Settings from "@/features/profile/components/Settings"
import useAuthStore from "@/features/auth/stores/auth"
import { createBrowserRouter, redirect } from "react-router"

const router = createBrowserRouter([
    {
        path: "/",
        errorElement: <Error />,
        hydrateFallbackElement: <PageLoading />,
        Component: VerticalLayout,
        loader: async () => {
            if (useAuthStore.getState().isAuthenticated()) {
                return null
            }

            if (useAuthStore.getState().token === null) {
                return redirect("/auth/login/")
            }

            await useAuthStore.getState().loadUser()

            if (useAuthStore.getState().isAuthenticated()) {
                return null
            }
            useAuthStore.getState().logout()
            return redirect("/auth/login/")
        },
        children: [
            {
                index: true,
                Component: MainMenu,
            },
            {
                path: "game/:id",
                Component: PlayGamePage,
            },
            {
                path: "settings",
                Component: Settings,
            },
        ],
    },
    {
        path: "/auth",
        errorElement: <Error />,
        hydrateFallbackElement: <PageLoading />,
        loader: async () => {
            if (useAuthStore.getState().isAuthenticated()) {
                return redirect("/")
            }

            if (useAuthStore.getState().token === null) {
                return null
            }

            await useAuthStore.getState().loadUser()

            if (useAuthStore.getState().isAuthenticated()) {
                return redirect("/")
            }
            useAuthStore.getState().logout()
            return null
        },
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
