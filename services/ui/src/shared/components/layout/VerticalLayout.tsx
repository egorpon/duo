import { Outlet } from "react-router"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "./AppSidebar"

export default function VerticalLayout() {
    return (
        <SidebarProvider defaultOpen={true}>
            <AppSidebar />
            <main className="flex p-2">
                <Outlet />
            </main>
        </SidebarProvider>
    )
}
