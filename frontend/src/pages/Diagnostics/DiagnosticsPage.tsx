import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ClipboardList, Lock, CheckCircle2, ChevronRight, X, Users } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { DiagnosticsService } from '@/services/diagnostics.service'
import { Button } from '@/components/ui/Button'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { DiagnosticLevel, DiagnosticLevelStatus, FamilyJourney } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

// ── Конфиг уровней ────────────────────────────────────────────────────────────

const LEVEL_COLORS: Record<number, { from: string; to: string; light: string; accent: string }> = {
  1:  { from: '#386858', to: '#2C7A5C', light: '#E2EDE8', accent: '#386858' },
  2:  { from: '#2C5678', to: '#385C8A', light: '#DDEAF5', accent: '#2C5678' },
  3:  { from: '#3C3888', to: '#4C48A8', light: '#EDEAF8', accent: '#3C3888' },
  4:  { from: '#74364A', to: '#8A3C5C', light: '#F2E0E6', accent: '#74364A' },
  5:  { from: '#744E26', to: '#885040', light: '#EEE2D4', accent: '#744E26' },
  6:  { from: '#885068', to: '#A04878', light: '#F2E0EA', accent: '#885068' },
  7:  { from: '#886028', to: '#A07030', light: '#F0E8D4', accent: '#886028' },
  8:  { from: '#286250', to: '#308060', light: '#D8EDE7', accent: '#286250' },
  9:  { from: '#463E80', to: '#584890', light: '#E4E0F5', accent: '#463E80' },
  10: { from: '#1A4060', to: '#2C5678', light: '#D4E4F0', accent: '#1A4060' },
}
const DEFAULT_COLOR = { from: '#3C3888', to: '#385C8A', light: '#EDEAF8', accent: '#3C3888' }

// ── Level detail sheet ────────────────────────────────────────────────────────

