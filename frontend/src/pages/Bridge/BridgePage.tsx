import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeftRight, Sparkles, TrendingUp, AlertCircle } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { AnalyticsService } from '@/services/analytics.service'
import { Button } from '@/components/ui/Button'
import { EmptyState } from '@/components/feedback/EmptyState'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 14 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease, delay },
})

const ZONE_COLORS: Record<string, { from: string; to: string; light: string }> = {
  communication: { from: '#3C3888', to: '#385C8A', light: '#EDEAF8' },
  trust:         { from: '#386858', to: '#385C8A', light: '#E2EDE8' },
  intimacy:      { from: '#885040', to: '#3C3888', light: '#EEE4DC' },
  conflict:      { from: '#886028', to: '#885040', light: '#FDF4E8' },
  values:        { from: '#385C8A', to: '#3C3888', light: '#DDE8F2' },
  future:        { from: '#386858', to: '#385C8A', light: '#E2EDE8' },
}

const DEFAULT_ZONE_COLOR = { from: '#3C3888', to: '#385C8A', light: '#EDEAF8' }

export const BridgePage = () => {
  const navigate = useNavigate()
  const { t } = useTranslation('index')
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const { data: result, isLoading } = useQuery({
    queryKey: ['analytics', 'latest'],
    queryFn: AnalyticsService.getLatest,
    enabled: !!me?.couple,
    retry: false,
  })

  if (!me?.couple) {
    return (
      <div className="min-h-full flex items-center justify-center p-6">
        <EmptyState
          icon={<ArrowLeftRight />}
          title={t('no_couple_title')}
          description={t('bridge_no_couple_desc', { defaultValue: 'Мост понимания доступен только для пары' })}
          actionLabel={t('bridge_create_btn', { defaultValue: 'Создать пару' })}
          onAction={() => navigate('/app/couple')}
        />
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {/* Premium hero header */}
      <div
        className="relative overflow-hidden px-5 pt-8 pb-8"
        style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)' }}
      >
        {/* Decorative orbs */}
        <div className="absolute -top-10 -right-10 h-40 w-40 rounded-full bg-primary/10 blur-3xl pointer-events-none" />
        <div className="absolute -bottom-8 -left-8 h-32 w-32 rounded-full bg-violet/10 blur-2xl pointer-events-none" />

        <motion.div {...fadeUp(0)} className="relative">
          <div className="flex items-center gap-3 mb-3">
            <div
              className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-brand"
              style={{ boxShadow: '0 6px 20px rgba(60,56,136,0.35)' }}
            >
              <ArrowLeftRight size={18} className="text-white" />
            </div>
            <div>
              <p className="label-caps text-primary/60">{t('bridge_feature_tag', { defaultValue: 'Ключевая функция' })}</p>
              <h1 className="text-2xl font-bold text-ink" style={{ letterSpacing: '-0.02em' }}>
                {t('tab_bridge')}
              </h1>
            </div>
          </div>
          <p className="text-sm text-muted leading-relaxed max-w-sm">
            {t('bridge_hero_desc', { defaultValue: 'Визуализация разрыва между вашими восприятиями. Где ваши взгляды совпадают, а где — расходятся.' })}
          </p>
        </motion.div>
      </div>

      <div className="px-4 pt-5 md:px-5">
        {isLoading ? (
          <div className="flex flex-col gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 rounded-card shimmer" />
            ))}
          </div>
        ) : !result ? (
          <EmptyState
            icon={<ArrowLeftRight />}
            title={t('bridge_empty_title', { defaultValue: 'Нет данных диагностики' })}
            description={t('bridge_empty_desc', { defaultValue: 'Пройдите диагностику вместе, чтобы увидеть мост понимания' })}
            actionLabel={t('bridge_to_diag', { defaultValue: 'К диагностике' })}
            onAction={() => navigate('/app/diagnostics')}
          />
        ) : (
          <div className="space-y-4">
            {/* Summary */}
            <motion.div {...fadeUp(0)}>
              <div
                className="rounded-[22px] p-5 bg-canvas"
                style={{
                  border: '1px solid rgba(60,56,136,0.12)',
                  boxShadow: '0 4px 20px rgba(60,56,136,0.08)',
                }}
              >
                <div className="flex items-center gap-3 mb-4">
                  <Sparkles size={16} className="text-primary" />
                  <h2 className="font-bold text-ink text-sm">{t('bridge_total_label')}</h2>
                  <span
                    className="ml-auto text-2xl font-bold"
                    style={{ color: '#3C3888', letterSpacing: '-0.03em' }}
                  >
                    {Math.round(result.overall_score)}
                  </span>
                  <span className="text-sm text-muted">/ 100</span>
                </div>

                {/* Bridge visual */}
                <div className="relative h-3 rounded-full overflow-hidden bg-sand/60">
                  <motion.div
                    className="absolute inset-y-0 left-0 rounded-full"
                    style={{ background: 'linear-gradient(90deg, #3C3888, #385C8A, #386858)' }}
                    initial={{ width: 0 }}
                    animate={{ width: `${result.overall_score}%` }}
                    transition={{ duration: 1, ease, delay: 0.2 }}
                  />
                </div>

                <div className="mt-3 flex items-center justify-between text-xs text-muted">
                  <span>{t('gap_label')}</span>
                  <span>{t('unity_label')}</span>
                </div>
              </div>
            </motion.div>

            {/* Zone bridges */}
            <motion.div {...fadeUp(0.06)}>
              <p className="label-caps text-muted mb-3 px-1">{t('zones_label')}</p>
              <div className="space-y-3">
                {result.zone_scores.map((z: any, idx: number) => {
                  const colors = ZONE_COLORS[z.zone] ?? DEFAULT_ZONE_COLOR
                  const myScore = Math.round(z.my_score ?? z.couple_avg)
                  const partnerScore = Math.round(z.partner_score ?? z.couple_avg)
                  const gap = Math.abs(myScore - partnerScore)
                  const hasGap = gap > 15

                  return (
                    <motion.div
                      key={z.zone}
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.35, ease, delay: 0.08 + idx * 0.05 }}
                      className="rounded-[20px] bg-canvas p-4"
                      style={{
                        border: hasGap ? '1px solid rgba(184,144,74,0.25)' : '1px solid rgba(232,227,218,0.6)',
                        boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 4px 12px rgba(23,21,42,0.04)',
                      }}
                    >
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-sm font-semibold text-ink">
                          {t(`common:zones.${z.zone}`, { defaultValue: z.zone })}
                        </span>
                        {hasGap && (
                          <div className="flex items-center gap-1 text-xs font-medium text-warning">
                            <AlertCircle size={12} />
                            {t('gap_warning', { gap })}
                          </div>
                        )}
                      </div>

                      {/* Two-sided bar */}
                      <div className="space-y-2">
                        {/* My bar */}
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

                        {/* Partner bar */}
                        <div>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-[10px] font-semibold text-muted uppercase tracking-wider">{t('common:partner', { defaultValue: 'Партнёр' })}</span>
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
            </motion.div>

            {/* Strengths */}
            {result.strengths_summary && (
              <motion.div {...fadeUp(0.18)}>
                <div
                  className="rounded-[20px] p-5"
                  style={{
                    background: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)',
                    border: '1px solid rgba(56,104,88,0.15)',
                  }}
                >
                  <p className="font-bold text-ink mb-1">
                    <span className="mr-2">🤝</span>
                    {result.strengths_summary.headline}
                  </p>
                  <p className="text-xs text-muted leading-relaxed mt-1">
                    {t('common_ground_note')}
                  </p>
                </div>
              </motion.div>
            )}

            {/* CTA */}
            <motion.div {...fadeUp(0.22)} className="flex gap-3 pb-2">
              <Button variant="secondary" fullWidth onClick={() => navigate('/app/ai')}>
                <Sparkles size={14} /> {t('discuss_ai_btn')}
              </Button>
              <Button fullWidth onClick={() => navigate('/app/mediation')}>
                {t('open_mediator_btn')}
              </Button>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  )
}
