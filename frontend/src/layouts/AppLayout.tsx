import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import {
  Home, ClipboardList, MessageCircle,
  LogOut, User, Scale, Sun, Heart, Sparkles, Brain,
  MoreHorizontal, X,
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQueryClient } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { cn } from '@/lib/cn'
import { useAuthStore } from '@/store/auth.store'
import { AuthService } from '@/services/auth.service'
import { LanguageSwitcher } from '@/components/LanguageSwitcher'

const NAV_ITEMS = [
  { to: '/app',             icon: Home,          key: 'nav.home',        end: true  },
  { to: '/app/diagnostics', icon: ClipboardList, key: 'nav.diagnostics', end: false },
  { to: '/app/index',       icon: Heart,         key: 'nav.index',       end: false },
  { to: '/app/academy',     icon: Brain,         key: 'nav.academy',     end: false },
  { to: '/app/practices',   icon: Sun,           key: 'nav.practices',   end: false },
  { to: '/app/ai',          icon: MessageCircle, key: 'nav.ai',          end: false },
  { to: '/app/mediation',   icon: Scale,         key: 'nav.mediation',   end: false },
]

// 4 primary tabs always visible
const PRIMARY_NAV = [
  { to: '/app',           icon: Home,          key: 'nav.home',      end: true  },
  { to: '/app/practices', icon: Sun,           key: 'nav.practices', end: false },
  { to: '/app/academy',   icon: Brain,         key: 'nav.academy',   end: false },
  { to: '/app/ai',        icon: MessageCircle, key: 'nav.ai',        end: false },
]

// Secondary items in "More" sheet
const MORE_NAV = [
  { to: '/app/index',       icon: Heart,         key: 'nav.index'      },
  { to: '/app/mediation',   icon: Scale,         key: 'nav.mediation'  },
  { to: '/app/diagnostics', icon: ClipboardList, key: 'nav.diagnostics'},
  { to: '/app/profile',     icon: User,          key: 'nav.profile'    },
]

