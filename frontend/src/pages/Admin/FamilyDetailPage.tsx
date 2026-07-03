import { useParams, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  RadarChart, PolarGrid, PolarAngleAxis, Radar,
} from 'recharts'
import { ChevronLeft, Calendar, ClipboardList, Sun, AlertTriangle, AlertOctagon, CheckCircle2, Users } from 'lucide-react'
import { AdminService } from '@/services/admin.service'

const ZONE_COLORS: Record<string, string> = {
  communication: '#2C5678', trust: '#286250', intimacy: '#74364A',
  conflict: '#744E26', values: '#463E80', future: '#385C8A',
}

const CRISIS_META: Record<string, { color: string; bg: string; icon: any }> = {
  none:     { color: '#386858', bg: '#E2EDE8', icon: CheckCircle2  },
  warning:  { color: '#886028', bg: '#F5EDD8', icon: AlertTriangle },
  critical: { color: '#843048', bg: '#F5DDE4', icon: AlertOctagon  },
}

const SCORE_KEY = (score: number | null) => {
  if (score === null) return 'none'
  if (score < 40) return 'critical'
  if (score < 60) return 'warning'
  if (score < 80) return 'stable'
  return 'excellent'
}

const SCORE_COLOR: Record<string, string> = {
  none: '#68647C', critical: '#843048', warning: '#886028', stable: '#385C8A', excellent: '#386858',
}

