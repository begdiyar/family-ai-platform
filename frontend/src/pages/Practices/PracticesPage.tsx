import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import {
  Sun, CheckCircle2, Circle, Sparkles,
  Calendar, Lock, ChevronDown, Check, Sparkles as SparklesAlt,
} from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { PracticesService } from '@/services/practices.service'
import { PlanService } from '@/services/plan.service'
import { CoupleService } from '@/services/couple.service'
import { AnalyticsService } from '@/services/analytics.service'
import { Button } from '@/components/ui/Button'
import { ProgressBar } from '@/components/ui/ProgressBar'
import { Badge } from '@/components/ui/Badge'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { PracticeItem, PlanTask } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease, delay },
})

type Tab = 'today' | 'plan'

const PRACTICE_META: Record<string, { icon: string; bg: string; accent: string }> = {
  question_of_day:        { icon: '💬', bg: 'linear-gradient(135deg, #EDEAF8 0%, #DDE8F2 100%)', accent: '#3C3888' },
  conversation_topic:     { icon: '🗣️', bg: 'linear-gradient(135deg, #DDE8F2 0%, #E6F0FA 100%)', accent: '#385C8A' },
  trust_exercise:         { icon: '🤝', bg: 'linear-gradient(135deg, #E2EDE8 0%, #D2DDF0 100%)', accent: '#386858' },
  communication_exercise: { icon: '📡', bg: 'linear-gradient(135deg, #EEE4DC 0%, #EDEAF8 100%)', accent: '#885040' },
  family_activity:        { icon: '🏠', bg: 'linear-gradient(135deg, #FDF4E8 0%, #EEE4DC 100%)', accent: '#886028' },
  romantic_idea:          { icon: '❤️', bg: 'linear-gradient(135deg, #EDEAF8 0%, #EEE4DC 100%)', accent: '#3C3888' },
}
const DEFAULT_META = { icon: '⭐', bg: 'linear-gradient(135deg, #E8E2D4 0%, #EDEAF8 100%)', accent: '#68647C' }

const TASK_EMOJI: Record<PlanTask['task_type'], string> = {
  exercise: '🏃', question: '💬', reading: '📖', practice: '✨',
}

const WEEK_COLORS = ['#3C3888', '#385C8A', '#386858', '#885040', '#886028', '#3C3888', '#385C8A']

// ── Practice card ─────────────────────────────────────────────────────────────

function PracticeCard({
  item, onToggle, loading,
}: { item: PracticeItem; onToggle: () => void; loading: boolean }) {
  const { t } = useTranslation('practices')
  const meta = PRACTICE_META[item.key] ?? DEFAULT_META
  return (
    <div
      className={`rounded-[20px] p-5 transition-all duration-200 ${item.completed ? 'opacity-55' : 'cursor-pointer hover:-translate-y-0.5'}`}
      style={{
        background: item.completed ? 'rgba(248,246,242,0.9)' : meta.bg,
        border: item.completed ? '1px solid rgba(56,104,88,0.22)' : '1px solid rgba(232,227,218,0.5)',
        boxShadow: item.completed ? 'none' : '0 1px 3px rgba(23,21,42,0.04), 0 4px 14px rgba(23,21,42,0.04)',
      }}
      onClick={onToggle}
    >
      <div className="flex items-start gap-4">
        <span className="text-2xl flex-shrink-0 select-none">{meta.icon}</span>
        <div className="flex-1 min-w-0">
          <p className="mb-1.5 text-[10px] font-bold uppercase tracking-wider" style={{ color: meta.accent }}>
            {t(item.key, { defaultValue: item.key })}
          </p>
          <p className={`text-sm leading-relaxed ${item.completed ? 'text-muted line-through' : 'text-ink'}`}>
            {item.content}
          </p>
        </div>
        <button
          onClick={(e) => { e.stopPropagation(); onToggle() }}
          disabled={item.completed || loading}
          className="flex-shrink-0 mt-0.5"
        >
          {loading ? (
            <div className="h-6 w-6 animate-spin rounded-full border-2" style={{ borderColor: `${meta.accent}40`, borderTopColor: 'transparent' }} />
          ) : item.completed ? (
            <CheckCircle2 size={24} className="text-success" />
          ) : (
            <Circle size={24} style={{ color: `${meta.accent}60` }} className="hover:opacity-80 transition-opacity" />
          )}
        </button>
      </div>
    </div>
  )
}

// ── Tab: Сегодня ──────────────────────────────────────────────────────────────