export const AppLayout = () => {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t } = useTranslation('common')
  const [moreOpen, setMoreOpen] = useState(false)
  const { refreshToken, logout } = useAuthStore((s) => ({
    refreshToken: s.refreshToken,
    logout: s.logout,
  }))

  const handleLogout = async () => {
    try { if (refreshToken) await AuthService.logout(refreshToken) } catch {}
    finally { logout(); qc.clear(); navigate('/login', { replace: true }) }
  }

  const handleMoreNav = (to: string) => {
    setMoreOpen(false)
    navigate(to)
  }

  return (
    <div className="flex h-dvh bg-surface">
      {/* ── Sidebar (desktop) ───────────────────────────────────── */}
      <aside className="hidden w-60 flex-shrink-0 md:flex md:flex-col">
        <div className="flex h-[60px] items-center gap-3 px-5 border-b border-white/8">
          <div className="flex h-8 w-8 items-center justify-center rounded-[10px] bg-gradient-brand shadow-[0_3px_14px_rgba(23,21,42,0.50)] overflow-hidden">
            <img src="/favicon.png" alt="Oila AI" className="w-full h-full object-cover" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-bold text-[#F7F8FC]">{t('app_name')}</p>
            <p className="text-[10px] text-[#9DA1C4]">{t('app_tagline')}</p>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-3 space-y-0.5">
          {NAV_ITEMS.map(({ to, icon: Icon, key, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) => cn(
                'flex items-center gap-2.5 rounded-[14px] px-3 py-2.5 text-sm font-medium transition-all duration-150',
                isActive
                  ? 'bg-[#4A4F80] text-[#F7F8FC] shadow-[inset_0_0_0_1px_rgba(255,255,255,0.14),_0_2px_10px_rgba(74,79,128,0.35)]'
                  : 'text-[#C8CCDD] hover:bg-[#3A3E66] hover:text-[#F7F8FC]',
              )}
            >
              {({ isActive }) => (
                <>
                  <Icon size={16} className={isActive ? 'text-[#F7F8FC]' : 'text-[#9DA1C4]'} strokeWidth={isActive ? 2.5 : 2} />
                  <span>{t(key)}</span>
                  {isActive && <span className="ml-auto h-1.5 w-1.5 rounded-full bg-[#F7F8FC]/65" />}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-white/8 px-3 py-3 space-y-0.5">
          <div className="px-3 py-1.5">
            <LanguageSwitcher />
          </div>
          <NavLink
            to="/app/profile"
            className={({ isActive }) => cn(
              'flex items-center gap-2.5 rounded-[14px] px-3 py-2.5 text-sm font-medium transition-all duration-150',
              isActive
                ? 'bg-[#4A4F80] text-[#F7F8FC] shadow-[inset_0_0_0_1px_rgba(255,255,255,0.14),_0_2px_10px_rgba(74,79,128,0.35)]'
                : 'text-[#C8CCDD] hover:bg-[#3A3E66] hover:text-[#F7F8FC]',
            )}
          >
            {({ isActive }) => (
              <>
                <User size={16} className={isActive ? 'text-[#F7F8FC]' : 'text-[#9DA1C4]'} strokeWidth={isActive ? 2.5 : 2} />
                <span>{t('nav.profile')}</span>
              </>
            )}
          </NavLink>
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-2.5 rounded-[14px] px-3 py-2.5 text-sm font-medium text-[#9DA1C4] transition-all duration-150 hover:bg-red-900/40 hover:text-red-300"
          >
            <LogOut size={16} strokeWidth={2} />
            {t('nav.logout')}
          </button>
        </div>
      </aside>

      {/* ── Main content ────────────────────────────────────────── */}
      <main className="flex-1 overflow-y-auto main-mobile-pb md:pb-0">
        <Outlet />
      </main>

      {/* ── Mobile bottom nav (4 tabs + More) ───────────────────── */}
      <nav
        className="mobile-bottom-nav fixed bottom-0 left-0 right-0 z-50 flex items-start border-t border-sand/50 bg-canvas md:hidden"
        style={{ boxShadow: '0 -4px 24px rgba(23,21,42,0.14)' }}
      >
        {PRIMARY_NAV.map(({ to, icon: Icon, key, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => cn(
              'flex flex-1 flex-col items-center justify-center gap-0.5 text-[10px] font-semibold transition-colors h-[60px]',
              isActive ? 'text-primary' : 'text-muted',
            )}
          >
            {({ isActive }) => (
              <>
                <span className={cn(
                  'flex h-7 w-7 items-center justify-center rounded-xl transition-all duration-150',
                  isActive && 'bg-primary-50',
                )}>
                  <Icon size={18} strokeWidth={isActive ? 2.5 : 2} />
                </span>
                {t(key)}
              </>
            )}
          </NavLink>
        ))}

        {/* More button */}
        <button
          onClick={() => setMoreOpen(true)}
          className={cn(
            'flex flex-1 flex-col items-center justify-center gap-0.5 text-[10px] font-semibold transition-colors h-[60px]',
            moreOpen ? 'text-primary' : 'text-muted',
          )}
        >
          <span className={cn(
            'flex h-7 w-7 items-center justify-center rounded-xl transition-all duration-150',
            moreOpen && 'bg-primary-50',
          )}>
            <MoreHorizontal size={18} strokeWidth={2} />
          </span>
          {t('nav.more', { defaultValue: 'Ещё' })}
        </button>
      </nav>

      {/* ── More bottom sheet ────────────────────────────────────── */}
      <AnimatePresence>
        {moreOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              key="backdrop"
              className="fixed inset-0 z-40 md:hidden"
              style={{ background: 'rgba(23,21,42,0.45)', backdropFilter: 'blur(4px)' }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setMoreOpen(false)}
            />

            {/* Sheet */}
            <motion.div
              key="sheet"
              className="fixed bottom-0 left-0 right-0 z-50 md:hidden"
              style={{
                background: '#F4EFE4',
                borderRadius: '24px 24px 0 0',
                paddingBottom: 'env(safe-area-inset-bottom, 0px)',
                boxShadow: '0 -8px 40px rgba(23,21,42,0.18)',
              }}
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              transition={{ type: 'spring', damping: 32, stiffness: 320 }}
            >
              {/* Handle + header */}
              <div className="flex items-center justify-between px-5 pt-4 pb-2">
                <div className="mx-auto h-1 w-10 rounded-full bg-sand/70 absolute left-1/2 -translate-x-1/2 top-3" />
                <p className="text-xs font-bold uppercase tracking-wider text-muted pt-1">
                  {t('nav.more', { defaultValue: 'Ещё' })}
                </p>
                <button
                  onClick={() => setMoreOpen(false)}
                  className="flex h-7 w-7 items-center justify-center rounded-full"
                  style={{ background: 'rgba(23,21,42,0.07)' }}
                >
                  <X size={14} className="text-ink/60" />
                </button>
              </div>

              {/* Nav items grid */}
              <div className="px-4 pb-4 grid grid-cols-2 gap-2">
                {MORE_NAV.map(({ to, icon: Icon, key }) => (
                  <button
                    key={to}
                    onClick={() => handleMoreNav(to)}
                    className="flex items-center gap-3 rounded-[16px] px-4 py-3.5 text-left transition-all active:scale-[0.97]"
                    style={{
                      background: 'rgba(60,56,136,0.06)',
                      border: '1px solid rgba(60,56,136,0.10)',
                    }}
                  >
                    <span
                      className="flex h-9 w-9 shrink-0 items-center justify-center rounded-[12px]"
                      style={{ background: 'linear-gradient(135deg, #3C3888, #385C8A)' }}
                    >
                      <Icon size={16} className="text-white" strokeWidth={2} />
                    </span>
                    <span className="text-sm font-semibold text-ink leading-tight">{t(key)}</span>
                  </button>
                ))}
              </div>

              {/* Divider */}
              <div className="mx-4 mb-3 h-px bg-sand/50" />

              {/* Language + Logout */}
              <div className="px-4 pb-3 flex items-center justify-between gap-2">
                <div className="flex-1">
                  <LanguageSwitcher />
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 rounded-[12px] px-4 py-2.5 text-sm font-semibold text-danger transition-all"
                  style={{ background: 'rgba(132,48,72,0.08)' }}
                >
                  <LogOut size={15} />
                  {t('nav.logout')}
                </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}
