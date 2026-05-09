import { TooltipProvider } from "@/components/ui/tooltip"
import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { Toaster } from "@/components/ui/sonner"
import { ThemeProvider } from "@/shared/components/theme-provider"
import router from "@/router"
import "@/styles/index.css"
import { RouterProvider } from "react-router"

createRoot(document.getElementById("root")!).render(
    <StrictMode>
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
                    warning: "bg-yellow-50 border-yellow-200 text-yellow-700",
                    info: "bg-blue-50 border-blue-200 text-blue-700",
                },
            }}
        />
    </StrictMode>
)
