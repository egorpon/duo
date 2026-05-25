import { Outlet } from "react-router"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "./AppSidebar"
import { MobileHeader } from "./MobileHeader"

export default function VerticalLayout() {
    return (
        <SidebarProvider defaultOpen={true}>
            <AppSidebar />
            <main className="flex flex-1 flex-col">
                <MobileHeader />
                <div className="flex w-full flex-1 p-2">
                    <Outlet />
                </div>
            </main>
        </SidebarProvider>
    )
}
