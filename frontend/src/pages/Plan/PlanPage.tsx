import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import { Calendar, Lock, CheckCircle2, Circle, Sparkles, ChevronDown, Check } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { PlanService } from '@/services/plan.service'
import { AuthService } from '@/services/auth.service'
import { CoupleService } from '@/services/couple.service'
import { AnalyticsService } from '@/services/analytics.service'
import { Button } from '@/components/ui/Button'
import { ProgressBar } from '@/components/ui/ProgressBar'
import { Badge } from '@/components/ui/Badge'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { PlanTask } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

const TASK_EMOJI: Record<PlanTask['task_type'], string> = {
  exercise: '🏃',
  question: '💬',
  reading:  '📖',
  practice: '✨',
}

const WEEK_THEMES_COLORS = [
  '#3C3888', '#385C8A', '#386858',
  '#885040', '#886028', '#3C3888',
  '#385C8A',
]

export const PlanPage = () => {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t } = useTranslation('practices')
  const [expandedWeek, setExpandedWeek] = useState<number>(1)

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: couple } = useQuery({
    queryKey: ['couple'],
    queryFn: CoupleService.getMe,
    enabled: !!me?.couple,
    retry: false,
  })
  const { data: analytics } = useQuery({
    queryKey: ['analytics', 'list'],
    queryFn: AnalyticsService.list,
    enabled: !!me?.couple,
    retry: false,
  })
  const { data: plan, isLoading } = useQuery({
    queryKey: ['plan', 'current'],
    queryFn: PlanService.getCurrent,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: PlanService.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['plan', 'current'] })
      toast.success(t('plan_toast_created'))
    },
    onError: (e: any) => toast.error(e?.response?.data?.message || t('plan_toast_error')),
  })

  const completeMutation = useMutation({
    mutationFn: ({ taskId }: { taskId: string }) =>
      PlanService.completeTask({ planId: plan!.id, taskId }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['plan', 'current'] }),
    onError: () => toast.error(t('error_generic')),
  })

  const undoMutation = useMutation({
    mutationFn: ({ taskId }: { taskId: string }) =>
      PlanService.undoTask({ planId: plan!.id, taskId }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['plan', 'current'] }),
    onError: () => toast.error(t('error_generic')),
  })

  const myId = me?.id
  const partnerName = couple?.partner_b?.first_name ?? couple?.partner_a?.first_name ?? t('common:partner', { defaultValue: 'Партнёр' })
  const myName = me?.first_name ?? t('common:you', { defaultValue: 'Я' })

  const assignedLabel = (assigned: PlanTask['assigned_to']): string => {
    if (assigned === 'both') return t('together_label')
    if (assigned === 'partner_a') return couple?.partner_a?.id === myId ? `👤 ${myName}` : `👤 ${partnerName}`
    if (assigned === 'partner_b') return couple?.partner_b?.id === myId ? `👤 ${myName}` : `👤 ${partnerName}`
    return assigned
  }

  /* ── Header ─────────────────────────────────────────────────────── */
  const header = (
    <div className="page-hero px-5 pt-6 pb-5">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-brand shadow-[0_4px_12px_rgba(60,56,136,0.28)]">
          <Calendar size={16} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-ink">
            {plan?.title ?? t('plan_recovery_title', { defaultValue: 'План восстановления' })}
          </h1>
          {plan && (
            <p className="text-xs text-muted mt-0.5">
              {t('plan_duration_label', { n: plan.duration_weeks, defaultValue: `${plan.duration_weeks} недель · Персональный план` })}
            </p>
          )}
        </div>
      </div>
    </div>
  )

  /* ── Loading ─────────────────────────────────────────────────────── */
  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        {header}
        <div className="px-4 pt-5 space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-20 rounded-[20px] shimmer" />
          ))}
        </div>
      </div>
    )
  }

  /* ── No plan ─────────────────────────────────────────────────────── */
  if (!plan) {
    const hasAnalytics = (analytics?.count ?? 0) > 0
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        {header}
        <div className="px-4 pt-5 max-w-lg">
          {hasAnalytics ? (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, ease }}
            >
              <div
                className="rounded-[24px] p-6 text-center"
                style={{
                  background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 100%)',
                  border: '1px solid rgba(60,56,136,0.12)',
                }}
              >
                <div className="mb-4 flex justify-center">
                  <div
                    className="flex h-16 w-16 items-center justify-center rounded-[20px]"
                    style={{ background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)', boxShadow: '0 8px 24px rgba(60,56,136,0.28)' }}
                  >
                    <span className="text-2xl">📋</span>
                  </div>
                </div>
                <h2 className="text-lg font-bold text-ink mb-2">{t('plan_create_title')}</h2>
                <p className="text-sm text-muted leading-relaxed mb-6 max-w-xs mx-auto">
                  {t('plan_create_desc')}
                </p>
                <Button onClick={() => createMutation.mutate(undefined)} loading={createMutation.isPending} size="lg">
                  <Sparkles size={16} /> {t('plan_create_btn')}
                </Button>
              </div>
            </motion.div>
          ) : (
            <EmptyState
              icon={<Calendar />}
              title={t('plan_no_diagnostics_title')}
              description={t('plan_no_diagnostics_desc')}
              actionLabel={t('plan_no_diagnostics_btn')}
              onAction={() => navigate('/app/diagnostics')}
            />
          )}
        </div>
      </div>
    )
  }

  /* ── Plan journey ────────────────────────────────────────────────── */
  const completedWeeks = plan.weeks.filter((w: any) => w.progress >= 100 && !w.locked).length

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {header}

      <div className="px-4 pt-4 md:px-5">

        {/* ── Progress hero ──────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease }}
        >
          <div
            className="rounded-[24px] p-5 mb-5"
            style={{
              background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 60%, #D6E8E2 100%)',
              border: '1px solid rgba(60,56,136,0.12)',
              boxShadow: '0 4px 20px rgba(60,56,136,0.09)',
            }}
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="label-caps text-primary/70">{t('progress_label')}</p>
                <div className="flex items-baseline gap-1 mt-0.5">
                  <span className="text-3xl font-bold text-ink" style={{ letterSpacing: '-0.02em' }}>
                    {Math.round(plan.overall_progress)}%
                  </span>
                </div>
              </div>
              <div className="text-right">
                <p className="label-caps text-muted">{t('week_label')}</p>
                <p className="text-2xl font-bold text-ink mt-0.5">{plan.current_week} / {plan.duration_weeks}</p>
              </div>
            </div>
            <ProgressBar value={plan.overall_progress} size="md" />
            <div className="mt-3 flex gap-3">
              <div className="flex-1 rounded-[14px] __BGWHITE_ALPHA___ px-3 py-2 text-center">
                <p className="text-lg font-bold text-ink">{completedWeeks}</p>
                <p className="text-[11px] text-muted">{t('weeks_done')}</p>
              </div>
              <div className="flex-1 rounded-[14px] __BGWHITE_ALPHA___ px-3 py-2 text-center">
                <p className="text-lg font-bold text-ink">
                  {plan.weeks.find((w: any) => w.week === plan.current_week)?.tasks.filter((task: any) => task.completed_by_me).length ?? 0}
                </p>
                <p className="text-[11px] text-muted">{t('tasks_this_week')}</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* ── Journey timeline ───────────────────────────────────────── */}
        <p className="label-caps text-muted mb-4 px-1">{t('weeks_header')}</p>

        <div className="relative">
          {/* Vertical track line */}
          <div
            className="absolute left-[21px] top-4 bottom-4 w-0.5"
            style={{ background: 'linear-gradient(180deg, rgba(60,56,136,0.25) 0%, rgba(232,227,218,0.6) 100%)' }}
          />

          <div className="space-y-3">
            {plan.weeks.map((week: any, idx: number) => {
              const isCompleted = week.progress >= 100 && !week.locked
              const isCurrent = week.week === plan.current_week
              const isLocked = week.locked
              const isExpanded = expandedWeek === week.week && !isLocked
              const color = WEEK_THEMES_COLORS[idx % WEEK_THEMES_COLORS.length]

              return (
                <motion.div
                  key={week.week}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.35, ease, delay: idx * 0.05 }}
                  className={`relative pl-12 ${isLocked ? 'opacity-50' : ''}`}
                >
                  {/* Circle indicator */}
                  <div
                    className={`absolute left-0 flex h-[43px] w-[43px] items-center justify-center rounded-full border-2 bg-canvas transition-all duration-200 ${
                      isCompleted
                        ? 'border-sage-700 bg-sage-50'
                        : isCurrent
                        ? 'border-primary bg-primary-50'
                        : isLocked
                        ? 'border-sand'
                        : 'border-sand'
                    }`}
                    style={isCurrent ? { boxShadow: '0 0 0 3px rgba(60,56,136,0.14)' } : {}}
                  >
                    {isCompleted ? (
                      <Check size={18} className="text-sage-700" />
                    ) : isLocked ? (
                      <Lock size={14} className="text-muted/50" />
                    ) : (
                      <span className={`text-sm font-bold ${isCurrent ? 'text-primary' : 'text-muted'}`}>
                        {week.week}
                      </span>
                    )}
                  </div>

                  {/* Week card */}
                  <div
                    className={`rounded-[20px] bg-canvas border overflow-hidden transition-all duration-200 ${
                      isCurrent
                        ? 'border-primary-100 shadow-[0_4px_20px_rgba(60,56,136,0.12)]'
                        : 'border-sand/70 shadow-card'
                    }`}
                  >
                    {/* Week header */}
                    <button
                      className="flex w-full items-center gap-3 p-4 text-left"
                      onClick={() => !isLocked && setExpandedWeek(isExpanded ? 0 : week.week)}
                      disabled={isLocked}
                    >
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1.5">
                          {isCurrent && <Badge variant="primary">{t('current_badge')}</Badge>}
                          {isCompleted && <Badge variant="success">{t('completed_badge')}</Badge>}
                        </div>
                        <p className="font-bold text-ink text-sm leading-snug truncate">
                          {t('week_n', { n: week.week })}: {week.theme}
                        </p>
                        <div className="mt-2">
                          <ProgressBar value={week.progress} size="xs" color={isCompleted ? 'success' : 'primary'} />
                        </div>
                      </div>
                      {!isLocked && (
                        <ChevronDown
                          size={16}
                          className={`shrink-0 text-muted transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`}
                        />
                      )}
                    </button>

                    {/* Tasks (expanded) */}
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3, ease }}
                          className="overflow-hidden"
                        >
                          <div
                            className="px-4 pb-4 pt-1 space-y-2"
                            style={{ borderTop: '1px solid rgba(232,227,218,0.7)' }}
                          >
                            {week.tasks.map((task: PlanTask) => (
                              <div
                                key={task.id}
                                className={`flex items-start gap-3 rounded-[14px] p-3 transition-colors ${
                                  task.completed_by_me
                                    ? 'bg-sage-50'
                                    : 'bg-surface'
                                }`}
                              >
                                <button
                                  onClick={() =>
                                    task.completed_by_me
                                      ? undoMutation.mutate({ taskId: task.id })
                                      : completeMutation.mutate({ taskId: task.id })
                                  }
                                  className="mt-0.5 shrink-0 transition-transform hover:scale-110"
                                >
                                  {task.completed_by_me ? (
                                    <CheckCircle2 size={22} className="text-sage-700" />
                                  ) : (
                                    <Circle size={22} className="text-sand hover:text-primary transition-colors" />
                                  )}
                                </button>

                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center gap-1.5 mb-0.5">
                                    <span className="text-sm">{TASK_EMOJI[task.task_type]}</span>
                                    <p className={`text-sm font-semibold leading-snug ${
                                      task.completed_by_me ? 'line-through text-muted' : 'text-ink'
                                    }`}>
                                      {task.title}
                                    </p>
                                  </div>
                                  {task.description && (
                                    <p className="text-xs text-muted leading-relaxed">{task.description}</p>
                                  )}
                                  <div className="mt-1.5 flex items-center gap-2">
                                    <span className="text-[11px] text-muted font-medium">
                                      {assignedLabel(task.assigned_to)}
                                    </span>
                                    {task.completed_by_partner && (
                                      <span className="text-[11px] font-semibold text-sage-700">
                                        {t('partner_done')}
                                      </span>
                                    )}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
