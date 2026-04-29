import { Button } from "@/components/ui/button"
import useAuthStore from "./stores/auth"

export default function App() {
    const logout = useAuthStore((state) => state.logout)
    return (
        <div className="flex max-w-md min-w-0 flex-col gap-4 text-sm leading-loose">
            <div>
                <h1 className="font-medium">Project ready!</h1>
                <p>You may now add components and start building.</p>
                <p>We&apos;ve already added the button component for you.</p>
                <Button onClick={logout} className="mt-2">
                    Logout
                </Button>
            </div>
            <div className="flex">
                <Button>Connect to game</Button>
            </div>
        </div>
    )
}
