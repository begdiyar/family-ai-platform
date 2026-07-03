import { Navigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { AuthService } from '@/services/auth.service'
import type { User } from '@/types/domain.types'

const isProfileComplete = (me: User) =>
  Boolean(me.last_name?.trim()) && Boolean(me.birth_date)

export const ProfileGuard = ({ children }: { children: React.ReactNode }) => {
  const { data: me, isLoading, isError } = useQuery({
    queryKey: ['me'],
    queryFn: AuthService.getMe,
  })

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    )
  }

  if (isError || !me) return <>{children}</>

  if (!isProfileComplete(me)) {
    return <Navigate to="/setup" replace />
  }

  return <>{children}</>
}
