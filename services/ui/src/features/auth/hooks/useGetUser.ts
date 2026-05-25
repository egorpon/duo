import { UserService } from "@/features/auth/services/user.service"
import { useApiCall } from "@/shared/hooks/useApiCall"

export function useGetUser() {
    const {
        loading,
        error,
        data: user,
        call: getUser,
    } = useApiCall(UserService.get)
    return { loading, error, user, getUser }
}
