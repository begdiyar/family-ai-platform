import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ClipboardList, CheckCircle2, Sparkles } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { DiagnosticsService } from '@/services/diagnostics.service'
import { AuthService } from '@/services/auth.service'
import { Button } from '@/components/ui/Button'
import { ProgressBar } from '@/components/ui/ProgressBar'
import { Badge } from '@/components/ui/Badge'
import { EmptyState } from '@/components/feedback/EmptyState'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

const ZONE_KEYS = ['communication', 'trust', 'intimacy', 'conflict', 'values', 'future'] as const

export const DiagnosticsPage = () => {
  const navigate = useNavigate()
  const { t } = useTranslation(['diagnostics', 'common'])

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: session } = useQuery({
    queryKey: ['session', 'current'],
    queryFn: DiagnosticsService.getCurrentSession,
    retry: false,
    enabled: !!me?.couple,
  })

  const PageHeader = () => (
    <div className="page-hero px-5 pt-6 pb-5">
      <div className="flex items-center gap-3">
        <div
          className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
          style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
        >
          <ClipboardList size={17} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
          <p className="text-xs text-muted mt-0.5">{t('subtitle')}</p>
        </div>
      </div>
    </div>
  )

  if (!me?.couple) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4 md:px-5">
          <EmptyState
            icon={<ClipboardList />}
            title={t('no_couple_title')}
            description={t('no_couple_desc')}
            actionLabel={t('no_couple_btn')}
            onAction={() => navigate('/app/couple')}
          />
        </div>
      </div>
    )
  }

  if (session?.status === 'completed') {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4 md:px-5 max-w-lg">
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, ease }}>
            <div
              className="rounded-[22px] p-6 bg-canvas"
              style={{ border: '1px solid rgba(56,104,88,0.20)', boxShadow: '0 4px 20px rgba(56,104,88,0.08)' }}
            >
              <div className="mb-4 flex items-center gap-2">
                <CheckCircle2 size={20} className="text-success" />
                <Badge variant="success">{t('completed_badge')}</Badge>
              </div>
              <h2 className="mb-2 text-lg font-bold text-ink">{t('completed_title')}</h2>
              <ProgressBar
                value={100}
                label={`${session.total_questions} ${t('completed_of')} ${session.total_questions} ${t('completed_questions')}`}
                showValue
                className="mb-4"
              />
              <p className="mb-4 text-sm text-muted leading-relaxed">{t('completed_desc')}</p>
              <Button variant="secondary" onClick={() => navigate('/app/analytics')}>
                {t('completed_btn')}
              </Button>
            </div>
          </motion.div>
        </div>
      </div>
    )
  }

  if (session?.status === 'in_progress') {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4 md:px-5 max-w-lg">
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, ease }}>
            <div
              className="rounded-[22px] p-6 bg-canvas"
              style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)' }}
            >
              <h2 className="mb-2 text-lg font-bold text-ink">{t('in_progress_title')}</h2>
              <ProgressBar
                value={session.progress_percent}
                label={`${session.answers_count} ${t('in_progress_of')} ${session.total_questions} ${t('in_progress_questions')}`}
                showValue
                size="md"
                className="mb-4"
              />
              <Button onClick={() => navigate('/app/diagnostics/start')}>{t('in_progress_btn')}</Button>
            </div>
          </motion.div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <PageHeader />
      <div className="px-4 pt-4 md:px-5 max-w-lg">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease }}
        >
          <div
            className="mb-4 rounded-[22px] p-5"
            style={{
              background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 50%, #D6E8E2 100%)',
              border: '1px solid rgba(60,56,136,0.12)',
            }}
          >
            <div className="flex gap-4">
              <span className="text-3xl shrink-0">📋</span>
              <div>
                <p className="font-bold text-ink">{t('intro_title')}</p>
                <p className="mt-1 text-sm text-muted leading-relaxed">{t('intro_desc')}</p>
              </div>
            </div>
          </div>

          <div className="mb-4 grid grid-cols-3 gap-2">
            {ZONE_KEYS.map((key, i) => (
              <motion.div
                key={key}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, ease, delay: 0.1 + i * 0.04 }}
                className="rounded-[14px] px-2 py-2.5 text-center text-xs font-semibold text-primary"
                style={{ background: 'rgba(60,56,136,0.08)' }}
              >
                {t(`common:zones.${key}`)}
              </motion.div>
            ))}
          </div>

          <div className="mb-3 flex items-center gap-2 rounded-2xl px-4 py-2.5" style={{ background: '#EDEAF8' }}>
            <Sparkles size={14} className="text-primary shrink-0" />
            <span className="text-xs font-medium text-primary">{t('privacy_note')}</span>
          </div>

          <Button fullWidth onClick={() => navigate('/app/diagnostics/start')}>
            {t('start_btn')}
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
