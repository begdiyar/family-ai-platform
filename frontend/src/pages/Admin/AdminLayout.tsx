import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard, Users, AlertTriangle, BarChart2,
  Download, Settings, LogOut, ShieldCheck, Loader2,
} from 'lucide-react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { Navigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { cn } from '@/lib/cn'
import { AuthService } from '@/services/auth.service'
import { useAuthStore } from '@/store/auth.store'
import { LanguageSwitcher } from '@/components/LanguageSwitcher'

const NAV_SECTION_KEYS = [
  {
    labelKey: 'layout.sections.analytics',
    items: [
      { to: '/admin',            labelKey: 'layout.nav.overview',    icon: LayoutDashboard, end: true  },
      { to: '/admin/families',   labelKey: 'layout.nav.families',    icon: Users,           end: false },
      { to: '/admin/problems',   labelKey: 'layout.nav.problems',    icon: AlertTriangle,   end: false },
      { to: '/admin/statistics', labelKey: 'layout.nav.statistics',  icon: BarChart2,       end: false },
    ],
  },
  {
    labelKey: 'layout.sections.data',
    items: [
      { to: '/admin/export',   labelKey: 'layout.nav.export',    icon: Download, end: false },
    ],
  },
  {
    labelKey: 'layout.sections.system',
    items: [
      { to: '/admin/settings', labelKey: 'layout.nav.settings',  icon: Settings, end: false },
    ],
  },
]

const MOBILE_NAV_KEYS = [
  { to: '/admin',            labelKey: 'layout.nav.overview',   icon: LayoutDashboard, end: true  },
  { to: '/admin/families',   labelKey: 'layout.nav.families',   icon: Users,           end: false },
  { to: '/admin/statistics', labelKey: 'layout.nav.stat_short', icon: BarChart2,       end: false },
  { to: '/admin/export',     labelKey: 'layout.nav.export',     icon: Download,        end: false },
  { to: '/admin/settings',   labelKey: 'layout.nav.settings',   icon: Settings,        end: false },
]

// Sidebar background: deep navy, more austere than user sidebar
const S = {
  bg:          '#13122B',
  border:      'rgba(255,255,255,0.07)',
  label:       'rgba(255,255,255,0.32)',
  navDefault:  '#8B89C0',
  navHoverBg:  'rgba(255,255,255,0.06)',
  navActiveBg: '#3C3888',
  navActiveText: '#FFFFFF',
  navDefaultText: '#9B99C8',
}

