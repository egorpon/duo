import { Button } from "@/components/ui/button"
import useAuthStore from "@/features/auth/stores/auth"

export default function Settings() {
    const logout = useAuthStore((state) => state.logout)
    return (
        <div>
            <h1 className="font-medium">Settings</h1>
            <p>More on that later</p>
            <Button onClick={logout} className="mt-2">
                Logout
            </Button>
        </div>
    )
}
