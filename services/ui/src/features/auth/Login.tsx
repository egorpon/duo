import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Spinner } from "@/components/ui/spinner"
import { AuthService } from "@/services/auth.service"
import useAuthStore from "@/stores/auth"
import { AtSign, Eye, EyeOff, Lock } from "lucide-react"
import { useState } from "react"
import { Link, useNavigate } from "react-router"

export default function Login() {
    const store = useAuthStore()
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (formData: FormData) => {
        setError(null)
        setLoading(true)
        const { result: token, error } = await AuthService.login(
            formData.get("email") as string,
            formData.get("password") as string
        )
        setLoading(false)
        if (error) {
            setError(error || "Invalid credentials")
            return
        }
        if (token) {
            store.setToken(token)
            navigate("/")
        }
    }

    return (
        <div className="flex h-screen w-screen">
            <div className="hidden flex-col items-center justify-center bg-primary px-16 text-primary-foreground lg:flex lg:w-1/2">
                <div className="max-w-sm">
                    <div className="mb-8 flex size-14 items-center justify-center rounded-2xl bg-primary-foreground/15 text-3xl font-bold">
                        D
                    </div>
                    <h1 className="mb-4 text-4xl font-bold tracking-tight">
                        Welcome back to Duo
                    </h1>
                    <p className="text-lg text-primary-foreground/70">
                        Sign in to continue your journey.
                    </p>
                </div>
            </div>

            <div className="flex w-full flex-col items-center justify-center px-8 lg:w-1/2">
                <div className="w-full max-w-sm">
                    <div className="mb-8">
                        <h2 className="text-2xl font-semibold tracking-tight">
                            Sign in
                        </h2>
                        <p className="mt-1 text-sm text-muted-foreground">
                            Enter your credentials to access your account
                        </p>
                    </div>

                    <form action={handleSubmit} className="space-y-4">
                        <div className="space-y-1.5">
                            <Label htmlFor="email">Email</Label>
                            <div className="relative">
                                <AtSign className="absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground" />
                                <Input
                                    id="email"
                                    name="email"
                                    type="email"
                                    placeholder="you@example.com"
                                    className="pl-9"
                                    required
                                    autoComplete="email"
                                />
                            </div>
                        </div>

                        <div className="space-y-1.5">
                            <Label htmlFor="password">Password</Label>
                            <div className="relative">
                                <Lock className="absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground" />
                                <Input
                                    id="password"
                                    name="password"
                                    type={showPassword ? "text" : "password"}
                                    placeholder="••••••••"
                                    className="pr-9 pl-9"
                                    required
                                    autoComplete="current-password"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword((v) => !v)}
                                    className="absolute top-1/2 right-2.5 -translate-y-1/2 text-muted-foreground transition-colors hover:text-foreground"
                                    tabIndex={-1}
                                >
                                    {showPassword ? (
                                        <EyeOff className="size-4" />
                                    ) : (
                                        <Eye className="size-4" />
                                    )}
                                </button>
                            </div>
                        </div>

                        {error && (
                            <p className="rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive">
                                {error}
                            </p>
                        )}

                        <Button
                            type="submit"
                            className="w-full"
                            size="lg"
                            disabled={loading}
                        >
                            {loading && <Spinner className="mr-2" />}
                            Sign in
                        </Button>
                    </form>

                    <p className="mt-6 text-center text-sm text-muted-foreground">
                        Don't have an account?{" "}
                        <Link
                            to="/auth/register"
                            className="font-medium text-primary hover:underline"
                        >
                            Sign up
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
