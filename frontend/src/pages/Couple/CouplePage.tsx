import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { Heart, Link2, ChevronLeft, Copy, RefreshCw } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { CoupleService } from '@/services/couple.service'
import { AuthService } from '@/services/auth.service'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Input } from '@/components/ui/Input'

const extractToken = (value: string): string => {
  const trimmed = value.trim()
  try {
    const url = new URL(trimmed)
    const parts = url.pathname.split('/').filter(Boolean)
    if (parts.length >= 2 && parts[parts.length - 2] === 'invite') {
      return parts[parts.length - 1]
    }
  } catch {
    // not a URL — use as token directly
  }
  return trimmed
}

export const CouplePage = () => {
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('couple')
  const [joinMode, setJoinMode] = useState(false)
  const [linkInput, setLinkInput] = useState('')
  const [joinFromPending, setJoinFromPending] = useState(false)

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  const { data: me, isLoading } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: couple, isLoading: coupleLoading } = useQuery({
    queryKey: ['couple'],
    queryFn: CoupleService.getMe,
    retry: false,
    enabled: !!me?.couple,
  })

  const createMutation = useMutation({
    mutationFn: CoupleService.create,
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['me'] }); qc.invalidateQueries({ queryKey: ['couple'] }) },
    onError: (e: any) => toast.error(e?.response?.data?.message || t('toast_create_error')),
  })

  const joinMutation = useMutation({
    mutationFn: (token: string) => CoupleService.acceptInvite(token),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['me'] })
      qc.invalidateQueries({ queryKey: ['couple'] })
      toast.success(t('toast_joined'))
      setJoinMode(false)
      setLinkInput('')
    },
    onError: (e: any) => toast.error(e?.response?.data?.message || t('toast_invalid_link')),
  })

  const regenMutation = useMutation({
    mutationFn: CoupleService.regenerateInvite,
    onSuccess: () => { toast.success(t('toast_link_updated')); qc.invalidateQueries({ queryKey: ['couple'] }) },
    onError: () => toast.error(t('toast_link_error')),
  })

  const copyLink = (link: string) => {
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(link)
        .then(() => toast.success(t('toast_link_copied')))
        .catch(() => copyFallback(link))
    } else {
      copyFallback(link)
    }
  }

  const copyFallback = (link: string) => {
    const el = document.createElement('textarea')
    el.value = link
    el.style.position = 'fixed'
    el.style.opacity = '0'
    document.body.appendChild(el)
    el.focus()
    el.select()
    try {
      document.execCommand('copy')
      toast.success(t('toast_link_copied'))
    } catch {
      toast.error(t('toast_copy_error', { defaultValue: 'Скопируйте ссылку вручную' }))
    }
    document.body.removeChild(el)
  }

  const handleJoin = () => {
    const token = extractToken(linkInput)
    if (!token) { toast.error(t('toast_empty_link')); return }
    joinMutation.mutate(token)
  }

  const pageHeader = (
    <div className="page-hero px-5 pt-6 pb-5">
      <div className="flex items-center gap-3">
        <div
          className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
          style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
        >
          <Heart size={17} className="text-white" fill="white" />
        </div>
        <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
      </div>
    </div>
  )

  if (isLoading || coupleLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        {pageHeader}
        <div className="px-4 pt-4 md:px-5">
          <div className="h-48 rounded-card shimmer" />
        </div>
      </div>
    )
  }

  if (!me?.couple) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        {pageHeader}
        <div className="px-4 pt-4 md:px-5 max-w-lg">
          {!joinMode ? (
            <div className="flex flex-col gap-3">
              <div
                className="rounded-[22px] p-6 text-center"
                style={{
                  background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)',
                  border: '1px solid rgba(60,56,136,0.12)',
                }}
              >
                <span className="mb-3 block text-4xl select-none">👫</span>
                <h2 className="mb-2 text-lg font-bold text-ink">{t('create_title')}</h2>
                <p className="mb-5 text-sm text-muted">{t('create_desc')}</p>
                <Button fullWidth onClick={() => createMutation.mutate()} loading={createMutation.isPending}>
                  <Heart size={15} fill="white" /> {t('create_btn')}
                </Button>
              </div>

              <div className="flex items-center gap-3">
                <div className="h-px flex-1 bg-sand/60" />
                <span className="text-xs text-muted">{t('common:or', { defaultValue: 'или' })}</span>
                <div className="h-px flex-1 bg-sand/60" />
              </div>

              <div
                className="rounded-[22px] p-6 text-center"
                style={{
                  background: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)',
                  border: '1px solid rgba(56,92,138,0.12)',
                }}
              >
                <span className="mb-3 block text-4xl select-none">🔗</span>
                <h2 className="mb-2 text-lg font-bold text-ink">{t('join_title')}</h2>
                <p className="mb-5 text-sm text-muted">{t('join_desc')}</p>
                <Button variant="secondary" fullWidth onClick={() => setJoinMode(true)}>
                  <Link2 size={16} /> {t('join_btn')}
                </Button>
              </div>
            </div>
          ) : (
            <div
              className="rounded-[22px] bg-canvas p-6"
              style={{
                border: '1px solid rgba(232,227,218,0.6)',
                boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)',
              }}
            >
              <button
                onClick={() => { setJoinMode(false); setLinkInput('') }}
                className="mb-4 flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary transition-colors"
              >
                <ChevronLeft size={16} /> {t('back_btn')}
              </button>
              <h2 className="mb-1 font-bold text-ink">{t('join_form_title')}</h2>
              <p className="mb-4 text-sm text-muted">{t('join_form_desc')}</p>
              <div className="flex flex-col gap-3">
                <Input
                  value={linkInput}
                  onChange={(e) => setLinkInput(e.target.value)}
                  placeholder="http://localhost:5173/invite/..."
                  onKeyDown={(e: any) => e.key === 'Enter' && handleJoin()}
                  autoFocus
                />
                <Button onClick={handleJoin} loading={joinMutation.isPending} disabled={!linkInput.trim()} fullWidth>
                  {t('join_submit_btn')}
                </Button>
              </div>
              <p className="mt-3 text-xs text-muted text-center">{t('join_form_hint')}</p>
            </div>
          )}
        </div>
      </div>
    )
  }

  if (couple?.status === 'pending' || me.couple.status === 'pending') {
    const inviteLink = couple?.invite?.link
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        {pageHeader}
        <div className="px-4 pt-4 md:px-5 max-w-lg">
          <div
            className="rounded-[22px] bg-canvas p-6"
            style={{
              border: '1px solid rgba(184,144,74,0.20)',
              boxShadow: '0 4px 20px rgba(184,144,74,0.08)',
            }}
          >
            <div className="mb-4">
              <Badge variant="warning">{t('pending_badge')}</Badge>
            </div>
            <h2 className="mb-1 font-bold text-ink">{t('share_title')}</h2>
            <p className="mb-4 text-sm text-muted leading-relaxed">
              {t('share_desc')}
            </p>

            {inviteLink ? (
              <>
                <div
                  className="mb-3 flex items-center gap-2 rounded-2xl px-4 py-3"
                  style={{ background: '#E8E2D4', border: '1px solid rgba(232,227,218,0.8)' }}
                >
                  <span className="flex-1 truncate text-sm text-ink select-all font-mono">{inviteLink}</span>
                </div>
                <div className="flex gap-2">
                  <Button onClick={() => copyLink(inviteLink)} className="flex-1">
                    <Copy size={15} /> {t('copy_btn')}
                  </Button>
                  <Button variant="ghost" onClick={() => regenMutation.mutate()} loading={regenMutation.isPending}>
                    <RefreshCw size={15} />
                  </Button>
                </div>
                <div className="mt-4 rounded-2xl px-4 py-3" style={{ background: '#DDE8F2' }}>
                  <p className="text-xs text-violet font-medium">
                    {t('partner_hint')}
                  </p>
                </div>
              </>
            ) : (
              <Button variant="secondary" onClick={() => qc.invalidateQueries({ queryKey: ['couple'] })}>
                {t('common:btn.retry', { defaultValue: 'Обновить' })}
              </Button>
            )}

            <div className="mt-5 flex items-center gap-3">
              <div className="h-px flex-1 bg-sand/60" />
              <span className="text-xs text-muted">{t('common:or', { defaultValue: 'или' })}</span>
              <div className="h-px flex-1 bg-sand/60" />
            </div>

            {!joinFromPending ? (
              <button
                onClick={() => setJoinFromPending(true)}
                className="mt-3 w-full text-sm text-primary font-medium text-center hover:underline"
              >
                {t('join_title')}
              </button>
            ) : (
              <div className="mt-3 flex flex-col gap-3">
                <Input
                  value={linkInput}
                  onChange={(e) => setLinkInput(e.target.value)}
                  placeholder="http://localhost:5173/invite/..."
                  onKeyDown={(e: any) => e.key === 'Enter' && handleJoin()}
                  autoFocus
                />
                <div className="flex gap-2">
                  <Button variant="ghost" onClick={() => { setJoinFromPending(false); setLinkInput('') }} className="flex-1">
                    {t('back_btn')}
                  </Button>
                  <Button onClick={handleJoin} loading={joinMutation.isPending} disabled={!linkInput.trim()} className="flex-1">
                    {t('join_submit_btn')}
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {pageHeader}
      <div className="px-4 pt-4 md:px-5 max-w-lg">
        <div
          className="rounded-[22px] bg-canvas p-6"
          style={{
            border: '1px solid rgba(56,104,88,0.20)',
            boxShadow: '0 4px 20px rgba(56,104,88,0.08)',
          }}
        >
          <Badge variant="success" className="mb-5">{t('active_badge')}</Badge>
          <div className="flex items-center gap-5">
            <div className="relative shrink-0">
              <div
                className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-brand text-white text-xl font-bold"
                style={{ boxShadow: '0 4px 16px rgba(60,56,136,0.35)' }}
              >
                {couple?.partner_a?.first_name?.[0]?.toUpperCase()}
              </div>
              <div
                className="absolute -right-4 top-1/2 -translate-y-1/2 flex h-10 w-10 items-center justify-center rounded-full bg-gradient-peach text-white text-base font-bold"
                style={{ boxShadow: '0 4px 12px rgba(136,80,64,0.30)' }}
              >
                {couple?.partner_b?.first_name?.[0]?.toUpperCase() ?? '?'}
              </div>
            </div>
            <div className="ml-6">
              <p className="font-bold text-ink text-lg">
                {couple?.partner_a?.first_name} & {couple?.partner_b?.first_name}
              </p>
              <p className="text-sm text-muted mt-0.5">
                {t('since')} {new Date(couple?.created_at ?? '').toLocaleDateString(dateLocale, { day: 'numeric', month: 'long', year: 'numeric' })}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
