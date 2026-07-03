import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import { Sun, CheckCircle2, Circle, AlertCircle, X, Clock, ChevronRight, BookOpen } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { PracticesService } from '@/services/practices.service'
import { Button } from '@/components/ui/Button'
import { EmptyState } from '@/components/feedback/EmptyState'
import { celebrateSmall, celebrateBig } from '@/lib/confetti'
import type { AssignmentSlot, FamilyDevelopmentPlan } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease, delay },
})

// ── Visual config ─────────────────────────────────────────────────────────────

const PRACTICE_META: Record<string, { icon: string; bg: string; accent: string }> = {
  main:         { icon: '✨', bg: 'linear-gradient(135deg, #EDEAF8 0%, #DDE8F2 100%)', accent: '#3C3888' },
  conversation: { icon: '💬', bg: 'linear-gradient(135deg, #E2EDE8 0%, #D2DDF0 100%)', accent: '#386858' },
  gesture:      { icon: '🌸', bg: 'linear-gradient(135deg, #EEE4DC 0%, #EDEAF8 100%)', accent: '#885040' },
  activity:     { icon: '🏃', bg: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)', accent: '#385C8A' },
  ritual:       { icon: '🕯️', bg: 'linear-gradient(135deg, #EDE8F0 0%, #E8DDF2 100%)', accent: '#6B4A8A' },
  growth:       { icon: '📖', bg: 'linear-gradient(135deg, #F0EDE4 0%, #EEE4DC 100%)', accent: '#886028' },
}
const DEFAULT_META = { icon: '⭐', bg: 'linear-gradient(135deg, #E8E2D4 0%, #EDEAF8 100%)', accent: '#68647C' }

// ── Diagnostics gate ──────────────────────────────────────────────────────────

function DiagnosticsGate({
  partnerADone, partnerBDone, iAmPartnerA,
}: { partnerADone: boolean; partnerBDone: boolean; iAmPartnerA: boolean }) {
  const navigate = useNavigate()
  const { t } = useTranslation('practices')

  const myDone      = iAmPartnerA ? partnerADone : partnerBDone
  const partnerDone = iAmPartnerA ? partnerBDone : partnerADone

  return (
    <motion.div {...fadeUp(0)} className="px-4 pt-2">
      <div
        className="rounded-[24px] p-6 text-center"
        style={{
          background: 'linear-gradient(145deg, #F0EDE4 0%, #EDEAF8 100%)',
          border: '1px solid rgba(60,56,136,0.12)',
          boxShadow: '0 4px 20px rgba(60,56,136,0.09)',
        }}
      >
        <div className="mb-5 flex justify-center">
          <div
            className="flex h-16 w-16 items-center justify-center rounded-[20px]"
            style={{
              background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
              boxShadow: '0 8px 24px rgba(60,56,136,0.28)',
            }}
          >
            <span className="text-2xl">🔐</span>
          </div>
        </div>

        <h2 className="text-lg font-bold text-ink mb-2">{t('gate_title')}</h2>
        <p className="text-sm text-muted leading-relaxed mb-6 max-w-xs mx-auto">
          {t('gate_desc')}
        </p>

        <div className="flex flex-col gap-2 mb-6 max-w-xs mx-auto">
          <DiagStatus label={t('gate_you')} done={myDone} />
          <DiagStatus label={t('gate_partner')} done={partnerDone} />
        </div>

        {!myDone && (
          <Button onClick={() => navigate('/app/diagnostics')} size="lg">
            {t('gate_btn_start')}
          </Button>
        )}
        {myDone && !partnerDone && (
          <Button size="lg" disabled>
            {t('gate_btn_waiting')}
          </Button>
        )}

        <p className="mt-3 text-xs text-muted">{t('gate_hint')}</p>
      </div>
    </motion.div>
  )
}

