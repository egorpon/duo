import { api } from "@/lib/api"
import type { User } from "@/types/user"
import { create } from "zustand"
import { persist } from "zustand/middleware"

interface AuthStore {
    token: string | null
    user: User | null
    loading: boolean
    setToken: (token: string) => void
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
            setToken: (token: string) => set({ token }),
            isAuthenticated: () => get().user === null,
            loadUser: async () => {
                set({ loading: true })
                const user = await api<User>("/users/me/")
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
