import { Link, Navigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { ClipboardList, MessageCircle, Sun, Heart, Shield, Globe, TrendingUp } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { LanguageSwitcher } from '@/components/LanguageSwitcher'
import { useAuthStore } from '@/store/auth.store'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.55, ease, delay },
})

const FEATURES = [
  { icon: ClipboardList, key: 'diag',     color: 'bg-primary/10 text-primary' },
  { icon: MessageCircle, key: 'ai',       color: 'bg-violet/10 text-violet' },
  { icon: Sun,           key: 'practice', color: 'bg-accent/10 text-accent' },
  { icon: TrendingUp,    key: 'index',    color: 'bg-sage/10 text-sage' },
]

const TRUST = [Shield, Globe, Heart]

export const LandingPage = () => {
  const { t } = useTranslation('landing')
  const token = useAuthStore((s) => s.tokens?.access)

  if (token) return <Navigate to="/app" replace />

  return (
    <div className="min-h-screen bg-surface">

      {/* ── Header ───────────────────────────────────────────────── */}
      <header className="fixed top-0 inset-x-0 z-50 flex items-center justify-between px-5 py-3"
        style={{ background: 'rgba(232,226,212,0.85)', backdropFilter: 'blur(20px)', borderBottom: '1px solid rgba(194,184,164,0.35)' }}
      >
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-brand shadow-[0_4px_12px_rgba(60,56,136,0.32)]">
            <img src="/favicon.png" alt="Oila AI" className="w-full h-full object-cover rounded-xl" />
          </div>
          <span className="text-[15px] font-bold text-ink tracking-tight">Oila AI</span>
        </div>
        <div className="flex items-center gap-3">
          <LanguageSwitcher />
          <Link to="/login">
            <Button variant="ghost" size="sm">{t('cta_login')}</Button>
          </Link>
          <Link to="/register">
            <Button size="sm">{t('cta_start')}</Button>
          </Link>
        </div>
      </header>

      {/* ── Hero ─────────────────────────────────────────────────── */}
      <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-5 pt-20 pb-16">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-hero" />
        <div className="absolute inset-0 bg-dots-light opacity-30" />

        {/* Orbs */}
        <div className="pointer-events-none absolute -top-32 -left-32 h-[500px] w-[500px] rounded-full bg-primary/7 blur-[100px]" />
        <div className="pointer-events-none absolute -bottom-32 -right-32 h-[500px] w-[500px] rounded-full bg-violet/7 blur-[100px]" />
        <div className="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-64 w-64 rounded-full bg-sage/5 blur-[80px]" />

        <div className="relative z-10 flex max-w-2xl flex-col items-center text-center gap-6">
          {/* Badge */}
          <motion.div {...fadeUp(0)}>
            <div className="inline-flex items-center gap-2 rounded-full px-4 py-1.5"
              style={{ background: 'rgba(60,56,136,0.10)', border: '1px solid rgba(60,56,136,0.16)' }}
            >
              <Heart size={12} className="text-primary" fill="currentColor" />
              <span className="text-xs font-semibold text-primary">{t('hero_badge')}</span>
            </div>
          </motion.div>

          {/* Logo */}
          <motion.div {...fadeUp(0.06)}
            className="flex h-20 w-20 items-center justify-center rounded-[24px] bg-gradient-brand animate-float"
            style={{ boxShadow: '0 16px 48px rgba(60,56,136,0.40)' }}
          >
            <img src="/favicon.png" alt="Oila AI" className="w-full h-full object-cover rounded-[24px]" />
          </motion.div>

          {/* Headline */}
          <motion.h1 {...fadeUp(0.10)}
            className="font-display text-5xl md:text-6xl text-ink whitespace-pre-line"
          >
            {t('hero_title').split('\n')[0]}{' '}
            <span className="text-gradient">{t('hero_title').split('\n')[1]}</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p {...fadeUp(0.15)}
            className="max-w-lg text-base md:text-lg text-muted leading-relaxed text-balance"
          >
            {t('hero_subtitle')}
          </motion.p>

          {/* CTAs */}
          <motion.div {...fadeUp(0.20)} className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
            <Link to="/register" className="sm:w-auto w-full">
              <Button size="lg" fullWidth className="text-base px-8">
                {t('cta_start')}
              </Button>
            </Link>
            <Link to="/login" className="sm:w-auto w-full">
              <Button size="lg" variant="ghost" fullWidth className="text-base px-8">
                {t('cta_login')}
              </Button>
            </Link>
          </motion.div>

          {/* Trust row */}
          <motion.div {...fadeUp(0.25)} className="flex flex-col sm:flex-row items-center gap-4 mt-2">
            {[0, 1, 2].map((i) => {
              const Icon = TRUST[i]
              return (
                <div key={i} className="flex items-center gap-2">
                  <Icon size={14} className="text-primary/60" />
                  <span className="text-xs text-muted">{t(`trust_${i + 1}`)}</span>
                </div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* ── Features ─────────────────────────────────────────────── */}
      <section className="px-5 py-20 bg-surface">
        <div className="mx-auto max-w-3xl">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-80px' }}
            transition={{ duration: 0.5, ease }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-ink mb-3">{t('features_title')}</h2>
            <p className="text-muted text-balance max-w-md mx-auto">{t('features_subtitle')}</p>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {FEATURES.map(({ icon: Icon, key, color }, i) => (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{ duration: 0.45, ease, delay: i * 0.07 }}
                className="card-base lift p-6 flex flex-col gap-4"
              >
                <div className={`flex h-11 w-11 items-center justify-center rounded-2xl ${color}`}>
                  <Icon size={22} />
                </div>
                <div>
                  <h3 className="font-bold text-ink mb-1.5">{t(`feat_${key}_title`)}</h3>
                  <p className="text-sm text-muted leading-relaxed">{t(`feat_${key}_desc`)}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Final CTA ────────────────────────────────────────────── */}
      <section className="px-5 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.5, ease }}
          className="mx-auto max-w-lg text-center"
        >
          <div className="relative overflow-hidden rounded-[32px] px-8 py-12"
            style={{
              background: 'linear-gradient(145deg, #3C3888 0%, #385C8A 100%)',
              boxShadow: '0 20px 60px rgba(60,56,136,0.35)',
            }}
          >
            <div className="pointer-events-none absolute -top-10 -right-10 h-40 w-40 rounded-full bg-white/10" />
            <div className="pointer-events-none absolute -bottom-10 -left-10 h-32 w-32 rounded-full bg-white/[0.07]" />

            <div className="relative z-10 flex flex-col items-center gap-5">
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-white/15">
                <Heart size={26} className="text-white" fill="currentColor" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">{t('trust_title')}</h2>
                <p className="text-white/70 text-sm">{t('footer_tagline')}</p>
              </div>
              <Link to="/register">
                <button className="inline-flex items-center gap-2 rounded-btn bg-white px-7 py-3 text-[15px] font-semibold text-primary shadow-[0_4px_20px_rgba(0,0,0,0.20)] hover:brightness-95 active:scale-[0.97] transition-all">
                  {t('cta_start')}
                </button>
              </Link>
            </div>
          </div>
        </motion.div>
      </section>

      {/* ── Footer ───────────────────────────────────────────────── */}
      <footer className="px-5 py-6 border-t border-sand/40">
        <div className="mx-auto max-w-3xl flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-gradient-brand">
              <img src="/favicon.png" alt="Oila AI" className="w-full h-full object-cover rounded-lg" />
            </div>
            <span className="text-sm font-semibold text-ink">Oila AI</span>
          </div>
          <span className="text-xs text-muted">© 2026 Oila AI</span>
        </div>
      </footer>
    </div>
  )
}