export const FamilyDetailPage = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation('admin')

  const { data: family, isLoading } = useQuery({
    queryKey: ['admin-family', id],
    queryFn: () => AdminService.getFamilyDetail(id!),
    enabled: !!id,
  })

  const zoneLabel = (key: string) => t(`common.zones.${key}`, { defaultValue: key })

  if (isLoading) return (
    <div className="min-h-full bg-surface p-4 md:p-6 space-y-4">
      <div className="h-8 w-48 rounded-xl shimmer" />
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[...Array(4)].map((_, i) => <div key={i} className="h-24 rounded-[20px] shimmer" />)}
      </div>
      <div className="h-64 rounded-[20px] shimmer" />
    </div>
  )

  if (!family) return (
    <div className="min-h-full bg-surface p-4 md:p-6 flex items-center justify-center">
      <p className="text-muted">{t('family.not_found')}</p>
    </div>
  )

  const latestHistory = family.analytics_history[family.analytics_history.length - 1]
  const crisisMeta = CRISIS_META[family.latest_crisis] ?? CRISIS_META.none
  const CrisisIcon = crisisMeta.icon
  const scoreKey = SCORE_KEY(family.latest_score)
  const scoreColor = SCORE_COLOR[scoreKey]

  const radarData = latestHistory
    ? Object.entries(latestHistory.zones)
        .filter(([, v]) => v !== null)
        .map(([zone, value]) => ({
          zone: zoneLabel(zone),
          value: value as number,
          fullMark: 100,
        }))
    : []

  const timelineData = family.analytics_history.map(h => ({
    date: h.date,
    overall: h.overall_score,
    ...Object.fromEntries(
      Object.entries(h.zones)
        .filter(([, v]) => v !== null)
        .map(([k, v]) => [k, v])
    ),
  }))

  const SCORE_RANGES = [
    { range: '80–100', key: 'excellent', color: '#386858' },
    { range: '60–79',  key: 'stable',    color: '#385C8A' },
    { range: '40–59',  key: 'warning',   color: '#886028' },
    { range: '0–39',   key: 'critical',  color: '#843048' },
  ]

  return (
    <div className="min-h-full bg-surface p-4 md:p-6 space-y-5">

      {/* Header */}
      <div className="flex flex-wrap items-center gap-3">
        <button onClick={() => navigate('/admin/families')}
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-[12px] bg-canvas border border-sand/60 hover:bg-surface transition-colors">
          <ChevronLeft size={16} className="text-muted" />
        </button>
        <div className="min-w-0 flex-1">
          <h1 className="text-lg md:text-xl font-bold text-ink truncate">
            {family.partner_a.name} & {family.partner_b?.name ?? '—'}
          </h1>
          <p className="text-sm text-muted">
            {t('family.registered_on', { date: family.created_at })}
          </p>
        </div>
        <div className="flex items-center gap-2 rounded-[12px] px-3 py-1.5 shrink-0"
             style={{ background: crisisMeta.bg }}>
          <CrisisIcon size={13} style={{ color: crisisMeta.color }} />
          <span className="text-xs font-semibold" style={{ color: crisisMeta.color }}>
            {t(`common.crisis.${family.latest_crisis}`)}
          </span>
        </div>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { icon: ClipboardList, labelKey: 'family.kpi.diagnostics', value: family.diagnostics_count, color: '#3C3888' },
          { icon: Sun,           labelKey: 'family.kpi.practices',   value: family.practices_count,   color: '#886028' },
          { icon: Calendar,      labelKey: 'family.kpi.registered',  value: family.created_at,        color: '#385C8A' },
          {
            icon: Users,
            labelKey: 'family.kpi.children',
            value: family.has_children ? family.children_count : t('family.kpi.no_children'),
            color: '#386858',
          },
        ].map(({ icon: Icon, labelKey, value, color }) => (
          <div key={labelKey} className="rounded-[18px] bg-canvas p-4 flex items-start gap-3"
               style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 1px 6px rgba(23,21,42,0.06)' }}>
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-[12px]"
                 style={{ background: `${color}18` }}>
              <Icon size={16} style={{ color }} />
            </div>
            <div>
              <p className="text-xs text-muted">{t(labelKey)}</p>
              <p className="text-lg font-bold text-ink">{value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Score + Radar */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {/* Score card */}
        <div className="rounded-[20px] bg-canvas p-5"
             style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
          <p className="text-sm font-bold text-ink mb-4">{t('family.score_card')}</p>
          <div className="flex items-center gap-4">
            <div className="relative h-24 w-24 shrink-0">
              <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
                <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(194,184,164,0.4)" strokeWidth="10" />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke={scoreColor}
                  strokeWidth="10"
                  strokeLinecap="round"
                  strokeDasharray={`${2 * Math.PI * 40}`}
                  strokeDashoffset={`${2 * Math.PI * 40 * (1 - (family.latest_score ?? 0) / 100)}`}
                  style={{ transition: 'stroke-dashoffset 0.8s ease' }}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl font-bold" style={{ color: scoreColor }}>
                  {family.latest_score ?? '—'}
                </span>
              </div>
            </div>
            <div>
              <p className="text-lg md:text-2xl font-bold" style={{ color: scoreColor }}>
                {scoreKey === 'none' ? '—' : t(`common.score_detail.${scoreKey}`)}
              </p>
              <p className="text-xs text-muted mt-1">{t('family.score_out_of')}</p>
              <div className="mt-3 space-y-1">
                {SCORE_RANGES.map(({ range, key, color }) => (
                  <div key={range} className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full shrink-0" style={{ background: color }} />
                    <span className="text-xs text-muted">{range} — {t(`common.score_detail.${key}`)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Radar chart */}
        {radarData.length > 0 && (
          <div className="rounded-[20px] bg-canvas p-5"
               style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
            <p className="text-sm font-bold text-ink mb-2">{t('family.radar_title')}</p>
            <ResponsiveContainer width="100%" height={220}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(194,184,164,0.40)" />
                <PolarAngleAxis dataKey="zone" tick={{ fontSize: 11, fill: '#68647C' }} />
                <Radar name={t('family.radar_title')} dataKey="value" stroke="#3C3888" fill="#3C3888" fillOpacity={0.18} strokeWidth={2} />
                <Tooltip
                  contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }}
                  formatter={(v: number) => [`${v}%`, t('common.score.stable')]}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Timeline chart */}
      {timelineData.length > 1 && (
        <div className="rounded-[20px] bg-canvas p-5"
             style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
          <p className="text-sm font-bold text-ink mb-4">{t('family.timeline_title')}</p>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={timelineData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(194,184,164,0.40)" />
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#68647C' }} tickLine={false} axisLine={false} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#68647C' }} tickLine={false} axisLine={false} />
              <Tooltip
                contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }}
                labelStyle={{ color: '#17152A', fontWeight: 600 }}
                formatter={(v: number) => [`${v}%`]}
              />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Line type="monotone" dataKey="overall" name={t('family.overall')} stroke="#3C3888" strokeWidth={3} dot={{ r: 4 }} />
              {Object.entries(ZONE_COLORS).map(([zone, color]) => (
                <Line key={zone} type="monotone" dataKey={zone} name={zoneLabel(zone)}
                  stroke={color} strokeWidth={1.5} dot={false} strokeDasharray="4 2" />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Zone table */}
      {latestHistory && (
        <div className="rounded-[20px] bg-canvas p-5"
             style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
          <p className="text-sm font-bold text-ink mb-4">{t('family.zone_detail')}</p>
          <div className="space-y-3">
            {Object.entries(latestHistory.zones).map(([zone, value]) => {
              if (value === null) return null
              const color = ZONE_COLORS[zone] ?? '#3C3888'
              return (
                <div key={zone}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-ink">{zoneLabel(zone)}</span>
                    <span className="text-sm font-bold" style={{ color }}>{value}%</span>
                  </div>
                  <div className="h-2 w-full rounded-full overflow-hidden bg-sand/40">
                    <div className="h-full rounded-full transition-all duration-700"
                         style={{ width: `${value}%`, background: color }} />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
