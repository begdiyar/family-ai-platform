import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Brain, BookOpen, Zap, Target, ChevronRight,
  Flame, Clock, CheckCircle2, Play, Sparkles, Trophy,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { useTranslation } from 'react-i18next'
import { AcademyService } from '@/services/academy.service'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import type { AcademyCategory, AcademyArticle, AcademyTraining, AcademyProgram } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.38, ease, delay },
})

type Tab = 'home' | 'articles' | 'skills' | 'courses'

const CATEGORY_ICONS: Record<AcademyCategory, string> = {
  communication:   '💬',
  trust:           '🤝',
  conflict:        '⚡',
  intimacy:        '❤️',
  love:            '✨',
  finance:         '💰',
  stress:          '🧘',
  crisis_recovery: '🌱',
  parenting:       '🧒',
  traditions:      '🏡',
  husband_role:    '👨',
  wife_role:       '👩',
  relatives:       '👨‍👩‍👧',
  marriage_prep:   '💍',
}

const CATEGORY_COLORS: Record<AcademyCategory, string> = {
  communication:   '#3C3888',
  trust:           '#386858',
  conflict:        '#843048',
  intimacy:        '#885040',
  love:            '#3C3888',
  finance:         '#886028',
  stress:          '#385C8A',
  crisis_recovery: '#386858',
  parenting:       '#886028',
  traditions:      '#3C3888',
  husband_role:    '#385C8A',
  wife_role:       '#885040',
  relatives:       '#386858',
  marriage_prep:   '#885040',
}

const SKILL_ICONS: Record<string, string> = {
  active_listening:      '👂',
  emotion_management:    '🧠',
  gratitude:             '🙏',
  partner_support:       '🫂',
  constructive_dialogue: '💬',
  conflict_resolution:   '🕊️',
  joint_planning:        '📅',
}

const VISIBLE_CATEGORIES: AcademyCategory[] = [
  'communication', 'trust', 'conflict', 'intimacy',
  'love', 'finance', 'stress', 'crisis_recovery',
  'parenting', 'traditions',
]

// ── Cards ─────────────────────────────────────────────────────────────────────

function ArticleCard({ article, onClick }: { article: AcademyArticle; onClick: () => void }) {
  const { t } = useTranslation('academy')
  const icon = CATEGORY_ICONS[article.category]
  const color = CATEGORY_COLORS[article.category]
  const label = t(`categories.${article.category}`, { defaultValue: article.category })
  return (
    <button
      onClick={onClick}
      className="w-full text-left rounded-[20px] bg-canvas p-4 transition-all duration-150 hover:shadow-md"
      style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
    >
      <div className="flex items-start gap-3">
        <span className="text-2xl leading-none">{icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color }}>
              {label}
            </span>
            <span className="text-[10px] text-muted">{article.read_time_minutes} {t('common:min', { defaultValue: 'мин' })}</span>
            {article.is_completed && <CheckCircle2 size={12} className="text-success ml-auto" />}
          </div>
          <p className="text-sm font-semibold text-ink leading-snug">{article.title}</p>
          <p className="text-xs text-muted mt-1 leading-relaxed line-clamp-2">{article.brief}</p>
        </div>
      </div>
    </button>
  )
}

function SkillCard({ training, onClick }: { training: AcademyTraining; onClick: () => void }) {
  const { t } = useTranslation('academy')
  const icon = SKILL_ICONS[training.skill_type]
  const diffLabel = t(`difficulty.${training.difficulty}`, { defaultValue: training.difficulty })
  return (
    <button
      onClick={onClick}
      className="w-full text-left rounded-[20px] bg-canvas p-4 transition-all duration-150 hover:shadow-md"
      style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
    >
      <div className="flex items-center gap-3">
        <div
          className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl text-xl"
          style={{
            background: training.is_completed
              ? 'linear-gradient(135deg, #386858, #385C8A)'
              : 'linear-gradient(135deg, #EDEAF8, #DDE8F2)',
          }}
        >
          {training.is_completed ? '✓' : icon}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <p className="text-sm font-semibold text-ink truncate">{training.title}</p>
            {training.is_completed && <Badge variant="success" className="ml-auto shrink-0">{t('skill_done_badge')}</Badge>}
          </div>
          <div className="flex items-center gap-3 text-xs text-muted">
            <span className="flex items-center gap-1"><Clock size={10} />{training.duration_minutes} {t('common:min', { defaultValue: 'мин' })}</span>
            <span>{diffLabel}</span>
          </div>
        </div>
        <ChevronRight size={16} className="text-muted shrink-0" />
      </div>
    </button>
  )
}