function DiagStatus({ label, done }: { label: string; done: boolean }) {
  const { t } = useTranslation('practices')
  return (
    <div
      className="flex items-center justify-between rounded-2xl px-4 py-3"
      style={{
        background: done ? 'rgba(56,104,88,0.12)' : 'rgba(232,227,218,0.8)',
        border: done ? '1px solid rgba(56,104,88,0.2)' : '1px solid rgba(232,227,218,0.6)',
      }}
    >
      <span className="text-sm font-semibold text-ink">{label}</span>
      {done ? (
        <span className="text-xs font-bold text-success">{t('gate_status_done')}</span>
      ) : (
        <span className="text-xs text-muted">{t('gate_status_pending')}</span>
      )}
    </div>
  )
}

// ── Family level strip ────────────────────────────────────────────────────────

function LevelPill({ children }: { children: React.ReactNode }) {
  return (
    <div
      className="flex items-center gap-1 rounded-full px-3 py-1"
      style={{ background: 'rgba(60,56,136,0.12)' }}
    >
      {children}
    </div>
  )
}

function FamilyLevelStrip({ plan }: { plan: FamilyDevelopmentPlan }) {
  const { t } = useTranslation('practices')
  const stageEmojis: Record<number, string> = { 1: '🌱', 2: '🌿', 3: '🌀', 4: '💎', 5: '🌟' }
  const stageEmoji = stageEmojis[plan.current_stage] ?? '🌱'

  return (
    <motion.div {...fadeUp(0)}>
      <div
        className="rounded-[22px] p-5"
        style={{
          background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 60%, #D6E8E2 100%)',
          border: '1px solid rgba(60,56,136,0.12)',
          boxShadow: '0 4px 20px rgba(60,56,136,0.09)',
        }}
      >
        <div className="flex items-start justify-between mb-3">
          {/* Left: stage */}
          <div>
            <p className="text-[10px] font-bold uppercase tracking-wider text-primary/60 mb-0.5">
              {t('stage_of_5', { n: plan.current_stage })}
            </p>
            <p className="text-base font-bold text-ink leading-snug">
              {stageEmoji} {t(`stage_${plan.current_stage}` as any)}
            </p>
          </div>

          {/* Right: level badge + XP badge — same pill style */}
          <div className="flex flex-col items-end gap-1.5">
            <LevelPill>
              <span className="text-sm leading-none">{plan.level_emoji}</span>
              <span className="text-xs font-bold text-primary">{t('level_n', { n: plan.current_level })}</span>
            </LevelPill>
            {plan.level_xp_for_next > 0 ? (
              <LevelPill>
                <span className="text-xs font-bold text-primary">{plan.level_xp_current}</span>
                <span className="text-xs text-muted">/ {plan.level_xp_for_next} XP</span>
              </LevelPill>
            ) : (
              <LevelPill>
                <span className="text-xs font-bold text-primary">{t('max_level')}</span>
              </LevelPill>
            )}
          </div>
        </div>

        <div className="h-2 w-full rounded-full overflow-hidden bg-white/40">
          <motion.div
            className="h-full rounded-full"
            style={{ background: 'linear-gradient(90deg, #3C3888, #385C8A)' }}
            initial={{ width: 0 }}
            animate={{ width: `${plan.level_progress_pct}%` }}
            transition={{ duration: 0.8, ease, delay: 0.2 }}
          />
        </div>

        {plan.requires_diagnostic && (
          <div
            className="mt-3 flex items-center gap-2 rounded-2xl px-3 py-2"
            style={{ background: 'rgba(136,80,64,0.1)' }}
          >
            <AlertCircle size={14} style={{ color: '#885040' }} />
            <p className="text-xs font-semibold" style={{ color: '#885040' }}>
              {t('diagnostic_overdue')}
            </p>
          </div>
        )}

        {!plan.requires_diagnostic && plan.next_diagnostic_in_days !== null && plan.next_diagnostic_in_days <= 3 && (
          <div
            className="mt-3 flex items-center gap-2 rounded-2xl px-3 py-2"
            style={{ background: 'rgba(60,56,136,0.08)' }}
          >
            <AlertCircle size={14} className="text-primary/70" />
            <p className="text-xs text-primary/70">
              {t('diagnostic_soon', { n: plan.next_diagnostic_in_days })}
            </p>
          </div>
        )}
      </div>
    </motion.div>
  )
}

