import { UserService } from "@/features/auth/services/user.service"
import type { JWT } from "@/features/auth/types/token"
import type { User } from "@/features/auth/types/user"
import { create } from "zustand"
import { persist } from "zustand/middleware"

interface AuthStore {
    token: JWT | null
    user: User | null
    loading: boolean
    setToken: (token: JWT) => void
    isAuthenticated: () => boolean
    loadUser: () => Promise<void>
    logout: () => void
}

const useAuthStore = create<AuthStore>()(
    persist(
        (set, get) => ({
            token: null,
            user: null,
            loading: false,
            setToken: (token: JWT) => set({ token }),
            isAuthenticated: () => get().user !== null,
            loadUser: async () => {
                set({ loading: true })
                const { result: user } = await UserService.me()
                set({ loading: false, user })
            },
            logout: () => {
                set({ user: null, token: null })
            },
        }),
        { name: "authstore", partialize: (state) => ({ token: state.token }) }
    )
)

export default useAuthStore
