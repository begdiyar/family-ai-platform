import { useQuery } from '@tanstack/react-query'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from 'recharts'
import { ChevronLeft, AlertOctagon, AlertTriangle, Sparkles } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AnalyticsService } from '@/services/analytics.service'
import { AuthService } from '@/services/auth.service'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import type { ZoneScoreDetail } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.38, ease, delay },
})

const STATUS_BADGE: Record<ZoneScoreDetail['status'], 'success' | 'warning' | 'danger'> = {
  strong: 'success',
  growth: 'warning',
  attention: 'danger',
}

export const AnalyticsDetailPage = () => {
  const { resultId } = useParams<{ resultId: string }>()
  const navigate = useNavigate()
  const { t, i18n } = useTranslation(['analytics', 'common'])

  const { data: result, isLoading } = useQuery({
    queryKey: ['analytics', resultId],
    queryFn: () => (resultId === 'latest' ? AnalyticsService.getLatest() : AnalyticsService.getById(resultId!)),
  })

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const zoneLabel = (zone: string) => t(`common:zones.${zone}`, { defaultValue: zone })
  const zoneStatusLabel = (status: string) => t(`common:zone_status.${status}`, { defaultValue: status })
  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="page-hero px-5 pt-6 pb-5">
          <div className="h-7 w-48 rounded-xl shimmer" />
        </div>
        <div className="px-4 pt-4 space-y-4 md:px-5">
          {[...Array(4)].map((_, i) => <div key={i} className="h-28 rounded-card shimmer" />)}
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="flex min-h-full items-center justify-center p-6">
        <p className="text-muted text-sm">{t('not_found')}</p>
      </div>
    )
  }

  const myName = me?.first_name || t('common:you')
  const partnerName = me?.couple?.partner?.first_name || t('common:partner')

  const radarData = result.zone_scores.map((z) => ({
    zone: zoneLabel(z.zone),
    [myName]: z.partner_a.percent,
    [partnerName]: z.partner_b.percent,
  }))

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <div className="page-hero px-5 pt-6 pb-5">
        <button
          onClick={() => navigate('/app/analytics')}
          className="mb-3 flex items-center gap-1 text-sm font-medium text-muted hover:text-primary transition-colors"
        >
          <ChevronLeft size={16} /> {t('back_btn')}
        </button>
        <div>
          <h1 className="text-xl font-bold text-ink">{t('detail_title')}</h1>
          <p className="text-xs text-muted mt-0.5">
            {new Date(result.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'long', year: 'numeric' })}
          </p>
        </div>
      </div>

      <div className="px-4 pt-4 md:px-5 space-y-4">

        {result.crisis_level === 'critical' && (
          <motion.div {...fadeUp(0)}>
            <div className="rounded-[20px] border border-rose-200 bg-rose-50 px-5 py-4">
              <div className="flex gap-3">
                <AlertOctagon size={18} className="shrink-0 text-rose-600 mt-0.5" />
                <div>
                  <p className="font-bold text-rose-800 text-sm">{t('crisis_critical_title')}</p>
                  <p className="mt-0.5 text-xs text-rose-600 leading-relaxed">{t('crisis_critical_desc')}</p>
                </div>
              </div>
            </div>
          </motion.div>
        )}
        {result.crisis_level === 'warning' && (
          <motion.div {...fadeUp(0)}>
            <div className="rounded-[20px] border border-amber-200 bg-amber-50 px-5 py-4">
              <div className="flex gap-3">
                <AlertTriangle size={18} className="shrink-0 text-amber-600 mt-0.5" />
                <div>
                  <p className="font-bold text-amber-800 text-sm">{t('crisis_warning_title')}</p>
                  <p className="mt-0.5 text-xs text-amber-600 leading-relaxed">{t('crisis_warning_desc')}</p>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        <motion.div {...fadeUp(0.04)}>
          <div
            className="rounded-[22px] p-6 text-center"
            style={{
              background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)',
              border: '1px solid rgba(60,56,136,0.12)',
            }}
          >
            <p className="text-xs text-muted mb-2">{t('detail_score_label')}</p>
            <div className="flex items-baseline justify-center gap-1">
              <span className="text-6xl font-bold text-ink" style={{ letterSpacing: '-0.04em', color: '#3C3888' }}>
                {Math.round(result.overall_score)}
              </span>
              <span className="text-xl font-semibold text-muted/60">/ 100</span>
            </div>
            <div className="mt-4 mx-auto max-w-xs h-2 rounded-full overflow-hidden __BGWHITE_ALPHA___">
              <motion.div
                className="h-full rounded-full"
                style={{ background: 'linear-gradient(90deg, #3C3888, #385C8A)' }}
                initial={{ width: 0 }}
                animate={{ width: `${result.overall_score}%` }}
                transition={{ duration: 0.9, ease, delay: 0.1 }}
              />
            </div>
          </div>
        </motion.div>

        <motion.div {...fadeUp(0.08)}>
          <div
            className="rounded-[22px] bg-canvas p-5"
            style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)' }}
          >
            <h2 className="mb-4 text-sm font-bold text-ink">{t('radar_title')}</h2>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(232,227,218,0.8)" />
                <PolarAngleAxis dataKey="zone" tick={{ fill: '#68647C', fontSize: 11 }} />
                <Radar name={myName} dataKey={myName} stroke="#3C3888" fill="#3C3888" fillOpacity={0.18} strokeWidth={2} />
                <Radar name={partnerName} dataKey={partnerName} stroke="#885040" fill="#885040" fillOpacity={0.15} strokeWidth={2} />
                <Tooltip
                  formatter={(value: number) => [`${Math.round(value)}%`]}
                  contentStyle={{
                    borderRadius: 16,
                    border: '1px solid rgba(232,227,218,0.8)',
                    boxShadow: '0 8px 24px rgba(23,21,42,0.10)',
                    fontSize: 12,
                    color: '#17152A',
                  }}
                />
                <Legend wrapperStyle={{ fontSize: 12, color: '#68647C' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div {...fadeUp(0.12)}>
          <p className="label-caps text-muted mb-3 px-1">{t('detail_zones')}</p>
          <div className="flex flex-col gap-3">
            {result.zone_scores.map((z, idx) => (
              <motion.div
                key={z.zone}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.32, ease, delay: 0.14 + idx * 0.04 }}
                className="rounded-[20px] bg-canvas p-4"
                style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
              >
                <div className="mb-3 flex items-center justify-between">
                  <span className="font-semibold text-sm text-ink">{zoneLabel(z.zone)}</span>
                  <Badge variant={STATUS_BADGE[z.status]}>{zoneStatusLabel(z.status)}</Badge>
                </div>
                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-3">
                    <span className="w-20 text-xs text-muted shrink-0">{myName}</span>
                    <div className="flex-1 h-1.5 rounded-full overflow-hidden bg-sand/60">
                      <div className="h-full rounded-full" style={{ width: `${z.partner_a.percent}%`, background: 'linear-gradient(90deg, #3C3888, #385C8A)' }} />
                    </div>
                    <span className="w-9 text-right text-xs font-semibold text-ink">{Math.round(z.partner_a.percent)}%</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="w-20 text-xs text-muted shrink-0">{partnerName}</span>
                    <div className="flex-1 h-1.5 rounded-full overflow-hidden bg-sand/60">
                      <div className="h-full rounded-full" style={{ width: `${z.partner_b.percent}%`, background: 'linear-gradient(90deg, #885040, #3C3888)' }} />
                    </div>
                    <span className="w-9 text-right text-xs font-semibold text-ink">{Math.round(z.partner_b.percent)}%</span>
                  </div>
                  {z.gap > 15 && (
                    <p className="mt-1 text-xs font-medium text-warning">
                      {t('gap_discuss', { gap: Math.round(z.gap) })}
                    </p>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {result.key_insights?.length > 0 && (
          <motion.div {...fadeUp(0.18)}>
            <div
              className="rounded-[20px] bg-canvas p-5"
              style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
            >
              <div className="flex items-center gap-2 mb-3">
                <Sparkles size={15} className="text-primary" />
                <h2 className="font-bold text-ink text-sm">{t('detail_insights')}</h2>
              </div>
              <ul className="flex flex-col gap-2.5">
                {result.key_insights.map((insight, i) => (
                  <li key={i} className="flex gap-2.5 text-sm text-ink leading-relaxed">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    {insight}
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}

        {(result.strengths?.length > 0 || result.attention_zones?.length > 0) && (
          <motion.div {...fadeUp(0.20)} className="grid grid-cols-2 gap-3">
            {result.strengths?.length > 0 && (
              <div
                className="rounded-[20px] p-4"
                style={{ background: 'linear-gradient(135deg, #E2EDE8 0%, #D2DDF0 100%)', border: '1px solid rgba(56,104,88,0.15)' }}
              >
                <p className="label-caps text-success mb-2">{t('detail_strong')}</p>
                <ul className="flex flex-col gap-1">
                  {result.strengths.map((z) => (
                    <li key={z} className="text-xs font-medium text-ink">{zoneLabel(z)}</li>
                  ))}
                </ul>
              </div>
            )}
            {result.attention_zones?.length > 0 && (
              <div
                className="rounded-[20px] p-4"
                style={{ background: 'linear-gradient(135deg, #FDF4E8 0%, #EDEAF8 100%)', border: '1px solid rgba(184,144,74,0.15)' }}
              >
                <p className="label-caps text-warning mb-2">{t('detail_attention')}</p>
                <ul className="flex flex-col gap-1">
                  {result.attention_zones.map((z) => (
                    <li key={z} className="text-xs font-medium text-ink">{zoneLabel(z)}</li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}

        {result.bridge_analysis && (
          <motion.div {...fadeUp(0.22)}>
            <div
              className="rounded-[22px] p-5"
              style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)', border: '1px solid rgba(60,56,136,0.12)' }}
            >
              <h2 className="mb-4 text-sm font-bold text-ink">{t('detail_bridge')}</h2>
              <div className="grid gap-3 sm:grid-cols-2 mb-3">
                <div className="rounded-[14px] p-3" style={{ background: 'rgba(255,255,255,0.75)' }}>
                  <p className="label-caps text-violet mb-1">{myName} {t('perceives')}</p>
                  <p className="text-sm text-ink leading-relaxed">{result.bridge_analysis.partner_a_perspective}</p>
                </div>
                <div className="rounded-[14px] p-3" style={{ background: 'rgba(255,255,255,0.75)' }}>
                  <p className="label-caps text-accent mb-1">{partnerName} {t('perceives')}</p>
                  <p className="text-sm text-ink leading-relaxed">{result.bridge_analysis.partner_b_perspective}</p>
                </div>
              </div>
              <div className="rounded-[14px] p-3 mb-3" style={{ background: 'rgba(255,255,255,0.70)' }}>
                <p className="label-caps text-success mb-1">{t('common_ground')}</p>
                <p className="text-sm text-ink leading-relaxed">{result.bridge_analysis.common_ground}</p>
              </div>
              <div className="rounded-[14px] p-3 mb-3" style={{ background: 'rgba(255,255,255,0.70)' }}>
                <p className="label-caps text-warning mb-1">{t('key_misunderstanding')}</p>
                <p className="text-sm text-ink leading-relaxed">{result.bridge_analysis.key_misunderstanding}</p>
              </div>
              <div className="rounded-[14px] p-3" style={{ background: 'rgba(255,255,255,0.80)' }}>
                <p className="label-caps text-primary mb-1">{t('first_step')}</p>
                <p className="text-sm font-semibold text-ink">{result.bridge_analysis.first_step}</p>
              </div>
            </div>
          </motion.div>
        )}

        {result.strengths_summary && (
          <motion.div {...fadeUp(0.24)}>
            <div
              className="rounded-[22px] p-5"
              style={{ background: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)', border: '1px solid rgba(56,104,88,0.15)' }}
            >
              <h2 className="mb-1 font-bold text-ink">💪 {result.strengths_summary.headline}</h2>
              <p className="mb-4 text-sm text-muted">{result.strengths_summary.achievement}</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {result.strengths_summary.strengths.map((s, i) => (
                  <span
                    key={i}
                    className="rounded-full px-3 py-1 text-xs font-semibold"
                    style={{ background: 'rgba(56,104,88,0.12)', color: '#1C4438' }}
                  >
                    {s}
                  </span>
                ))}
              </div>
              <p className="text-sm text-muted italic">"{result.strengths_summary.encouragement}"</p>
            </div>
          </motion.div>
        )}

        {result.problem_chain && result.problem_chain.length > 0 && (
          <motion.div {...fadeUp(0.26)}>
            <div
              className="rounded-[22px] bg-canvas p-5"
              style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
            >
              <h2 className="mb-4 text-sm font-bold text-ink">{t('problem_chain')}</h2>
              <div className="flex flex-col gap-3">
                {result.problem_chain.map((item, i) => (
                  <div key={i} className="flex gap-3">
                    <div className="flex shrink-0 flex-col items-center">
                      <div
                        className="flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold text-white"
                        style={{ background: 'linear-gradient(135deg, #3C3888, #385C8A)' }}
                      >
                        {item.step}
                      </div>
                      {i < result.problem_chain!.length - 1 && (
                        <div className="mt-1 w-0.5 flex-1 bg-sand min-h-[16px]" />
                      )}
                    </div>
                    <div className="pb-3">
                      <p className="font-semibold text-ink text-sm">{item.problem}</p>
                      <p className="text-xs text-muted mt-0.5 leading-relaxed">{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        <motion.div {...fadeUp(0.28)}>
          <Button fullWidth onClick={() => navigate('/app/plan')}>
            <Sparkles size={14} /> {t('recovery_plan_btn')}
          </Button>
        </motion.div>

      </div>
    </div>
  )
}