function CourseCard({ program, onClick }: { program: AcademyProgram; onClick: () => void }) {
  const { t } = useTranslation('academy')
  return (
    <button
      onClick={onClick}
      className="w-full text-left rounded-[22px] p-5 transition-all duration-150 hover:shadow-md"
      style={{ background: program.cover_gradient, border: '1px solid rgba(255,255,255,0.2)' }}
    >
      <div className="flex items-start justify-between mb-3">
        <span className="label-caps text-white/70">{program.duration_days} {t('duration_days_unit', { defaultValue: 'дней' })}</span>
        {program.is_enrolled && (
          <span
            className="rounded-full px-2.5 py-1 text-[10px] font-bold text-white"
            style={{ background: 'rgba(255,255,255,0.25)' }}
          >
            {program.enrollment_status === 'completed'
              ? t('course_completed')
              : t('course_day', { day: program.current_day })}
          </span>
        )}
      </div>
      <p className="text-base font-bold text-white mb-1 leading-snug">{program.title}</p>
      <p className="text-xs text-white/70 leading-relaxed line-clamp-2 mb-3">{program.description}</p>
      {program.is_enrolled && program.enrollment_status === 'active' && (
        <div className="h-1.5 w-full rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.25)' }}>
          <div className="h-full rounded-full bg-canvas" style={{ width: `${program.progress_percent}%` }} />
        </div>
      )}
    </button>
  )
}

// ── Tabs ──────────────────────────────────────────────────────────────────────

