import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  RadarChart, PolarGrid, PolarAngleAxis, Radar,
  ResponsiveContainer, Tooltip,
} from 'recharts'
import {
  Heart, AlertOctagon, TrendingUp, TrendingDown,
  Sparkles, Brain, Target, Lightbulb,
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

const ZONE_META: Record<string, { emoji: string; from: string; to: string; light: string }> = {
  communication: { emoji: '💬', from: '#2C5678', to: '#385C8A', light: '#DDEAF5' },
  trust:         { emoji: '🤝', from: '#286250', to: '#385C8A', light: '#D8EDE7' },
  intimacy:      { emoji: '❤️', from: '#74364A', to: '#3C3888', light: '#EEE0E6' },
  conflict:      { emoji: '⚡', from: '#744E26', to: '#885040', light: '#EEE2D4' },
  values:        { emoji: '🌟', from: '#463E80', to: '#3C3888', light: '#E4E0F5' },
  future:        { emoji: '🔮', from: '#386858', to: '#385C8A', light: '#E2EDE8' },
}
const DEFAULT_ZONE = { emoji: '○', from: '#3C3888', to: '#385C8A', light: '#EDEAF8' }

const CRISIS_VARIANT = {
  none:     'success' as const,
  warning:  'warning' as const,
  critical: 'danger'  as const,
}

const STATUS_VARIANT = {
  strong:    'success' as const,
  growth:    'warning' as const,
  attention: 'danger'  as const,
}

export const RelationshipIndexPage = () => {
  const navigate = useNavigate()
  const { t, i18n } = useTranslation(['index', 'common'])

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: result, isLoading } = useQuery({
    queryKey: ['analytics', 'latest'],
    queryFn: AnalyticsService.getLatest,
    enabled: me?.couple?.status === 'active',
    retry: false,
  })
  const { data: insight } = useQuery({
    queryKey: ['analytics', 'insight'],
    queryFn: AnalyticsService.getInsight,
    enabled: me?.couple?.status === 'active' && !!result,
    retry: false,
  })
  const { data: listData } = useQuery({
    queryKey: ['analytics', 'list'],
    queryFn: AnalyticsService.list,
    enabled: me?.couple?.status === 'active',
    retry: false,
  })
  const currLevelN = listData?.results?.[0]?.level_number as number | undefined
  const prevResultId = (listData?.results as any[])?.find(
    (r: any, i: number) => i > 0 && r.level_number !== currLevelN
  )?.id as string | undefined
  const { data: prevResult } = useQuery({
    queryKey: ['analytics', prevResultId],
    queryFn: () => AnalyticsService.getById(prevResultId!),
    enabled: !!prevResultId,
  })

  const zoneLabel = (zone: string) => t(`common:zones.${zone}`, { defaultValue: zone })
  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  if (me?.couple?.status === 'pending') {
    return (
      <div className="p-6">
        <EmptyState
          icon={<Heart />}
          title={t('common:pending_couple_title')}
          description={t('common:invite_partner_first')}
          actionLabel={t('common:invite_partner_btn')}
          onAction={() => navigate('/app/couple')}
        />
      </div>
    )
  }

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

  const score     = result ? Math.round(result.overall_score) : 0
  const crisis    = (result?.crisis_level ?? 'none') as keyof typeof CRISIS_VARIANT
  const prevScore = historyPoints.length >= 2 ? historyPoints[historyPoints.length - 2]?.score : null
  const delta     = prevScore !== null ? score - prevScore : null

  const currLvl = result?.level_number ?? 0
  const prevLvl = prevResult?.level_number ?? 0
  const showPrevLayer = !!prevResult && prevLvl !== currLvl
  const levelLabel = (n: number) => {
    if (i18n.language === 'en') return `Level ${n}`
    if (i18n.language.startsWith('uz')) return `${n}-daraja`
    return `Уровень ${n}`
  }
  const KEY_CURR = levelLabel(currLvl)
  const KEY_PREV = levelLabel(prevLvl)

  const radarData = result?.zone_scores.map((z: any) => {
    const prevZone = prevResult?.zone_scores.find((pz: any) => pz.zone === z.zone)
    return {
      zone: zoneLabel(z.zone),
      [KEY_CURR]: Math.round(z.couple_avg),
      ...(showPrevLayer && prevZone ? { [KEY_PREV]: Math.round(prevZone.couple_avg) } : {}),
    }
  }) ?? []

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">

      {/* ── Header ──────────────────────────────────────────────── */}
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

      <div className="px-4 md:px-5 space-y-4">
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
          <>

            {/* ── Hero: score + radar ──────────────────────────── */}
            <motion.div {...fadeUp(0)}>
              <div
                className="rounded-[28px] overflow-hidden"
                style={{
                  background: 'linear-gradient(145deg, #EDEAF8 0%, #DDE8F2 55%, #D6E8E2 100%)',
                  border: '1px solid rgba(60,56,136,0.12)',
                  boxShadow: '0 8px 32px rgba(60,56,136,0.12)',
                }}
              >
                {/* Score row */}
                <div className="px-5 pt-5 flex items-start justify-between">
                  <div>
                    <div className="flex items-baseline gap-1">
                      <span className="text-6xl font-bold" style={{ color: '#3C3888', letterSpacing: '-0.04em' }}>{score}</span>
                      <span className="text-xl font-semibold text-muted/60">/ 100</span>
                    </div>
                    <p className="mt-0.5 text-[11px] text-muted">
                      {new Date(result.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'long', year: 'numeric' })}
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-1.5 mt-1">
                    <Badge variant={CRISIS_VARIANT[crisis]}>{t(`common:crisis.${crisis}`)}</Badge>
                    {delta !== null && (
                      <span className={`flex items-center gap-0.5 text-xs font-semibold ${
                        delta > 0 ? 'text-success' : delta < 0 ? 'text-danger' : 'text-muted'
                      }`}>
                        {delta > 0 ? <TrendingUp size={11} /> : delta < 0 ? <TrendingDown size={11} /> : null}
                        {delta > 0 ? '+' : ''}{delta} {t('from_last_session')}
                      </span>
                    )}
                  </div>
                </div>

                {/* Radar chart */}
                <ResponsiveContainer width="100%" height={230}>
                  <RadarChart data={radarData} margin={{ top: 8, right: 28, bottom: 8, left: 28 }}>
                    <PolarGrid stroke="rgba(60,56,136,0.12)" />
                    <PolarAngleAxis dataKey="zone" tick={{ fill: '#68647C', fontSize: 10 }} />
                    {showPrevLayer && (
                      <Radar
                        name={KEY_PREV}
                        dataKey={KEY_PREV}
                        stroke="#5B8DB8"
                        fill="#5B8DB8"
                        fillOpacity={0.12}
                        strokeWidth={1.5}
                        strokeDasharray="4 3"
                        dot={{ fill: '#5B8DB8', r: 2.5, strokeWidth: 0 } as any}
                      />
                    )}
                    <Radar
                      name={KEY_CURR}
                      dataKey={KEY_CURR}
                      stroke="#3C3888"
                      fill="#3C3888"
                      fillOpacity={0.22}
                      strokeWidth={2}
                      dot={{ fill: '#3C3888', r: 3, strokeWidth: 0 } as any}
                    />
                    <Tooltip
                      formatter={(v: number) => [`${v}%`]}
                      contentStyle={{
                        borderRadius: 14,
                        border: '1px solid rgba(232,227,218,0.8)',
                        boxShadow: '0 8px 24px rgba(23,21,42,0.10)',
                        fontSize: 12,
                        color: '#17152A',
                      }}
                    />
                  </RadarChart>
                </ResponsiveContainer>

                {/* Legend */}
                {showPrevLayer && (
                  <div className="flex justify-center gap-6 px-5 pb-5">
                    <div className="flex items-center gap-1.5">
                      <div className="h-2 w-6 rounded-full flex-shrink-0" style={{ background: '#5B8DB8', opacity: 0.7 }} />
                      <span className="text-xs text-muted">{KEY_PREV}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="h-2 w-6 rounded-full flex-shrink-0" style={{ background: '#3C3888' }} />
                      <span className="text-xs font-semibold" style={{ color: '#3C3888' }}>{KEY_CURR}</span>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>

            {/* ── Crisis block ─────────────────────────────────── */}
            {crisis === 'critical' && (
              <motion.div {...fadeUp(0.06)}>
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
              </motion.div>
            )}

            {/* ── Zone cards ───────────────────────────────────── */}
            <motion.div {...fadeUp(0.10)}>
              <p className="label-caps text-muted mb-3 px-1">{t('zones_label')}</p>
              <div className="space-y-2.5">
                {result.zone_scores.map((z: any, idx: number) => {
                  const meta = ZONE_META[z.zone] ?? DEFAULT_ZONE
                  const pct  = Math.round(z.couple_avg)
                  return (
                    <motion.div
                      key={z.zone}
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.35, ease, delay: 0.12 + idx * 0.05 }}
                      className="rounded-[20px] bg-white p-4"
                      style={{ border: '1px solid rgba(232,227,218,0.7)', boxShadow: '0 2px 8px rgba(23,21,42,0.04)' }}
                    >
                      <div className="flex items-center gap-3">
                        {/* Icon */}
                        <div
                          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[12px] text-xl"
                          style={{ background: meta.light }}
                        >
                          {meta.emoji}
                        </div>

                        {/* Label + badge */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-sm font-bold text-ink">{zoneLabel(z.zone)}</span>
                            <div className="flex items-center gap-2 shrink-0 ml-2">
                              <Badge variant={STATUS_VARIANT[z.status as keyof typeof STATUS_VARIANT] ?? 'warning'}>
                                {t(`common:zone_status.${z.status}`)}
                              </Badge>
                              <span className="text-sm font-bold" style={{ color: meta.from }}>{pct}%</span>
                            </div>
                          </div>
                          {/* Progress bar */}
                          <div className="h-1.5 w-full rounded-full overflow-hidden bg-sand/60">
                            <motion.div
                              className="h-full rounded-full"
                              style={{ background: `linear-gradient(90deg, ${meta.from}, ${meta.to})` }}
                              initial={{ width: 0 }}
                              animate={{ width: `${pct}%` }}
                              transition={{ duration: 0.8, ease, delay: 0.15 + idx * 0.05 }}
                            />
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )
                })}
              </div>
            </motion.div>

            {/* ── AI Insight Report ────────────────────────────── */}
            {insight ? (
              <>
                {/* Block 3: AI-анализ отношений */}
                <motion.div {...fadeUp(0.36)}>
                  <div
                    className="rounded-[20px] p-5"
                    style={{
                      background: 'linear-gradient(145deg, #F0EEF9 0%, #EAF1F9 100%)',
                      border: '1px solid rgba(60,56,136,0.12)',
                      boxShadow: '0 2px 12px rgba(60,56,136,0.08)',
                    }}
                  >
                    <div className="flex items-center gap-2 mb-4">
                      <Brain size={15} className="text-primary" />
                      <p className="text-sm font-bold text-ink">{t('ai_report_label')}</p>
                    </div>

                    {/* Three summary pills */}
                    <div className="space-y-2.5 mb-4">
                      {insight.strengths_summary && (
                        <div className="rounded-[12px] px-4 py-3" style={{ background: 'rgba(56,104,88,0.08)', border: '1px solid rgba(56,104,88,0.14)' }}>
                          <p className="text-[10px] font-bold uppercase tracking-wider text-success mb-1">{t('ai_strengths_label')}</p>
                          <p className="text-xs text-ink/75 leading-relaxed">{insight.strengths_summary}</p>
                        </div>
                      )}
                      {insight.growth_summary && (
                        <div className="rounded-[12px] px-4 py-3" style={{ background: 'rgba(116,78,38,0.07)', border: '1px solid rgba(116,78,38,0.14)' }}>
                          <p className="text-[10px] font-bold uppercase tracking-wider text-warning mb-1">{t('ai_growth_label')}</p>
                          <p className="text-xs text-ink/75 leading-relaxed">{insight.growth_summary}</p>
                        </div>
                      )}
                      {insight.attention_summary && (
                        <div className="rounded-[12px] px-4 py-3" style={{ background: 'rgba(220,38,38,0.06)', border: '1px solid rgba(220,38,38,0.12)' }}>
                          <p className="text-[10px] font-bold uppercase tracking-wider text-danger mb-1">{t('ai_attention_label')}</p>
                          <p className="text-xs text-ink/75 leading-relaxed">{insight.attention_summary}</p>
                        </div>
                      )}
                    </div>

                    {/* Main analysis */}
                    {insight.ai_analysis && (
                      <div>
                        <p className="text-[10px] font-bold uppercase tracking-wider text-primary mb-2">{t('ai_analysis_label')}</p>
                        <p className="text-sm text-ink/80 leading-relaxed">{insight.ai_analysis}</p>
                      </div>
                    )}
                  </div>
                </motion.div>

                {/* Block 4: Следующий фокус развития */}
                {insight.next_focus && (
                  <motion.div {...fadeUp(0.40)}>
                    <div
                      className="rounded-[20px] p-5"
                      style={{
                        background: 'linear-gradient(145deg, #EAF0F9 0%, #E4EBF5 100%)',
                        border: '1px solid rgba(56,92,138,0.14)',
                      }}
                    >
                      <div className="flex items-center gap-2 mb-3">
                        <Target size={15} style={{ color: '#385C8A' }} />
                        <p className="text-sm font-bold text-ink">{t('next_focus_label')}</p>
                      </div>
                      <p className="text-sm text-ink/75 leading-relaxed">{insight.next_focus}</p>
                    </div>
                  </motion.div>
                )}

                {/* Block 5: Рекомендация AI */}
                {insight.recommendation && (
                  <motion.div {...fadeUp(0.44)}>
                    <div
                      className="rounded-[20px] p-5"
                      style={{
                        background: 'linear-gradient(145deg, #FDFCFF 0%, #F5F3FB 100%)',
                        border: '1px solid rgba(60,56,136,0.12)',
                        boxShadow: '0 2px 8px rgba(23,21,42,0.04)',
                      }}
                    >
                      <div className="flex items-center gap-2 mb-3">
                        <Lightbulb size={15} className="text-primary" />
                        <p className="text-sm font-bold text-ink">{t('recommendation_label')}</p>
                      </div>
                      <p className="text-sm text-ink/80 leading-relaxed">{insight.recommendation}</p>
                    </div>
                  </motion.div>
                )}
              </>
            ) : result && (
              <motion.div {...fadeUp(0.36)}>
                <div
                  className="rounded-[20px] px-5 py-4 flex items-center gap-3"
                  style={{ background: '#F5F3FB', border: '1px solid rgba(60,56,136,0.10)' }}
                >
                  <Brain size={16} className="text-primary/50 shrink-0" />
                  <p className="text-sm text-muted">{t('ai_generating')}</p>
                </div>
              </motion.div>
            )}

            {/* ── Key insights ─────────────────────────────────── */}
            {result.key_insights?.length > 0 && (
              <motion.div {...fadeUp(0.42)}>
                <div
                  className="rounded-[20px] bg-white p-5"
                  style={{ border: '1px solid rgba(232,227,218,0.7)', boxShadow: '0 2px 8px rgba(23,21,42,0.04)' }}
                >
                  <div className="flex items-center gap-2 mb-3">
                    <Sparkles size={15} className="text-primary" />
                    <p className="text-sm font-bold text-ink">{t('key_insights_label')}</p>
                  </div>
                  <ul className="flex flex-col gap-2.5">
                    {result.key_insights.map((kInsight: string, i: number) => (
                      <li key={i} className="flex gap-2.5 text-sm text-ink/80 leading-relaxed">
                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                        {kInsight}
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            )}

            {/* ── Common ground (safe part of bridge_analysis) ─── */}
            {result.bridge_analysis?.common_ground && (
              <motion.div {...fadeUp(0.44)}>
                <div
                  className="rounded-[20px] p-5"
                  style={{
                    background: 'linear-gradient(145deg, #E2EDE8 0%, #DDE8F2 100%)',
                    border: '1px solid rgba(56,104,88,0.15)',
                  }}
                >
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-lg">🌿</span>
                    <p className="text-sm font-bold text-ink">{t('common_ground_label')}</p>
                  </div>
                  <p className="text-sm text-ink/75 leading-relaxed">{result.bridge_analysis.common_ground}</p>
                  {result.bridge_analysis.first_step && (
                    <div
                      className="mt-3 rounded-[12px] px-4 py-3"
                      style={{ background: 'rgba(56,104,88,0.10)', border: '1px solid rgba(56,104,88,0.15)' }}
                    >
                      <p className="text-[11px] font-bold uppercase tracking-wider text-success mb-1">{t('first_step_label')}</p>
                      <p className="text-xs text-ink/70 leading-relaxed">{result.bridge_analysis.first_step}</p>
                    </div>
                  )}
                </div>
              </motion.div>
            )}

            {/* ── Strengths ────────────────────────────────────── */}
            {result.strengths_summary && (
              <motion.div {...fadeUp(0.50)}>
                <div
                  className="rounded-[20px] p-5"
                  style={{
                    background: 'linear-gradient(145deg, #F5F3FB 0%, #EFF4FB 100%)',
                    border: '1px solid rgba(60,56,136,0.10)',
                  }}
                >
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-lg">💪</span>
                    <p className="text-sm font-bold text-ink">{result.strengths_summary.headline}</p>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {result.strengths_summary.strengths.map((s: string, i: number) => (
                      <Badge key={i} variant="success">{s}</Badge>
                    ))}
                  </div>
                  {result.strengths_summary.encouragement && (
                    <p className="text-xs text-muted leading-relaxed">{result.strengths_summary.encouragement}</p>
                  )}
                </div>
              </motion.div>
            )}

            {/* ── Problem chain ────────────────────────────────── */}
            {result.problem_chain && result.problem_chain.length > 0 && (
              <motion.div {...fadeUp(0.54)}>
                <p className="label-caps text-muted mb-3 px-1">{t('problem_chain_label')}</p>
                <div
                  className="rounded-[20px] bg-white p-4"
                  style={{ border: '1px solid rgba(232,227,218,0.7)', boxShadow: '0 2px 8px rgba(23,21,42,0.04)' }}
                >
                  <div className="space-y-3">
                    {result.problem_chain.map((item: any, idx: number) => (
                      <div key={idx} className="flex gap-3">
                        <div
                          className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold text-white mt-0.5"
                          style={{ background: 'linear-gradient(135deg, #3C3888, #385C8A)' }}
                        >
                          {item.step}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-ink">{item.problem}</p>
                          {item.description && (
                            <p className="text-xs text-muted mt-0.5 leading-relaxed">{item.description}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* ── Actions ──────────────────────────────────────── */}
            <motion.div {...fadeUp(0.62)} className="pb-2">
              <Button fullWidth onClick={() => navigate('/app/practices')}>
                <Sparkles size={14} /> {t('to_plan_btn')}
              </Button>
            </motion.div>

          </>
        )}
      </div>
    </div>
  )
}