export const AdminLayout = () => {
  const { t } = useTranslation('admin')
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { refreshToken, logout } = useAuthStore(s => ({ refreshToken: s.refreshToken, logout: s.logout }))

  const { data: me, isLoading: meLoading } = useQuery({
    queryKey: ['me'],
    queryFn: AuthService.getMe,
    staleTime: 5 * 60_000,
  })

  // While checking identity — show spinner
  if (meLoading && !me) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface">
        <Loader2 size={32} className="animate-spin text-muted" />
      </div>
    )
  }

  // Not an admin — redirect to user app
  if (me && !me.is_staff && !me.is_superuser) {
    return <Navigate to="/app" replace />
  }

  const handleLogout = async () => {
    try { if (refreshToken) await AuthService.logout(refreshToken) } catch {}
    finally { logout(); qc.clear(); navigate('/login', { replace: true }) }
  }

  const initials = me?.first_name?.charAt(0).toUpperCase() ?? 'A'

  return (
    <div className="flex h-screen overflow-hidden" style={{ background: '#F4EFE4' }}>

      {/* ── Admin Sidebar ─────────────────────────────────────────── */}
      <aside
        className="hidden w-[240px] flex-shrink-0 md:flex md:flex-col"
        style={{ background: S.bg, borderRight: `1px solid ${S.border}` }}
      >
        {/* Brand */}
        <div className="flex h-[60px] items-center gap-3 px-5"
             style={{ borderBottom: `1px solid ${S.border}` }}>
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-[10px]"
               style={{ background: 'linear-gradient(135deg, #4A4F80 0%, #3C3888 100%)', boxShadow: '0 3px 14px rgba(60,56,136,0.55)' }}>
            <ShieldCheck size={15} className="text-white" strokeWidth={2.5} />
          </div>
          <div className="leading-tight">
            <p className="text-[13px] font-bold text-white">{t('layout.brand')}</p>
            <p className="text-[10px]" style={{ color: S.label }}>Oila AI</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
          {NAV_SECTION_KEYS.map(section => (
            <div key={section.labelKey}>
              <p className="mb-1.5 px-3 text-[10px] font-bold uppercase tracking-widest"
                 style={{ color: S.label }}>
                {t(section.labelKey)}
              </p>
              <div className="space-y-0.5">
                {section.items.map(({ to, labelKey, icon: Icon, end }) => (
                  <NavLink
                    key={to}
                    to={to}
                    end={end}
                    className={({ isActive }) => cn(
                      'flex items-center gap-2.5 rounded-[12px] px-3 py-2 text-[13px] font-medium transition-all duration-150',
                      isActive ? '' : '',
                    )}
                    style={({ isActive }) => isActive
                      ? { background: S.navActiveBg, color: S.navActiveText, boxShadow: '0 2px 12px rgba(60,56,136,0.45)' }
                      : { color: S.navDefaultText }
                    }
                  >
                    {({ isActive }) => (
                      <>
                        <Icon size={15} strokeWidth={isActive ? 2.5 : 2}
                              style={{ color: isActive ? '#fff' : S.navDefault }} />
                        {t(labelKey)}
                        {isActive && <span className="ml-auto h-1.5 w-1.5 rounded-full bg-white/50" />}
                      </>
                    )}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>

        {/* Footer */}
        <div className="px-3 pb-4 space-y-2" style={{ borderTop: `1px solid ${S.border}` }}>

          {/* User card */}
          <div className="mt-3 flex items-center gap-2.5 rounded-[12px] px-3 py-2.5"
               style={{ background: 'rgba(255,255,255,0.05)' }}>
            <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#3C3888] text-[11px] font-bold text-white">
              {initials}
            </div>
            <div className="min-w-0">
              <p className="truncate text-[12px] font-semibold text-white">{me?.first_name ?? 'Admin'}</p>
              <p className="truncate text-[10px]" style={{ color: S.label }}>{me?.email ?? ''}</p>
            </div>
          </div>

          {/* Language + Logout row */}
          <div className="flex items-center gap-1">
            <LanguageSwitcher dark />
            <button
              onClick={handleLogout}
              className="flex flex-1 items-center gap-2 rounded-[12px] px-3 py-2 text-[13px] font-medium transition-all duration-150"
              style={{ color: S.navDefaultText }}
              onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = 'rgba(132,48,72,0.20)'; (e.currentTarget as HTMLElement).style.color = '#FDA4AF' }}
              onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = ''; (e.currentTarget as HTMLElement).style.color = S.navDefaultText }}
            >
              <LogOut size={14} />
              {t('layout.logout')}
            </button>
          </div>
        </div>
      </aside>

      {/* ── Mobile top bar (admin) ─────────────────────────────────── */}
      <div className="fixed inset-x-0 top-0 z-50 flex h-14 items-center justify-between px-4 md:hidden"
           style={{ background: S.bg, borderBottom: `1px solid ${S.border}` }}>
        <div className="flex items-center gap-2">
          <ShieldCheck size={16} className="text-[#8B89C0]" />
          <span className="text-sm font-bold text-white">{t('layout.brand')}</span>
        </div>
        <div className="flex items-center gap-1">
          <LanguageSwitcher compact dropDirection="down" dark />
          <button onClick={handleLogout} className="p-2">
            <LogOut size={16} style={{ color: S.navDefaultText }} />
          </button>
        </div>
      </div>

      {/* ── Mobile bottom nav ─────────────────────────────────────── */}
      <nav
        className="fixed inset-x-0 bottom-0 z-50 flex h-16 items-stretch md:hidden"
        style={{ background: S.bg, borderTop: `1px solid ${S.border}` }}
      >
        {MOBILE_NAV_KEYS.map(({ to, labelKey, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className="flex flex-1 flex-col items-center justify-center gap-0.5 text-[10px] font-medium transition-colors"
            style={({ isActive }) => ({
              color: isActive ? '#FFFFFF' : S.navDefaultText,
            })}
          >
            {({ isActive }) => (
              <>
                <Icon size={18} strokeWidth={isActive ? 2.5 : 1.8}
                      style={{ color: isActive ? '#A09DE0' : S.navDefault }} />
                <span>{t(labelKey)}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* ── Content ───────────────────────────────────────────────── */}
      <main className="flex-1 overflow-y-auto pt-14 pb-16 md:pt-0 md:pb-0">
        <Outlet />
      </main>
    </div>
  )
}
