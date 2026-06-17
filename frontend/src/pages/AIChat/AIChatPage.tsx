import { useState, useRef, useEffect, useCallback } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageCircle, Plus, ArrowRight, SendHorizonal, Square, ChevronLeft, Sparkles } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AIService } from '@/services/ai.service'
import { AuthService } from '@/services/auth.service'
import { AnalyticsService } from '@/services/analytics.service'
import { Button } from '@/components/ui/Button'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { Message } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

/* ── Message bubbles ─────────────────────────────────────────────────── */
const BubbleUser = ({ text }: { text: string }) => (
  <motion.div
    initial={{ opacity: 0, y: 8, scale: 0.97 }}
    animate={{ opacity: 1, y: 0, scale: 1 }}
    transition={{ duration: 0.25, ease }}
    className="flex justify-end"
  >
    <div
      className="max-w-[78%] px-4 py-3 text-sm text-white leading-relaxed"
      style={{
        borderRadius: '20px 20px 6px 20px',
        background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
        boxShadow: '0 4px 14px rgba(60,56,136,0.25)',
      }}
    >
      {text}
    </div>
  </motion.div>
)

const BubbleAssistant = ({ text, streaming }: { text: string; streaming?: boolean }) => (
  <motion.div
    initial={{ opacity: 0, y: 8, scale: 0.97 }}
    animate={{ opacity: 1, y: 0, scale: 1 }}
    transition={{ duration: 0.25, ease }}
    className="flex justify-start gap-2.5"
  >
    <div
      className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full mt-0.5"
      style={{
        background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
        boxShadow: '0 2px 8px rgba(60,56,136,0.22)',
      }}
    >
      <Sparkles size={12} className="text-white" />
    </div>
    <div
      className="max-w-[78%] px-4 py-3 text-sm text-ink leading-relaxed"
      style={{
        borderRadius: '20px 20px 20px 6px',
        background: '#F4EFE4',
        border: '1px solid rgba(232,227,218,0.8)',
        boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 4px 12px rgba(23,21,42,0.06)',
      }}
    >
      {text}
      {streaming && (
        <span className="ml-1 inline-block h-3.5 w-0.5 rounded-full bg-primary align-middle animate-pulse-soft" />
      )}
    </div>
  </motion.div>
)

