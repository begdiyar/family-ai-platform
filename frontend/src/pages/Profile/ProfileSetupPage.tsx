import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { Heart, Sparkles } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { useAuthStore } from '@/store/auth.store'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Button } from '@/components/ui/Button'

type Form = {
  last_name: string
  birth_date: string
  gender: string
  preferred_language: string
}

export const ProfileSetupPage = () => {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('profile')
  const setUser = useAuthStore((s) => s.setUser)

  const schema = z.object({
    last_name: z.string().min(1, t('validation_last_name')),
    birth_date: z.string().min(1, t('validation_birth_date')),
    gender: z.string().min(1, t('validation_gender')),
    preferred_language: z.string(),
  })

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const { register, handleSubmit, formState: { errors } } = useForm<Form>({
    resolver: zodResolver(schema),
    values: {
      last_name: me?.last_name ?? '',
      birth_date: me?.birth_date ?? '',
      gender: me?.gender ?? '',
      preferred_language: me?.preferred_language ?? 'ru',
    },
  })

  const mutation = useMutation({
    mutationFn: (data: Form) =>
      AuthService.updateMe({ ...data, birth_date: data.birth_date || null }),
    onSuccess: (user) => {
      setUser(user)
      qc.setQueryData(['me'], user)
      if (user.preferred_language) i18n.changeLanguage(user.preferred_language)
      navigate('/app', { replace: true })
    },
    onError: () => toast.error(t('toast_error')),
  })

  return (
    <div className="min-h-screen bg-surface flex flex-col items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm">

        {/* ── Hero ────────────────────────────────────────────── */}
        <div className="mb-8 text-center">
          <div
            className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-[22px]"
            style={{
              background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
              boxShadow: '0 8px 28px rgba(60,56,136,0.32)',
            }}
          >
            <Heart size={28} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold text-ink">{t('setup_title')}</h1>
          {me?.first_name && (
            <p className="mt-1 text-base font-semibold text-primary">
              {t('setup_greeting')}, {me.first_name}!
            </p>
          )}
          <p className="mt-2 text-sm text-muted leading-relaxed px-2">
            {t('setup_desc')}
          </p>
        </div>

        {/* ── Form ─────────────────────────────────────────────── */}
        <form
          onSubmit={handleSubmit((d) => mutation.mutate(d))}
          className="rounded-[24px] bg-canvas px-6 py-6 flex flex-col gap-4"
          style={{
            border: '1px solid rgba(232,227,218,0.6)',
            boxShadow: '0 4px 24px rgba(23,21,42,0.08), 0 1px 4px rgba(23,21,42,0.04)',
          }}
        >
          <Input
            label={t('last_name_label')}
            placeholder={t('last_name_placeholder')}
            error={errors.last_name?.message}
            autoFocus
            {...register('last_name')}
          />

          <Input
            label={t('birth_date_label')}
            type="date"
            max={new Date().toISOString().split('T')[0]}
            error={errors.birth_date?.message}
            {...register('birth_date')}
          />

          <Select
            label={t('gender_label')}
            error={errors.gender?.message}
            {...register('gender')}
          >
            <option value="">{t('gender_empty')}</option>
            <option value="male">{t('gender_male')}</option>
            <option value="female">{t('gender_female')}</option>
            <option value="other">{t('gender_other')}</option>
            <option value="prefer_not_to_say">{t('gender_prefer_not')}</option>
          </Select>

          <Select label={t('language_label')} {...register('preferred_language')}>
            <option value="ru">{t('lang_ru')}</option>
            <option value="en">{t('lang_en')}</option>
            <option value="uz">{t('lang_uz')}</option>
          </Select>

          <Button type="submit" loading={mutation.isPending} className="mt-1">
            <Sparkles size={15} /> {t('setup_btn')}
          </Button>
        </form>

        <p className="mt-4 text-center text-xs text-muted/60">
          {t('setup_hint')}
        </p>
      </div>
    </div>
  )
}
