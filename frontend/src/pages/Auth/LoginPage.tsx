import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { useAuthStore } from '@/store/auth.store'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { LanguageSwitcher } from '@/components/LanguageSwitcher'

type Form = { email: string; password: string }

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

export const LoginPage = () => {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const setAuth = useAuthStore((s) => s.setAuth)
  const { t } = useTranslation('auth')

  const schema = z.object({
    email: z.string().email(t('login.validation_email')),
    password: z.string().min(1, t('login.validation_password')),
  })

  const { register, handleSubmit, formState: { errors } } = useForm<Form>({ resolver: zodResolver(schema) })

  const mutation = useMutation({
    mutationFn: AuthService.login,
    onSuccess: ({ user, tokens }) => {
      setAuth(user, tokens)
      const next = searchParams.get('next')
      const target = next && next.startsWith('/') && !next.startsWith('//') ? next : '/app'
      navigate(target)
    },
    onError: () => toast.error(t('login.error_credentials')),
  })

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4">
      <div className="absolute inset-0 bg-gradient-hero" />
      <div className="absolute inset-0 bg-dots-light opacity-25" />

      <div className="absolute -top-40 -left-40 h-[420px] w-[420px] rounded-full bg-primary/8 blur-[80px] pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 h-[420px] w-[420px] rounded-full bg-violet/8 blur-[80px] pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 h-48 w-48 rounded-full bg-sage/6 blur-[60px] pointer-events-none" />

      <motion.div
        className="relative w-full max-w-md"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease }}
      >
        <div
          className="rounded-[32px] p-8 backdrop-blur-xl"
          style={{
            background: 'rgba(244,239,228,0.88)',
            border: '1px solid rgba(244,239,228,0.70)',
            boxShadow: '0 8px 40px rgba(60,56,136,0.12), 0 2px 8px rgba(23,21,42,0.07)',
          }}
        >
          <div className="mb-8 flex flex-col items-center gap-3">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.4, delay: 0.1, ease }}
              className="flex h-16 w-16 items-center justify-center rounded-3xl bg-gradient-brand"
              style={{ boxShadow: '0 8px 24px rgba(60,56,136,0.38)' }}
            >
              <Sparkles size={26} className="text-white" />
            </motion.div>
            <div className="text-center">
              <h1 className="text-2xl font-bold text-ink">{t('login.title')}</h1>
              <p className="mt-1 text-sm text-muted">{t('login.subtitle')}</p>
            </div>
          </div>

          <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className="flex flex-col gap-4">
            <Input
              label={t('login.email_label')}
              type="email"
              placeholder="you@email.com"
              error={errors.email?.message}
              {...register('email')}
            />
            <Input
              label={t('login.password_label')}
              type="password"
              placeholder="••••••••"
              error={errors.password?.message}
              {...register('password')}
            />
            <Button type="submit" fullWidth loading={mutation.isPending} size="lg" className="mt-2">
              {t('login.submit')}
            </Button>
          </form>

          <div className="mt-6 flex items-center gap-3">
            <div className="h-px flex-1 bg-sand/50" />
            <span className="text-xs text-muted">{t('common:or', { defaultValue: 'или' })}</span>
            <div className="h-px flex-1 bg-sand/50" />
          </div>

          <p className="mt-4 text-center text-sm text-muted">
            {t('login.no_account')}{' '}
            <Link to="/register" className="font-semibold text-primary hover:text-primary-700 transition-colors">
              {t('login.register_link')}
            </Link>
          </p>

          <div className="mt-4 flex justify-center">
            <LanguageSwitcher />
          </div>
        </div>
      </motion.div>
    </div>
  )
}
