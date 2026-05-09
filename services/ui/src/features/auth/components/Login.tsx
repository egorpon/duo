import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Spinner } from "@/components/ui/spinner"
import { useLogin } from "@/features/auth/hooks/useLogin"
import useAuthStore from "@/features/auth/stores/auth"
import { zodResolver } from "@hookform/resolvers/zod"
import { AtSign, Eye, EyeOff, Lock } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { Link, useNavigate } from "react-router"
import { toast } from "sonner"
import { z } from "zod"

const LoginSchema = z.object({
    email: z.email("Invalid email"),
    password: z.string().min(8, "Password should be longer than 8 characters"),
})

type LoginInputs = z.infer<typeof LoginSchema>

export default function Login() {
    const setToken = useAuthStore((state) => state.setToken)
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const { error, loading, login } = useLogin()

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginInputs>({
        resolver: zodResolver(LoginSchema),
    })

    const onSubmit = async (data: LoginInputs) => {
        const token = await login(data.email, data.password)
        if (token) {
            setToken(token)
            toast.success("Logged in")
            navigate("/")
            return
        }
    }

    return (
        <div className="flex h-screen w-screen">
            <div className="hidden flex-col items-center justify-center bg-primary px-16 text-primary-foreground lg:flex lg:w-1/2">
                <div className="max-w-sm">
                    <div className="mb-8 flex size-16 items-center justify-center rounded-2xl bg-primary-foreground/15 text-3xl font-bold">
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

                    <form
                        onSubmit={handleSubmit(onSubmit)}
                        className="space-y-4"
                    >
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <div className="relative">
                                <AtSign className="absolute top-1/2 left-2 size-4 -translate-y-1/2 text-muted-foreground" />
                                <Input
                                    {...register("email")}
                                    placeholder="you@example.com"
                                    className="pl-8"
                                    autoComplete="email"
                                />
                            </div>
                            {errors.email && (
                                <p className="text-xs text-destructive">
                                    {errors.email.message}
                                </p>
                            )}
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <div className="relative">
                                <Lock className="absolute top-1/2 left-2 size-4 -translate-y-1/2 text-muted-foreground" />
                                <Input
                                    {...register("password")}
                                    type={showPassword ? "text" : "password"}
                                    placeholder="••••••••"
                                    className="pr-8 pl-8"
                                    autoComplete="current-password"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword((v) => !v)}
                                    className="absolute top-1/2 right-2 -translate-y-1/2 text-muted-foreground transition-colors hover:text-foreground"
                                    tabIndex={-1}
                                >
                                    {showPassword ? (
                                        <EyeOff className="size-4" />
                                    ) : (
                                        <Eye className="size-4" />
                                    )}
                                </button>
                            </div>
                            {errors.password && (
                                <p className="text-xs text-destructive">
                                    {errors.password.message}
                                </p>
                            )}
                        </div>

                        {error && (
                            <p className="rounded-md bg-destructive/10 px-4 py-2 text-sm text-destructive">
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

                    <p className="mt-8 text-center text-sm text-muted-foreground">
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