function TodayTab({ me }: { me: any }) {
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('practices')

  const { data: practice, isLoading } = useQuery({
    queryKey: ['practices-today', i18n.language],
    queryFn: PracticesService.getToday,
    enabled: !!me?.couple,
  })

  const completeMutation = useMutation({
    mutationFn: ({ fieldName }: { fieldName: string }) =>
      PracticesService.complete(practice!.id, fieldName),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['practices-today'] }),
    onError: () => toast.error(t('error_generic')),
  })

  if (!me?.couple) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <EmptyState icon={<Sun />} title={t('no_couple_title')} description={t('no_couple_desc')} />
      </div>
    )
  }

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'
  const today = new Date().toLocaleDateString(dateLocale, { weekday: 'long', day: 'numeric', month: 'long' })
  const completedCount = practice?.items.filter((i) => i.completed).length ?? 0
  const totalCount = practice?.items.length ?? 0
  const progressPct = totalCount > 0 ? (completedCount / totalCount) * 100 : 0
  const allDone = completedCount === totalCount && totalCount > 0

  if (isLoading) return (
    <div className="flex flex-col gap-3">
      {[...Array(5)].map((_, i) => <div key={i} className="h-28 rounded-card shimmer" />)}
    </div>
  )

  if (!practice) return (
    <div className="rounded-[20px] bg-canvas p-6 text-center border border-sand/60">
      <p className="text-muted text-sm">{t('forming')}</p>
    </div>
  )

  return (
    <div className="space-y-3">
      <motion.div {...fadeUp(0)}>
        <div
          className="rounded-[22px] p-5 bg-canvas"
          style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)' }}
        >
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs text-muted capitalize">{today}</span>
            <span className="text-sm font-bold text-primary">{completedCount} / {totalCount}</span>
          </div>
          <div className="h-2 w-full rounded-full overflow-hidden bg-sand/60 mb-1">
            <motion.div
              className="h-full rounded-full"
              style={{ background: 'linear-gradient(90deg, #3C3888, #385C8A)' }}
              initial={{ width: 0 }}
              animate={{ width: `${progressPct}%` }}
              transition={{ duration: 0.7, ease, delay: 0.15 }}
            />
          </div>
          <AnimatePresence>
            {allDone && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-3 flex items-center justify-center gap-2 rounded-2xl py-2.5"
                style={{ background: '#E2EDE8' }}
              >
                <CheckCircle2 size={16} className="text-success" />
                <p className="text-sm font-bold text-success">{t('all_done_title')}</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {practice.is_ai_generated && (
        <motion.div {...fadeUp(0.04)}>
          <div className="flex items-center gap-2 rounded-2xl px-4 py-2.5" style={{ background: '#DDE8F2' }}>
            <Sparkles size={14} className="text-violet" />
            <span className="text-xs font-medium text-violet">{t('ai_badge')}</span>
          </div>
        </motion.div>
      )}

      <div className="flex flex-col gap-3">
        {practice.items.map((item, idx) => (
          <motion.div
            key={item.key}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease, delay: 0.08 + idx * 0.05 }}
          >
            <PracticeCard
              item={item}
              onToggle={() => !item.completed && completeMutation.mutate({ fieldName: item.key })}
              loading={completeMutation.isPending && completeMutation.variables?.fieldName === item.key}
            />
          </motion.div>
        ))}
      </div>
    </div>
  )
}

// ── Tab: План ────────────────────────────────────────────────────────────────