function LevelSheet({
  level,
  journey,
  iAmPartnerA,
  onClose,
}: {
  level: DiagnosticLevel | null
  journey: FamilyJourney
  iAmPartnerA: boolean
  onClose: () => void
}) {
  const navigate = useNavigate()
  const { t } = useTranslation('diagnostics')
  if (!level) return null

  const colors = LEVEL_COLORS[level.level_number] ?? DEFAULT_COLOR
  const isLocked = level.status === 'locked'
  const isCompleted = level.status === 'completed'
  const isDiagnosed = level.status === 'diagnosed'
  const isInProgress = level.status === 'in_progress'
  const isUnlocked = level.status === 'unlocked'

  const myDone = iAmPartnerA ? level.partner_a_done : level.partner_b_done
  const partnerDone = iAmPartnerA ? level.partner_b_done : level.partner_a_done

  const canStart = (isUnlocked || isInProgress) && !myDone
  const waitingForPartner = myDone && !partnerDone && !isDiagnosed && !isCompleted
  const waitingPractices = isDiagnosed && !isCompleted

  const handleStart = () => {
    onClose()
    navigate('/app/diagnostics/start', { state: { levelNumber: level.level_number } })
  }

  return (
    <AnimatePresence>
      {level && (
        <>
          <motion.div
            key="backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-[60] bg-black/40"
            style={{ backdropFilter: 'blur(4px)' }}
            onClick={onClose}
          />
          <motion.div
            key="sheet"
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: 'spring', damping: 32, stiffness: 320 }}
            className="fixed bottom-0 left-0 right-0 z-[70] rounded-t-[28px] overflow-hidden"
            style={{
              background: '#FEFCFA',
              maxHeight: '88dvh',
              boxShadow: '0 -8px 40px rgba(23,21,42,0.16)',
            }}
          >
            <div className="flex justify-center pt-3 pb-1">
              <div className="h-1 w-10 rounded-full bg-sand/60" />
            </div>

            {/* Header */}
            <div
              className="px-5 pt-4 pb-5"
              style={{ background: `linear-gradient(135deg, ${colors.light}, ${colors.light}cc)` }}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-4xl">{level.emoji}</span>
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-wider mb-0.5"
                      style={{ color: colors.accent }}>
                      {t('level_n', { n: level.level_number })}
                    </p>
                    <p className="text-lg font-bold text-ink leading-snug">{t(`lvl_${level.level_number}_title`)}</p>
                  </div>
                </div>
                <button
                  onClick={onClose}
                  className="flex h-8 w-8 items-center justify-center rounded-full flex-shrink-0"
                  style={{ background: 'rgba(23,21,42,0.08)' }}
                >
                  <X size={16} className="text-ink/60" />
                </button>
              </div>
              <p className="mt-3 text-sm text-ink/70 leading-relaxed">{t(`lvl_${level.level_number}_desc`)}</p>
            </div>

            <div className="overflow-y-auto px-5 py-4 space-y-4" style={{ maxHeight: 'calc(88dvh - 160px)' }}>
              {/* Partner statuses */}
              {!isLocked && (
                <div className="space-y-2">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-muted">
                    {t('partners_status')}
                  </p>
                  <PartnerStatus label={t('you_label')} done={iAmPartnerA ? level.partner_a_done : level.partner_b_done} />
                  <PartnerStatus label={t('partner_label')} done={iAmPartnerA ? level.partner_b_done : level.partner_a_done} />
                </div>
              )}

              {/* Locked info */}
              {isLocked && (
                <div
                  className="rounded-[16px] p-4 flex items-start gap-3"
                  style={{ background: 'rgba(23,21,42,0.04)', border: '1px solid rgba(23,21,42,0.08)' }}
                >
                  <Lock size={16} className="text-muted mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-muted leading-relaxed">{t('locked_hint')}</p>
                </div>
              )}

              {/* I'm done — waiting for partner */}
              {waitingForPartner && (
                <div
                  className="rounded-[16px] p-4 flex items-start gap-3"
                  style={{ background: 'rgba(56,104,88,0.08)', border: '1px solid rgba(56,104,88,0.18)' }}
                >
                  <CheckCircle2 size={16} className="text-success mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-success mb-1">{t('waiting_partner_title')}</p>
                    <p className="text-xs text-muted leading-relaxed">{t('waiting_partner_hint')}</p>
                  </div>
                </div>
              )}

              {/* Diagnosed — waiting for practices */}
              {waitingPractices && (
                <div
                  className="rounded-[16px] p-4 flex items-start gap-3"
                  style={{ background: 'rgba(60,56,136,0.08)', border: '1px solid rgba(60,56,136,0.15)' }}
                >
                  <span className="text-xl">✨</span>
                  <div>
                    <p className="text-sm font-semibold text-primary mb-1">{t('diagnosed_title')}</p>
                    <p className="text-xs text-muted leading-relaxed">{t('diagnosed_hint')}</p>
                  </div>
                </div>
              )}

              {/* Completed */}
              {isCompleted && (
                <div
                  className="rounded-[16px] p-4 flex items-center gap-3"
                  style={{ background: 'rgba(56,104,88,0.12)', border: '1px solid rgba(56,104,88,0.2)' }}
                >
                  <CheckCircle2 size={18} className="text-success flex-shrink-0" />
                  <div>
                    <p className="text-sm font-bold text-success">{t('level_completed')}</p>
                    {level.both_diagnosed_at && (
                      <p className="text-xs text-muted mt-0.5">
                        {new Date(level.both_diagnosed_at).toLocaleDateString('ru-RU', {
                          day: 'numeric', month: 'long',
                        })}
                      </p>
                    )}
                  </div>
                </div>
              )}

              <div className="h-2" />
            </div>

            {/* Footer */}
            <div
              className="sticky bottom-0 px-5 pt-4"
              style={{
                background: 'rgba(254,252,250,0.96)',
                backdropFilter: 'blur(8px)',
                borderTop: '1px solid rgba(232,227,218,0.6)',
                paddingBottom: 'calc(1rem + env(safe-area-inset-bottom))',
              }}
            >
              {canStart ? (
                <Button fullWidth size="lg" onClick={handleStart}>
                  {isInProgress ? t('continue_btn') : t('start_btn')}
                </Button>
              ) : waitingForPartner ? (
                <div
                  className="flex items-center justify-center gap-2 rounded-[16px] py-3.5"
                  style={{ background: 'rgba(56,104,88,0.08)', border: '1px solid rgba(56,104,88,0.18)' }}
                >
                  <CheckCircle2 size={15} className="text-success" />
                  <span className="text-sm font-semibold text-success">{t('waiting_partner_btn')}</span>
                </div>
              ) : isCompleted ? (
                <div
                  className="flex items-center justify-center gap-2 rounded-[16px] py-3.5"
                  style={{ background: 'rgba(56,104,88,0.1)', border: '1px solid rgba(56,104,88,0.2)' }}
                >
                  <CheckCircle2 size={16} className="text-success" />
                  <span className="text-sm font-bold text-success">{t('level_completed')}</span>
                </div>
              ) : waitingPractices ? (
                <Button fullWidth variant="secondary" onClick={() => { onClose(); navigate('/app/practices') }}>
                  {t('go_to_practices')}
                </Button>
              ) : (
                <div
                  className="flex items-center justify-center gap-2 rounded-[16px] py-3.5"
                  style={{ background: 'rgba(23,21,42,0.05)', border: '1px solid rgba(23,21,42,0.08)' }}
                >
                  <Lock size={14} className="text-muted" />
                  <span className="text-sm font-semibold text-muted">{t('locked_btn')}</span>
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

function PartnerStatus({ label, done }: { label: string; done: boolean }) {
  const { t } = useTranslation('diagnostics')
  return (
    <div
      className="flex items-center justify-between rounded-2xl px-4 py-2.5"
      style={{
        background: done ? 'rgba(56,104,88,0.1)' : 'rgba(232,227,218,0.5)',
        border: done ? '1px solid rgba(56,104,88,0.18)' : '1px solid rgba(232,227,218,0.6)',
      }}
    >
      <span className="text-sm font-semibold text-ink">{label}</span>
      {done ? (
        <span className="text-xs font-bold text-success flex items-center gap-1">
          <CheckCircle2 size={12} /> {t('status_done')}
        </span>
      ) : (
        <span className="text-xs text-muted">{t('status_pending')}</span>
      )}
    </div>
  )
}

// ── Level tile ─────────────────────────────────────────────────────────────────

function LevelTile({
  level,
  isCurrent,
  onClick,
  delay,
}: {
  level: DiagnosticLevel
  isCurrent: boolean
  onClick: () => void
  delay: number
}) {
  const { t } = useTranslation('diagnostics')
  const colors = LEVEL_COLORS[level.level_number] ?? DEFAULT_COLOR
  const isLocked = level.status === 'locked'
  const isCompleted = level.status === 'completed'

  return (
    <motion.button
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease, delay }}
      onClick={onClick}
      disabled={false}
      className="w-full text-left transition-all duration-200 active:scale-[0.98]"
    >
      <div
        className="rounded-[20px] p-4 flex items-center gap-4"
        style={{
          background: isLocked
            ? 'rgba(248,246,242,0.8)'
            : isCompleted
              ? `linear-gradient(135deg, ${colors.light}, ${colors.light}bb)`
              : isCurrent
                ? `linear-gradient(135deg, ${colors.light}, #FEFCFA)`
                : `linear-gradient(135deg, ${colors.light}88, #FEFCFA)`,
          border: isCurrent
            ? `1.5px solid ${colors.accent}40`
            : isCompleted
              ? '1px solid rgba(56,104,88,0.2)'
              : '1px solid rgba(232,227,218,0.6)',
          boxShadow: isCurrent
            ? `0 4px 20px ${colors.accent}14`
            : '0 1px 4px rgba(23,21,42,0.04)',
          opacity: isLocked ? 0.55 : 1,
        }}
      >
        {/* Left: number badge */}
        <div
          className="flex-shrink-0 flex h-12 w-12 items-center justify-center rounded-[14px]"
          style={{
            background: isLocked
              ? 'rgba(23,21,42,0.06)'
              : isCompleted
                ? 'rgba(56,104,88,0.15)'
                : `linear-gradient(135deg, ${colors.from}, ${colors.to})`,
            boxShadow: isLocked || isCompleted ? 'none' : `0 4px 12px ${colors.accent}30`,
          }}
        >
          {isLocked ? (
            <Lock size={18} className="text-muted/60" />
          ) : isCompleted ? (
            <CheckCircle2 size={20} className="text-success" />
          ) : (
            <span className="text-xl">{level.emoji}</span>
          )}
        </div>

        {/* Middle: title + meta */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <p className="text-[10px] font-bold uppercase tracking-wider"
              style={{ color: isLocked ? '#68647C' : colors.accent }}>
              {t('level_n', { n: level.level_number })}
            </p>
            {isCurrent && !isCompleted && (
              <span
                className="text-[9px] font-bold px-1.5 py-0.5 rounded-full"
                style={{ background: `${colors.accent}18`, color: colors.accent }}
              >
                {t('current_badge')}
              </span>
            )}
          </div>
          <p className={`text-sm font-bold leading-snug ${isLocked ? 'text-muted' : 'text-ink'}`}>
            {t(`lvl_${level.level_number}_title`)}
          </p>
          <p className="text-[11px] text-muted mt-0.5 line-clamp-1">{t(`lvl_${level.level_number}_desc`)}</p>

          {/* Partner progress dots */}
          {!isLocked && !isCompleted && (
            <div className="mt-1.5 flex items-center gap-1.5">
              <span
                className="h-1.5 w-1.5 rounded-full"
                style={{ background: level.partner_a_done ? '#386858' : 'rgba(23,21,42,0.15)' }}
              />
              <span
                className="h-1.5 w-1.5 rounded-full"
                style={{ background: level.partner_b_done ? '#386858' : 'rgba(23,21,42,0.15)' }}
              />
              <span className="text-[10px] text-muted">
                {level.partner_a_done && level.partner_b_done
                  ? t('both_done_short')
                  : level.partner_a_done || level.partner_b_done
                    ? t('one_done_short')
                    : t('none_done_short')}
              </span>
            </div>
          )}
        </div>

        {/* Right: chevron */}
        <ChevronRight
          size={16}
          className="flex-shrink-0"
          style={{ color: isLocked ? 'rgba(23,21,42,0.2)' : colors.accent + '80' }}
        />
      </div>
    </motion.button>
  )
}

// ── Hero strip ─────────────────────────────────────────────────────────────────

function JourneyHero({ journey }: { journey: FamilyJourney }) {
  const { t } = useTranslation('diagnostics')
  const completed = journey.last_completed_level
  const current = journey.max_unlocked_level
  const pct = Math.round((completed / 10) * 100)
  const colors = LEVEL_COLORS[current] ?? DEFAULT_COLOR

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease }}
      className="rounded-[22px] p-5"
      style={{
        background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)',
        border: '1px solid rgba(60,56,136,0.12)',
        boxShadow: '0 4px 20px rgba(60,56,136,0.09)',
      }}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-wider text-primary/60 mb-0.5">
            {t('journey_title')}
          </p>
          <p className="text-base font-bold text-ink">
            {completed === 0
              ? t('journey_start')
              : t('journey_progress', { done: completed, total: 10 })}
          </p>
        </div>
        <div
          className="flex items-center gap-1.5 rounded-full px-3 py-1"
          style={{ background: 'rgba(60,56,136,0.12)' }}
        >
          <span className="text-sm">{LEVEL_COLORS[current] ? '🔓' : '🌱'}</span>
          <span className="text-xs font-bold text-primary">{t('level_n', { n: current })}</span>
        </div>
      </div>

      <div className="h-2 w-full rounded-full overflow-hidden bg-white/40">
        <motion.div
          className="h-full rounded-full"
          style={{ background: `linear-gradient(90deg, ${colors.from}, ${colors.to})` }}
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, ease, delay: 0.2 }}
        />
      </div>
      <p className="mt-1.5 text-xs text-ink/50">
        {t('journey_pct', { pct })}
      </p>
    </motion.div>
  )
}

