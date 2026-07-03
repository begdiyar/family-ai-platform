import { Navigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '@/store/auth.store'
import { AuthService } from '@/services/auth.service'

const USER_MODE_KEY = 'admin_user_mode'

/** True when admin explicitly chose to browse the user-facing app. */
export const isUserModeActive = (): boolean =>
  typeof window !== 'undefined' && sessionStorage.getItem(USER_MODE_KEY) === 'true'

/** Set or clear the "user mode" override. */
export const setUserMode = (active: boolean): void => {
  if (typeof window === 'undefined') return
  if (active) sessionStorage.setItem(USER_MODE_KEY, 'true')
  else sessionStorage.removeItem(USER_MODE_KEY)
}

const isAdmin = (u: { is_staff?: boolean; is_superuser?: boolean } | null | undefined) =>
  Boolean(u && (u.is_staff || u.is_superuser))

/**
 * Wraps /app/** routes.
 * Redirects admins to /admin unless they enabled "user mode".
 *
 * Priority order:
 *   1. sessionStorage flag → allow through
 *   2. Persisted store user → decide immediately (no flash)
 *   3. /me API response → decide after network
 */
export const AdminRedirectGuard = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, user: storeUser } = useAuthStore()

  // Fetches fresh role from API; result shared via React Query cache with other consumers
  const { data: me, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: AuthService.getMe,
    enabled: isAuthenticated,
    staleTime: 5 * 60_000,
  })

  // Admin opted into user mode — skip redirect entirely
  if (isUserModeActive()) return <>{children}</>

  // ── Fast path: store user is already hydrated (persisted in localStorage) ──
  if (storeUser !== null) {
    return isAdmin(storeUser) ? <Navigate to="/admin" replace /> : <>{children}</>
  }

  // ── Slow path: store user is null (e.g. old session without persisted user) ──
  // Wait for /me to load before deciding; show neutral blank to avoid flash
  if (isLoading) {
    return <div className="min-h-screen bg-surface" />
  }

  // /me finished — route based on fresh API data
  if (isAdmin(me)) return <Navigate to="/admin" replace />

  return <>{children}</>
}
