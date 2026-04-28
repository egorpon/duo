import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Spinner } from "@/components/ui/spinner"
import { useRegister } from "@/hooks/auth/useRegister"
import useAuthStore from "@/stores/auth"
import { zodResolver } from "@hookform/resolvers/zod"
import { AtSign, Eye, EyeOff, Lock } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { Link, useNavigate } from "react-router"
import { z } from "zod"

const RegisterSchema = z.object({
    email: z.email("Invalid email"),
    password: z.string().min(8, "Password should be longer than 8 characters"),
})
type RegisterInputs = z.infer<typeof RegisterSchema>

export default function Register() {
    const setToken = useAuthStore((state) => state.setToken)
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const { error, loading, register: registerUser } = useRegister()

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<RegisterInputs>({ resolver: zodResolver(RegisterSchema) })

    const onSubmit = async (data: RegisterInputs) => {
        const token = await registerUser(data.email, data.password)
        if (token) {
            setToken(token)
            navigate("/")
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
                                    autoComplete="new-password"
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
                            Create account
                        </Button>
                    </form>

                    <p className="mt-8 text-center text-sm text-muted-foreground">
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