function PlanTab({ me }: { me: any }) {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [expandedWeek, setExpandedWeek] = useState<number>(1)
  const { t } = useTranslation('practices')

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
    mutationFn: ({ taskId }: { taskId: string }) => PlanService.completeTask({ planId: plan!.id, taskId }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['plan', 'current'] }),
    onError: () => toast.error(t('error_generic')),
  })
  const undoMutation = useMutation({
    mutationFn: ({ taskId }: { taskId: string }) => PlanService.undoTask({ planId: plan!.id, taskId }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['plan', 'current'] }),
    onError: () => toast.error(t('error_generic')),
  })

  const myId = me?.id
  const partnerName = couple?.partner_b?.first_name ?? couple?.partner_a?.first_name ?? t('common:partner')
  const myName = me?.first_name ?? t('common:you')

  const assignedLabel = (assigned: PlanTask['assigned_to']): string => {
    if (assigned === 'both') return t('together_label')
    const isMeA = couple?.partner_a?.id === myId
    if (assigned === 'partner_a') return `👤 ${isMeA ? myName : partnerName}`
    if (assigned === 'partner_b') return `👤 ${!isMeA ? myName : partnerName}`
    return assigned
  }

  if (isLoading) return (
    <div className="flex flex-col gap-3">
      {[...Array(3)].map((_, i) => <div key={i} className="h-20 rounded-[20px] shimmer" />)}
    </div>
  )

  if (!plan) {
    const hasAnalytics = (analytics?.count ?? 0) > 0
    return (
      <div className="pt-2">
        {hasAnalytics ? (
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, ease }}>
            <div
              className="rounded-[24px] p-6 text-center"
              style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 100%)', border: '1px solid rgba(60,56,136,0.12)' }}
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
              <p className="text-sm text-muted leading-relaxed mb-6 max-w-xs mx-auto">{t('plan_create_desc')}</p>
              <Button onClick={() => createMutation.mutate(undefined)} loading={createMutation.isPending} size="lg">
                <SparklesAlt size={16} /> {t('plan_create_btn')}
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
    )
  }

  const completedWeeks = plan.weeks.filter((w: any) => w.progress >= 100 && !w.locked).length

  return (
    <div className="space-y-4">
      <motion.div {...fadeUp(0)}>
        <div
          className="rounded-[24px] p-5"
          style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 60%, #D6E8E2 100%)', border: '1px solid rgba(60,56,136,0.12)', boxShadow: '0 4px 20px rgba(60,56,136,0.09)' }}
        >
          <p className="text-sm font-bold text-ink mb-1 truncate">{plan.title}</p>
          <div className="flex items-center justify-between mb-3">
            <div>
              <p className="label-caps text-primary/70 mb-0.5">{t('progress_label')}</p>
              <span className="text-3xl font-bold text-ink" style={{ letterSpacing: '-0.02em' }}>
                {Math.round(plan.overall_progress)}%
              </span>
            </div>
            <div className="text-right">
              <p className="label-caps text-muted mb-0.5">{t('week_label')}</p>
              <p className="text-2xl font-bold text-ink">{plan.current_week} / {plan.duration_weeks}</p>
            </div>
          </div>
          <ProgressBar value={plan.overall_progress} size="md" />
          <div className="mt-3 grid grid-cols-2 gap-2">
            <div className="rounded-[14px] __BGWHITE_ALPHA___ px-3 py-2 text-center">
              <p className="text-lg font-bold text-ink">{completedWeeks}</p>
              <p className="text-[11px] text-muted">{t('weeks_done')}</p>
            </div>
            <div className="rounded-[14px] __BGWHITE_ALPHA___ px-3 py-2 text-center">
              <p className="text-lg font-bold text-ink">
                {plan.weeks.find((w: any) => w.week === plan.current_week)?.tasks.filter((tk: any) => tk.completed_by_me).length ?? 0}
              </p>
              <p className="text-[11px] text-muted">{t('tasks_this_week')}</p>
            </div>
          </div>
        </div>
      </motion.div>

      <p className="label-caps text-muted px-1">{t('weeks_header')}</p>

      <div className="relative">
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
            const color = WEEK_COLORS[idx % WEEK_COLORS.length]

            return (
              <motion.div
                key={week.week}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.35, ease, delay: idx * 0.05 }}
                className={`relative pl-12 ${isLocked ? 'opacity-50' : ''}`}
              >
                <div
                  className={`absolute left-0 flex h-[43px] w-[43px] items-center justify-center rounded-full border-2 bg-canvas transition-all duration-200 ${
                    isCompleted ? 'border-sage-700 bg-sage-50' : isCurrent ? 'border-primary bg-primary-50' : 'border-sand'
                  }`}
                  style={isCurrent ? { boxShadow: '0 0 0 3px rgba(60,56,136,0.14)' } : {}}
                >
                  {isCompleted ? (
                    <Check size={18} className="text-sage-700" />
                  ) : isLocked ? (
                    <Lock size={14} className="text-muted/50" />
                  ) : (
                    <span className={`text-sm font-bold ${isCurrent ? 'text-primary' : 'text-muted'}`}>{week.week}</span>
                  )}
                </div>

                <div
                  className={`rounded-[20px] bg-canvas border overflow-hidden transition-all duration-200 ${
                    isCurrent ? 'border-primary-100 shadow-[0_4px_20px_rgba(60,56,136,0.12)]' : 'border-sand/70 shadow-card'
                  }`}
                >
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

                  <AnimatePresence>
                    {isExpanded && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3, ease }}
                        className="overflow-hidden"
                      >
                        <div className="px-4 pb-4 pt-1 space-y-2" style={{ borderTop: '1px solid rgba(232,227,218,0.7)' }}>
                          {week.tasks.map((task: PlanTask) => (
                            <div
                              key={task.id}
                              className={`flex items-start gap-3 rounded-[14px] p-3 transition-colors ${
                                task.completed_by_me ? 'bg-sage-50' : 'bg-surface'
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
                                  <span className="text-[11px] text-muted font-medium">{assignedLabel(task.assigned_to)}</span>
                                  {task.completed_by_partner && (
                                    <span className="text-[11px] font-semibold text-sage-700">{t('partner_done')}</span>
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
  )
}

// ── Main ──────────────────────────────────────────────────────────────────────

export const PracticesPage = () => {
  const [tab, setTab] = useState<Tab>('today')
  const { t, i18n } = useTranslation('practices')
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'
  const today = new Date().toLocaleDateString(dateLocale, { weekday: 'short', day: 'numeric', month: 'short' })

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <div className="page-hero px-5 pt-6 pb-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-peach" style={{ boxShadow: '0 4px 14px rgba(136,80,64,0.30)' }}>
            <Sun size={18} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
            <p className="text-xs text-muted mt-0.5">{today}</p>
          </div>
        </div>
      </div>

      <div className="mx-5 mb-4 flex rounded-2xl p-1" style={{ background: 'rgba(60,56,136,0.08)' }}>
        {([
          { key: 'today', icon: Sun,      label: t('tab_today') },
          { key: 'plan',  icon: Calendar, label: t('tab_plan') },
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

      <div className="px-4 md:px-5">
        <AnimatePresence mode="wait">
          <motion.div
            key={tab}
            initial={{ opacity: 0, x: tab === 'today' ? -10 : 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.22, ease }}
          >
            {tab === 'today' ? <TodayTab me={me} /> : <PlanTab me={me} />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}
