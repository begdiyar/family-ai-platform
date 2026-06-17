import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Heart, Sparkles, Sun, MessageCircle, ArrowRight,
  TrendingUp, TrendingDown, Minus, AlertTriangle, AlertOctagon,
  Calendar, CheckCircle2,
} from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/auth.store'
import { AuthService } from '@/services/auth.service'
import { PlanService } from '@/services/plan.service'
import { AnalyticsService } from '@/services/analytics.service'
import { PracticesService } from '@/services/practices.service'
import { Button } from '@/components/ui/Button'
import { ProgressBar } from '@/components/ui/ProgressBar'
import { Badge } from '@/components/ui/Badge'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 14 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] as [number, number, number, number], delay },
})

const CRISIS_COLOR: Record<string, string> = {
  none: '#386858',
  warning: '#886028',
  critical: '#843048',
}

export const DashboardPage = () => {
  const navigate = useNavigate()
  const user = useAuthStore((s) => s.user)
  const { t } = useTranslation(['dashboard', 'common'])

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: plan } = useQuery({ queryKey: ['plan', 'current'], queryFn: PlanService.getCurrent, retry: false })
  const { data: latestAnalytics } = useQuery({
    queryKey: ['analytics', 'latest'],
    queryFn: AnalyticsService.getLatest,
    enabled: !!me?.couple,
    retry: false,
  })
  const { data: analyticsList } = useQuery({
    queryKey: ['analytics'],
    queryFn: AnalyticsService.list,
    enabled: !!me?.couple,
    retry: false,
  })
  const { data: todayPractice } = useQuery({
    queryKey: ['practices-today'],
    queryFn: PracticesService.getToday,
    enabled: !!me?.couple,
    retry: false,
  })

  const couple = me?.couple
  const firstName = me?.first_name || user?.first_name || ''
  const partnerName = couple?.partner?.first_name || ''

  const score = latestAnalytics ? Math.round(latestAnalytics.overall_score) : null
  const crisis = (latestAnalytics?.crisis_level ?? 'none') as string

  const results = analyticsList?.results ?? []
  const prevScore = results.length >= 2 ? Math.round(results[1]?.overall_score ?? 0) : null
  const delta = score !== null && prevScore !== null ? score - prevScore : null

  const todayTask = plan?.weeks.find((w: any) => !w.locked)?.tasks.find((tk: any) => !tk.completed_by_me)
  const practicesDone = todayPractice?.items.filter((i: any) => i.completed).length ?? 0
  const practicesTotal = todayPractice?.items.length ?? 0

  const greeting = (): string => {
    const h = new Date().getHours()
    if (h < 12) return t('greeting_morning')
    if (h < 18) return t('greeting_day')
    return t('greeting_evening')
  }

  const crisisLabel = (level: string) => t(`common:crisis.${level}`, { defaultValue: level })

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">

      {/* ── Top bar ─────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between px-5 pt-6 pb-2">
        <div>
          <p className="label-caps text-muted">{greeting()}</p>
          <h1 className="text-xl font-bold text-ink mt-0.5">{firstName}</h1>
        </div>
        {couple && (
          <button
            onClick={() => navigate('/app/profile')}
            className="flex items-center gap-2 rounded-pill bg-primary-50 px-3 py-1.5 border border-primary-100/60"
          >
            <Heart size={12} className="text-primary" fill="currentColor" />
            <span className="text-xs font-semibold text-primary-700">
              {firstName} & {partnerName || t('common:partner')}
            </span>
          </button>
        )}
      </div>

      <div className="px-4 pt-2 md:px-5 space-y-3">

        {/* ── Alerts ──────────────────────────────────────────────────── */}
        {crisis === 'critical' && (
          <motion.div {...fadeUp(0)}
            className="rounded-2xl border border-rose-200 bg-rose-50 px-5 py-4"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex gap-3">
                <AlertOctagon size={18} className="mt-0.5 shrink-0 text-rose-600" />
                <div>
                  <p className="font-bold text-rose-800 text-sm">{t('crisis_critical_title')}</p>
                  <p className="text-xs text-rose-600 mt-0.5">{t('crisis_critical_desc')}</p>
                </div>
              </div>
              <Button size="sm" variant="danger" onClick={() => navigate('/app/practices')}>
                {t('crisis_critical_btn')}
              </Button>
            </div>
          </motion.div>
        )}
        {crisis === 'warning' && (
          <motion.div {...fadeUp(0)}
            className="rounded-2xl border border-amber-200 bg-amber-50 px-5 py-3"
          >
            <div className="flex items-center gap-3">
              <AlertTriangle size={16} className="shrink-0 text-amber-600" />
              <p className="text-sm text-amber-800">{t('crisis_warning_text')}</p>
              <button
                onClick={() => navigate('/app/index')}
                className="ml-auto text-xs font-semibold text-amber-700 shrink-0"
              >
                {t('crisis_warning_link')}
              </button>
            </div>
          </motion.div>
        )}

        {/* ── Hero: Индекс отношений ──────────────────────────────────── */}
        {score !== null && (
          <motion.div {...fadeUp(0.05)}>
            <div
              className="relative overflow-hidden rounded-[28px] cursor-pointer"
              style={{
                background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 60%, #D6E8E2 100%)',
                border: '1px solid rgba(60,56,136,0.14)',
                boxShadow: '0 4px 24px rgba(23,21,42,0.10), 0 1px 6px rgba(23,21,42,0.06)',
              }}
              onClick={() => navigate('/app/index')}
            >
              <div className="absolute -top-10 -right-10 h-40 w-40 rounded-full bg-primary/8 blur-3xl" />
              <div className="absolute -bottom-8 -left-8 h-32 w-32 rounded-full bg-violet/8 blur-2xl" />
              <div className="absolute top-4 right-4">
                <ArrowRight size={16} className="text-primary/40" />
              </div>

              <div className="relative p-6">
                <p className="label-caps text-primary/70 mb-3">{t('index_label')}</p>

                <div className="flex items-end gap-4 mb-4">
                  <div className="flex items-baseline gap-1">
                    <span className="font-display text-6xl text-ink" style={{ letterSpacing: '-0.04em' }}>
                      {score}
                    </span>
                    <span className="text-2xl font-semibold text-muted/70 mb-1">/ 100</span>
                  </div>

                  <div className="mb-2 flex flex-col items-start gap-1">
                    <Badge variant={crisis === 'none' ? 'success' : crisis === 'warning' ? 'warning' : 'danger'}>
                      {crisisLabel(crisis)}
                    </Badge>
                    {delta !== null && (
                      <div className={`flex items-center gap-1 text-xs font-semibold ${
                        delta > 0 ? 'text-sage-700' : delta < 0 ? 'text-danger' : 'text-muted'
                      }`}>
                        {delta > 0
                          ? <TrendingUp size={12} />
                          : delta < 0
                          ? <TrendingDown size={12} />
                          : <Minus size={12} />
                        }
                        {delta > 0 ? '+' : ''}{delta} {t('from_last_session')}
                      </div>
                    )}
                  </div>
                </div>

                <div className="h-2 w-full rounded-full overflow-hidden"
                     style={{ background: 'rgba(60,56,136,0.14)' }}>
                  <div
                    className="h-full rounded-full transition-all duration-1000"
                    style={{
                      width: `${score}%`,
                      background: `linear-gradient(90deg, ${CRISIS_COLOR[crisis]}, ${
                        crisis === 'none' ? '#385C8A' : CRISIS_COLOR[crisis]
                      })`,
                    }}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* ── Нет данных — CTA пройти диагностику ───────────────────── */}
        {!score && couple && (
          <motion.div {...fadeUp(0.05)}>
            <div
              className="rounded-[28px] p-6 text-center"
              style={{
                background: 'linear-gradient(145deg, #EDEAF8 0%, #DDE8F2 100%)',
                border: '1px solid rgba(60,56,136,0.12)',
              }}
            >
              <div className="mb-3 flex justify-center">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-brand shadow-[0_6px_20px_rgba(60,56,136,0.32)]">
                  <Heart size={24} className="text-white" />
                </div>
              </div>
              <p className="font-bold text-ink mb-1">{t('no_score_title')}</p>
              <p className="text-sm text-muted mb-4">{t('no_score_desc')}</p>
              <Button onClick={() => navigate('/app/diagnostics')} size="md">
                <Sparkles size={15} /> {t('no_score_btn')}
              </Button>
            </div>
          </motion.div>
        )}

        {!couple && (
          <motion.div {...fadeUp(0.05)}>
            <div
              className="rounded-[28px] p-6 text-center"
              style={{
                background: 'linear-gradient(145deg, #EDEAF8 0%, #DDE8F2 100%)',
                border: '1px solid rgba(60,56,136,0.12)',
              }}
            >
              <div className="mb-3 flex justify-center">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-brand shadow-[0_6px_20px_rgba(60,56,136,0.32)]">
                  <Heart size={24} className="text-white" />
                </div>
              </div>
              <p className="font-bold text-ink mb-1">{t('no_couple_title')}</p>
              <p className="text-sm text-muted mb-4">{t('common:invite_partner_first')}</p>
              <Button onClick={() => navigate('/app/couple')} size="md">
                {t('common:invite_partner_btn')}
              </Button>
            </div>
          </motion.div>
        )}

        {/* ── 2 мини-карточки ─────────────────────────────────────────── */}
        <motion.div {...fadeUp(0.10)} className="grid grid-cols-2 gap-3">

          <div
            className="rounded-[20px] p-4 cursor-pointer"
            style={{
              background: 'linear-gradient(135deg, #EEE4DC 0%, #EDEAF8 100%)',
              border: '1px solid rgba(136,80,64,0.18)',
            }}
            onClick={() => navigate('/app/practices')}
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-peach shadow-[0_3px_10px_rgba(136,80,64,0.28)] mb-3">
              <Sun size={16} className="text-white" />
            </div>
            <p className="label-caps text-accent/70">{t('practices_label')}</p>
            <p className="mt-0.5 text-lg font-bold text-ink">
              {practicesTotal > 0 ? `${practicesDone}/${practicesTotal}` : '—'}
            </p>
            {practicesTotal > 0 && (
              <div className="mt-2">
                <ProgressBar
                  value={practicesTotal > 0 ? (practicesDone / practicesTotal) * 100 : 0}
                  color="accent"
                  size="xs"
                />
              </div>
            )}
          </div>

          <div
            className="rounded-[20px] p-4 cursor-pointer"
            style={{
              background: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)',
              border: '1px solid rgba(56,104,88,0.18)',
            }}
            onClick={() => navigate('/app/practices')}
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-sage shadow-[0_3px_10px_rgba(56,104,88,0.28)] mb-3">
              <Calendar size={16} className="text-white" />
            </div>
            <p className="label-caps text-sage-700/70">{t('plan_label')}</p>
            {plan ? (
              <>
                <p className="mt-0.5 text-lg font-bold text-ink">{Math.round(plan.overall_progress)}%</p>
                <div className="mt-2">
                  <ProgressBar value={plan.overall_progress} color="success" size="xs" />
                </div>
              </>
            ) : (
              <p className="mt-0.5 text-sm text-muted">{t('plan_not_started')}</p>
            )}
          </div>
        </motion.div>

        {/* ── Задание дня ─────────────────────────────────────────────── */}
        {todayTask && (
          <motion.div {...fadeUp(0.15)}>
            <div
              className="rounded-[20px] p-5 cursor-pointer"
              style={{
                background: '#F4EFE4',
                border: '1px solid rgba(194,184,164,0.90)',
                boxShadow: '0 2px 8px rgba(23,21,42,0.07), 0 8px 24px rgba(23,21,42,0.08)',
              }}
              onClick={() => navigate('/app/practices')}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <p className="label-caps text-primary/70 mb-1.5">{t('task_of_day')}</p>
                  <p className="font-semibold text-ink leading-snug">{todayTask.title}</p>
                  {todayTask.description && (
                    <p className="mt-1 text-xs text-muted line-clamp-2 leading-relaxed">
                      {todayTask.description}
                    </p>
                  )}
                </div>
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-primary-50">
                  <ArrowRight size={16} className="text-primary" />
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* ── Практика дня (первая невыполненная) ────────────────────── */}
        {todayPractice && practicesDone < practicesTotal && (
          <motion.div {...fadeUp(0.20)}>
            {(() => {
              const next = todayPractice.items.find((i: any) => !i.completed)
              if (!next) return null
              return (
                <div
                  className="rounded-[20px] p-5 cursor-pointer"
                  style={{
                    background: 'linear-gradient(135deg, #E8E2D4 0%, #EDEAF8 100%)',
                    border: '1px solid rgba(60,56,136,0.12)',
                  }}
                  onClick={() => navigate('/app/practices')}
                >
                  <p className="label-caps text-muted mb-2">{t('recommendation')}</p>
                  <div className="flex items-start gap-3">
                    <span className="text-2xl mt-0.5 shrink-0">
                      {next.key === 'question_of_day' ? '💬' :
                       next.key === 'romantic_idea' ? '🌸' :
                       next.key === 'trust_exercise' ? '🤝' : '✨'}
                    </span>
                    <div>
                      <p className="text-xs font-semibold text-primary mb-1">{next.label}</p>
                      <p className="text-sm text-ink leading-relaxed">{next.content}</p>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center gap-1 text-xs font-semibold text-primary">
                    {t('complete_action')} <ArrowRight size={12} />
                  </div>
                </div>
              )
            })()}
          </motion.div>
        )}

        {/* ── Все выполнены ────────────────────────────────────────────── */}
        {practicesTotal > 0 && practicesDone === practicesTotal && (
          <motion.div {...fadeUp(0.20)}>
            <div className="rounded-[20px] p-5 text-center"
                 style={{ background: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)', border: '1px solid rgba(56,104,88,0.18)' }}>
              <CheckCircle2 size={28} className="mx-auto mb-2 text-sage-700" />
              <p className="font-semibold text-ink">{t('all_done_title')}</p>
              <p className="mt-1 text-xs text-muted">{t('all_done_desc')}</p>
            </div>
          </motion.div>
        )}

        {/* ── Быстрые действия ────────────────────────────────────────── */}
        <motion.div {...fadeUp(0.25)}>
          <p className="label-caps text-muted mb-2 px-1">{t('quick_access')}</p>
          <div className="grid grid-cols-2 gap-3">
            <QuickAction
              icon={<MessageCircle size={16} />}
              label={t('common:nav.ai')}
              sublabel={t('ai_sublabel')}
              color="lavender"
              onClick={() => navigate('/app/ai')}
            />
            <QuickAction
              icon={<TrendingUp size={16} />}
              label={t('analytics_label')}
              sublabel={t('analytics_sublabel')}
              color="sky"
              onClick={() => navigate('/app/analytics')}
            />
          </div>
        </motion.div>
      </div>
    </div>
  )
}

