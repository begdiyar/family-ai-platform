import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  RadialBarChart, RadialBar, ResponsiveContainer,
  LineChart, Line, XAxis, YAxis, Tooltip,
} from 'recharts'
import {
  Heart, AlertOctagon, TrendingUp, TrendingDown, ArrowRight,
  Sparkles, AlertCircle, ArrowLeftRight,
} from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { AnalyticsService } from '@/services/analytics.service'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { EmptyState } from '@/components/feedback/EmptyState'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease, delay },
})

const ZONE_COLORS: Record<string, { from: string; to: string; light: string }> = {
  communication: { from: '#2C5678', to: '#385C8A', light: '#DDEAF5' },
  trust:         { from: '#286250', to: '#385C8A', light: '#D8EDE7' },
  intimacy:      { from: '#74364A', to: '#3C3888', light: '#EEE0E6' },
  conflict:      { from: '#744E26', to: '#885040', light: '#EEE2D4' },
  values:        { from: '#463E80', to: '#3C3888', light: '#E4E0F5' },
  future:        { from: '#386858', to: '#385C8A', light: '#E2EDE8' },
}
const DEFAULT_ZONE = { from: '#3C3888', to: '#385C8A', light: '#EDEAF8' }

const ZONE_GRADIENTS: Record<string, [string, string]> = {
  communication: ['#2C5678', '#385C8A'],
  trust:         ['#286250', '#385C8A'],
  intimacy:      ['#74364A', '#3C3888'],
  conflict:      ['#744E26', '#885040'],
  values:        ['#463E80', '#3C3888'],
  future:        ['#386858', '#385C8A'],
}

const CRISIS_VARIANT = {
  none:     'success' as const,
  warning:  'warning' as const,
  critical: 'danger'  as const,
}

type Tab = 'index' | 'bridge'

