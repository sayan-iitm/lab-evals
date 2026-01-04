// Pinia store for authentication and user state
import { defineStore } from 'pinia'
import type { UserResponse, UserRole } from '../types/api'

interface AuthState {
  token: string | null
  role: UserRole | null
  user: UserResponse | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => {
    let token = null,
      role = null,
      user = null
    try {
      const raw = localStorage.getItem('auth')
      if (raw) {
        const parsed = JSON.parse(raw)
        token = parsed.token || null
        role = parsed.role || null
        user = parsed.user || null
      }
    } catch {}
    return { token, role, user }
  },
  actions: {
    setAuth(token: string, role: UserRole, user: UserResponse) {
      this.token = token
      this.role = role
      this.user = user
      localStorage.setItem('auth', JSON.stringify({ token, role, user }))
    },
    clearAuth() {
      this.token = null
      this.role = null
      this.user = null
      localStorage.removeItem('auth')
    },
  },
})
