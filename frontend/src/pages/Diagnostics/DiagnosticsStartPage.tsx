import { useState, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { DiagnosticsService } from '@/services/diagnostics.service'
import { Button } from '@/components/ui/Button'
import { ProgressBar } from '@/components/ui/ProgressBar'
import type { Question } from '@/types/domain.types'

type AnswerPayload = { value_scale?: number; value_choice?: string; value_text?: string }

const STORAGE_KEY = 'diag_progress'

const saveProgress = (sessionId: string, index: number, answers: Record<string, AnswerPayload>) => {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ sessionId, index, answers }))
  } catch {}
}

const loadProgress = () => {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as { sessionId: string; index: number; answers: Record<string, AnswerPayload> }
  } catch {
    return null
  }
}

const clearProgress = () => {
  try { sessionStorage.removeItem(STORAGE_KEY) } catch {}
}

export const DiagnosticsStartPage = () => {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t } = useTranslation('diagnostics')

  const saved = loadProgress()
  const [currentIndex, setCurrentIndex] = useState(saved?.index ?? 0)
  const [answers, setAnswers] = useState<Record<string, AnswerPayload>>(saved?.answers ?? {})
  const [textInput, setTextInput] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(saved?.sessionId ?? null)

  const { data: questions } = useQuery({
    queryKey: ['questions'],
    queryFn: DiagnosticsService.getQuestions,
  })

  const startMutation = useMutation({
    mutationFn: DiagnosticsService.startSession,
    onSuccess: (session) => {
      clearProgress()
      setAnswers({})
      setCurrentIndex(0)
      setSessionId(session.id)
    },
    onError: async () => {
      try {
        const session = await DiagnosticsService.getCurrentSession()
        setSessionId(session.id)
        setCurrentIndex(session.answers_count)
      } catch {
        toast.error(t('toast_start_error'))
      }
    },
  })

  const completeMutation = useMutation({
    mutationFn: () => DiagnosticsService.completeSession(sessionId!),
    onSuccess: (result) => {
      qc.invalidateQueries({ queryKey: ['session'] })
      if (result.partner_completed) {
        toast.success(t('toast_both_done'))
        navigate('/app/analytics')
      } else {
        toast.success(t('toast_waiting_partner'))
        navigate('/app/diagnostics')
      }
    },
  })

  const allQuestions = questions?.zones.flatMap((z) => z.questions) ?? []
  const total = allQuestions.length
  const current: Question | undefined = allQuestions[currentIndex]

  const handleStart = () => startMutation.mutate()

  const advance = (qId: string, payload: AnswerPayload) => {
    const newAnswers = { ...answers, [qId]: payload }
    const nextIndex = currentIndex < total - 1 ? currentIndex + 1 : currentIndex

    setAnswers(newAnswers)
    setTextInput('')

    if (sessionId) saveProgress(sessionId, nextIndex, newAnswers)

    DiagnosticsService.saveAnswers(sessionId!, [{ question_id: qId, ...payload }]).catch(() => {
      toast.error(t('toast_save_error'))
    })

    if (currentIndex < total - 1) {
      setCurrentIndex(nextIndex)
    } else {
      clearProgress()
      completeMutation.mutate()
    }
  }

  const handleScaleAnswer = useCallback((value: number) => {
    if (!current || !sessionId) return
    advance(current.id, { value_scale: value })
  }, [current, sessionId, currentIndex, total, answers])

  const handleChoiceAnswer = (option: string) => {
    if (!current || !sessionId) return
    advance(current.id, { value_choice: option })
  }

  const handleTextAnswer = () => {
    if (!current || !sessionId || !textInput.trim()) return
    advance(current.id, { value_text: textInput.trim() })
  }

  if (!sessionId) {
    return (
      <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden p-6 text-center">
        <div className="absolute inset-0 bg-gradient-hero" />
        <div className="absolute inset-0 bg-dots-light opacity-25" />
        <div className="absolute -top-32 -left-32 h-72 w-72 rounded-full bg-primary/10 blur-[80px] pointer-events-none" />
        <div className="absolute -bottom-32 -right-32 h-72 w-72 rounded-full bg-violet/10 blur-[80px] pointer-events-none" />

        <div
          className="relative w-full max-w-sm rounded-[32px] px-8 py-10 backdrop-blur-xl"
          style={{
            background: 'rgba(255,255,255,0.88)',
            border: '1px solid rgba(255,255,255,0.80)',
            boxShadow: '0 8px 40px rgba(60,56,136,0.12), 0 1px 3px rgba(23,21,42,0.06)',
          }}
        >
          <div className="mb-5 flex justify-center">
            <div
              className="flex h-16 w-16 items-center justify-center rounded-3xl bg-gradient-brand"
              style={{ boxShadow: '0 8px 24px rgba(60,56,136,0.35)' }}
            >
              <span className="text-2xl select-none">📋</span>
            </div>
          </div>
          <h2 className="mb-2 text-2xl font-bold text-ink">{t('start_title')}</h2>
          <p className="mb-1 text-sm text-muted">{t('start_count')}</p>
          <p className="mb-6 text-xs text-muted">{t('start_privacy')}</p>
          <Button fullWidth size="lg" onClick={handleStart} loading={startMutation.isPending}>
            {t('start_btn')}
          </Button>
        </div>
      </div>
    )
  }

  if (!current) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    )
  }

  const zone = questions?.zones.find((z) => z.zone === current.zone)
  const progress = (currentIndex / total) * 100

  return (
    <div className="flex min-h-screen flex-col" style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)' }}>
      <div
        className="px-5 pt-5 pb-4 backdrop-blur-sm"
        style={{ background: 'rgba(255,255,255,0.75)', borderBottom: '1px solid rgba(232,227,218,0.5)' }}
      >
        <div className="mb-2 flex items-center justify-between">
          <span className="text-xs font-bold text-primary">{zone ? t(`common:zones.${zone.zone}`, { defaultValue: zone.label }) : ''}</span>
          <span className="text-xs font-semibold text-muted">{currentIndex + 1} / {total}</span>
        </div>
        <div className="h-1.5 w-full rounded-full overflow-hidden bg-sand/50">
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{ width: `${progress}%`, background: 'linear-gradient(90deg, #3C3888, #385C8A)' }}
          />
        </div>
      </div>

      <div className="flex flex-1 flex-col items-center justify-center px-4 py-8">
        <div className="w-full max-w-lg">
          <div
            className="rounded-[28px] p-8"
            style={{
              background: 'rgba(255,255,255,0.92)',
              border: '1px solid rgba(255,255,255,0.80)',
              boxShadow: '0 8px 40px rgba(60,56,136,0.12), 0 1px 3px rgba(23,21,42,0.06)',
            }}
          >
            <p className="mb-8 text-center text-xl font-semibold leading-relaxed text-ink">
              {current.text}
            </p>

            {current.question_type === 'scale' && (
              <div className="flex items-center justify-between gap-2">
                <span className="text-[11px] font-medium text-muted w-16 text-center leading-tight">{t('scale_never')}</span>
                <div className="flex gap-2.5">
                  {[1, 2, 3, 4, 5].map((v) => (
                    <button
                      key={v}
                      onClick={() => handleScaleAnswer(v)}
                      className="flex h-12 w-12 items-center justify-center rounded-full text-base font-bold transition-all duration-150"
                      style={
                        answers[current.id]?.value_scale === v
                          ? { background: 'linear-gradient(135deg, #3C3888, #385C8A)', color: '#fff', transform: 'scale(1.1)', boxShadow: '0 4px 14px rgba(60,56,136,0.40)' }
                          : { background: '#EDEAF8', color: '#3C3888' }
                      }
                    >
                      {v}
                    </button>
                  ))}
                </div>
                <span className="text-[11px] font-medium text-muted w-16 text-center leading-tight">{t('scale_always')}</span>
              </div>
            )}

            {current.question_type === 'choice' && current.options && (
              <div className="flex flex-col gap-2.5">
                {current.options.map((option) => (
                  <button
                    key={option}
                    onClick={() => handleChoiceAnswer(option)}
                    className="w-full rounded-2xl px-4 py-3 text-left text-sm font-semibold transition-all duration-150"
                    style={
                      answers[current.id]?.value_choice === option
                        ? { background: '#EDEAF8', border: '2px solid #3C3888', color: '#3C3888', boxShadow: '0 0 0 3px rgba(60,56,136,0.10)' }
                        : { background: 'white', border: '2px solid rgba(232,227,218,0.8)', color: '#17152A' }
                    }
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}

            {current.question_type === 'text' && (
              <div className="flex flex-col gap-4">
                <textarea
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder={t('text_placeholder')}
                  rows={4}
                  className="w-full resize-none rounded-[14px] px-4 py-3 text-sm text-ink placeholder:text-muted/60 focus:outline-none transition-all"
                  style={{
                    border: '1.5px solid rgba(232,227,218,0.8)',
                    background: 'white',
                    boxShadow: 'none',
                  }}
                  onFocus={(e) => { e.currentTarget.style.borderColor = 'rgba(60,56,136,0.5)'; e.currentTarget.style.boxShadow = '0 0 0 3px rgba(60,56,136,0.10)' }}
                  onBlur={(e) => { e.currentTarget.style.borderColor = 'rgba(232,227,218,0.8)'; e.currentTarget.style.boxShadow = 'none' }}
                />
                <Button onClick={handleTextAnswer} disabled={!textInput.trim()} loading={completeMutation.isPending} fullWidth>
                  {t('next_question')}
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between px-6 pb-8 pt-2">
        <Button
          variant="ghost"
          size="sm"
          disabled={currentIndex === 0}
          onClick={() => setCurrentIndex((i) => Math.max(0, i - 1))}
        >
          {t('nav_back')}
        </Button>
        <p className="text-[11px] font-medium text-muted">{t('your_eyes_only')}</p>
      </div>
    </div>
  )
}
