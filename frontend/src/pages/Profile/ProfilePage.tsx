import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { User } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { useAuthStore } from '@/store/auth.store'
import { Card } from '@/components/ui/Card'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'

type Form = { first_name: string }

export const ProfilePage = () => {
  const qc = useQueryClient()
  const { t } = useTranslation('profile')
  const setUser = useAuthStore((s) => s.setUser)

  const schema = z.object({
    first_name: z.string().min(2, t('validation_name')),
  })

  const { data: me, isLoading } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const { register, handleSubmit, formState: { errors } } = useForm<Form>({
    resolver: zodResolver(schema),
    values: { first_name: me?.first_name ?? '' },
  })

  const mutation = useMutation({
    mutationFn: (data: Form) => AuthService.updateMe(data),
    onSuccess: (user) => {
      setUser(user)
      qc.setQueryData(['me'], user)
      toast.success(t('toast_updated'))
    },
    onError: () => toast.error(t('toast_error')),
  })

  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="page-hero px-5 pt-6 pb-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 rounded-2xl shimmer" />
            <div className="h-6 w-32 rounded-xl shimmer" />
          </div>
        </div>
        <div className="px-4 pt-4 md:px-5 max-w-md">
          <div className="h-52 rounded-card shimmer" />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <div className="page-hero px-5 pt-6 pb-5">
        <div className="flex items-center gap-3">
          <div
            className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
            style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
          >
            <User size={17} className="text-white" />
          </div>
          <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
        </div>
      </div>

      <div className="px-4 pt-4 md:px-5 max-w-md">
        <div
          className="rounded-[22px] bg-canvas p-6"
          style={{
            border: '1px solid rgba(232,227,218,0.6)',
            boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)',
          }}
        >
          <div className="mb-6 flex items-center gap-4">
            <div
              className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-brand text-2xl font-bold text-white"
              style={{ boxShadow: '0 4px 16px rgba(60,56,136,0.35)' }}
            >
              {me?.first_name?.[0]?.toUpperCase() ?? '?'}
            </div>
            <div>
              <p className="font-bold text-ink">{me?.first_name}</p>
              <p className="text-sm text-muted">{me?.email}</p>
            </div>
          </div>

          <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className="flex flex-col gap-4">
            <Input
              label={t('name_label')}
              placeholder={t('name_placeholder')}
              error={errors.first_name?.message}
              {...register('first_name')}
            />
            <Button type="submit" loading={mutation.isPending}>
              {t('save_btn')}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
