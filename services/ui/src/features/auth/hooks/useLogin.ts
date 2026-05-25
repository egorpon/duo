import { AuthService } from "@/features/auth/services/auth.service"
import { useApiCall } from "@/shared/hooks/useApiCall"

export function useLogin() {
    const { loading, error, call: login } = useApiCall(AuthService.login)
    return { loading, error, login }
}