// ── Practice card ─────────────────────────────────────────────────────────────

function PracticeCard({
  item, onToggle, onOpen, loading,
}: {
  item: AssignmentSlot
  onToggle: () => void
  onOpen: () => void
  loading: boolean
}) {
  const { t } = useTranslation('practices')
  const meta     = PRACTICE_META[item.slot_type] ?? DEFAULT_META
  const isGrowth = item.slot_type === 'growth'
  const slotLabel = t(`slot_${item.slot_type}` as any)
  const catLabel  = item.practice?.category
    ? t(`cat_${item.practice.category}` as any)
    : undefined
  const title = item.practice?.title ?? ''
  const mins  = item.practice?.duration_minutes

  return (
    <motion.div
      className={`rounded-[20px] p-5 cursor-pointer ${item.completed ? 'opacity-55' : ''}`}
      style={{
        background: item.completed ? 'rgba(248,246,242,0.9)' : meta.bg,
        border: item.completed ? '1px solid rgba(56,104,88,0.22)' : '1px solid rgba(232,227,218,0.5)',
        boxShadow: item.completed ? 'none' : '0 1px 3px rgba(23,21,42,0.04), 0 4px 14px rgba(23,21,42,0.04)',
      }}
      whileHover={!item.completed ? { scale: 1.015, boxShadow: '0 4px 20px rgba(60,56,136,0.13)' } : {}}
      whileTap={!item.completed ? { scale: 0.975 } : {}}
      transition={{ type: 'spring', stiffness: 400, damping: 28 }}
      onClick={onOpen}
    >
      <div className="flex items-start gap-4">
        <span className="text-2xl flex-shrink-0 select-none">{meta.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1.5 flex-wrap">
            <p className="text-[10px] font-bold uppercase tracking-wider" style={{ color: meta.accent }}>
              {slotLabel}
            </p>
            {catLabel && (
              <span
                className="text-[9px] font-semibold px-1.5 py-0.5 rounded-full"
                style={{ background: `${meta.accent}18`, color: meta.accent }}
              >
                {catLabel}
              </span>
            )}
            {mins && (
              <span className="flex items-center gap-0.5 text-[9px] text-muted ml-auto">
                <Clock size={9} />
                {t('detail_min', { n: mins })}
              </span>
            )}
          </div>
          {title && (
            <p className={`text-sm font-semibold leading-snug ${
              item.completed ? 'text-muted line-through' : 'text-ink'
            }`}>
              {title}
            </p>
          )}
          {isGrowth && (
            <p className="mt-1 text-[10px] font-semibold opacity-60" style={{ color: meta.accent }}>
              {t('growth_reading_label')}
            </p>
          )}
        </div>
        {/* Right side: checkbox for completable, chevron for growth */}
        {!isGrowth ? (
          <motion.button
            onClick={(e) => { e.stopPropagation(); onToggle() }}
            disabled={item.completed || loading}
            className="flex-shrink-0 mt-0.5"
            aria-label={item.completed ? t('detail_already_done') : t('detail_mark_done')}
            whileTap={!item.completed && !loading ? { scale: 1.35 } : {}}
            transition={{ type: 'spring', stiffness: 500, damping: 20 }}
          >
            {loading ? (
              <div
                className="h-6 w-6 animate-spin rounded-full border-2"
                style={{ borderColor: `${meta.accent}40`, borderTopColor: 'transparent' }}
              />
            ) : item.completed ? (
              <motion.div
                initial={{ scale: 0, rotate: -30 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 500, damping: 22 }}
              >
                <CheckCircle2 size={24} className="text-success" />
              </motion.div>
            ) : (
              <Circle
                size={24}
                style={{ color: `${meta.accent}60` }}
                className="hover:opacity-80 transition-opacity"
              />
            )}
          </motion.button>
        ) : (
          <ChevronRight size={18} className="flex-shrink-0 mt-1 text-ink/30" />
        )}
      </div>
    </motion.div>
  )
}

// ── Progress card ─────────────────────────────────────────────────────────────

function PracticeProgressCard({ plan }: { plan: FamilyDevelopmentPlan }) {
  const navigate = useNavigate()
  const { t } = useTranslation('practices')

  const zones = [
    { key: plan.priority_zone,  rank: 1 },
    { key: plan.secondary_zone, rank: 2 },
    { key: plan.tertiary_zone,  rank: 3 },
  ].filter(z => z.key)

  return (
    <motion.div {...fadeUp(0.1)}>
      <div
        className="rounded-[22px] p-5"
        style={{
          background: 'rgba(255,255,255,0.8)',
          border: '1px solid rgba(232,227,218,0.6)',
          boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)',
        }}
      >
        <p className="text-[10px] font-bold uppercase tracking-wider text-muted mb-3">
          {t('zones_title')}
        </p>
        <div className="flex flex-col gap-2 mb-4">
          {zones.map((z) => (
            <div key={z.key} className="flex items-center gap-3">
              <span
                className="flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold text-white"
                style={{
                  background: z.rank === 1 ? '#3C3888' : z.rank === 2 ? '#385C8A' : '#886028',
                }}
              >
                {z.rank}
              </span>
              <span className="text-sm font-semibold text-ink">
                {t(`cat_${z.key}` as any, { defaultValue: z.key })}
              </span>
              {z.rank === 1 && (
                <span
                  className="ml-auto text-[10px] font-bold px-2 py-0.5 rounded-full"
                  style={{ background: 'rgba(60,56,136,0.1)', color: '#3C3888' }}
                >
                  {t('zone_priority_label')}
                </span>
              )}
            </div>
          ))}
        </div>

        <div
          className="flex items-center justify-between rounded-2xl px-4 py-3"
          style={{ background: 'rgba(60,56,136,0.06)' }}
        >
          <div>
            <p className="text-xs text-muted mb-0.5">{t('level_xp_label', { n: plan.current_level })}</p>
            <p className="text-xl font-bold text-ink">
              {plan.level_xp_for_next > 0
                ? t('xp_progress', { current: plan.level_xp_current, max: plan.level_xp_for_next })
                : t('max_level')}
            </p>
          </div>
          {plan.requires_diagnostic ? (
            <Button size="sm" onClick={() => navigate('/app/diagnostics')}>
              {t('btn_update_diagnostic')}
            </Button>
          ) : plan.next_diagnostic_in_days !== null ? (
            <div className="text-right">
              <p className="text-xs text-muted">{t('next_diagnostic_label')}</p>
              <p className="text-sm font-bold text-primary">
                {t('in_n_days', { n: plan.next_diagnostic_in_days })}
              </p>
            </div>
          ) : null}
        </div>
      </div>
    </motion.div>
  )
}

