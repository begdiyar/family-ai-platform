import { useTranslation } from 'react-i18next'
import { useQuery, useMutation } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'
import { Server, Database, Shield, Clock, Lock } from 'lucide-react'
import { AdminService } from '@/services/admin.service'
import { AuthService } from '@/services/auth.service'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'

type PwdForm = { current_password: string; new_password: string; confirm_password: string }

function ChangePasswordCard({ cardClass, cardStyle }: { cardClass: string; cardStyle: object }) {
  const { t } = useTranslation('admin')

  const schema = z.object({
    current_password: z.string().min(1, t('settings.pwd_current_required')),
    new_password: z.string().min(8, t('settings.pwd_min')),
    confirm_password: z.string(),
  }).refine(d => d.new_password === d.confirm_password, {
    message: t('settings.pwd_mismatch'),
    path: ['confirm_password'],
  })

  const { register, handleSubmit, reset, formState: { errors } } = useForm<PwdForm>({
    resolver: zodResolver(schema),
  })

  const mutation = useMutation({
    mutationFn: (d: PwdForm) =>
      AuthService.changePassword({ current_password: d.current_password, new_password: d.new_password }),
    onSuccess: () => { toast.success(t('settings.pwd_changed')); reset() },
    onError: (e: any) => toast.error(e?.response?.data?.current_password?.[0] ?? t('settings.pwd_error')),
  })

  return (
    <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className={cardClass} style={cardStyle}>
      <div className="flex items-center gap-2 mb-4">
        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#EDEAF8]">
          <Lock size={14} className="text-[#3C3888]" />
        </div>
        <p className="text-sm font-bold text-ink">{t('settings.pwd_title')}</p>
      </div>
      <div className="flex flex-col gap-3">
        <Input label={t('settings.pwd_current')} type="password" placeholder="••••••••"
               error={errors.current_password?.message} {...register('current_password')} />
        <Input label={t('settings.pwd_new')} type="password" placeholder="••••••••"
               error={errors.new_password?.message} {...register('new_password')} />
        <Input label={t('settings.pwd_confirm')} type="password" placeholder="••••••••"
               error={errors.confirm_password?.message} {...register('confirm_password')} />
        <Button type="submit" loading={mutation.isPending} fullWidth>{t('settings.pwd_save')}</Button>
      </div>
    </form>
  )
}

export const AdminSettingsPage = () => {
  const { t } = useTranslation('admin')

  const { data: overview } = useQuery({
    queryKey: ['admin-overview'],
    queryFn: AdminService.getOverview,
    staleTime: 60_000,
  })
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const CARD = 'rounded-[20px] bg-canvas p-5'
  const CARD_STYLE = { border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }

  const sysInfo = [
    { icon: Server,   labelKey: 'settings.sys.platform',  value: 'Oila AI v1.0' },
    { icon: Database, labelKey: 'settings.sys.database',  value: 'PostgreSQL 16' },
    { icon: Shield,   labelKey: 'settings.sys.auth',      value: 'JWT / SimpleJWT' },
    { icon: Clock,    labelKey: 'settings.sys.timezone',  value: 'UTC' },
  ]

  return (
    <div className="min-h-full bg-surface p-4 md:p-6 space-y-5">
      <div>
        <h1 className="text-xl md:text-2xl font-bold text-ink">{t('settings.title')}</h1>
        <p className="text-sm text-muted mt-0.5">{t('settings.subtitle')}</p>
      </div>

      {/* System info */}
      <div className={CARD} style={CARD_STYLE}>
        <p className="text-sm font-bold text-ink mb-4">{t('settings.sys_info')}</p>
        <div className="space-y-3">
          {sysInfo.map(({ icon: Icon, labelKey, value }) => (
            <div key={labelKey} className="flex items-center justify-between py-2.5"
                 style={{ borderBottom: '1px solid rgba(194,184,164,0.30)' }}>
              <div className="flex items-center gap-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#EDEAF8]">
                  <Icon size={14} className="text-[#3C3888]" />
                </div>
                <span className="text-sm text-muted">{t(labelKey)}</span>
              </div>
              <span className="text-sm font-semibold text-ink">{value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Admin user */}
      <div className={CARD} style={CARD_STYLE}>
        <p className="text-sm font-bold text-ink mb-4">{t('settings.admin_user')}</p>
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#3C3888] text-white text-lg font-bold">
            {me?.first_name?.charAt(0).toUpperCase() ?? 'A'}
          </div>
          <div>
            <p className="font-semibold text-ink">{me?.first_name ?? '—'}</p>
            <p className="text-sm text-muted">{me?.email ?? '—'}</p>
            <div className="mt-1 flex gap-1.5">
              {me?.is_staff    && <span className="rounded-full bg-[#EDEAF8] px-2 py-0.5 text-[10px] font-bold text-[#3C3888]">staff</span>}
              {me?.is_superuser && <span className="rounded-full bg-[#F5DDE4] px-2 py-0.5 text-[10px] font-bold text-[#843048]">superuser</span>}
            </div>
          </div>
        </div>
      </div>

      {/* Change password */}
      <ChangePasswordCard cardClass={CARD} cardStyle={CARD_STYLE} />

      {/* Platform metrics */}
      {overview && (
        <div className={CARD} style={CARD_STYLE}>
          <p className="text-sm font-bold text-ink mb-4">{t('settings.platform_state')}</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { labelKey: 'settings.state.users',       value: overview.total_users },
              { labelKey: 'settings.state.families',    value: overview.total_couples },
              { labelKey: 'settings.state.diagnostics', value: overview.completed_diagnostics },
              { labelKey: 'settings.state.ai_messages', value: overview.ai_messages },
            ].map(({ labelKey, value }) => (
              <div key={labelKey} className="rounded-[14px] bg-surface p-3 text-center">
                <p className="text-xl font-bold text-ink">{value}</p>
                <p className="text-xs text-muted mt-0.5">{t(labelKey)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Coming soon */}
      <div className={CARD} style={{ ...CARD_STYLE, opacity: 0.65 }}>
        <div className="flex items-center justify-between">
          <p className="text-sm font-bold text-ink">{t('settings.coming_soon')}</p>
          <span className="rounded-full bg-sand px-2.5 py-0.5 text-[10px] font-bold text-muted">{t('settings.coming_soon_badge')}</span>
        </div>
        <p className="text-xs text-muted mt-2">{t('settings.coming_soon_desc')}</p>
      </div>
    </div>
  )
}