function HomeTab({ navigate }: { navigate: ReturnType<typeof useNavigate> }) {
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('academy')
  const lang = i18n.language

  const { data: progress } = useQuery({ queryKey: ['academy-progress'], queryFn: AcademyService.getProgress })
  const { data: microData } = useQuery({ queryKey: ['academy-micro-today', lang], queryFn: AcademyService.getTodayMicroPractice })
  const { data: recs } = useQuery({ queryKey: ['academy-recommendations', lang], queryFn: AcademyService.getRecommendations })
  const { data: activeProgram } = useQuery({ queryKey: ['academy-active-program', lang], queryFn: AcademyService.getActiveProgram })

  const microMutation = useMutation({
    mutationFn: (id: string) => AcademyService.completeMicroPractice(id),
    onSuccess: () => {
      toast.success(t('micro_toast_done'))
      qc.invalidateQueries({ queryKey: ['academy-micro-today'] })
      qc.invalidateQueries({ queryKey: ['academy-progress'] })
    },
  })

  return (
    <div className="space-y-5">
      {/* Progress stats */}
      <motion.div {...fadeUp(0)}>
        <div
          className="rounded-[22px] p-5"
          style={{ background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 55%, #D6E8E2 100%)', border: '1px solid rgba(60,56,136,0.10)' }}
        >
          <div className="flex items-center gap-2 mb-4">
            <Brain size={15} className="text-primary" />
            <p className="text-sm font-bold text-ink">{t('progress_title')}</p>
            {(progress?.current_streak ?? 0) > 0 && (
              <div className="ml-auto flex items-center gap-1 text-xs font-bold text-warning">
                <Flame size={12} /> {progress?.current_streak}{t('streak_label')}
              </div>
            )}
          </div>
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: t('stat_articles'), value: progress?.articles_read ?? 0,      icon: <BookOpen size={14} /> },
              { label: t('stat_skills'),   value: progress?.trainings_completed ?? 0, icon: <Zap size={14} /> },
              { label: t('stat_courses'),  value: progress?.programs_completed ?? 0,  icon: <Target size={14} /> },
            ].map((s) => (
              <div key={s.label} className="rounded-[14px] __BGWHITE_ALPHA___ py-3 text-center">
                <div className="flex justify-center mb-1 text-primary">{s.icon}</div>
                <p className="text-xl font-bold text-ink">{s.value}</p>
                <p className="text-[10px] text-muted">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Micro practice */}
      {microData?.practice && (
        <motion.div {...fadeUp(0.04)}>
          <div
            className="rounded-[20px] p-4"
            style={{
              background: microData.is_completed ? 'linear-gradient(135deg, #E2EDE8, #D2DDF0)' : 'white',
              border: microData.is_completed ? '1px solid rgba(56,104,88,0.20)' : '1px solid rgba(232,227,218,0.6)',
              boxShadow: '0 1px 3px rgba(23,21,42,0.04)',
            }}
          >
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-gradient-brand">
                <Sparkles size={16} className="text-white" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="label-caps text-primary mb-1">{t('micro_label')}</p>
                <p className="text-sm font-semibold text-ink mb-1">{microData.practice.title}</p>
                <p className="text-xs text-muted leading-relaxed">{microData.practice.instruction}</p>
                <div className="flex items-center gap-3 mt-3">
                  <span className="text-xs text-muted flex items-center gap-1">
                    <Clock size={10} />{microData.practice.duration_minutes} {t('common:min', { defaultValue: 'мин' })}
                  </span>
                  {!microData.is_completed ? (
                    <Button size="sm" onClick={() => microMutation.mutate(microData.practice!.id)} loading={microMutation.isPending}>
                      <CheckCircle2 size={13} /> {t('micro_done_btn')}
                    </Button>
                  ) : (
                    <span className="flex items-center gap-1 text-xs font-semibold text-success">
                      <CheckCircle2 size={12} /> {t('micro_done_today')}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Active course */}
      {activeProgram?.active_program && (
        <motion.div {...fadeUp(0.06)}>
          <div
            className="rounded-[20px] bg-canvas p-4"
            style={{ border: '1px solid rgba(60,56,136,0.15)', boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
          >
            <p className="label-caps text-primary mb-3">{t('active_course_label')}</p>
            <p className="text-sm font-bold text-ink mb-1">{activeProgram.active_program.title}</p>
            <p className="text-xs text-muted mb-3">
              {t('active_course_day', { day: activeProgram.active_program.current_day, total: activeProgram.active_program.duration_days })}
            </p>
            <div className="h-1.5 w-full rounded-full overflow-hidden bg-sand/50 mb-3">
              <div
                className="h-full rounded-full"
                style={{ width: `${activeProgram.active_program.progress_percent}%`, background: 'linear-gradient(90deg, #3C3888, #385C8A)' }}
              />
            </div>
            <Button size="sm" onClick={() => navigate(`/app/academy/programs/${activeProgram.active_program!.slug}`)}>
              <Play size={13} /> {t('continue_btn')}
            </Button>
          </div>
        </motion.div>
      )}

      {/* Recommendations */}
      {recs && recs.results.length > 0 && (
        <motion.div {...fadeUp(0.08)}>
          <p className="label-caps text-muted mb-3 px-1">{t('recs_label')}</p>
          <div className="flex flex-col gap-2">
            {recs.results.slice(0, 3).map((rec, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.28, ease, delay: 0.1 + i * 0.04 }}
              >
                <button
                  onClick={() => {
                    const item = rec.item as any
                    if (rec.type === 'article') navigate(`/app/academy/articles/${item.slug}`)
                    else if (rec.type === 'training') navigate(`/app/academy/trainings/${item.slug}`)
                    else navigate(`/app/academy/programs/${item.slug}`)
                  }}
                  className="w-full text-left rounded-[18px] bg-canvas p-3.5 transition-all hover:shadow-sm"
                  style={{ border: '1px solid rgba(232,227,218,0.6)' }}
                >
                  <div className="flex items-start gap-2.5">
                    <span className="text-base shrink-0 mt-0.5">
                      {rec.type === 'article' ? '📖' : rec.type === 'training' ? '⚡' : '🎯'}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-muted mb-0.5">{rec.reason}</p>
                      <p className="text-sm font-semibold text-ink truncate">{(rec.item as any).title}</p>
                    </div>
                    <ChevronRight size={14} className="text-muted shrink-0 mt-1" />
                  </div>
                </button>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Categories grid */}
      <motion.div {...fadeUp(0.12)}>
        <p className="label-caps text-muted mb-3 px-1">{t('themes_label')}</p>
        <div className="grid grid-cols-2 gap-2">
          {VISIBLE_CATEGORIES.map((key) => {
            const icon = CATEGORY_ICONS[key]
            const color = CATEGORY_COLORS[key]
            const label = t(`categories.${key}`, { defaultValue: key })
            return (
              <button
                key={key}
                onClick={() => navigate(`/app/academy?tab=articles&category=${key}`)}
                className="flex items-center gap-2.5 rounded-[16px] bg-canvas p-3 text-left transition-all hover:shadow-sm"
                style={{ border: '1px solid rgba(232,227,218,0.6)' }}
              >
                <span className="text-lg">{icon}</span>
                <span className="text-xs font-semibold text-ink leading-tight">{label}</span>
              </button>
            )
          })}
        </div>
      </motion.div>
    </div>
  )
}

function ArticlesTab({ navigate }: { navigate: ReturnType<typeof useNavigate> }) {
  const [activeCategory, setActiveCategory] = useState<AcademyCategory | ''>('')
  const { t, i18n } = useTranslation('academy')
  const lang = i18n.language

  const { data, isLoading } = useQuery({
    queryKey: ['academy-articles', activeCategory, lang],
    queryFn: () => AcademyService.listArticles(activeCategory ? { category: activeCategory } : undefined),
  })

  return (
    <div className="space-y-4">
      <div className="flex gap-2 overflow-x-auto pb-1 -mx-4 px-4 scrollbar-hide">
        <button
          onClick={() => setActiveCategory('')}
          className="shrink-0 rounded-full px-3 py-1.5 text-xs font-semibold transition-all"
          style={!activeCategory
            ? { background: 'linear-gradient(135deg, #3C3888, #385C8A)', color: 'white' }
            : { background: '#EDEAF8', color: '#3C3888' }
          }
        >
          {t('filter_all')}
        </button>
        {VISIBLE_CATEGORIES.map((key) => {
          const icon = CATEGORY_ICONS[key]
          const color = CATEGORY_COLORS[key]
          const label = t(`categories.${key}`, { defaultValue: key })
          return (
            <button
              key={key}
              onClick={() => setActiveCategory(key)}
              className="shrink-0 flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-semibold transition-all"
              style={activeCategory === key
                ? { background: color, color: 'white' }
                : { background: '#EDEAF8', color: '#3C3888' }
              }
            >
              {icon} {label}
            </button>
          )
        })}
      </div>

      {isLoading && (
        <div className="flex flex-col gap-3">
          {[...Array(5)].map((_, i) => <div key={i} className="h-24 rounded-[20px] shimmer" />)}
        </div>
      )}

      {!isLoading && data && (
        <div className="flex flex-col gap-2">
          {data.results.map((article, i) => (
            <motion.div
              key={article.id}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.28, ease, delay: i * 0.04 }}
            >
              <ArticleCard article={article} onClick={() => navigate(`/app/academy/articles/${article.slug}`)} />
            </motion.div>
          ))}
          {data.results.length === 0 && (
            <div className="py-12 text-center text-sm text-muted">{t('no_articles')}</div>
          )}
        </div>
      )}
    </div>
  )
}

function SkillsTab({ navigate }: { navigate: ReturnType<typeof useNavigate> }) {
  const { t, i18n } = useTranslation('academy')
  const lang = i18n.language
  const { data, isLoading } = useQuery({ queryKey: ['academy-trainings', lang], queryFn: AcademyService.listTrainings })

  return (
    <div className="space-y-4">
      <div
        className="rounded-[20px] p-4"
        style={{ background: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)', border: '1px solid rgba(56,92,138,0.12)' }}
      >
        <p className="text-sm font-bold text-ink mb-1">{t('skills_header_title')}</p>
        <p className="text-xs text-muted leading-relaxed">{t('skills_header_desc')}</p>
      </div>

      {isLoading && (
        <div className="flex flex-col gap-3">
          {[...Array(4)].map((_, i) => <div key={i} className="h-20 rounded-[20px] shimmer" />)}
        </div>
      )}

      {!isLoading && data && (
        <div className="flex flex-col gap-2">
          {data.results.map((training, i) => (
            <motion.div
              key={training.id}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.28, ease, delay: i * 0.04 }}
            >
              <SkillCard training={training} onClick={() => navigate(`/app/academy/trainings/${training.slug}`)} />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}

function CoursesTab({ navigate }: { navigate: ReturnType<typeof useNavigate> }) {
  const { t, i18n } = useTranslation('academy')
  const lang = i18n.language
  const { data, isLoading } = useQuery({ queryKey: ['academy-programs', lang], queryFn: AcademyService.listPrograms })
  const { data: achievementsData } = useQuery({ queryKey: ['academy-achievements', lang], queryFn: AcademyService.getAchievements })

  return (
    <div className="space-y-4">
      {isLoading && (
        <div className="flex flex-col gap-3">
          {[...Array(3)].map((_, i) => <div key={i} className="h-40 rounded-[22px] shimmer" />)}
        </div>
      )}

      {!isLoading && data && (
        <>
          <div className="flex flex-col gap-3">
            {data.results.map((program, i) => (
              <motion.div
                key={program.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.32, ease, delay: i * 0.05 }}
              >
                <CourseCard program={program} onClick={() => navigate(`/app/academy/programs/${program.slug}`)} />
              </motion.div>
            ))}
          </div>

          {achievementsData && achievementsData.results.length > 0 && (
            <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.32, ease, delay: 0.2 }}>
              <p className="label-caps text-muted mb-3 px-1 mt-2">{t('achievements_label')}</p>
              <div className="flex flex-wrap gap-2">
                {achievementsData.results.map((ua) => (
                  <div
                    key={ua.achievement.key}
                    className="flex items-center gap-2 rounded-2xl px-3 py-2"
                    style={{ background: '#EDEAF8', border: '1px solid rgba(60,56,136,0.12)' }}
                    title={ua.achievement.description}
                  >
                    <span className="text-lg">{ua.achievement.icon}</span>
                    <span className="text-xs font-semibold text-ink">{ua.achievement.title}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </>
      )}
    </div>
  )
}

// ── Main ──────────────────────────────────────────────────────────────────────

export const AcademyPage = () => {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<Tab>('home')
  const { t } = useTranslation('academy')

  const TABS: { id: Tab; label: string; icon: typeof BookOpen }[] = [
    { id: 'home',     label: t('tab_home'),     icon: Brain },
    { id: 'articles', label: t('tab_articles'), icon: BookOpen },
    { id: 'skills',   label: t('tab_skills'),   icon: Zap },
    { id: 'courses',  label: t('tab_courses'),  icon: Target },
  ]

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <div className="page-hero px-5 pt-6 pb-0">
        <div className="flex items-center gap-3 mb-5">
          <div
            className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
            style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
          >
            <Brain size={17} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
            <p className="text-xs text-muted">{t('subtitle')}</p>
          </div>
        </div>

        <div className="flex gap-1 overflow-x-auto scrollbar-hide">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className="shrink-0 flex items-center gap-1.5 rounded-[12px] px-3 py-2 text-xs font-semibold transition-all duration-150"
              style={
                activeTab === id
                  ? { background: 'linear-gradient(135deg, #3C3888, #385C8A)', color: 'white' }
                  : { background: 'transparent', color: '#68647C' }
              }
            >
              <Icon size={12} />
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="px-4 pt-4 md:px-5">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.22, ease }}
          >
            {activeTab === 'home'     && <HomeTab navigate={navigate} />}
            {activeTab === 'articles' && <ArticlesTab navigate={navigate} />}
            {activeTab === 'skills'   && <SkillsTab navigate={navigate} />}
            {activeTab === 'courses'  && <CoursesTab navigate={navigate} />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}
