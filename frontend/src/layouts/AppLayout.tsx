import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import {
  Home, ClipboardList, BarChart2, MessageCircle,
  LogOut, User, Scale, Sun, Heart, Sparkles, Brain,
} from 'lucide-react'
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
  { to: '/app/analytics',   icon: BarChart2,     key: 'nav.analytics',   end: false },
  { to: '/app/academy',     icon: Brain,         key: 'nav.academy',     end: false },
  { to: '/app/practices',   icon: Sun,           key: 'nav.practices',   end: false },
  { to: '/app/ai',          icon: MessageCircle, key: 'nav.ai',          end: false },
  { to: '/app/mediation',   icon: Scale,         key: 'nav.mediation',   end: false },
]

const MOBILE_NAV_ITEMS = [
  { to: '/app',           icon: Home,          key: 'nav.home',      end: true  },
  { to: '/app/index',     icon: Heart,         key: 'nav.index',     end: false },
  { to: '/app/academy',   icon: Brain,         key: 'nav.academy',   end: false },
  { to: '/app/practices', icon: Sun,           key: 'nav.practices', end: false },
  { to: '/app/ai',        icon: MessageCircle, key: 'nav.ai',        end: false },
]

export const AppLayout = () => {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t } = useTranslation('common')
  const { refreshToken, logout } = useAuthStore((s) => ({
    refreshToken: s.refreshToken,
    logout: s.logout,
  }))

  const handleLogout = async () => {
    try { if (refreshToken) await AuthService.logout(refreshToken) } catch {}
    finally { logout(); qc.clear(); navigate('/login', { replace: true }) }
  }

  return (
    <div className="flex h-screen bg-surface">
      {/* ── Sidebar (dark anchor) ────────────────────────────────── */}
      <aside className="hidden w-60 flex-shrink-0 md:flex md:flex-col">

        {/* Logo */}
        <div className="flex h-[60px] items-center gap-3 px-5 border-b border-white/8">
          <div className="flex h-8 w-8 items-center justify-center rounded-[10px] bg-gradient-brand shadow-[0_3px_14px_rgba(23,21,42,0.50)]">
            <Sparkles size={14} className="text-white" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-bold text-[#F7F8FC]">{t('app_name')}</p>
            <p className="text-[10px] text-[#9DA1C4]">{t('app_tagline')}</p>
          </div>
        </div>

        {/* Nav */}
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
                  <Icon
                    size={16}
                    className={isActive ? 'text-[#F7F8FC]' : 'text-[#9DA1C4]'}
                    strokeWidth={isActive ? 2.5 : 2}
                  />
                  <span>{t(key)}</span>
                  {isActive && (
                    <span className="ml-auto h-1.5 w-1.5 rounded-full bg-[#F7F8FC]/65" />
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
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

      {/* ── Main content ────────────────────────────────────────────── */}
      <main className="flex-1 overflow-y-auto pb-16 md:pb-0">
        <Outlet />
      </main>

      {/* ── Mobile bottom nav ───────────────────────────────────────── */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 flex h-[60px] border-t border-sand/50 bg-canvas md:hidden"
           style={{ boxShadow: '0 -4px 24px rgba(23,21,42,0.14)' }}>
        {MOBILE_NAV_ITEMS.map(({ to, icon: Icon, key, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => cn(
              'flex flex-1 flex-col items-center justify-center gap-0.5 text-[10px] font-semibold transition-colors',
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
      </nav>
    </div>
  )
}
