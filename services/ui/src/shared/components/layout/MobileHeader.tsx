import { SidebarTrigger } from "@/components/ui/sidebar"

export function MobileHeader() {
    return (
        <header className="flex h-12 items-center border-b border-border px-4 sm:hidden">
            <SidebarTrigger />
        </header>
    )
}