/* ── Main component ──────────────────────────────────────────────────── */
export const AIChatPage = () => {
  const qc = useQueryClient()
  const { convId } = useParams<{ convId?: string }>()
  const { t, i18n } = useTranslation('ai')
  const [conversationId, setConversationId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [streamingText, setStreamingText] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)
  const abortRef = useRef<AbortController | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const QUICK_TOPICS = [
    { label: t('quick_conflict_label'),      emoji: '⚡', prompt: t('quick_conflict_prompt') },
    { label: t('quick_intimacy_label'),      emoji: '💫', prompt: t('quick_intimacy_prompt') },
    { label: t('quick_communication_label'), emoji: '💬', prompt: t('quick_communication_prompt') },
    { label: t('quick_goals_label'),         emoji: '🎯', prompt: t('quick_goals_prompt') },
  ]

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: conversations } = useQuery({
    queryKey: ['conversations'],
    queryFn: AIService.listConversations,
  })
  const { data: latestAnalytics } = useQuery({
    queryKey: ['analytics', 'latest'],
    queryFn: AnalyticsService.getLatest,
    enabled: !!me?.couple,
    retry: false,
  })

  const createMutation = useMutation({
    mutationFn: () => AIService.createConversation(),
    onSuccess: (conv) => {
      setConversationId(conv.id)
      setMessages([])
      qc.invalidateQueries({ queryKey: ['conversations'] })
    },
  })

  const loadConversation = async (id: string) => {
    const data = await AIService.getMessages(id)
    setConversationId(id)
    setMessages(data.results ?? [])
  }

  useEffect(() => {
    if (convId && convId !== conversationId) loadConversation(convId)
  }, [convId])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, streamingText])

  const sendMessage = useCallback(async (text?: string) => {
    const userText = (text ?? input).trim()
    if (!userText || isStreaming || !conversationId) return

    setInput('')
    setMessages((prev) => [
      ...prev,
      { id: Date.now().toString(), role: 'user', content: userText, created_at: new Date().toISOString() },
    ])
    setIsStreaming(true)
    setStreamingText('')
    abortRef.current = new AbortController()

    try {
      let full = ''
      await AIService.streamMessage(
        conversationId,
        userText,
        (chunk) => { full += chunk; setStreamingText(full) },
        abortRef.current.signal,
      )
      setMessages((prev) => [
        ...prev,
        { id: Date.now().toString(), role: 'assistant', content: full, created_at: new Date().toISOString() },
      ])
    } catch (e: any) {
      if (e?.name !== 'AbortError') {
        setMessages((prev) => [
          ...prev,
          { id: 'err', role: 'assistant', content: t('error_message'), created_at: new Date().toISOString() },
        ])
      }
    } finally {
      setIsStreaming(false)
      setStreamingText('')
    }
  }, [input, isStreaming, conversationId, t])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() }
  }

  const score = latestAnalytics ? Math.round(latestAnalytics.overall_score) : null

  /* ── No couple ───────────────────────────────────────────────────── */
  if (!me?.couple) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="page-hero px-5 pt-6 pb-5">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-brand shadow-[0_4px_12px_rgba(60,56,136,0.28)]">
              <MessageCircle size={16} className="text-white" />
            </div>
            <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
          </div>
        </div>
        <div className="px-4 pt-4">
          <EmptyState
            icon={<MessageCircle />}
            title={t('no_couple_title')}
            description={t('no_couple_desc')}
          />
        </div>
      </div>
    )
  }

  /* ── Conversation list ───────────────────────────────────────────── */
  if (!conversationId) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">

        {/* Consultant card */}
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease }}
        >
          <div
            className="px-5 pt-6 pb-6"
            style={{
              background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 100%)',
              borderBottom: '1px solid rgba(60,56,136,0.10)',
            }}
          >
            <div className="flex items-start gap-4">
              {/* Avatar */}
              <div
                className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl"
                style={{
                  background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
                  boxShadow: '0 6px 20px rgba(60,56,136,0.30)',
                }}
              >
                <Sparkles size={24} className="text-white" />
              </div>
              <div className="flex-1 pt-1">
                <h1 className="text-lg font-bold text-ink">{t('title')}</h1>
                <p className="text-xs text-muted mt-0.5">{t('subtitle')}</p>
                {/* Status pills */}
                <div className="mt-2 flex gap-2">
                  <span className="inline-flex items-center gap-1 rounded-pill __BGWHITE_ALPHA___ px-2.5 py-1 text-[11px] font-semibold text-primary-700 border border-primary-100/60">
                    <span className="h-1.5 w-1.5 rounded-full bg-sage-700 animate-pulse-soft" />
                    {t('online')}
                  </span>
                  <span className="inline-flex items-center rounded-pill __BGWHITE_ALPHA___ px-2.5 py-1 text-[11px] font-semibold text-muted border border-sand/60">
                    {t('confidential')}
                  </span>
                </div>
              </div>
            </div>

            {/* Couple context */}
            {score !== null && (
              <div
                className="mt-4 rounded-[16px] px-4 py-3 flex items-center gap-3"
                style={{ background: 'rgba(255,255,255,0.65)', border: '1px solid rgba(60,56,136,0.12)' }}
              >
                <div className="flex-1">
                  <p className="text-[11px] font-semibold text-muted uppercase tracking-wide">{t('couple_context')}</p>
                  <p className="text-sm font-bold text-ink mt-0.5">{t('couple_index', { score })}</p>
                </div>
                <div
                  className="h-10 w-10 rounded-[12px] flex items-center justify-center text-sm font-bold text-white"
                  style={{ background: `linear-gradient(135deg, #3C3888, #385C8A)` }}
                >
                  {score}
                </div>
              </div>
            )}
          </div>
        </motion.div>

        <div className="px-4 pt-5 space-y-5">

          {/* Quick topics */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease, delay: 0.08 }}
          >
            <p className="label-caps text-muted mb-3">{t('topics_label')}</p>
            <div className="grid grid-cols-2 gap-2.5">
              {QUICK_TOPICS.map((topic, i) => (
                <motion.button
                  key={topic.label}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.25, ease, delay: 0.1 + i * 0.04 }}
                  onClick={() => {
                    createMutation.mutate(undefined, {
                      onSuccess: (conv) => {
                        setConversationId(conv.id)
                        setMessages([])
                        setTimeout(() => sendMessageDirect(conv.id, topic.prompt), 100)
                      },
                    })
                  }}
                  className="flex items-start gap-2.5 rounded-[18px] bg-canvas p-4 text-left border border-sand/60 transition-all duration-150 hover:border-primary-100 hover:shadow-hover hover:-translate-y-0.5"
                  style={{ boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
                >
                  <span className="text-xl mt-0.5">{topic.emoji}</span>
                  <div>
                    <p className="text-sm font-bold text-ink">{topic.label}</p>
                    <p className="text-xs text-muted mt-0.5 leading-snug">{topic.prompt}</p>
                  </div>
                </motion.button>
              ))}
            </div>
          </motion.div>

          {/* New conversation button */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease, delay: 0.15 }}
          >
            <Button
              fullWidth
              onClick={() => createMutation.mutate()}
              loading={createMutation.isPending}
              size="lg"
            >
              <Plus size={16} /> {t('new_chat_btn')}
            </Button>
          </motion.div>

          {/* Past conversations */}
          {(conversations?.results?.length ?? 0) > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, ease, delay: 0.18 }}
            >
              <p className="label-caps text-muted mb-3">{t('past_chats')}</p>
              <div className="flex flex-col gap-2.5">
                {(conversations!.results ?? []).map((c) => (
                  <button
                    key={c.id}
                    onClick={() => loadConversation(c.id)}
                    className="flex items-center justify-between rounded-[20px] bg-canvas px-5 py-4 text-left border border-sand/60 transition-all duration-150 hover:border-primary-100 hover:shadow-hover hover:-translate-y-0.5"
                    style={{ boxShadow: '0 1px 3px rgba(23,21,42,0.04)' }}
                  >
                    <div>
                      <p className="font-semibold text-ink text-sm">{c.title || t('chat_fallback_title')}</p>
                      <p className="text-xs text-muted mt-0.5">
                        {c.messages_count} {t('common:messages')} · {new Date(c.updated_at).toLocaleDateString(dateLocale)}
                      </p>
                    </div>
                    <ArrowRight size={15} className="text-muted/40" />
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </div>
      </div>
    )
  }

  /* ── Active chat ─────────────────────────────────────────────────── */
  return (
    <div className="flex h-full flex-col bg-surface">

      {/* Chat header */}
      <div
        className="flex items-center gap-3 px-4 py-3 flex-shrink-0"
        style={{
          background: 'rgba(248,246,242,0.92)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(232,227,218,0.8)',
        }}
      >
        <button
          onClick={() => setConversationId(null)}
          className="flex h-8 w-8 items-center justify-center rounded-xl bg-primary-50 text-primary-700 transition-colors hover:bg-primary-100"
        >
          <ChevronLeft size={16} />
        </button>

        <div
          className="flex h-9 w-9 items-center justify-center rounded-xl"
          style={{ background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)', boxShadow: '0 3px 10px rgba(60,56,136,0.25)' }}
        >
          <Sparkles size={15} className="text-white" />
        </div>

        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-ink leading-tight">{t('title')}</p>
          <p className="text-[11px] text-muted">
            {isStreaming ? (
              <span className="text-primary font-semibold">{t('typing')}</span>
            ) : t('status_bar')}
          </p>
        </div>

        {score !== null && (
          <div
            className="flex h-8 items-center px-2.5 rounded-pill text-[11px] font-bold text-white"
            style={{ background: 'linear-gradient(135deg, #3C3888, #385C8A)' }}
          >
            {score}
          </div>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-5 space-y-3">
        {!messages.length && !streamingText && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, ease }}
            className="mt-8 flex flex-col items-center text-center px-4"
          >
            <div
              className="mb-4 flex h-16 w-16 items-center justify-center rounded-3xl"
              style={{
                background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
                boxShadow: '0 8px 28px rgba(60,56,136,0.28)',
              }}
            >
              <Sparkles size={28} className="text-white" />
            </div>
            <p className="text-base font-semibold text-ink">{t('empty_hint')}</p>
            <p className="mt-1.5 text-sm text-muted leading-relaxed max-w-xs">
              {t('empty_sub')}
            </p>

            {/* Quick topics in chat */}
            <div className="mt-5 flex flex-col gap-2 w-full max-w-xs">
              {QUICK_TOPICS.map((topic) => (
                <button
                  key={topic.label}
                  onClick={() => sendMessage(topic.prompt)}
                  disabled={isStreaming}
                  className="flex items-center gap-2.5 rounded-[14px] bg-canvas px-4 py-2.5 text-left border border-sand/60 text-sm text-ink font-medium hover:border-primary-100 transition-colors"
                >
                  <span>{topic.emoji}</span>
                  <span>{topic.prompt}</span>
                </button>
              ))}
            </div>
          </motion.div>
        )}

        <AnimatePresence>
          {messages.map((msg) =>
            msg.role === 'user'
              ? <BubbleUser key={msg.id} text={msg.content} />
              : <BubbleAssistant key={msg.id} text={msg.content} />
          )}
          {streamingText && <BubbleAssistant text={streamingText} streaming />}
        </AnimatePresence>
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div
        className="px-4 py-3 flex-shrink-0"
        style={{
          background: 'rgba(248,246,242,0.96)',
          backdropFilter: 'blur(20px)',
          borderTop: '1px solid rgba(232,227,218,0.8)',
        }}
      >
        <div className="flex items-end gap-2.5">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={t('input_placeholder')}
            rows={1}
            className="flex-1 resize-none rounded-[16px] border border-sand bg-canvas px-4 py-2.5 text-sm text-ink placeholder:text-muted/50 outline-none transition-all duration-200 focus:border-primary/40 focus:shadow-[0_0_0_3px_rgba(60,56,136,0.11)]"
            style={{ minHeight: '42px', maxHeight: '120px' }}
          />

          {isStreaming ? (
            <button
              onClick={() => abortRef.current?.abort()}
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[14px] bg-rose-50 text-rose-600 hover:bg-rose-100 transition-colors"
            >
              <Square size={15} fill="currentColor" />
            </button>
          ) : (
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim()}
              className="flex h-10 w-10 shrink-0 items-center justify-center rounded-[14px] text-white transition-all disabled:opacity-40 disabled:cursor-not-allowed"
              style={{
                background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
                boxShadow: input.trim() ? '0 4px 14px rgba(60,56,136,0.30)' : 'none',
              }}
            >
              <SendHorizonal size={15} />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

/* Helper for quick topics — fires after conversation is created */
async function sendMessageDirect(convId: string, text: string) {
  try {
    await AIService.streamMessage(convId, text, () => {}, new AbortController().signal)
  } catch {}
}
