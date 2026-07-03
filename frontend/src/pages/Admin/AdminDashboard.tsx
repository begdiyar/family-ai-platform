import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from 'recharts'
import {
  Users, Activity, AlertTriangle, CheckCircle2,
  AlertOctagon, ArrowRight, TrendingUp,
} from 'lucide-react'
import { AdminService } from '@/services/admin.service'

type Period = 'day' | 'week' | 'month'

const SCORE_COLOR = (score: number | null) => {
  if (score === null) return '#68647C'
  if (score < 40) return '#843048'
  if (score < 60) return '#886028'
  if (score < 80) return '#385C8A'
  return '#386858'
}

export const AdminDashboard = () => {
  const { t } = useTranslation('admin')
  const navigate = useNavigate()
  const [period, setPeriod] = useState<Period>('day')

  const { data: overview, isLoading } = useQuery({
    queryKey: ['admin-overview'],
    queryFn: AdminService.getOverview,
    retry: 1,
  })

  const { data: regData = [] } = useQuery({
    queryKey: ['admin-registrations', period],
    queryFn: () => AdminService.getRegistrations(period, period === 'day' ? 30 : 12),
    retry: 1,
  })

  const formatDate = (d: string) => {
    const dt = new Date(d)
    if (period === 'day') return dt.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
    if (period === 'week') return `Н${Math.ceil(dt.getDate() / 7)} ${dt.toLocaleDateString('ru-RU', { month: 'short' })}`
    return dt.toLocaleDateString('ru-RU', { month: 'short', year: '2-digit' })
  }

  const crisis = overview?.crisis_breakdown
  const score = overview?.avg_relationship_score
  const scoreColor = SCORE_COLOR(score ?? null)

  if (isLoading) {
    return (
      <div className="p-4 md:p-8 space-y-4">
        <div className="h-7 w-40 rounded-xl shimmer" />
        <div className="grid grid-cols-3 gap-3">
          {[...Array(3)].map((_, i) => <div key={i} className="h-24 rounded-2xl shimmer" />)}
        </div>
        <div className="h-36 rounded-2xl shimmer" />
        <div className="h-52 rounded-2xl shimmer" />
      </div>
    )
  }

  const PERIODS: Period[] = ['day', 'week', 'month']

  return (
    <div className="min-h-full p-4 md:p-8 space-y-6" style={{ background: '#F4EFE4' }}>

      {/* ── Header ───────────────────────────────────────────── */}
      <div>
        <h1 className="text-xl font-bold text-ink">{t('dashboard.title')}</h1>
        <p className="text-sm text-muted mt-0.5">
          {new Date().toLocaleDateString('ru-RU', { weekday: 'long', day: 'numeric', month: 'long' })}
        </p>
      </div>

      {/* ── 3 Key Metrics ────────────────────────────────────── */}
      <div className="grid grid-cols-3 gap-3">
        {/* Total families */}
        <div className="rounded-2xl bg-white p-4 flex flex-col gap-2"
             style={{ border: '1px solid rgba(60,56,136,0.08)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
          <div className="flex h-8 w-8 items-center justify-center rounded-xl"
               style={{ background: 'rgba(60,56,136,0.10)' }}>
            <Users size={15} className="text-primary" />
          </div>
          <div>
            <p className="text-2xl font-bold text-ink leading-none">{overview?.total_couples ?? '—'}</p>
            <p className="text-[11px] text-muted mt-1 leading-snug">{t('dashboard.kpi.families')}</p>
          </div>
        </div>

        {/* Active this month */}
        <div className="rounded-2xl bg-white p-4 flex flex-col gap-2"
             style={{ border: '1px solid rgba(56,104,88,0.12)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
          <div className="flex h-8 w-8 items-center justify-center rounded-xl"
               style={{ background: 'rgba(56,104,88,0.12)' }}>
            <Activity size={15} style={{ color: '#386858' }} />
          </div>
          <div>
            <p className="text-2xl font-bold text-ink leading-none">{overview?.active_families_30d ?? '—'}</p>
            <p className="text-[11px] text-muted mt-1 leading-snug">{t('dashboard.kpi.active_30d')}</p>
          </div>
        </div>

        {/* Avg index */}
        <div className="rounded-2xl bg-white p-4 flex flex-col gap-2"
             style={{ border: `1px solid ${scoreColor}22`, boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
          <div className="flex h-8 w-8 items-center justify-center rounded-xl"
               style={{ background: `${scoreColor}15` }}>
            <TrendingUp size={15} style={{ color: scoreColor }} />
          </div>
          <div>
            <p className="text-2xl font-bold leading-none" style={{ color: scoreColor }}>
              {score ?? '—'}
            </p>
            <p className="text-[11px] text-muted mt-1 leading-snug">{t('dashboard.kpi.avg_index')}</p>
          </div>
        </div>
      </div>

      {/* ── Crisis Status ─────────────────────────────────────── */}
      {crisis && (
        <div className="rounded-2xl bg-white p-5"
             style={{ border: '1px solid rgba(60,56,136,0.08)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm font-bold text-ink">{t('dashboard.crisis_title')}</p>
            <button
              onClick={() => navigate('/admin/problems')}
              className="flex items-center gap-1 text-xs font-semibold text-primary hover:opacity-70 transition-opacity"
            >
              {t('common.see_all')} <ArrowRight size={12} />
            </button>
          </div>
          <div className="grid grid-cols-3 gap-2.5">
            {[
              { key: 'none',     Icon: CheckCircle2, color: '#386858', bg: '#E8F2EE', label: t('common.crisis.none') },
              { key: 'warning',  Icon: AlertTriangle, color: '#886028', bg: '#F5EDD8', label: t('common.crisis.warning') },
              { key: 'critical', Icon: AlertOctagon,  color: '#843048', bg: '#F5DDE4', label: t('common.crisis.critical') },
            ].map(({ key, Icon, color, bg, label }) => {
              const count = crisis[key as keyof typeof crisis] ?? 0
              const total = overview?.total_couples || 1
              return (
                <div key={key} className="rounded-xl p-3 flex flex-col gap-1.5" style={{ background: bg }}>
                  <div className="flex items-center gap-1.5">
                    <Icon size={13} style={{ color }} />
                    <span className="text-[11px] font-semibold" style={{ color }}>{label}</span>
                  </div>
                  <p className="text-xl font-bold text-ink leading-none">{count}</p>
                  <p className="text-[10px] text-muted">{Math.round(count / total * 100)}%</p>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* ── Registrations Chart ───────────────────────────────── */}
      <div className="rounded-2xl bg-white p-5"
           style={{ border: '1px solid rgba(60,56,136,0.08)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm font-bold text-ink">{t('dashboard.charts.registrations')}</p>
          <div className="flex gap-1">
            {PERIODS.map(p => (
              <button key={p} onClick={() => setPeriod(p)}
                className="px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-all"
                style={period === p
                  ? { background: '#3C3888', color: '#fff' }
                  : { background: 'rgba(60,56,136,0.08)', color: '#3C3888' }}>
                {t(`common.period_short.${p}`)}
              </button>
            ))}
          </div>
        </div>
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={regData.map(d => ({ ...d, date: formatDate(d.date) }))}
                     margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(194,184,164,0.35)" vertical={false} />
            <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#68647C' }} tickLine={false} axisLine={false} />
            <YAxis tick={{ fontSize: 10, fill: '#68647C' }} tickLine={false} axisLine={false} allowDecimals={false} />
            <Tooltip
              contentStyle={{ background: '#fff', border: '1px solid rgba(194,184,164,0.5)', borderRadius: 12, fontSize: 12 }}
              labelStyle={{ color: '#17152A', fontWeight: 600 }}
            />
            <Line type="monotone" dataKey="count" stroke="#3C3888" strokeWidth={2.5}
                  dot={false} activeDot={{ r: 4, fill: '#3C3888' }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* ── Recent Families ───────────────────────────────────── */}
      <div className="rounded-2xl bg-white p-5"
           style={{ border: '1px solid rgba(60,56,136,0.08)', boxShadow: '0 2px 8px rgba(0,0,0,0.04)' }}>
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm font-bold text-ink">{t('dashboard.recent_families')}</p>
          <button onClick={() => navigate('/admin/families')}
            className="flex items-center gap-1 text-xs font-semibold text-primary hover:opacity-70 transition-opacity">
            {t('common.see_all')} <ArrowRight size={12} />
          </button>
        </div>
        <RecentFamilies />
      </div>

    </div>
  )
}

function RecentFamilies() {
  const { t } = useTranslation('admin')
  const navigate = useNavigate()
  const { data, isLoading } = useQuery({
    queryKey: ['admin-families-quick'],
    queryFn: () => AdminService.getFamilies({ page: 1, page_size: 6 }),
  })

  if (isLoading) return (
    <div className="space-y-2">
      {[...Array(4)].map((_, i) => <div key={i} className="h-12 rounded-xl shimmer" />)}
    </div>
  )

  const CRISIS_STYLE: Record<string, { color: string; bg: string; label: string }> = {
    none:     { color: '#386858', bg: '#E8F2EE', label: t('common.crisis.none') },
    warning:  { color: '#886028', bg: '#F5EDD8', label: t('common.crisis.warning') },
    critical: { color: '#843048', bg: '#F5DDE4', label: t('common.crisis.critical') },
  }

  return (
    <div className="space-y-2">
      {data?.results.map(f => {
        const scoreColor = SCORE_COLOR(f.relationship_score)
        const crisis = CRISIS_STYLE[f.crisis_level] ?? CRISIS_STYLE.none
        return (
          <div
            key={f.id}
            onClick={() => navigate(`/admin/families/${f.id}`)}
            className="flex items-center gap-3 rounded-xl px-3 py-2.5 cursor-pointer transition-colors hover:bg-surface"
            style={{ border: '1px solid rgba(194,184,164,0.40)' }}
          >
            {/* Avatar */}
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-bold text-white"
                 style={{ background: 'linear-gradient(135deg, #3C3888, #385C8A)' }}>
              {f.partner_a?.charAt(0).toUpperCase()}
            </div>

            {/* Names */}
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-ink truncate">
                {f.partner_a}{f.partner_b ? ` & ${f.partner_b}` : ''}
              </p>
              <p className="text-[11px] text-muted">{f.created_at}</p>
            </div>

            {/* Score */}
            <span className="text-sm font-bold shrink-0" style={{ color: scoreColor }}>
              {f.relationship_score ?? '—'}
            </span>

            {/* Crisis badge */}
            <span className="shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold"
                  style={{ background: crisis.bg, color: crisis.color }}>
              {crisis.label}
            </span>
          </div>
        )
      })}
    </div>
  )
}
