import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Heart, Sparkles, Sun, MessageCircle, ArrowRight,
  ClipboardList, Brain, Scale, Users, Shield, CheckSquare, UserPlus,
} from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { AuthService } from '@/services/auth.service'

const ease = [0.16, 1, 0.3, 1] as [number, number, number, number]
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 14 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease, delay },
})

const FEATURES = [
  { key: 'diagnostics', Icon: ClipboardList, path: '/app/diagnostics' },
  { key: 'index',       Icon: Heart,         path: '/app/index' },
  { key: 'practices',   Icon: Sun,           path: '/app/practices' },
  { key: 'academy',     Icon: Brain,         path: '/app/academy' },
  { key: 'ai',          Icon: MessageCircle, path: '/app/ai' },
  { key: 'mediation',   Icon: Scale,         path: '/app/mediation' },
]

const VALUES = [
  { key: 'two',    Icon: Users },
  { key: 'honest', Icon: Shield },
  { key: 'steps',  Icon: CheckSquare },
]

export const DashboardPage = () => {
  const navigate = useNavigate()
  const { t } = useTranslation('dashboard')
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const hasCouple = !!me?.couple

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">

      {/* ── Hero Banner ─────────────────────────────────────────── */}
      <motion.div {...fadeUp(0)} className="px-4 pt-5">
        <div
          className="relative overflow-hidden rounded-[28px] px-6 pt-7 pb-8"
          style={{
            background: 'linear-gradient(145deg, #3C3888 0%, #2B5EA7 100%)',
            boxShadow: '0 14px 44px rgba(60,56,136,0.30)',
          }}
        >
          {/* Decorative blobs */}
          <div className="pointer-events-none absolute -top-10 -right-10 h-40 w-40 rounded-full bg-white/10" />
          <div className="pointer-events-none absolute -bottom-14 -left-8 h-32 w-32 rounded-full bg-white/[0.07]" />
          <div className="pointer-events-none absolute top-4 right-16 h-12 w-12 rounded-full bg-white/[0.06]" />

          {/* Badge */}
          <div className="mb-4 inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1.5">
            <Heart size={11} className="text-rose-200" fill="currentColor" />
            <span className="text-xs font-semibold text-white/90">{t('hero_title')}</span>
          </div>

          <h1 className="text-[22px] font-bold leading-tight text-white">
            {t('hero_tagline')}
          </h1>
          <p className="mt-2.5 max-w-[280px] text-sm leading-relaxed text-white/65">
            {t('hero_desc')}
          </p>

          <button
            onClick={() => navigate('/app/diagnostics')}
            className="mt-6 inline-flex items-center gap-2 rounded-[12px] bg-white px-5 py-2.5 text-sm font-bold shadow-lg transition-opacity active:opacity-75"
            style={{ color: '#3C3888' }}
          >
            <Sparkles size={14} />
            {t('cta_btn')}
          </button>
        </div>
      </motion.div>

      <div className="mt-5 space-y-5 px-4">

        {/* ── No-couple CTA ────────────────────────────────────── */}
        {me && !hasCouple && (
          <motion.div {...fadeUp(0.06)}>
            <button
              onClick={() => navigate('/app/couple')}
              className="w-full flex items-center gap-4 rounded-[18px] p-4 text-left transition-all duration-150 active:scale-[0.98]"
              style={{
                background: 'linear-gradient(135deg, #FFF8EC 0%, #FFF3E4 100%)',
                border: '1px solid rgba(136,96,40,0.20)',
                boxShadow: '0 2px 10px rgba(136,96,40,0.08)',
              }}
            >
              <div
                className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl"
                style={{ background: 'rgba(136,96,40,0.12)' }}
              >
                <UserPlus size={18} style={{ color: '#886028' }} />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-bold" style={{ color: '#886028' }}>{t('no_couple_cta_title')}</p>
                <p className="mt-0.5 text-xs leading-relaxed" style={{ color: '#886028', opacity: 0.75 }}>
                  {t('no_couple_cta_desc')}
                </p>
              </div>
              <ArrowRight size={15} style={{ color: '#886028', opacity: 0.5 }} className="shrink-0" />
            </button>
          </motion.div>
        )}

        {/* ── Features List ────────────────────────────────────── */}
        <div>
          <motion.p {...fadeUp(0.08)} className="label-caps mb-3 px-0.5 text-muted">
            {t('features_label')}
          </motion.p>

          <div className="flex flex-col gap-2.5">
            {FEATURES.map(({ key, Icon, path }, i) => (
              <motion.div key={key} {...fadeUp(0.10 + i * 0.04)}>
                <div
                  onClick={() => navigate(path)}
                  className="flex items-center gap-4 cursor-pointer rounded-[18px] bg-white p-4 transition-all duration-150 active:scale-[0.98]"
                  style={{
                    border: '1px solid rgba(60,56,136,0.08)',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
                  }}
                >
                  <div
                    className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-white"
                    style={{
                      background: 'linear-gradient(135deg, #3C3888 0%, #385C8A 100%)',
                      boxShadow: '0 3px 10px rgba(60,56,136,0.22)',
                    }}
                  >
                    <Icon size={18} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-bold text-ink">{t(`feat_${key}_title`)}</p>
                    <p className="line-clamp-2 mt-0.5 text-xs leading-relaxed text-muted">
                      {t(`feat_${key}_desc`)}
                    </p>
                  </div>
                  <ArrowRight size={15} className="shrink-0 text-muted/30" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* ── Values ───────────────────────────────────────────── */}
        <div>
          <motion.p {...fadeUp(0.46)} className="label-caps mb-3 px-0.5 text-muted">
            {t('values_label')}
          </motion.p>
          <div className="space-y-2.5">
            {VALUES.map(({ key, Icon }, i) => (
              <motion.div key={key} {...fadeUp(0.48 + i * 0.04)}>
                <div
                  className="flex items-start gap-3 rounded-[18px] p-4"
                  style={{
                    background: 'linear-gradient(145deg, #F5F3FB 0%, #EFF4FB 100%)',
                    border: '1px solid rgba(60,56,136,0.08)',
                  }}
                >
                  <div
                    className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl"
                    style={{ background: 'rgba(60,56,136,0.10)' }}
                  >
                    <Icon size={16} className="text-primary" />
                  </div>
                  <div className="pt-0.5">
                    <p className="text-sm font-bold text-ink">{t(`value_${key}_title`)}</p>
                    <p className="mt-0.5 text-xs leading-relaxed text-muted">{t(`value_${key}_desc`)}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}
