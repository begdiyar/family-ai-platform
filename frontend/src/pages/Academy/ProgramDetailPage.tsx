import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, CheckCircle2, Lock, Play, ChevronDown, ChevronUp } from 'lucide-react'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { AcademyService } from '@/services/academy.service'
import { Button } from '@/components/ui/Button'
import { celebrateSmall, celebrateBig } from '@/lib/confetti'
import type { ProgramDayItem } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.38, ease, delay },
})

function DayCard({
  day,
  isLocked,
  isCurrent,
  onComplete,
  isCompleting,
}: {
  day: ProgramDayItem
  isLocked: boolean
  isCurrent: boolean
  onComplete: (reflection: string) => void
  isCompleting: boolean
}) {
  const { t } = useTranslation('academy')
  const [expanded, setExpanded] = useState(isCurrent)
  const [reflection, setReflection] = useState('')
  const [showExercise, setShowExercise] = useState(false)

  return (
    <div
      className="rounded-[20px] overflow-hidden"
      style={{
        background: day.is_completed ? '#E8E2D4' : 'white',
        border: isCurrent
          ? '1px solid rgba(60,56,136,0.30)'
          : day.is_completed
          ? '1px solid rgba(232,227,218,0.4)'
          : '1px solid rgba(232,227,218,0.6)',
        boxShadow: isCurrent ? '0 4px 16px rgba(60,56,136,0.12)' : '0 1px 3px rgba(23,21,42,0.03)',
        opacity: isLocked ? 0.5 : 1,
      }}
    >
      <button
        className="w-full flex items-center gap-3 p-4"
        onClick={() => !isLocked && setExpanded((v) => !v)}
        disabled={isLocked}
      >
        <div
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-bold"
          style={
            day.is_completed
              ? { background: '#386858', color: 'white' }
              : isCurrent
              ? { background: 'linear-gradient(135deg, #3C3888, #385C8A)', color: 'white' }
              : isLocked
              ? { background: '#EDEAF8', color: '#B0AACC' }
              : { background: '#EDEAF8', color: '#3C3888' }
          }
        >
          {day.is_completed ? '✓' : isLocked ? <Lock size={10} /> : day.day_number}
        </div>
        <div className="flex-1 text-left min-w-0">
          <p className={`text-sm font-semibold leading-snug ${day.is_completed ? 'text-muted' : 'text-ink'}`}>
            {t('day_label', { n: day.day_number, defaultValue: `День ${day.day_number}` })}: {day.title}
          </p>
          {isCurrent && !day.is_completed && (
            <p className="text-[10px] font-bold text-primary mt-0.5">{t('current_day_label', { defaultValue: 'Текущий день' })}</p>
          )}
        </div>
        {!isLocked && (
          expanded
            ? <ChevronUp size={14} className="text-muted shrink-0" />
            : <ChevronDown size={14} className="text-muted shrink-0" />
        )}
      </button>

      <AnimatePresence>
        {expanded && !isLocked && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease }}
          >
            <div className="px-4 pb-4 space-y-3">
              <div className="h-px bg-sand/60" />

              {/* Material */}
              <div>
                <p className="label-caps text-primary mb-2">{t('day_material_label', { defaultValue: 'Материал дня' })}</p>
                <p className="text-sm text-ink leading-relaxed">{day.material}</p>
              </div>

              {/* Exercise toggle */}
              <button
                onClick={() => setShowExercise((v) => !v)}
                className="flex items-center gap-2 text-sm font-semibold text-primary hover:opacity-80 transition-opacity"
              >
                {showExercise ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                {showExercise
                  ? t('hide_exercise', { defaultValue: 'Скрыть упражнение' })
                  : t('show_exercise', { defaultValue: 'Показать упражнение' })}
              </button>

              <AnimatePresence>
                {showExercise && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2, ease }}
                  >
                    <div
                      className="rounded-[16px] p-3"
                      style={{ background: 'linear-gradient(135deg, #E2EDE8, #D2DDF0)', border: '1px solid rgba(56,104,88,0.12)' }}
                    >
                      <p className="label-caps text-success mb-2">{t('step_exercise', { defaultValue: 'Упражнение' })}</p>
                      <p className="text-sm text-ink leading-relaxed">{day.exercise}</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Complete form */}
              {!day.is_completed && (
                <div className="space-y-2 pt-1">
                  <p className="label-caps text-muted">{day.reflection_prompt}</p>
                  <textarea
                    value={reflection}
                    onChange={(e) => setReflection(e.target.value)}
                    placeholder={t('thoughts_placeholder', { defaultValue: 'Запишите ваши мысли...' })}
                    rows={2}
                    className="w-full resize-none rounded-[12px] px-3 py-2.5 text-sm text-ink placeholder:text-muted/60 focus:outline-none transition-all"
                    style={{
                      border: '1.5px solid rgba(232,227,218,0.8)',
                      background: 'white',
                    }}
                    onFocus={(e) => { e.currentTarget.style.borderColor = 'rgba(60,56,136,0.4)' }}
                    onBlur={(e) => { e.currentTarget.style.borderColor = 'rgba(232,227,218,0.8)' }}
                  />
                  <Button
                    size="sm"
                    fullWidth
                    onClick={() => onComplete(reflection)}
                    loading={isCompleting}
                  >
                    <CheckCircle2 size={13} /> {t('day_done_btn', { defaultValue: 'День выполнен' })}
                  </Button>
                </div>
              )}

              {day.is_completed && (
                <div className="flex items-center gap-2 text-xs text-success font-semibold">
                  <CheckCircle2 size={13} /> {t('done_label', { defaultValue: 'Выполнено' })}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export const ProgramDetailPage = () => {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('academy')

  const { data: program, isLoading } = useQuery({
    queryKey: ['academy-program', slug, i18n.language],
    queryFn: () => AcademyService.getProgram(slug!),
    enabled: !!slug,
  })

  const [completingDay, setCompletingDay] = useState<number | null>(null)

  const enrollMutation = useMutation({
    mutationFn: () => AcademyService.enrollProgram(slug!),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['academy-program', slug] })
      qc.invalidateQueries({ queryKey: ['academy-programs'] })
      qc.invalidateQueries({ queryKey: ['academy-active-program'] })
      toast.success(t('toast_enrolled', { defaultValue: 'Записались на программу!' }))
    },
    onError: (e: any) => toast.error(e?.response?.data?.message || t('common:error', { defaultValue: 'Ошибка' })),
  })

  const completeDayMutation = useMutation({
    mutationFn: ({ day, reflection }: { day: number; reflection: string }) =>
      AcademyService.completeProgramDay(slug!, day, reflection),
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['academy-program', slug] })
      qc.invalidateQueries({ queryKey: ['academy-active-program'] })
      qc.invalidateQueries({ queryKey: ['academy-progress'] })
      toast.success(t('toast_day_done', { defaultValue: 'День засчитан!' }))
      if (data?.program_completed) {
        setTimeout(() => celebrateBig(), 100)
      } else {
        celebrateSmall()
      }
      setCompletingDay(null)
    },
  })

  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="h-48 shimmer" />
        <div className="px-4 pt-4 space-y-3">
          {[...Array(5)].map((_, i) => <div key={i} className="h-16 rounded-[20px] shimmer" />)}
        </div>
      </div>
    )
  }

  if (!program) {
    return (
      <div className="flex min-h-full items-center justify-center p-6">
        <p className="text-sm text-muted">{t('program_not_found', { defaultValue: 'Программа не найдена' })}</p>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {/* Hero */}
      <div
        className="relative px-5 pt-6 pb-8"
        style={{ background: program.cover_gradient }}
      >
        <button
          onClick={() => navigate('/app/academy')}
          className="mb-4 flex items-center gap-1 text-sm font-medium text-white/70 hover:text-white transition-colors"
        >
          <ChevronLeft size={16} /> {t('title')}
        </button>
        <span className="label-caps text-white/60 mb-2 block">
          {program.duration_days} {t('duration_days_unit', { defaultValue: 'дней' })}
        </span>
        <h1 className="text-xl font-bold text-white mb-2 leading-snug">{program.title}</h1>
        <p className="text-sm text-white/75 leading-relaxed mb-4">{program.description}</p>

        {program.is_enrolled && program.enrollment_status !== 'completed' && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs text-white/70 mb-2">
              <span>{t('progress_label', { defaultValue: 'Прогресс' })}</span>
              <span>{t('active_course_day', { day: program.current_day, total: program.duration_days })}</span>
            </div>
            <div className="h-2 w-full rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.25)' }}>
              <div
                className="h-full rounded-full bg-canvas transition-all duration-500"
                style={{ width: `${program.progress_percent}%` }}
              />
            </div>
          </div>
        )}

        {program.enrollment_status === 'completed' && (
          <div
            className="inline-flex items-center gap-2 rounded-2xl px-4 py-2 text-sm font-bold"
            style={{ background: 'rgba(255,255,255,0.25)', color: 'white' }}
          >
            <CheckCircle2 size={15} /> {t('program_completed', { defaultValue: 'Программа завершена!' })}
          </div>
        )}

        {!program.is_enrolled && (
          <Button
            onClick={() => enrollMutation.mutate()}
            loading={enrollMutation.isPending}
            className="bg-canvas text-primary hover:__BGWHITE_ALPHA___"
          >
            <Play size={14} /> {t('enroll_btn', { defaultValue: 'Начать программу' })}
          </Button>
        )}
      </div>

      {/* Days */}
      <div className="px-4 pt-4 md:px-5 space-y-2 max-w-2xl">
        {!program.is_enrolled && (
          <motion.div {...fadeUp(0)}>
            <div
              className="rounded-[20px] p-4 mb-2"
              style={{ background: '#EDEAF8', border: '1px solid rgba(60,56,136,0.12)' }}
            >
              <p className="text-sm text-primary font-medium">{t('enroll_hint', { defaultValue: 'Запишитесь на программу, чтобы начать работу с днями' })}</p>
            </div>
          </motion.div>
        )}

        {program.days?.map((day, i) => {
          const isCompleted = day.is_completed
          const isCurrent = program.is_enrolled && program.current_day === day.day_number && !isCompleted
          const isLocked = !program.is_enrolled || (day.day_number > program.current_day && !isCompleted)

          return (
            <motion.div
              key={day.id}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.28, ease, delay: i * 0.03 }}
            >
              <DayCard
                day={day}
                isLocked={isLocked}
                isCurrent={isCurrent}
                onComplete={(reflection) => {
                  setCompletingDay(day.day_number)
                  completeDayMutation.mutate({ day: day.day_number, reflection })
                }}
                isCompleting={completingDay === day.day_number && completeDayMutation.isPending}
              />
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