export const RelationshipIndexPage = () => {
  const navigate = useNavigate()
  const [tab, setTab] = useState<Tab>('index')
  const { t, i18n } = useTranslation(['index', 'common'])

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const { data: result, isLoading } = useQuery({
    queryKey: ['analytics', 'latest'],
    queryFn: AnalyticsService.getLatest,
    enabled: !!me?.couple,
    retry: false,
  })

  const { data: listData } = useQuery({
    queryKey: ['analytics', 'list'],
    queryFn: AnalyticsService.list,
    enabled: !!me?.couple,
    retry: false,
  })

  const zoneLabel = (zone: string) => t(`common:zones.${zone}`, { defaultValue: zone })
  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  if (!me?.couple) {
    return (
      <div className="p-6">
        <EmptyState icon={<Heart />} title={t('no_couple_title')} description={t('no_couple_desc')} />
      </div>
    )
  }

  const historyPoints = listData?.results
    ? [...listData.results].reverse().map((r: any, i: number) => ({
        name: `#${i + 1}`,
        score: Math.round(r.overall_score),
        date: new Date(r.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'short' }),
      }))
    : []

  const score = result ? Math.round(result.overall_score) : 0
  const crisis = (result?.crisis_level ?? 'none') as keyof typeof CRISIS_VARIANT
  const crisisVariant = CRISIS_VARIANT[crisis]
  const prevScore = historyPoints.length >= 2 ? historyPoints[historyPoints.length - 2]?.score : null
  const delta = prevScore !== null ? score - prevScore : null
  const radialData = [{ name: 'score', value: score, fill: 'url(#radGrad)' }]

  const TabBar = () => (
    <div className="mx-5 mb-4 flex rounded-2xl p-1" style={{ background: 'rgba(60,56,136,0.08)' }}>
      {([
        { key: 'index',  icon: Heart,          label: t('tab_index') },
        { key: 'bridge', icon: ArrowLeftRight, label: t('tab_bridge') },
      ] as const).map(({ key, icon: Icon, label }) => (
        <button
          key={key}
          onClick={() => setTab(key)}
          className="flex flex-1 items-center justify-center gap-1.5 rounded-[14px] py-2 text-sm font-semibold transition-all duration-200"
          style={
            tab === key
              ? { background: 'white', color: '#3C3888', boxShadow: '0 1px 4px rgba(60,56,136,0.18)' }
              : { color: '#68647C' }
          }
        >
          <Icon size={13} />
          {label}
        </button>
      ))}
    </div>
  )

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <div className="page-hero px-5 pt-6 pb-4">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-brand shadow-[0_4px_12px_rgba(60,56,136,0.28)]">
            <Heart size={16} className="text-white" fill="white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
            <p className="text-xs text-muted mt-0.5">{t('subtitle')}</p>
          </div>
        </div>
      </div>

      <TabBar />

      <div className="px-4 md:px-5">
        {isLoading ? (
          <div className="flex flex-col gap-4">
            {[...Array(4)].map((_, i) => <div key={i} className="h-32 rounded-card shimmer" />)}
          </div>
        ) : !result ? (
          <EmptyState
            icon={<Heart />}
            title={t('empty_title')}
            description={t('empty_desc')}
            actionLabel={t('empty_btn')}
            onAction={() => navigate('/app/diagnostics')}
          />
        ) : (
          <AnimatePresence mode="wait">
            {tab === 'index' ? (
              <motion.div
                key="index"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 10 }}
                transition={{ duration: 0.22, ease }}
                className="space-y-4"
              >
                {/* Hero score card */}
                <div
                  className="relative overflow-hidden rounded-[28px] p-6"
                  style={{
                    background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)',
                    border: '1px solid rgba(60,56,136,0.12)',
                    boxShadow: '0 4px 24px rgba(60,56,136,0.10)',
                  }}
                >
                  <div className="absolute -top-12 -right-12 h-40 w-40 rounded-full bg-primary/8 blur-3xl pointer-events-none" />
                  <div className="absolute -bottom-10 -left-8 h-32 w-32 rounded-full bg-violet/8 blur-2xl pointer-events-none" />

                  <div className="relative flex items-center gap-5">
                    <div className="relative flex-shrink-0" style={{ width: 110, height: 110 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <RadialBarChart
                          innerRadius="72%" outerRadius="100%"
                          data={radialData}
                          startAngle={90}
                          endAngle={90 - 360 * (score / 100)}
                        >
                          <defs>
                            <linearGradient id="radGrad" x1="0" y1="0" x2="1" y2="1">
                              <stop offset="0%" stopColor="#3C3888" />
                              <stop offset="100%" stopColor="#385C8A" />
                            </linearGradient>
                          </defs>
                          <RadialBar dataKey="value" cornerRadius={10} background={{ fill: 'rgba(60,56,136,0.10)' }} />
                        </RadialBarChart>
                      </ResponsiveContainer>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-2xl font-bold text-ink" style={{ letterSpacing: '-0.03em' }}>{score}</span>
                      </div>
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-baseline gap-1 mb-2">
                        <span className="font-display text-5xl text-ink">{score}</span>
                        <span className="text-xl font-semibold text-muted/60 mb-1">/ 100</span>
                      </div>
                      <Badge variant={crisisVariant}>{t(`common:crisis.${crisis}`)}</Badge>
                      {delta !== null && (
                        <div className={`mt-2 flex items-center gap-1 text-xs font-semibold ${
                          delta > 0 ? 'text-sage-700' : delta < 0 ? 'text-danger' : 'text-muted'
                        }`}>
                          {delta > 0 ? <TrendingUp size={12} /> : delta < 0 ? <TrendingDown size={12} /> : null}
                          {delta > 0 ? '+' : ''}{delta} {t('from_last_session')}
                        </div>
                      )}
                      <p className="mt-2 text-[11px] text-muted/70">
                        {new Date(result.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'long', year: 'numeric' })}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Crisis block */}
                {crisis === 'critical' && (
                  <div className="rounded-[20px] border border-rose-200 bg-rose-50 px-5 py-4">
                    <div className="flex items-start gap-3 mb-3">
                      <AlertOctagon size={18} className="shrink-0 text-rose-600 mt-0.5" />
                      <div>
                        <p className="font-bold text-rose-800 text-sm">{t('crisis_critical_title')}</p>
                        <p className="mt-0.5 text-xs text-rose-600 leading-relaxed">{t('crisis_critical_desc')}</p>
                      </div>
                    </div>
                    <div className="flex gap-2 ml-7">
                      <Button size="sm" variant="danger" onClick={() => navigate('/app/practices')}>{t('open_plan_btn')}</Button>
                      <Button size="sm" variant="ghost" onClick={() => navigate('/app/mediation')}>{t('mediator_btn')}</Button>
                    </div>
                  </div>
                )}

                {/* Zone cards */}
                <div>
                  <p className="label-caps text-muted mb-3 px-1">{t('zones_label')}</p>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {result.zone_scores.map((z: any, idx: number) => {
                      const [c1, c2] = ZONE_GRADIENTS[z.zone] ?? ['#3C3888', '#385C8A']
                      const statusVariant = z.status === 'strong'
                        ? 'success' : z.status === 'attention' ? 'danger' : 'warning'
                      const pct = Math.round(z.couple_avg)
                      return (
                        <motion.div
                          key={z.zone}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.35, ease, delay: 0.06 + idx * 0.04 }}
                          className="rounded-[20px] bg-canvas p-4 border border-sand/60"
                          style={{ boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 4px 12px rgba(23,21,42,0.04)' }}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm font-semibold text-ink">{zoneLabel(z.zone)}</span>
                            <Badge variant={statusVariant}>{pct}%</Badge>
                          </div>
                          <div className="h-2 w-full rounded-full overflow-hidden bg-sand/60">
                            <div
                              className="h-full rounded-full transition-all duration-700"
                              style={{ width: `${pct}%`, background: `linear-gradient(90deg, ${c1}, ${c2})` }}
                            />
                          </div>
                          {z.gap > 15 && (
                            <p className="mt-2 text-[11px] font-medium text-warning">
                              {t('gap_bridge_hint', { gap: Math.round(z.gap) })}
                            </p>
                          )}
                        </motion.div>
                      )
                    })}
                  </div>
                </div>

                {/* Strengths */}
                {result.strengths_summary && (
                  <div
                    className="rounded-[20px] p-5"
                    style={{
                      background: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)',
                      border: '1px solid rgba(56,104,88,0.15)',
                    }}
                  >
                    <p className="font-bold text-ink mb-3">
                      <span className="mr-2">💪</span>
                      {result.strengths_summary.headline}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {result.strengths_summary.strengths.map((s: string, i: number) => (
                        <Badge key={i} variant="success">{s}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* History chart */}
                {historyPoints.length > 1 && (
                  <div
                    className="rounded-[20px] bg-canvas p-5 border border-sand/60"
                    style={{ boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)' }}
                  >
                    <div className="flex items-center gap-2 mb-4">
                      <TrendingUp size={15} className="text-primary" />
                      <h2 className="font-bold text-ink text-sm">{t('history_label')}</h2>
                      <span className="ml-auto text-xs text-muted">{historyPoints.length} {t('common:sessions', { defaultValue: 'сессий' })}</span>
                    </div>
                    <ResponsiveContainer width="100%" height={130}>
                      <LineChart data={historyPoints} margin={{ left: -16, right: 4 }}>
                        <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#68647C' }} axisLine={false} tickLine={false} />
                        <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: '#68647C' }} axisLine={false} tickLine={false} width={28} />
                        <Tooltip
                          formatter={(v: number) => [`${v}%`, t('tooltip_index')]}
                          contentStyle={{
                            borderRadius: 16,
                            border: '1px solid rgba(232,227,218,0.8)',
                            boxShadow: '0 8px 24px rgba(23,21,42,0.10)',
                            fontSize: 12, color: '#17152A',
                          }}
                        />
                        <defs>
                          <linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
                            <stop offset="0%" stopColor="#3C3888" />
                            <stop offset="100%" stopColor="#385C8A" />
                          </linearGradient>
                        </defs>
                        <Line type="monotone" dataKey="score" stroke="url(#lineGrad)" strokeWidth={2.5}
                          dot={{ fill: '#3C3888', r: 4, strokeWidth: 0 }}
                          activeDot={{ r: 6, fill: '#385C8A', strokeWidth: 0 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-3 pb-2">
                  <Button variant="secondary" fullWidth onClick={() => navigate(`/app/analytics/${result.id}`)}>
                    <ArrowRight size={14} /> {t('detail_report_btn')}
                  </Button>
                  <Button fullWidth onClick={() => navigate('/app/practices')}>
                    <Sparkles size={14} /> {t('to_plan_btn')}
                  </Button>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="bridge"
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.22, ease }}
                className="space-y-4"
              >
                {/* Bridge summary */}
                <div
                  className="rounded-[22px] p-5 bg-canvas"
                  style={{ border: '1px solid rgba(60,56,136,0.12)', boxShadow: '0 4px 20px rgba(60,56,136,0.08)' }}
                >
                  <div className="flex items-center gap-3 mb-4">
                    <Sparkles size={16} className="text-primary" />
                    <h2 className="font-bold text-ink text-sm">{t('bridge_total_label')}</h2>
                    <span className="ml-auto text-2xl font-bold" style={{ color: '#3C3888', letterSpacing: '-0.03em' }}>
                      {score}
                    </span>
                    <span className="text-sm text-muted">/ 100</span>
                  </div>
                  <div className="relative h-3 rounded-full overflow-hidden bg-sand/60">
                    <motion.div
                      className="absolute inset-y-0 left-0 rounded-full"
                      style={{ background: 'linear-gradient(90deg, #3C3888, #385C8A, #386858)' }}
                      initial={{ width: 0 }}
                      animate={{ width: `${score}%` }}
                      transition={{ duration: 1, ease, delay: 0.15 }}
                    />
                  </div>
                  <div className="mt-3 flex items-center justify-between text-xs text-muted">
                    <span>{t('gap_label')}</span>
                    <span>{t('unity_label')}</span>
                  </div>
                </div>

                {/* Zone bridges */}
                <div>
                  <p className="label-caps text-muted mb-3 px-1">{t('zones_comparison')}</p>
                  <div className="space-y-3">
                    {result.zone_scores.map((z: any, idx: number) => {
                      const colors = ZONE_COLORS[z.zone] ?? DEFAULT_ZONE
                      const myScore = Math.round(z.my_score ?? z.couple_avg)
                      const partnerScore = Math.round(z.partner_score ?? z.couple_avg)
                      const gap = Math.abs(myScore - partnerScore)
                      const hasGap = gap > 15
                      return (
                        <motion.div
                          key={z.zone}
                          initial={{ opacity: 0, y: 8 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.35, ease, delay: 0.06 + idx * 0.05 }}
                          className="rounded-[20px] bg-canvas p-4"
                          style={{
                            border: hasGap ? '1px solid rgba(184,144,74,0.25)' : '1px solid rgba(232,227,218,0.6)',
                            boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 4px 12px rgba(23,21,42,0.04)',
                          }}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm font-semibold text-ink">{zoneLabel(z.zone)}</span>
                            {hasGap && (
                              <div className="flex items-center gap-1 text-xs font-medium text-warning">
                                <AlertCircle size={12} />
                                {t('gap_warning', { gap })}
                              </div>
                            )}
                          </div>
                          <div className="space-y-2">
                            <div>
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[10px] font-semibold text-muted uppercase tracking-wider">{t('you_label')}</span>
                                <span className="text-[10px] font-bold" style={{ color: colors.from }}>{myScore}%</span>
                              </div>
                              <div className="h-2 rounded-full overflow-hidden bg-sand/60">
                                <motion.div
                                  className="h-full rounded-full"
                                  style={{ background: `linear-gradient(90deg, ${colors.from}, ${colors.to})` }}
                                  initial={{ width: 0 }}
                                  animate={{ width: `${myScore}%` }}
                                  transition={{ duration: 0.7, ease, delay: 0.1 + idx * 0.05 }}
                                />
                              </div>
                            </div>
                            <div>
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[10px] font-semibold text-muted uppercase tracking-wider">{t('common:partner')}</span>
                                <span className="text-[10px] font-bold" style={{ color: colors.to }}>{partnerScore}%</span>
                              </div>
                              <div className="h-2 rounded-full overflow-hidden bg-sand/60">
                                <motion.div
                                  className="h-full rounded-full opacity-70"
                                  style={{ background: `linear-gradient(90deg, ${colors.to}, ${colors.from})` }}
                                  initial={{ width: 0 }}
                                  animate={{ width: `${partnerScore}%` }}
                                  transition={{ duration: 0.7, ease, delay: 0.15 + idx * 0.05 }}
                                />
                              </div>
                            </div>
                          </div>
                          {hasGap && (
                            <div
                              className="mt-3 rounded-[10px] px-3 py-2 text-xs text-warning font-medium"
                              style={{ background: '#FDF4E8' }}
                            >
                              {t('gap_discuss')}
                            </div>
                          )}
                        </motion.div>
                      )
                    })}
                  </div>
                </div>

                {/* Strengths */}
                {result.strengths_summary && (
                  <div
                    className="rounded-[20px] p-5"
                    style={{ background: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)', border: '1px solid rgba(56,104,88,0.15)' }}
                  >
                    <p className="font-bold text-ink mb-1">
                      <span className="mr-2">🤝</span>
                      {result.strengths_summary.headline}
                    </p>
                    <p className="text-xs text-muted leading-relaxed mt-1">{t('common_ground_note')}</p>
                  </div>
                )}

                {/* CTA */}
                <div className="flex gap-3 pb-2">
                  <Button variant="secondary" fullWidth onClick={() => navigate('/app/ai')}>
                    <Sparkles size={14} /> {t('discuss_ai_btn')}
                  </Button>
                  <Button fullWidth onClick={() => navigate('/app/mediation')}>
                    {t('open_mediator_btn')}
                  </Button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        )}
      </div>
    </div>
  )
}
