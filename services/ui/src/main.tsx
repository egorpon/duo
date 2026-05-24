import { TooltipProvider } from "@/components/ui/tooltip"
import { StrictMode, useEffect } from "react"
import { createRoot } from "react-dom/client"
import { Toaster } from "@/components/ui/sonner"
import { ThemeProvider } from "@/shared/components/theme-provider"
import router from "@/router"
import "@/styles/index.css"
import {
    RouterProvider,
    useLocation,
    useNavigationType,
    createRoutesFromChildren,
    matchRoutes,
} from "react-router"
import * as Sentry from "@sentry/react"

if (import.meta.env.VITE_SENTRY_DSN) {
    Sentry.init({
        dsn: import.meta.env.VITE_SENTRY_DSN,
        sendDefaultPii: true,
        tracesSampleRate: 0,
        release: import.meta.env.VITE_SENTRY_RELEASE,
        environment: import.meta.env.VITE_SENTRY_ENVIRONMENT,
        integrations: [
            Sentry.reactRouterV7BrowserTracingIntegration({
                useEffect,
                useLocation,
                useNavigationType,
                createRoutesFromChildren,
                matchRoutes,
            }),
        ],
    })
}

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <Sentry.ErrorBoundary fallback={<p>Something went wrong</p>}>
            <ThemeProvider>
                <TooltipProvider>
                    <RouterProvider router={router}></RouterProvider>
                </TooltipProvider>
            </ThemeProvider>
            <Toaster
                richColors
                toastOptions={{
                    classNames: {
                        success: "bg-green-50 border-green-200 text-green-700",
                        error: "bg-red-50 border-red-200 text-red-700",
                        warning:
                            "bg-yellow-50 border-yellow-200 text-yellow-700",
                        info: "bg-blue-50 border-blue-200 text-blue-700",
                    },
                }}
            />
        </Sentry.ErrorBoundary>
    </StrictMode>
)