const QUICK_COLORS = {
  lavender: {
    wrap: 'from-primary-50 to-violet-light border-primary-100/60',
    icon: 'bg-gradient-brand shadow-[0_3px_10px_rgba(60,56,136,0.28)]',
    label: 'text-primary-700',
    sub: 'text-muted',
  },
  sky: {
    wrap: 'from-violet-light to-primary-50 border-violet/15',
    icon: 'bg-gradient-violet shadow-[0_3px_10px_rgba(56,92,138,0.28)]',
    label: 'text-violet-700',
    sub: 'text-muted',
  },
}

const QuickAction = ({
  icon, label, sublabel, color, onClick,
}: {
  icon: React.ReactNode
  label: string
  sublabel: string
  color: keyof typeof QUICK_COLORS
  onClick: () => void
}) => {
  const c = QUICK_COLORS[color]
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-3 rounded-[20px] bg-gradient-to-br ${c.wrap} border p-4 text-left transition-all duration-150 hover:-translate-y-0.5 hover:shadow-hover`}
    >
      <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-white ${c.icon}`}>
        {icon}
      </div>
      <div>
        <p className={`text-xs font-bold ${c.label}`}>{label}</p>
        <p className={`text-[11px] mt-0.5 ${c.sub}`}>{sublabel}</p>
      </div>
    </button>
  )
}
