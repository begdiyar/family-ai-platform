import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, Clock, CheckCircle2, Play, Dumbbell } from 'lucide-react'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { AcademyService } from '@/services/academy.service'
import { Button } from '@/components/ui/Button'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.38, ease, delay },
})

const SKILL_META: Record<string, { icon: string; color: string; bg: string }> = {
  active_listening:      { icon: '👂', color: '#3C3888', bg: 'linear-gradient(135deg, #EDEAF8, #DDE8F2)' },
  emotion_management:    { icon: '🧠', color: '#385C8A', bg: 'linear-gradient(135deg, #DDE8F2, #EDEAF8)' },
  gratitude:             { icon: '🙏', color: '#386858', bg: 'linear-gradient(135deg, #E2EDE8, #D2DDF0)' },
  partner_support:       { icon: '🫂', color: '#885040', bg: 'linear-gradient(135deg, #EEE4DC, #EDEAF8)' },
  constructive_dialogue: { icon: '💬', color: '#3C3888', bg: 'linear-gradient(135deg, #EDEAF8, #DDE8F2)' },
  conflict_resolution:   { icon: '🕊️', color: '#386858', bg: 'linear-gradient(135deg, #E2EDE8, #EEE4DC)' },
  joint_planning:        { icon: '📅', color: '#886028', bg: 'linear-gradient(135deg, #FDF4E8, #DDE8F2)' },
}

type TrainingView = 'theory' | 'exercise' | 'reflection' | 'done'

function MarkdownSection({ text }: { text: string }) {
  const lines = text.split('\n')
  const parseInline = (s: string) => {
    const parts = s.split(/(\*\*[^*]+\*\*)/g)
    return parts.map((p, j) =>
      p.startsWith('**') ? <strong key={j}>{p.slice(2, -2)}</strong> : <span key={j}>{p}</span>
    )
  }
  return (
    <div className="space-y-1">
      {lines.map((line, i) => {
        if (line.startsWith('## ')) return <h2 key={i} className="text-sm font-bold text-ink mt-4 mb-1.5">{line.slice(3)}</h2>
        if (line.startsWith('### ')) return <h3 key={i} className="text-xs font-bold text-ink mt-3 mb-1">{line.slice(4)}</h3>
        if (line.startsWith('**') && line.endsWith('**')) return <p key={i} className="text-sm font-bold text-ink">{line.slice(2, -2)}</p>
        if (line.startsWith('- ') || line.startsWith('* '))
          return (
            <li key={i} className="flex gap-2 text-sm text-ink leading-relaxed">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
              <span>{parseInline(line.slice(2))}</span>
            </li>
          )
        if (line.trim() === '') return <div key={i} className="h-1.5" />
        return <p key={i} className="text-sm text-ink leading-relaxed">{parseInline(line)}</p>
      })}
    </div>
  )
}

