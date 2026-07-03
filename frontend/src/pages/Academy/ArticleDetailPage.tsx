import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, Clock, CheckCircle2, BookOpen, ExternalLink, Sparkles, Send } from 'lucide-react'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { AcademyService } from '@/services/academy.service'
import { Button } from '@/components/ui/Button'
import { celebrateMedium } from '@/lib/confetti'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.38, ease, delay },
})

const SOURCE_TYPE_ICON: Record<string, string> = {
  researcher: '🔬', organization: '🏛️', book: '📚', journal: '📰',
}

type ReflectionStep = 'understood' | 'try' | 'apply' | 'done'

// Simple markdown renderer (headers, bold, lists, tables)
function MarkdownBody({ text }: { text: string }) {
  const lines = text.split('\n')
  const result: JSX.Element[] = []
  let i = 0

  const parseInline = (s: string) => {
    const parts = s.split(/(\*\*[^*]+\*\*)/g)
    return parts.map((p, j) =>
      p.startsWith('**') ? <strong key={j}>{p.slice(2, -2)}</strong> : <span key={j}>{p}</span>
    )
  }

  while (i < lines.length) {
    const line = lines[i]
    if (line.startsWith('## ')) {
      result.push(<h2 key={i} className="text-base font-bold text-ink mt-5 mb-2">{line.slice(3)}</h2>)
    } else if (line.startsWith('### ')) {
      result.push(<h3 key={i} className="text-sm font-bold text-ink mt-4 mb-1.5">{line.slice(4)}</h3>)
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      result.push(
        <li key={i} className="flex gap-2 text-sm text-ink leading-relaxed mb-1">
          <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
          <span>{parseInline(line.slice(2))}</span>
        </li>
      )
    } else if (line.startsWith('> ')) {
      result.push(
        <blockquote key={i} className="border-l-2 border-primary pl-4 my-3 text-sm text-muted italic">
          {parseInline(line.slice(2))}
        </blockquote>
      )
    } else if (line.startsWith('|')) {
      const rows: string[][] = []
      while (i < lines.length && lines[i].startsWith('|')) {
        if (!lines[i].match(/^[|\s-]+$/)) {
          rows.push(lines[i].split('|').filter(Boolean).map(c => c.trim()))
        }
        i++
      }
      const [headRow, ...bodyRows] = rows
      result.push(
        <div key={`table-${i}`} className="overflow-x-auto my-3">
          <table className="w-full text-xs border-collapse">
            {headRow && (
              <thead>
                <tr className="bg-primary/5">
                  {headRow.map((cell, ci) => (
                    <th key={ci} className="border border-sand/60 px-3 py-2 text-ink font-semibold text-left">{parseInline(cell)}</th>
                  ))}
                </tr>
              </thead>
            )}
            <tbody>
              {bodyRows.map((row, ri) => (
                <tr key={ri} className={ri % 2 === 0 ? '' : 'bg-surface'}>
                  {row.map((cell, ci) => (
                    <td key={ci} className="border border-sand/60 px-3 py-2 text-ink">{parseInline(cell)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )
      continue
    } else if (line.trim() === '') {
      result.push(<div key={i} className="h-2" />)
    } else {
      result.push(<p key={i} className="text-sm text-ink leading-relaxed">{parseInline(line)}</p>)
    }
    i++
  }
  return <div className="space-y-0.5">{result}</div>
}

export const ArticleDetailPage = () => {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('academy')

  const [reflectionStep, setReflectionStep] = useState<ReflectionStep | null>(null)
  const [answer, setAnswer] = useState('')
  const [aiResponse, setAiResponse] = useState<string | null>(null)

  const REFLECTION_QUESTIONS: Record<Exclude<ReflectionStep, 'done'>, string> = {
    understood: t('reflect_q_understood', { defaultValue: 'Что вы поняли из этой статьи?' }),
    try:        t('reflect_q_try', { defaultValue: 'Что хотите попробовать в ближайшие дни?' }),
    apply:      t('reflect_q_apply', { defaultValue: 'Как конкретно вы можете применить это в вашей семье?' }),
  }

  const { data: article, isLoading } = useQuery({
    queryKey: ['academy-article', slug, i18n.language],
    queryFn: () => AcademyService.getArticle(slug!),
    enabled: !!slug,
  })

  const completeMutation = useMutation({
    mutationFn: () => AcademyService.completeArticle(slug!),
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ['academy-articles'] })
      qc.invalidateQueries({ queryKey: ['academy-article', slug] })
      qc.invalidateQueries({ queryKey: ['academy-progress'] })
      if (data.newly_completed) {
        toast.success(t('toast_article_read', { defaultValue: 'Статья прочитана!' }))
        celebrateMedium()
        setReflectionStep('understood')
      }
    },
  })

  const reflectMutation = useMutation({
    mutationFn: (payload: { question_key: 'understood' | 'try' | 'apply'; answer: string }) =>
      AcademyService.reflectArticle(slug!, payload),
    onSuccess: (data) => {
      setAiResponse(data.ai_response)
      setAnswer('')
      setTimeout(() => {
        setAiResponse(null)
        if (data.next_question_key) {
          setReflectionStep(data.next_question_key as ReflectionStep)
        } else {
          setReflectionStep('done')
        }
      }, 2500)
    },
  })

  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="page-hero px-5 pt-6 pb-5">
          <div className="h-6 w-32 rounded-xl shimmer" />
        </div>
        <div className="px-4 pt-4 space-y-4">
          <div className="h-10 rounded-2xl shimmer" />
          {[...Array(5)].map((_, i) => <div key={i} className="h-5 rounded-xl shimmer" />)}
        </div>
      </div>
    )
  }

  if (!article) {
    return (
      <div className="flex min-h-full items-center justify-center p-6">
        <p className="text-sm text-muted">{t('article_not_found', { defaultValue: 'Статья не найдена' })}</p>
      </div>
    )
  }

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
        <div className="flex items-center gap-2 mb-2 flex-wrap">
          <span className="label-caps text-primary">{t(`categories.${article.category}`, { defaultValue: article.category })}</span>
          <span className="label-caps text-muted">{t(`difficulty.${article.difficulty}`, { defaultValue: article.difficulty })}</span>
        </div>
        <h1 className="text-xl font-bold text-ink leading-snug mb-2">{article.title}</h1>
        <div className="flex items-center gap-3 text-xs text-muted">
          <span className="flex items-center gap-1">
            <Clock size={12} />
            {article.read_time_minutes} {t('read_min', { defaultValue: 'мин чтения' })}
          </span>
          {article.is_completed && (
            <span className="flex items-center gap-1 text-success font-semibold">
              <CheckCircle2 size={12} /> {t('article_read', { defaultValue: 'Прочитано' })}
            </span>
          )}
        </div>
      </div>

      <div className="px-4 md:px-5 max-w-2xl space-y-5">
        {/* Brief */}
        <motion.div {...fadeUp(0)}>
          <div
            className="rounded-[20px] p-4"
            style={{ background: 'linear-gradient(135deg, #EDEAF8 0%, #DDE8F2 100%)', border: '1px solid rgba(60,56,136,0.10)' }}
          >
            <p className="text-sm text-ink leading-relaxed font-medium">{article.brief}</p>
          </div>
        </motion.div>

        {/* Body */}
        <motion.div {...fadeUp(0.04)}>
          <div
            className="rounded-[22px] bg-canvas p-5"
            style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
          >
            {article.body && <MarkdownBody text={article.body} />}
          </div>
        </motion.div>

        {/* Sources */}
        {article.sources && article.sources.length > 0 && (
          <motion.div {...fadeUp(0.08)}>
            <div
              className="rounded-[20px] bg-canvas p-4"
              style={{ border: '1px solid rgba(232,227,218,0.6)' }}
            >
              <p className="label-caps text-muted mb-3">{t('sources_label', { defaultValue: 'Источники' })}</p>
              <div className="flex flex-col gap-2">
                {article.sources.map((source, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <span className="text-base">{SOURCE_TYPE_ICON[source.source_type]}</span>
                    <div className="flex-1 min-w-0">
                      <span className="text-sm font-medium text-ink">{source.name}</span>
                      {source.trust_level === 'high' && (
                        <span className="ml-2 text-[10px] font-bold text-success">{t('source_verified', { defaultValue: '✓ Проверено' })}</span>
                      )}
                    </div>
                    {source.url && (
                      <a href={source.url} target="_blank" rel="noopener noreferrer" className="text-muted hover:text-primary">
                        <ExternalLink size={12} />
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* Tags */}
        {article.tags && article.tags.length > 0 && (
          <motion.div {...fadeUp(0.1)}>
            <div className="flex flex-wrap gap-2">
              {article.tags.map((tag) => (
                <span
                  key={tag}
                  className="rounded-full px-3 py-1 text-xs font-medium"
                  style={{ background: '#EDEAF8', color: '#3C3888' }}
                >
                  #{tag}
                </span>
              ))}
            </div>
          </motion.div>
        )}

        {/* Complete / AI Reflection */}
        <motion.div {...fadeUp(0.12)}>
          {!article.is_completed && reflectionStep === null && (
            <Button
              fullWidth
              onClick={() => completeMutation.mutate()}
              loading={completeMutation.isPending}
            >
              <BookOpen size={14} /> {t('mark_read_btn', { defaultValue: 'Я прочитал(а) эту статью' })}
            </Button>
          )}

          <AnimatePresence mode="wait">
            {reflectionStep && reflectionStep !== 'done' && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.3, ease }}
              >
                <div
                  className="rounded-[22px] p-5"
                  style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)', border: '1px solid rgba(60,56,136,0.12)' }}
                >
                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-2xl bg-gradient-brand">
                      <Sparkles size={14} className="text-white" />
                    </div>
                    <p className="text-sm font-bold text-ink">{t('ai_mentor', { defaultValue: 'AI-наставник' })}</p>
                  </div>

                  <AnimatePresence mode="wait">
                    {aiResponse ? (
                      <motion.p
                        key="response"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="text-sm text-ink leading-relaxed"
                      >
                        {aiResponse}
                      </motion.p>
                    ) : (
                      <motion.div key="question" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                        <p className="text-sm font-semibold text-ink mb-3">
                          {REFLECTION_QUESTIONS[reflectionStep as Exclude<ReflectionStep, 'done'>]}
                        </p>
                        <textarea
                          value={answer}
                          onChange={(e) => setAnswer(e.target.value)}
                          placeholder={t('reflect_placeholder', { defaultValue: 'Напишите ваш ответ...' })}
                          rows={3}
                          className="w-full resize-none rounded-[14px] px-4 py-3 text-sm text-ink placeholder:text-muted/60 focus:outline-none transition-all mb-3"
                          style={{
                            border: '1.5px solid rgba(60,56,136,0.20)',
                            background: 'rgba(255,255,255,0.85)',
                          }}
                          onFocus={(e) => { e.currentTarget.style.borderColor = 'rgba(60,56,136,0.5)'; e.currentTarget.style.boxShadow = '0 0 0 3px rgba(60,56,136,0.10)' }}
                          onBlur={(e) => { e.currentTarget.style.borderColor = 'rgba(60,56,136,0.20)'; e.currentTarget.style.boxShadow = 'none' }}
                        />
                        <Button
                          fullWidth
                          onClick={() => reflectMutation.mutate({ question_key: reflectionStep as any, answer })}
                          disabled={!answer.trim()}
                          loading={reflectMutation.isPending}
                        >
                          <Send size={13} /> {t('reflect_submit_btn', { defaultValue: 'Ответить' })}
                        </Button>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </motion.div>
            )}

            {reflectionStep === 'done' && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.32, ease }}
              >
                <div
                  className="rounded-[20px] p-4 text-center"
                  style={{ background: 'linear-gradient(135deg, #E2EDE8, #D2DDF0)', border: '1px solid rgba(56,104,88,0.20)' }}
                >
                  <span className="text-3xl block mb-2">🎉</span>
                  <p className="text-sm font-bold text-ink mb-1">{t('reflect_done_title', { defaultValue: 'Отличная работа!' })}</p>
                  <p className="text-xs text-muted">{t('reflect_done_desc', { defaultValue: 'Рефлексия сохранена. Практикуйте то, что осознали.' })}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {article.is_completed && reflectionStep === null && (
            <div
              className="mt-2 flex items-center gap-2 rounded-[16px] px-4 py-3"
              style={{ background: '#E2EDE8', border: '1px solid rgba(56,104,88,0.20)' }}
            >
              <CheckCircle2 size={15} className="text-success" />
              <p className="text-xs font-semibold text-success">{t('article_already_read', { defaultValue: 'Вы уже прочитали эту статью' })}</p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
