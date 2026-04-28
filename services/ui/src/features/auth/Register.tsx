import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Spinner } from "@/components/ui/spinner"
import { useRegister } from "@/hooks/auth/useRegister"
import useAuthStore from "@/stores/auth"
import { AtSign, Eye, EyeOff, Lock } from "lucide-react"
import { useState } from "react"
import { Link, useNavigate } from "react-router"

export default function Register() {
    const store = useAuthStore()
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const { error, loading, register } = useRegister()

    const handleSubmit = async (formData: FormData) => {
        const token = await register(
            formData.get("email") as string,
            formData.get("password") as string
        )
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
                        Start your journey
                    </h1>
                    <p className="text-lg text-primary-foreground/70">
                        Create an account and join Duo today.
                    </p>
                </div>
            </div>

            <div className="flex w-full flex-col items-center justify-center px-8 lg:w-1/2">
                <div className="w-full max-w-sm">
                    <div className="mb-8">
                        <h2 className="text-2xl font-semibold tracking-tight">
                            Create account
                        </h2>
                        <p className="mt-1 text-sm text-muted-foreground">
                            Fill in your details to get started
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
                                    autoComplete="new-password"
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
                            Create account
                        </Button>
                    </form>

                    <p className="mt-6 text-center text-sm text-muted-foreground">
                        Already have an account?{" "}
                        <Link
                            to="/auth/login"
                            className="font-medium text-primary hover:underline"
                        >
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}
