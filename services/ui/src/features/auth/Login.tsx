import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AuthService } from "@/services/auth.service"
import useAuthStore from "@/stores/auth"
import { useState } from "react"
import { redirect } from "react-router"

export default function Login() {
    const store = useAuthStore()
    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const handleSubmit = async () => {
        const { result: token, error } = await AuthService.login(
            email,
            password
        )
        if (error) {
            console.error(error)
        }
        if (token) {
            store.setToken(token)
        }
        redirect("/")
    }
    return (
        <div className="flex h-screen w-screen items-center justify-around">
            <form className="w-1/5" action={handleSubmit}>
                <Label>Email</Label>
                <Input
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    type="email"
                />
                <Label>Password</Label>
                <Input
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type="password"
                />
                <Button type="submit">Login</Button>
            </form>
        </div>
    )
}