export const TrainingDetailPage = () => {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('academy')

  const [view, setView] = useState<TrainingView>('theory')
  const [reflection, setReflection] = useState('')

  const { data: training, isLoading } = useQuery({
    queryKey: ['academy-training', slug, i18n.language],
    queryFn: () => AcademyService.getTraining(slug!),
    enabled: !!slug,
  })

  const startMutation = useMutation({
    mutationFn: () => AcademyService.startTraining(slug!),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['academy-training', slug] })
      setView('exercise')
    },
  })

  const completeMutation = useMutation({
    mutationFn: () => AcademyService.completeTraining(slug!, reflection),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['academy-training', slug] })
      qc.invalidateQueries({ queryKey: ['academy-trainings'] })
      qc.invalidateQueries({ queryKey: ['academy-progress'] })
      toast.success(t('toast_training_done', { defaultValue: 'Тренировка завершена!' }))
      setView('done')
    },
  })

  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="page-hero px-5 pt-6 pb-5">
          <div className="h-6 w-32 rounded-xl shimmer" />
        </div>
        <div className="px-4 pt-4 space-y-4">
          {[...Array(4)].map((_, i) => <div key={i} className="h-24 rounded-[20px] shimmer" />)}
        </div>
      </div>
    )
  }

  if (!training) {
    return (
      <div className="flex min-h-full items-center justify-center p-6">
        <p className="text-sm text-muted">{t('training_not_found', { defaultValue: 'Тренировка не найдена' })}</p>
      </div>
    )
  }

  const skillMeta = SKILL_META[training.skill_type] ?? { icon: '💪', color: '#3C3888', bg: '#EDEAF8' }
  const skillLabel = t(`skills.${training.skill_type}`, { defaultValue: training.skill_type })
  const steps: TrainingView[] = ['theory', 'exercise', 'reflection', 'done']
  const stepIndex = steps.indexOf(view)

  const STEP_LABELS = [
    t('step_theory', { defaultValue: 'Теория' }),
    t('step_exercise', { defaultValue: 'Упражнение' }),
    t('step_reflection', { defaultValue: 'Рефлексия' }),
  ]

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {/* Header */}
      <div className="page-hero px-5 pt-6 pb-5">
        <button
          onClick={() => navigate('/app/academy')}
          className="mb-3 flex items-center gap-1 text-sm font-medium text-muted hover:text-primary transition-colors"
        >
          <ChevronLeft size={16} /> {t('title')}
        </button>
        <div className="flex items-center gap-3 mb-1">
          <div
            className="flex h-12 w-12 items-center justify-center rounded-2xl text-2xl"
            style={{ background: skillMeta.bg, border: '1px solid rgba(60,56,136,0.10)' }}
          >
            {skillMeta.icon}
          </div>
          <div>
            <p className="label-caps mb-0.5" style={{ color: skillMeta.color }}>{skillLabel}</p>
            <h1 className="text-lg font-bold text-ink leading-snug">{training.title}</h1>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs text-muted mt-2">
          <span className="flex items-center gap-1">
            <Clock size={12} />
            {training.duration_minutes} {t('training_min', { defaultValue: 'мин' })}
          </span>
          {training.is_completed && (
            <span className="flex items-center gap-1 text-success font-semibold">
              <CheckCircle2 size={12} /> {t('training_completed', { defaultValue: 'Завершена' })}
            </span>
          )}
        </div>
      </div>

      <div className="px-4 md:px-5 max-w-2xl">
        {/* Step indicator */}
        {view !== 'done' && !training.is_completed && (
          <motion.div {...fadeUp(0)} className="flex items-center gap-2 mb-5">
            {STEP_LABELS.map((label, i) => (
              <div key={i} className="flex items-center gap-2">
                <div
                  className="flex h-6 w-6 items-center justify-center rounded-full text-[10px] font-bold"
                  style={
                    i < stepIndex
                      ? { background: '#386858', color: 'white' }
                      : i === stepIndex
                      ? { background: 'linear-gradient(135deg, #3C3888, #385C8A)', color: 'white' }
                      : { background: '#EDEAF8', color: '#68647C' }
                  }
                >
                  {i < stepIndex ? '✓' : i + 1}
                </div>
                <span className={`text-xs font-semibold ${i === stepIndex ? 'text-ink' : 'text-muted'}`}>{label}</span>
                {i < 2 && <div className="h-px w-6 bg-sand" />}
              </div>
            ))}
          </motion.div>
        )}

        <AnimatePresence mode="wait">
          {/* Theory */}
          {view === 'theory' && (
            <motion.div
              key="theory"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.28, ease }}
              className="space-y-4"
            >
              <div
                className="rounded-[22px] bg-canvas p-5"
                style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
              >
                <p className="label-caps text-primary mb-3 flex items-center gap-2">
                  <Dumbbell size={12} /> {t('theory_label', { defaultValue: 'Теоретическая часть' })}
                </p>
                <MarkdownSection text={training.theory ?? ''} />
              </div>

              {!training.is_completed ? (
                <Button fullWidth onClick={() => startMutation.mutate()} loading={startMutation.isPending}>
                  <Play size={14} /> {t('to_exercise_btn', { defaultValue: 'К упражнению' })}
                </Button>
              ) : (
                <div
                  className="rounded-[16px] p-4 flex items-center gap-3"
                  style={{ background: '#E2EDE8', border: '1px solid rgba(56,104,88,0.20)' }}
                >
                  <CheckCircle2 size={16} className="text-success" />
                  <p className="text-sm font-semibold text-success">{t('training_already_done', { defaultValue: 'Тренировка уже завершена' })}</p>
                </div>
              )}
            </motion.div>
          )}

          {/* Exercise */}
          {view === 'exercise' && (
            <motion.div
              key="exercise"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.28, ease }}
              className="space-y-4"
            >
              <div
                className="rounded-[22px] bg-canvas p-5"
                style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
              >
                <p className="label-caps text-primary mb-3">{t('step_exercise', { defaultValue: 'Упражнение' })}</p>
                <MarkdownSection text={training.exercise_instruction ?? ''} />
              </div>
              <div
                className="rounded-[20px] p-4"
                style={{ background: '#FDF4E8', border: '1px solid rgba(184,144,74,0.15)' }}
              >
                <p className="label-caps text-warning mb-2">{t('check_label', { defaultValue: 'Как проверить выполнение' })}</p>
                <p className="text-sm text-ink leading-relaxed">{training.completion_check}</p>
              </div>
              <Button fullWidth onClick={() => setView('reflection')}>
                {t('exercise_done_btn', { defaultValue: 'Упражнение выполнено →' })}
              </Button>
            </motion.div>
          )}

          {/* Reflection */}
          {view === 'reflection' && (
            <motion.div
              key="reflection"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.28, ease }}
              className="space-y-4"
            >
              <div
                className="rounded-[22px] p-5"
                style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)', border: '1px solid rgba(60,56,136,0.10)' }}
              >
                <p className="text-sm font-bold text-ink mb-3">{t('step_reflection', { defaultValue: 'Рефлексия' })}</p>
                <p className="text-sm text-ink mb-4">{t('reflect_prompt', { defaultValue: 'Как прошло упражнение? Что вы заметили? Что хотите применить в жизни?' })}</p>
                <textarea
                  value={reflection}
                  onChange={(e) => setReflection(e.target.value)}
                  placeholder={t('reflect_thoughts_placeholder', { defaultValue: 'Ваши мысли о тренировке...' })}
                  rows={4}
                  className="w-full resize-none rounded-[14px] px-4 py-3 text-sm text-ink placeholder:text-muted/60 focus:outline-none transition-all"
                  style={{
                    border: '1.5px solid rgba(60,56,136,0.20)',
                    background: 'rgba(255,255,255,0.85)',
                  }}
                  onFocus={(e) => { e.currentTarget.style.borderColor = 'rgba(60,56,136,0.5)'; e.currentTarget.style.boxShadow = '0 0 0 3px rgba(60,56,136,0.10)' }}
                  onBlur={(e) => { e.currentTarget.style.borderColor = 'rgba(60,56,136,0.20)'; e.currentTarget.style.boxShadow = 'none' }}
                />
              </div>
              <Button
                fullWidth
                onClick={() => completeMutation.mutate()}
                loading={completeMutation.isPending}
              >
                <CheckCircle2 size={14} /> {t('complete_training_btn', { defaultValue: 'Завершить тренировку' })}
              </Button>
              <button
                onClick={() => setView('reflection')}
                className="w-full text-center text-xs text-muted hover:text-primary transition-colors py-1"
              >
                {t('skip_reflection_btn', { defaultValue: 'Пропустить рефлексию' })}
              </button>
            </motion.div>
          )}

          {/* Done */}
          {view === 'done' && (
            <motion.div
              key="done"
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.35, ease }}
              className="space-y-4"
            >
              <div
                className="rounded-[22px] p-6 text-center"
                style={{ background: 'linear-gradient(135deg, #E2EDE8, #D2DDF0)', border: '1px solid rgba(56,104,88,0.15)' }}
              >
                <span className="text-5xl block mb-3">🏆</span>
                <p className="text-lg font-bold text-ink mb-1">{t('training_done_title', { defaultValue: 'Тренировка завершена!' })}</p>
                <p className="text-sm text-muted">{t('skill_mastered', { label: skillLabel, defaultValue: `Навык «${skillLabel}» отмечен как освоенный` })}</p>
              </div>
              <Button variant="secondary" fullWidth onClick={() => navigate('/app/academy')}>
                {t('back_to_academy_btn', { defaultValue: 'Вернуться в Академию' })}
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