// ── Practice detail sheet ─────────────────────────────────────────────────────

function PracticeDetailSheet({
  slot,
  onClose,
  onComplete,
  isCompleting,
}: {
  slot: AssignmentSlot | null
  onClose: () => void
  onComplete: () => void
  isCompleting: boolean
}) {
  const { t } = useTranslation('practices')
  const navigate = useNavigate()

  const meta      = slot ? (PRACTICE_META[slot.slot_type] ?? DEFAULT_META) : DEFAULT_META
  const isGrowth  = slot?.slot_type === 'growth'
  const practice  = slot?.practice ?? null
  const slotLabel = slot ? t(`slot_${slot.slot_type}` as any) : ''
  const catLabel  = practice?.category ? t(`cat_${practice.category}` as any) : undefined
  const diffKey   = practice?.difficulty ? `diff_${practice.difficulty}` as any : null

  const steps = practice?.instructions
    ? practice.instructions.split('\n').map(s => s.trim()).filter(Boolean)
    : []

  return (
    <AnimatePresence>
      {slot && (
        <>
          {/* Backdrop */}
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

          {/* Sheet */}
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
            {/* Drag handle */}
            <div className="flex justify-center pt-3 pb-1">
              <div className="h-1 w-10 rounded-full bg-sand/60" />
            </div>

            <div className="overflow-y-auto" style={{ maxHeight: 'calc(88dvh - 20px)' }}>
              {/* Header */}
              <div
                className="px-5 pt-4 pb-5"
                style={{ background: slot.completed ? 'rgba(248,246,242,0.8)' : meta.bg }}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{meta.icon}</span>
                    <div>
                      <p
                        className="text-[10px] font-bold uppercase tracking-wider mb-0.5"
                        style={{ color: meta.accent }}
                      >
                        {slotLabel}
                      </p>
                      <p className="text-lg font-bold text-ink leading-snug">
                        {practice?.title ?? ''}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={onClose}
                    className="flex-shrink-0 flex h-8 w-8 items-center justify-center rounded-full"
                    style={{ background: 'rgba(23,21,42,0.08)' }}
                  >
                    <X size={16} className="text-ink/60" />
                  </button>
                </div>

                {/* Meta chips */}
                <div className="mt-3 flex items-center gap-2 flex-wrap">
                  {catLabel && (
                    <span
                      className="text-[10px] font-bold px-2.5 py-1 rounded-full"
                      style={{ background: `${meta.accent}18`, color: meta.accent }}
                    >
                      {catLabel}
                    </span>
                  )}
                  {practice?.duration_minutes && (
                    <span
                      className="flex items-center gap-1 text-[10px] font-semibold px-2.5 py-1 rounded-full"
                      style={{ background: 'rgba(23,21,42,0.07)', color: '#68647C' }}
                    >
                      <Clock size={10} />
                      {t('detail_min', { n: practice.duration_minutes })}
                    </span>
                  )}
                  {diffKey && (
                    <span
                      className="text-[10px] font-semibold px-2.5 py-1 rounded-full"
                      style={{ background: 'rgba(23,21,42,0.07)', color: '#68647C' }}
                    >
                      {t(diffKey)}
                    </span>
                  )}
                  {slot.completed && (
                    <span
                      className="text-[10px] font-bold px-2.5 py-1 rounded-full"
                      style={{ background: 'rgba(56,104,88,0.15)', color: '#386858' }}
                    >
                      {t('detail_already_done')}
                    </span>
                  )}
                </div>
              </div>

              {/* Body */}
              <div className="px-5 py-4 space-y-5">
                {/* Description */}
                {practice?.description && (
                  <p className="text-base text-ink/85 leading-relaxed">
                    {practice.description}
                  </p>
                )}

                {/* Instructions (step-by-step) */}
                {steps.length > 0 && (
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-wider text-muted mb-3">
                      {t('detail_how_to')}
                    </p>
                    <div className="space-y-3">
                      {steps.map((step, idx) => (
                        <div key={idx} className="flex gap-3">
                          <span
                            className="flex-shrink-0 flex h-6 w-6 items-center justify-center rounded-full text-[11px] font-bold text-white mt-0.5"
                            style={{ background: meta.accent }}
                          >
                            {idx + 1}
                          </span>
                          <p className="text-sm text-ink/85 leading-relaxed">{step}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Growth note */}
                {isGrowth && (
                  <div
                    className="flex items-start gap-3 rounded-[16px] p-4"
                    style={{ background: 'linear-gradient(135deg, #F0EDE4, #EEE4DC)' }}
                  >
                    <span className="text-xl">📖</span>
                    <p className="text-sm text-ink/70 leading-relaxed">{t('detail_growth_note')}</p>
                  </div>
                )}

                {/* Spacer for button */}
                <div className="h-4" />
              </div>

              {/* Footer button */}
              <div
                className="sticky bottom-0 px-5 pt-4"
                style={{ background: 'rgba(254,252,250,0.96)', backdropFilter: 'blur(8px)', borderTop: '1px solid rgba(232,227,218,0.6)', paddingBottom: 'calc(1rem + env(safe-area-inset-bottom))' }}
              >
                {isGrowth ? (
                  <Button
                    size="lg"
                    className="w-full"
                    onClick={() => {
                      onClose()
                      const slug = practice?.academy_article_slug
                      navigate(slug ? `/app/academy/articles/${slug}` : '/app/academy')
                    }}
                  >
                    <BookOpen size={16} />
                    {t('detail_open_academy')}
                  </Button>
                ) : slot.completed ? (
                  <div
                    className="flex items-center justify-center gap-2 rounded-[16px] py-3.5"
                    style={{ background: 'rgba(56,104,88,0.12)', border: '1px solid rgba(56,104,88,0.2)' }}
                  >
                    <CheckCircle2 size={18} className="text-success" />
                    <span className="font-bold text-success text-sm">{t('detail_already_done')}</span>
                  </div>
                ) : (
                  <Button
                    size="lg"
                    className="w-full"
                    onClick={onComplete}
                    loading={isCompleting}
                  >
                    <CheckCircle2 size={16} />
                    {t('detail_mark_done')}
                  </Button>
                )}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

// ── All done banner ───────────────────────────────────────────────────────────

function AllDoneBanner() {
  const { t } = useTranslation('practices')
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease }}
      className="rounded-[24px] p-6 text-center"
      style={{
        background: 'linear-gradient(145deg, #E2EDE8 0%, #D6E8E2 100%)',
        border: '1px solid rgba(56,104,88,0.2)',
        boxShadow: '0 4px 20px rgba(56,104,88,0.10)',
      }}
    >
      <div className="flex justify-center mb-4">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 400, damping: 18, delay: 0.15 }}
          className="flex h-14 w-14 items-center justify-center rounded-full"
          style={{ background: 'rgba(56,104,88,0.15)' }}
        >
          <CheckCircle2 size={28} className="text-success" />
        </motion.div>
      </div>
      <p className="text-base font-bold text-success mb-1">{t('all_done_message')}</p>
      <p className="text-sm text-success/70 mb-3">{t('all_done_subtitle')}</p>
      <div
        className="flex items-center justify-center gap-2 rounded-2xl px-4 py-2.5"
        style={{ background: 'rgba(56,104,88,0.1)' }}
      >
        <Clock size={14} className="text-success/60" />
        <p className="text-xs font-semibold text-success/80">{t('all_done_tomorrow')}</p>
      </div>
    </motion.div>
  )
}

// ── Page header ───────────────────────────────────────────────────────────────

function PageHeader({ todayStr, count, total }: { todayStr: string; count?: number; total?: number }) {
  const { t } = useTranslation('practices')
  const showProgress = typeof count === 'number' && typeof total === 'number' && total > 0
  return (
    <div className="page-hero px-5 pt-6 pb-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div
            className="flex h-10 w-10 items-center justify-center rounded-2xl"
            style={{
              background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
              boxShadow: '0 4px 14px rgba(60,56,136,0.30)',
            }}
          >
            <Sun size={18} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-ink">{t('page_title')}</h1>
            <p className="text-xs text-muted mt-0.5 capitalize">{todayStr}</p>
          </div>
        </div>
        {showProgress && (
          <div
            className="flex items-center gap-1 rounded-full px-3 py-1.5"
            style={{ background: 'rgba(60,56,136,0.1)' }}
          >
            <span className="text-sm font-bold text-primary">{count}</span>
            <span className="text-xs text-muted">/ {total}</span>
          </div>
        )}
      </div>
    </div>
  )
}

// ── Main ──────────────────────────────────────────────────────────────────────

export const PracticesPage = () => {
  const { t, i18n } = useTranslation('practices')
  const qc = useQueryClient()
  const navigate = useNavigate()
  const [selectedSlot, setSelectedSlot] = useState<AssignmentSlot | null>(null)
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const { data: todayRaw, isLoading } = useQuery({
    queryKey: ['practices-today', i18n.language],
    queryFn: PracticesService.getToday,
    enabled: me?.couple?.status === 'active',
  })

  const completeMutation = useMutation({
    mutationFn: ({ assignmentId, slot }: { assignmentId: string; slot: string }) =>
      PracticesService.complete(assignmentId, slot),
    onSuccess: (data) => {
      qc.setQueryData(['practices-today', i18n.language], data)
    },
    onError: () => toast.error(t('error_complete')),
  })

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'
  const todayStr   = new Date().toLocaleDateString(dateLocale, {
    weekday: 'long', day: 'numeric', month: 'long',
  })

  // ── Gate: pending couple ─────────────────────────────────────────────────────
  if (me?.couple?.status === 'pending') {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader todayStr={todayStr} />
        <div className="px-4 flex min-h-[40vh] items-center justify-center">
          <EmptyState
            icon={<Sun />}
            title={t('common:pending_couple_title')}
            description={t('common:invite_partner_first')}
            actionLabel={t('common:invite_partner_btn')}
            onAction={() => navigate('/app/couple')}
          />
        </div>
      </div>
    )
  }

  // ── Gate: no couple ─────────────────────────────────────────────────────────
  if (!me?.couple) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader todayStr={todayStr} />
        <div className="px-4 flex min-h-[40vh] items-center justify-center">
          <EmptyState
            icon={<Sun />}
            title={t('no_couple_title')}
            description={t('no_couple_desc')}
            actionLabel={t('no_couple_btn')}
            onAction={() => navigate('/app/couple')}
          />
        </div>
      </div>
    )
  }

  // ── Loading ─────────────────────────────────────────────────────────────────
  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader todayStr={todayStr} />
        <div className="px-4 flex flex-col gap-3">
          <div className="h-28 rounded-[22px] shimmer" />
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-28 rounded-[20px] shimmer" />
          ))}
        </div>
      </div>
    )
  }

  // ── Gate: diagnostics required ──────────────────────────────────────────────
  if (todayRaw?.requires_diagnostics) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader todayStr={todayStr} />
        <DiagnosticsGate
          partnerADone={todayRaw.partner_a_done ?? false}
          partnerBDone={todayRaw.partner_b_done ?? false}
          iAmPartnerA={todayRaw.i_am_partner_a ?? true}
        />
      </div>
    )
  }

  // ── Main content ────────────────────────────────────────────────────────────
  const practice       = todayRaw
  const plan           = practice?.plan ?? null
  const completedCount = practice?.completed_count ?? 0
  const totalCount     = practice?.total_completable ?? 0
  const allDone        = completedCount === totalCount && totalCount > 0

  const handleComplete = (slot: AssignmentSlot) => {
    if (!slot.completed && slot.slot_type !== 'growth' && practice) {
      completeMutation.mutate(
        { assignmentId: practice.id, slot: slot.slot_type },
        {
          onSuccess: (data) => {
            setSelectedSlot(null)
            const newCompleted = data?.completed_count ?? 0
            const total = data?.total_completable ?? 5
            if (newCompleted >= total) {
              setTimeout(() => celebrateBig(), 100)
            } else {
              celebrateSmall()
            }
          },
        },
      )
    }
  }

  return (
    <>
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader todayStr={todayStr} count={completedCount} total={totalCount} />

        <div className="px-4 flex flex-col gap-3">
          {plan && <FamilyLevelStrip plan={plan} />}

          <AnimatePresence>
            {allDone && <AllDoneBanner />}
          </AnimatePresence>

          {(practice?.slots ?? []).map((item, idx) => (
            <motion.div
              key={item.slot_type}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, ease, delay: 0.08 + idx * 0.05 }}
            >
              <PracticeCard
                item={item}
                onOpen={() => setSelectedSlot(item)}
                onToggle={() => handleComplete(item)}
                loading={
                  completeMutation.isPending &&
                  completeMutation.variables?.slot === item.slot_type
                }
              />
            </motion.div>
          ))}

          {!practice && (
            <div className="rounded-[20px] bg-canvas p-6 text-center border border-sand/60">
              <p className="text-muted text-sm">{t('forming')}</p>
            </div>
          )}
        </div>
      </div>

      <PracticeDetailSheet
        slot={selectedSlot}
        onClose={() => setSelectedSlot(null)}
        onComplete={() => selectedSlot && handleComplete(selectedSlot)}
        isCompleting={
          completeMutation.isPending &&
          completeMutation.variables?.slot === selectedSlot?.slot_type
        }
      />
    </>
  )
}
