import { Button } from "@/components/ui/button"
import useAuthStore from "@/features/auth/stores/auth"

export default function Settings() {
    const logout = useAuthStore((state) => state.logout)
    return (
        <div>
            <h1 className="font-medium">Project ready!</h1>
            <p>You may now add components and start building.</p>
            <p>We&apos;ve already added the button component for you.</p>
            <Button onClick={logout} className="mt-2">
                Logout
            </Button>
        </div>
    )
}
