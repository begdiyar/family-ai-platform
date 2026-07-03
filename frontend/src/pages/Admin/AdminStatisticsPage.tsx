import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell, Legend,
} from 'recharts'
import { AdminService } from '@/services/admin.service'

type Period = 'day' | 'week' | 'month'

function PeriodToggle({ value, onChange, t }: { value: Period; onChange: (p: Period) => void; t: (k: string) => string }) {
  return (
    <div className="flex rounded-[10px] border border-sand overflow-hidden bg-surface">
      {(['day', 'week', 'month'] as Period[]).map(p => (
        <button key={p} onClick={() => onChange(p)}
          className="px-3 py-1.5 text-xs font-semibold transition-colors"
          style={p === value
            ? { background: '#3C3888', color: '#fff' }
            : { color: '#68647C' }}>
          {t(`common.period.${p}`)}
        </button>
      ))}
    </div>
  )
}

export const AdminStatisticsPage = () => {
  const { t } = useTranslation('admin')
  const [trendPeriod, setTrendPeriod] = useState<Period>('day')
  const [actPeriod, setActPeriod]     = useState<Period>('day')

  const { data: trends, isLoading: trendsLoading } = useQuery({
    queryKey: ['admin-trends', trendPeriod],
    queryFn: () => AdminService.getTrends(trendPeriod, trendPeriod === 'day' ? 30 : 12),
    retry: 1,
  })

  const { data: actData = [], isLoading: actLoading } = useQuery({
    queryKey: ['admin-activity', actPeriod],
    queryFn: () => AdminService.getActivity(actPeriod, actPeriod === 'day' ? 30 : 12),
    retry: 1,
  })

  const formatDate = (d: string, period: Period) => {
    const dt = new Date(d)
    if (period === 'day') return dt.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
    if (period === 'week') return `Н${Math.ceil(dt.getDate() / 7)} ${dt.toLocaleDateString('ru-RU', { month: 'short' })}`
    return dt.toLocaleDateString('ru-RU', { month: 'short', year: '2-digit' })
  }

  const CARD       = 'rounded-[20px] bg-canvas p-5'
  const CARD_STYLE = { border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }

  const scoreTrend = trends?.score_trend ?? []
  const scoreDist  = trends?.score_distribution ?? []

  return (
    <div className="min-h-full bg-surface p-4 md:p-6 space-y-5">
      <div>
        <h1 className="text-xl md:text-2xl font-bold text-ink">{t('statistics.title')}</h1>
        <p className="text-sm text-muted mt-0.5">{t('statistics.subtitle')}</p>
      </div>

      {/* Score distribution */}
      <div className={CARD} style={CARD_STYLE}>
        <div className="mb-4">
          <p className="text-sm font-bold text-ink">{t('statistics.dist_title')}</p>
          <p className="text-xs text-muted mt-0.5">{t('statistics.dist_subtitle')}</p>
        </div>
        {trendsLoading ? (
          <div className="h-40 rounded-xl shimmer" />
        ) : scoreDist.every(d => d.count === 0) ? (
          <div className="h-40 flex items-center justify-center">
            <p className="text-sm text-muted">{t('statistics.no_data')}</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={scoreDist} layout="vertical" margin={{ left: 8, right: 16, top: 4, bottom: 4 }}>
              <CartesianGrid horizontal={false} stroke="rgba(194,184,164,0.35)" />
              <XAxis type="number" allowDecimals={false} tick={{ fontSize: 11, fill: '#68647C' }} tickLine={false} axisLine={false} />
              <YAxis type="category" dataKey="range" tick={{ fontSize: 12, fill: '#68647C' }} tickLine={false} axisLine={false} width={48} />
              <Tooltip
                contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }}
                formatter={(v: number) => [v, t('statistics.couples')]}
              />
              <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                {scoreDist.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
        {/* Legend */}
        {!trendsLoading && scoreDist.some(d => d.count > 0) && (
          <div className="flex flex-wrap gap-3 mt-3">
            {[
              { color: '#843048', label: t('statistics.dist_low') },
              { color: '#886028', label: t('statistics.dist_below') },
              { color: '#385C8A', label: t('statistics.dist_above') },
              { color: '#386858', label: t('statistics.dist_high') },
            ].map(({ color, label }) => (
              <div key={label} className="flex items-center gap-1.5">
                <div className="h-2.5 w-2.5 rounded-full" style={{ background: color }} />
                <span className="text-[11px] text-muted">{label}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Average score trend */}
      <div className={CARD} style={CARD_STYLE}>
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div>
            <p className="text-sm font-bold text-ink">{t('statistics.trend_title')}</p>
            <p className="text-xs text-muted mt-0.5">{t('statistics.trend_subtitle')}</p>
          </div>
          <PeriodToggle value={trendPeriod} onChange={setTrendPeriod} t={t as (k: string) => string} />
        </div>
        {trendsLoading ? (
          <div className="h-56 rounded-xl shimmer" />
        ) : scoreTrend.length === 0 ? (
          <div className="h-56 flex items-center justify-center">
            <p className="text-sm text-muted">{t('statistics.no_data')}</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={224}>
            <LineChart data={scoreTrend.map(d => ({ ...d, label: formatDate(d.date, trendPeriod) }))}>
              <CartesianGrid vertical={false} stroke="rgba(194,184,164,0.35)" />
              <XAxis dataKey="label" tick={{ fontSize: 11, fill: '#68647C' }} tickLine={false} axisLine={false} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#68647C' }} tickLine={false} axisLine={false} width={32} />
              <Tooltip
                contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }}
                formatter={(v: number) => [`${v}`, t('statistics.avg_score')]}
              />
              <Line type="monotone" dataKey="avg_score" stroke="#386858" strokeWidth={2.5} dot={false} activeDot={{ r: 4, fill: '#386858' }} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Activity chart */}
      <div className={CARD} style={CARD_STYLE}>
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
          <div>
            <p className="text-sm font-bold text-ink">{t('statistics.act_title')}</p>
            <p className="text-xs text-muted mt-0.5">{t('statistics.act_subtitle')}</p>
          </div>
          <PeriodToggle value={actPeriod} onChange={setActPeriod} t={t as (k: string) => string} />
        </div>
        {actLoading ? (
          <div className="h-56 rounded-xl shimmer" />
        ) : actData.length === 0 ? (
          <div className="h-56 flex items-center justify-center">
            <p className="text-sm text-muted">{t('statistics.no_data')}</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={224}>
            <BarChart data={actData.map(d => ({ ...d, label: formatDate(d.date, actPeriod) }))}>
              <CartesianGrid vertical={false} stroke="rgba(194,184,164,0.35)" />
              <XAxis dataKey="label" tick={{ fontSize: 11, fill: '#68647C' }} tickLine={false} axisLine={false} />
              <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#68647C' }} tickLine={false} axisLine={false} width={28} />
              <Tooltip contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="diagnostics" name={t('statistics.diagnostics')} fill="#3C3888" radius={[4, 4, 0, 0]} />
              <Bar dataKey="practices"   name={t('statistics.practices')}   fill="#386858" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}
