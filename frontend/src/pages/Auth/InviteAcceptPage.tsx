import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { CoupleService } from '@/services/couple.service'
import { useAuthStore } from '@/store/auth.store'
import { Button } from '@/components/ui/Button'

export const InviteAcceptPage = () => {
  const { token } = useParams<{ token: string }>()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const { t } = useTranslation('auth')

  const mutation = useMutation({
    mutationFn: () => CoupleService.acceptInvite(token!),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      qc.invalidateQueries({ queryKey: ['couple'] })
      toast.success(t('invite.success_toast'))
      navigate('/app/couple')
    },
    onError: (e: any) => {
      const msg = e?.response?.data?.message || t('invite.error_toast')
      toast.error(msg)
      navigate('/app')
    },
  })

  useEffect(() => {
    if (isAuthenticated && token && !mutation.isPending && !mutation.isSuccess && !mutation.isError) {
      mutation.mutate()
    }
  }, [isAuthenticated, token])

  if (!isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4">
        <div className="w-full max-w-md text-center">
          <div className="mb-4 text-5xl">👫</div>
          <h2 className="mb-2 text-2xl font-bold text-gray-900">{t('invite.not_auth_title')}</h2>
          <p className="mb-6 text-gray-500">{t('invite.not_auth_desc')}</p>
          <div className="flex gap-3">
            <Button
              fullWidth
              variant="secondary"
              onClick={() => navigate(`/login?next=/invite/${token}`)}
            >
              {t('invite.login_btn')}
            </Button>
            <Button
              fullWidth
              onClick={() => navigate(`/register?next=/invite/${token}`)}
            >
              {t('invite.register_btn')}
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md text-center">
        <div className="mb-4 text-5xl">💑</div>
        <h2 className="mb-2 text-2xl font-bold text-gray-900">{t('invite.joining_title')}</h2>
        <p className="text-gray-500">{t('invite.joining_desc')}</p>
        {mutation.isPending && (
          <div className="mt-6 flex justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          </div>
        )}
        {mutation.isError && (
          <Button className="mt-6" onClick={() => mutation.mutate()}>
            {t('common:btn.retry', { defaultValue: 'Попробовать снова' })}
          </Button>
        )}
      </div>
    </div>
  )
}
