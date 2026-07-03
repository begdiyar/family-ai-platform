import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/auth.store'

export const AdminRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, user } = useAuthStore()

  if (!isAuthenticated) return <Navigate to="/login" replace />

  // user is null: tokens exist but user not yet hydrated — allow through,
  // AdminLayout will handle the access check via /me query
  if (user !== null && !user.is_staff && !user.is_superuser) {
    return <Navigate to="/app" replace />
  }

  return <>{children}</>
}