// ── Main page ──────────────────────────────────────────────────────────────────

export const DiagnosticsPage = () => {
  const navigate = useNavigate()
  const { t } = useTranslation('diagnostics')
  const [selectedLevel, setSelectedLevel] = useState<DiagnosticLevel | null>(null)

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: journey, isLoading } = useQuery({
    queryKey: ['journey'],
    queryFn: DiagnosticsService.getJourney,
    enabled: me?.couple?.status === 'active',
    retry: false,
  })

  if (me?.couple?.status === 'pending') {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4">
          <EmptyState
            icon={<ClipboardList />}
            title={t('common:pending_couple_title')}
            description={t('common:invite_partner_first')}
            actionLabel={t('common:invite_partner_btn')}
            onAction={() => navigate('/app/couple')}
          />
        </div>
      </div>
    )
  }

  if (!me?.couple) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4">
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

  if (isLoading || !journey) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4 space-y-3">
          <div className="h-24 rounded-[22px] shimmer" />
          {[...Array(5)].map((_, i) => <div key={i} className="h-20 rounded-[20px] shimmer" />)}
        </div>
      </div>
    )
  }

  const currentLevel = journey.levels.find(l => l.level_number === journey.max_unlocked_level)

  return (
    <>
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />

        <div className="px-4 space-y-3">
          {journey.levels.map((level, idx) => (
            <LevelTile
              key={level.level_number}
              level={level}
              isCurrent={level.level_number === journey.max_unlocked_level}
              onClick={() => setSelectedLevel(level)}
              delay={0.05 + idx * 0.04}
            />
          ))}
        </div>
      </div>

      <LevelSheet
        level={selectedLevel}
        journey={journey}
        iAmPartnerA={journey.i_am_partner_a}
        onClose={() => setSelectedLevel(null)}
      />
    </>
  )
}

function PageHeader() {
  const { t } = useTranslation('diagnostics')
  return (
    <div className="page-hero px-5 pt-6 pb-4">
      <div className="flex items-center gap-3">
        <div
          className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
          style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
        >
          <ClipboardList size={17} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
          <p className="text-xs text-muted mt-0.5">{t('journey_subtitle')}</p>
        </div>
      </div>
    </div>
  )
}
