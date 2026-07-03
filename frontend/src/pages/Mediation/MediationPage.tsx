import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { motion } from 'framer-motion'
import { Scale, Plus, ChevronLeft, CheckCircle2, Clock, Loader2, ShieldCheck } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { MediationService } from '@/services/mediation.service'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Input, Textarea } from '@/components/ui/Input'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { ConflictSession } from '@/types/domain.types'

const STATUS_BADGE: Record<string, string> = {
  collecting: 'warning',
  analyzing: 'violet',
  complete: 'success',
}

export const MediationPage = () => {
  const qc = useQueryClient()
  const navigate = useNavigate()
  const { t, i18n } = useTranslation('mediation')
  const [view, setView] = useState<'list' | 'create' | 'session'>('list')
  const [activeId, setActiveId] = useState<string | null>(null)
  const [newTitle, setNewTitle] = useState('')

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  const statusLabel = (status: string) => {
    if (status === 'collecting') return t('status_collecting')
    if (status === 'analyzing') return t('status_analyzing')
    return t('status_complete')
  }

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: sessions = [], isLoading } = useQuery({
    queryKey: ['mediation'],
    queryFn: MediationService.list,
    enabled: me?.couple?.status === 'active',
  })

  const createMutation = useMutation({
    mutationFn: () => MediationService.create(newTitle || t('conflict_topic_label')),
    onSuccess: (session) => {
      qc.invalidateQueries({ queryKey: ['mediation'] })
      setActiveId(session.id)
      setView('session')
      setNewTitle('')
    },
    onError: () => toast.error(t('toast_create_error')),
  })

  if (me?.couple?.status === 'pending') {
    return (
      <div className="p-6">
        <EmptyState
          icon={<Scale />}
          title={t('common:pending_couple_title')}
          description={t('common:invite_partner_first')}
          actionLabel={t('common:invite_partner_btn')}
          onAction={() => navigate('/app/couple')}
        />
      </div>
    )
  }

  if (!me?.couple) {
    return (
      <div className="p-6">
        <EmptyState
          icon={<Scale />}
          title={t('no_couple_title')}
          description={t('no_couple_desc')}
        />
      </div>
    )
  }

  if (view === 'create') {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="page-hero px-5 pt-6 pb-5">
          <button onClick={() => setView('list')} className="mb-4 flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary transition-colors">
            <ChevronLeft size={16} /> {t('back_btn')}
          </button>
          <div className="flex items-center gap-3">
            <div
              className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-violet"
              style={{ boxShadow: '0 4px 14px rgba(56,92,138,0.28)' }}
            >
              <Scale size={17} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-ink">{t('new_session_title')}</h1>
              <p className="text-xs text-muted mt-0.5">{t('new_session_subtitle')}</p>
            </div>
          </div>
        </div>
        <div className="px-4 pt-4 md:px-5 max-w-lg">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
          >
            <div
              className="rounded-[22px] p-5 bg-white"
              style={{ border: '1px solid rgba(232,227,218,0.6)', boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)' }}
            >
              <p className="mb-1 text-sm font-semibold text-ink">{t('conflict_topic_label')}</p>
              <p className="mb-3 text-xs text-muted">{t('conflict_topic_hint')}</p>
              <Input
                placeholder={t('conflict_topic_placeholder')}
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                onKeyDown={(e: any) => e.key === 'Enter' && createMutation.mutate()}
              />
              <Button fullWidth onClick={() => createMutation.mutate()} loading={createMutation.isPending} className="mt-4">
                {t('start_session_btn')}
              </Button>
            </div>
          </motion.div>
        </div>
      </div>
    )
  }

  if (view === 'session' && activeId) {
    return <SessionView sessionId={activeId} me={me} onBack={() => setView('list')} />
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {/* Header */}
      <div className="page-hero px-5 pt-6 pb-5">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div
              className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-violet"
              style={{ boxShadow: '0 4px 14px rgba(56,92,138,0.28)' }}
            >
              <Scale size={17} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
              <p className="text-xs text-muted mt-0.5">{t('subtitle')}</p>
            </div>
          </div>
          <Button size="sm" variant="secondary" onClick={() => setView('create')}>
            <Plus size={15} /> {t('new_session_btn')}
          </Button>
        </div>
      </div>

      <div className="px-4 pt-4 md:px-5">
        {/* How it works */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
          className="mb-4 rounded-[20px] p-4"
          style={{ background: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)', border: '1px solid rgba(56,92,138,0.15)' }}
        >
          <div className="flex gap-3">
            <div
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-gradient-violet text-white"
              style={{ boxShadow: '0 4px 10px rgba(56,92,138,0.25)' }}
            >
              <ShieldCheck size={18} />
            </div>
            <div>
              <p className="font-semibold text-ink text-sm">{t('how_it_works_title')}</p>
              <p className="mt-1 text-xs text-muted leading-relaxed">
                {t('how_it_works_desc')}
              </p>
            </div>
          </div>
        </motion.div>

        {isLoading ? (
          <div className="flex flex-col gap-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-20 rounded-card shimmer" />
            ))}
          </div>
        ) : sessions.length === 0 ? (
          <EmptyState
            icon={<Scale />}
            title={t('empty_title')}
            description={t('empty_desc')}
            actionLabel={t('empty_btn')}
            onAction={() => setView('create')}
          />
        ) : (
          <div className="flex flex-col gap-3">
            {(sessions as ConflictSession[]).map((s, idx) => (
              <motion.div
                key={s.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] as [number, number, number, number], delay: idx * 0.05 }}
                className="rounded-[20px] bg-white p-5 cursor-pointer transition-all duration-200 hover:-translate-y-0.5"
                style={{
                  border: '1px solid rgba(232,227,218,0.6)',
                  boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 4px 12px rgba(23,21,42,0.04)',
                }}
                onClick={() => { setActiveId(s.id); setView('session') }}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-ink">{s.title}</p>
                    <p className="text-xs text-muted mt-0.5">
                      {new Date(s.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'long' })}
                    </p>
                  </div>
                  <Badge variant={(STATUS_BADGE as any)[s.status]}>{statusLabel(s.status)}</Badge>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

const SessionView = ({ sessionId, me, onBack }: { sessionId: string; me: any; onBack: () => void }) => {
  const { t } = useTranslation('mediation')
  const [form, setForm] = useState({ description: '', feelings: '', desired_outcome: '' })

  const { data: session, isLoading } = useQuery({
    queryKey: ['mediation', sessionId],
    queryFn: () => MediationService.get(sessionId),
    refetchInterval: (query) => (query.state.data as any)?.status === 'analyzing' ? 3000 : false,
  })

  const submitMutation = useMutation({
    mutationFn: () => MediationService.submitEntry(sessionId, form),
    onError: () => toast.error(t('toast_submit_error')),
  })

  if (isLoading || !session) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 size={24} className="animate-spin text-primary" />
      </div>
    )
  }

  const mySubmitted = session.my_entry_submitted
  const partnerSubmitted = session.partner_entry_submitted
  const isComplete = session.status === 'complete'
  const isAnalyzing = session.status === 'analyzing'

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <div className="page-hero px-5 pt-6 pb-5">
        <button onClick={onBack} className="mb-4 flex items-center gap-1.5 text-sm font-medium text-muted hover:text-primary transition-colors">
          <ChevronLeft size={16} /> {t('back_btn')}
        </button>
        <div className="flex items-center justify-between gap-3">
          <h1 className="text-xl font-bold text-ink leading-tight">{session.title}</h1>
          <Badge variant={(STATUS_BADGE as any)[session.status]}>{t(`status_${session.status}` as any)}</Badge>
        </div>
      </div>

      <div className="px-4 pt-4 md:px-5 max-w-2xl space-y-4">
        {/* Partner status */}
        <Card>
          <div className="flex items-center justify-around py-2">
            <div className="flex flex-col items-center gap-1.5">
              <div className={`flex h-11 w-11 items-center justify-center rounded-full text-sm font-bold transition-all ${
                mySubmitted ? 'bg-gradient-sage text-white shadow-[0_4px_10px_rgba(91,189,138,0.3)]' : 'bg-primary-light text-primary'
              }`}>
                {mySubmitted ? <CheckCircle2 size={20} /> : me?.first_name?.[0]?.toUpperCase()}
              </div>
              <p className="text-xs font-semibold text-ink">{me?.first_name ?? t('common:you', { defaultValue: 'Вы' })}</p>
              <p className="text-[10px] text-muted">{mySubmitted ? t('submitted_title') : t('waiting_title')}</p>
            </div>
            <Scale size={22} className="text-violet/40" />
            <div className="flex flex-col items-center gap-1.5">
              <div className={`flex h-11 w-11 items-center justify-center rounded-full text-sm font-bold transition-all ${
                partnerSubmitted ? 'bg-gradient-sage text-white shadow-[0_4px_10px_rgba(91,189,138,0.3)]' : 'bg-gray-100 text-muted'
              }`}>
                {partnerSubmitted ? <CheckCircle2 size={20} /> : <Clock size={18} />}
              </div>
              <p className="text-xs font-semibold text-ink">{t('common:partner', { defaultValue: 'Партнёр' })}</p>
              <p className="text-[10px] text-muted">{partnerSubmitted ? t('submitted_title') : t('waiting_title')}</p>
            </div>
          </div>
        </Card>

        {/* Entry form */}
        {!mySubmitted && (
          <Card>
            <h2 className="mb-4 font-bold text-ink">{t('your_version_title')}</h2>
            <div className="mb-4 flex items-center gap-2 rounded-2xl bg-violet-light px-3 py-2.5">
              <ShieldCheck size={14} className="text-violet shrink-0" />
              <span className="text-xs text-violet font-medium">{t('privacy_shield')}</span>
            </div>
            <div className="flex flex-col gap-4">
              <Textarea
                label={t('form_describe_label')}
                rows={4}
                placeholder={t('form_describe_placeholder')}
                value={form.description}
                onChange={(e) => setForm(f => ({ ...f, description: e.target.value }))}
              />
              <Textarea
                label={t('form_feelings_label')}
                rows={2}
                placeholder={t('form_feelings_placeholder')}
                value={form.feelings}
                onChange={(e) => setForm(f => ({ ...f, feelings: e.target.value }))}
              />
              <Textarea
                label={t('form_outcome_label')}
                rows={2}
                placeholder={t('form_outcome_placeholder')}
                value={form.desired_outcome}
                onChange={(e) => setForm(f => ({ ...f, desired_outcome: e.target.value }))}
              />
              <Button
                fullWidth
                variant="violet"
                onClick={() => submitMutation.mutate()}
                loading={submitMutation.isPending}
                disabled={!form.description.trim()}
              >
                {t('submit_btn')}
              </Button>
            </div>
          </Card>
        )}

        {mySubmitted && !isComplete && (
          <Card className="py-10 text-center">
            {isAnalyzing ? (
              <>
                <Loader2 size={36} className="mx-auto mb-3 animate-spin text-violet" />
                <p className="font-bold text-ink">{t('analyzing_title')}</p>
                <p className="mt-1 text-sm text-muted">{t('analyzing_desc')}</p>
              </>
            ) : (
              <>
                <Clock size={36} className="mx-auto mb-3 text-warning" />
                <p className="font-bold text-ink">{t('waiting_partner_title')}</p>
                <p className="mt-1 text-sm text-muted">{t('waiting_partner_desc')}</p>
              </>
            )}
          </Card>
        )}

        {/* Analysis result */}
        {isComplete && session.ai_analysis && (
          <>
            <div
              className="rounded-[20px] p-4"
              style={{ background: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)', border: '1px solid rgba(56,92,138,0.15)' }}
            >
              <p className="text-xs font-bold uppercase tracking-wider text-violet mb-2">{t('analysis_header')}</p>
              <p className="text-sm text-muted">{t('analysis_neutral')}</p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <Card>
                <p className="mb-2 text-xs font-bold uppercase tracking-wider text-violet">{t('position_a')}</p>
                <p className="text-sm text-ink leading-relaxed">{session.ai_analysis.partner_a_position}</p>
              </Card>
              <Card>
                <p className="mb-2 text-xs font-bold uppercase tracking-wider text-primary">{t('position_b')}</p>
                <p className="text-sm text-ink leading-relaxed">{session.ai_analysis.partner_b_position}</p>
              </Card>
            </div>

            <Card>
              <p className="mb-3 text-xs font-bold uppercase tracking-wider text-success">{t('common_interests')}</p>
              <ul className="flex flex-col gap-2">
                {session.ai_analysis.common_interests.map((item: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink">
                    <CheckCircle2 size={15} className="mt-0.5 shrink-0 text-success" /> {item}
                  </li>
                ))}
              </ul>
            </Card>

            <Card>
              <p className="mb-3 text-xs font-bold uppercase tracking-wider text-warning">{t('conflict_points')}</p>
              <ul className="flex flex-col gap-2">
                {session.ai_analysis.conflict_points.map((item: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink">
                    <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-warning" /> {item}
                  </li>
                ))}
              </ul>
            </Card>

            <Card>
              <p className="mb-3 text-xs font-bold uppercase tracking-wider text-primary">{t('compromises')}</p>
              <div className="flex flex-col gap-3">
                {session.ai_analysis.compromises.map((c: any, i: number) => (
                  <div key={i} className="rounded-2xl bg-primary-light px-4 py-3">
                    <p className="font-semibold text-ink text-sm">{c.title}</p>
                    <p className="mt-1 text-xs text-muted">{c.description}</p>
                  </div>
                ))}
              </div>
            </Card>

            <div className="rounded-card p-4" style={{ background: 'linear-gradient(135deg, #ECFDF5 0%, #F0FFF4 100%)', border: '1px solid rgba(91,189,138,0.2)' }}>
              <p className="text-xs font-bold uppercase tracking-wider text-success mb-2">{t('first_step')}</p>
              <p className="text-sm font-semibold text-ink">{session.ai_analysis.first_step}</p>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
