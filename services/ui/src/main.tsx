import { TooltipProvider } from "@/components/ui/tooltip"
import { StrictMode } from "react"
import { createRoot } from "react-dom/client"

import { ThemeProvider } from "@/components/theme-provider.tsx"
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
    </StrictMode>
)
