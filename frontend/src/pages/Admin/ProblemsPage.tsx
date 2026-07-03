import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import {
  RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer,
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from 'recharts'
import { AdminService } from '@/services/admin.service'

const ZONE_COLORS: Record<string, string> = {
  communication: '#2C5678', trust: '#286250', intimacy: '#74364A',
  conflict: '#744E26', values: '#463E80', future: '#385C8A',
}

const CRISIS_COLORS = { none: '#386858', warning: '#886028', critical: '#843048' }

export const ProblemsPage = () => {
  const { t } = useTranslation('admin')

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['admin-problems'],
    queryFn: AdminService.getProblems,
    retry: 1,
  })

  console.log('[AdminProblems] url=/admin-panel/problems/', { isLoading, isError, total_families: data?.total_families })
  if (isError) console.error('[AdminProblems] error:', error)

  if (isLoading) return (
    <div className="min-h-full bg-surface p-4 md:p-6 space-y-4">
      <div className="h-8 w-48 rounded-xl shimmer" />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[...Array(4)].map((_, i) => <div key={i} className="h-64 rounded-[20px] shimmer" />)}
      </div>
    </div>
  )

  if (isError) return (
    <div className="min-h-full bg-surface p-4 md:p-6 flex items-center justify-center">
      <div className="text-center">
        <p className="text-sm font-semibold text-[#843048]">{t('common.error')}</p>
        <p className="text-xs text-muted mt-1">{t('common.error_hint')}</p>
      </div>
    </div>
  )

  if (!data || data.total_families === 0) return (
    <div className="min-h-full bg-surface p-4 md:p-6 flex items-center justify-center">
      <div className="text-center max-w-sm">
        <p className="font-semibold text-ink">{t('problems.no_data')}</p>
        <p className="text-sm text-muted mt-1">{t('problems.no_data_hint')}</p>
      </div>
    </div>
  )

  const zoneLabel = (key: string) => t(`common.zones.${key}`, { defaultValue: key })

  const radarData = data.zones.map(z => ({
    zone: zoneLabel(z.zone),
    value: z.avg_percent,
    fullMark: 100,
  }))

  const barData = data.zones
    .map(z => ({
      name: zoneLabel(z.zone),
      percent: z.low_percent,
      count: z.low_count,
      color: ZONE_COLORS[z.zone] ?? '#3C3888',
    }))
    .sort((a, b) => b.percent - a.percent)

  const crisisPieData = [
    { name: t('common.crisis.none'),     value: data.crisis.none,     color: CRISIS_COLORS.none     },
    { name: t('common.crisis.warning'),  value: data.crisis.warning,  color: CRISIS_COLORS.warning  },
    { name: t('common.crisis.critical'), value: data.crisis.critical, color: CRISIS_COLORS.critical },
  ].filter(d => d.value > 0)

  return (
    <div className="min-h-full bg-surface p-4 md:p-6 space-y-5">
      <div>
        <h1 className="text-xl md:text-2xl font-bold text-ink">{t('problems.title')}</h1>
        <p className="text-sm text-muted mt-0.5">
          {t('problems.subtitle', { count: data.total_families })}
        </p>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { key: 'none',     color: CRISIS_COLORS.none,     bg: '#E2EDE8' },
          { key: 'warning',  color: CRISIS_COLORS.warning,  bg: '#F5EDD8' },
          { key: 'critical', color: CRISIS_COLORS.critical, bg: '#F5DDE4' },
        ].map(({ key, color, bg }) => {
          const count = data.crisis[key as keyof typeof data.crisis]
          const pct = Math.round(count / data.total_families * 100)
          return (
            <div key={key} className="rounded-[18px] p-3 md:p-4 text-center" style={{ background: bg }}>
              <p className="text-2xl md:text-3xl font-bold" style={{ color }}>{count}</p>
              <p className="text-xs font-semibold mt-0.5" style={{ color }}>{t(`common.crisis.${key}`)}</p>
              <p className="text-xs text-muted mt-0.5">{pct}%</p>
            </div>
          )
        })}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {/* Crisis pie */}
        <div className="rounded-[20px] bg-canvas p-5"
             style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
          <p className="text-sm font-bold text-ink mb-4">{t('problems.crisis_chart')}</p>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={crisisPieData} cx="50%" cy="50%" innerRadius={60} outerRadius={100}
                   paddingAngle={3} dataKey="value" nameKey="name">
                {crisisPieData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }}
                formatter={(v: number) => [v, t('problems.families_tooltip')]}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Zone radar */}
        <div className="rounded-[20px] bg-canvas p-5"
             style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
          <p className="text-sm font-bold text-ink mb-2">{t('problems.radar_title')}</p>
          <ResponsiveContainer width="100%" height={240}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="rgba(194,184,164,0.40)" />
              <PolarAngleAxis dataKey="zone" tick={{ fontSize: 11, fill: '#68647C' }} />
              <Radar name={t('problems.radar_title')} dataKey="value" stroke="#3C3888" fill="#3C3888" fillOpacity={0.18} strokeWidth={2} />
              <Tooltip
                contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }}
                formatter={(v: number) => [`${v}%`]}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Problematic zones bar */}
        <div className="rounded-[20px] bg-canvas p-5 md:col-span-2"
             style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
          <p className="text-sm font-bold text-ink mb-1">{t('problems.bar_title')}</p>
          <p className="text-xs text-muted mb-4">{t('problems.bar_subtitle')}</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={barData} layout="vertical">
              <CartesianGrid horizontal={false} stroke="rgba(194,184,164,0.40)" />
              <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11, fill: '#68647C' }}
                tickLine={false} axisLine={false} tickFormatter={v => `${v}%`} />
              <YAxis type="category" dataKey="name" tick={{ fontSize: 12, fill: '#17152A' }}
                tickLine={false} axisLine={false} width={100} />
              <Tooltip
                contentStyle={{ background: '#F4EFE4', border: '1px solid rgba(194,184,164,0.6)', borderRadius: 12, fontSize: 12 }}
                formatter={(v: number, _name: string, props: any) => [
                  t('problems.tooltip_families', { pct: v, count: props.payload?.count ?? 0 }),
                  t('problems.families_tooltip'),
                ]}
              />
              <Bar dataKey="percent" radius={[0,6,6,0]}>
                {barData.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Zone table */}
      <div className="rounded-[20px] bg-canvas overflow-hidden"
           style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
        <div className="px-5 py-4 border-b border-sand/40">
          <p className="text-sm font-bold text-ink">{t('problems.zone_table')}</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm min-w-[480px]">
            <thead style={{ background: 'rgba(232,227,218,0.40)' }}>
              <tr>
                <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide">{t('problems.cols.zone')}</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide">{t('problems.cols.avg_score')}</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide hidden sm:table-cell">{t('problems.cols.problem_count')}</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide">{t('problems.cols.problem_pct')}</th>
                <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide">{t('problems.cols.level')}</th>
              </tr>
            </thead>
            <tbody>
              {data.zones.map((z, i) => {
                const color = ZONE_COLORS[z.zone] ?? '#3C3888'
                const status = z.avg_percent >= 70
                  ? { labelKey: 'common.level.good', bg: '#E2EDE8', color: '#386858' }
                  : z.avg_percent >= 50
                  ? { labelKey: 'common.level.medium', bg: '#EDEAF8', color: '#3C3888' }
                  : { labelKey: 'common.level.warning', bg: '#F5EDD8', color: '#886028' }
                return (
                  <tr key={z.zone}
                    style={{ borderBottom: i < data.zones.length - 1 ? '1px solid rgba(194,184,164,0.30)' : 'none' }}>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ background: color }} />
                        <span className="font-medium text-ink">{zoneLabel(z.zone)}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-14 rounded-full bg-sand/50 overflow-hidden hidden sm:block">
                          <div className="h-full rounded-full" style={{ width: `${z.avg_percent}%`, background: color }} />
                        </div>
                        <span className="font-bold" style={{ color }}>{z.avg_percent}%</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 font-medium text-ink hidden sm:table-cell">{z.low_count}</td>
                    <td className="px-4 py-3 font-bold" style={{ color: z.low_percent > 40 ? '#843048' : '#68647C' }}>
                      {z.low_percent}%
                    </td>
                    <td className="px-4 py-3">
                      <span className="inline-flex rounded-full px-2 py-0.5 text-xs font-semibold whitespace-nowrap"
                            style={{ background: status.bg, color: status.color }}>
                        {t(status.labelKey)}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
