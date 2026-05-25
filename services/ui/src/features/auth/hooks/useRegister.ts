import { AuthService } from "@/features/auth/services/auth.service"
import { useApiCall } from "@/shared/hooks/useApiCall"

export function useRegister() {
    const { loading, error, call: register } = useApiCall(AuthService.register)
    return { loading, error, register }
}
