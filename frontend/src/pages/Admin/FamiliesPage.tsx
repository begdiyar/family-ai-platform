import { useState, useCallback } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, keepPreviousData } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { Search, ChevronLeft, ChevronRight, Filter, Download, X } from 'lucide-react'
import { AdminService } from '@/services/admin.service'
import { Button } from '@/components/ui/Button'
import * as XLSX from 'xlsx'

const SCORE_COLOR = (score: number | null) => {
  if (score === null) return '#68647C'
  if (score < 40)  return '#843048'
  if (score < 60)  return '#886028'
  if (score < 80)  return '#385C8A'
  return '#386858'
}

const SCORE_BG = (score: number | null) => {
  if (score === null) return '#E8E2D4'
  if (score < 40)  return '#F5DDE4'
  if (score < 60)  return '#F5EDD8'
  if (score < 80)  return '#DDE8F2'
  return '#E2EDE8'
}

const CRISIS_COLORS: Record<string, { color: string; bg: string }> = {
  none:     { color: '#386858', bg: '#E2EDE8' },
  warning:  { color: '#886028', bg: '#F5EDD8' },
  critical: { color: '#843048', bg: '#F5DDE4' },
}

export const FamiliesPage = () => {
  const { t } = useTranslation('admin')
  const navigate = useNavigate()
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState({
    date_from: '', date_to: '', min_score: '', max_score: '', active: '',
  })

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['admin-families', page, search, filters],
    queryFn: () => AdminService.getFamilies({
      page,
      page_size: 20,
      search: search || undefined,
      date_from: filters.date_from || undefined,
      date_to: filters.date_to || undefined,
      min_score: filters.min_score ? Number(filters.min_score) : undefined,
      max_score: filters.max_score ? Number(filters.max_score) : undefined,
      active: filters.active === 'true' ? true : undefined,
    }),
    placeholderData: keepPreviousData,
    retry: 1,
  })

  console.log('[AdminFamilies] url=/admin-panel/families/', { page, search, filters })
  console.log('[AdminFamilies] state:', { isLoading, isError, count: data?.count, results: data?.results?.length })
  if (isError) console.error('[AdminFamilies] error:', error)

  const handleSearch = useCallback(() => {
    setSearch(searchInput)
    setPage(1)
  }, [searchInput])

  const handleFilter = (key: string, value: string) => {
    setFilters(f => ({ ...f, [key]: value }))
    setPage(1)
  }

  const clearFilters = () => {
    setFilters({ date_from: '', date_to: '', min_score: '', max_score: '', active: '' })
    setSearch('')
    setSearchInput('')
    setPage(1)
  }

  const hasFilters = Object.values(filters).some(Boolean) || search

  const handleExport = async () => {
    const data = await AdminService.getExportData()
    const ws = XLSX.utils.json_to_sheet(data.results.map(f => ({
      'ID': f.id,
      'Партнёр A': f.partner_a,
      'Партнёр B': f.partner_b,
      'Дата регистрации': f.created_at,
      'Диагностик': f.diagnostics_count,
      'Практик': f.practices_count,
      'Индекс': f.relationship_score ?? '—',
      'Кризис': f.crisis_level,
    })))
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Семьи')
    XLSX.writeFile(wb, 'families.xlsx')
  }

  return (
    <div className="min-h-full bg-surface p-4 md:p-6">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-5">
        <div>
          <h1 className="text-xl md:text-2xl font-bold text-ink">{t('families.title')}</h1>
          <p className="text-sm text-muted mt-0.5">
            {data ? t('common.families_count', { count: data.count }) : t('common.loading')}
          </p>
        </div>
        <div className="flex gap-2 shrink-0">
          <Button variant="secondary" size="sm" onClick={() => setShowFilters(f => !f)}>
            <Filter size={13} /> {t('families.filters')} {hasFilters && <span className="ml-1 h-1.5 w-1.5 rounded-full bg-primary inline-block" />}
          </Button>
          <Button variant="secondary" size="sm" onClick={handleExport}>
            <Download size={13} /> {t('families.excel')}
          </Button>
        </div>
      </div>

      {/* Search */}
      <div className="flex gap-2 mb-4">
        <div className="flex-1 relative">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
          <input
            value={searchInput}
            onChange={e => setSearchInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            placeholder={t('families.search_placeholder')}
            className="w-full h-10 rounded-[12px] border border-sand bg-canvas pl-9 pr-4 text-sm text-ink placeholder:text-muted/50 outline-none focus:border-primary/50"
          />
        </div>
        <button onClick={handleSearch}
          className="px-4 h-10 rounded-[12px] bg-primary text-white text-sm font-semibold hover:opacity-90 transition-opacity">
          {t('families.search')}
        </button>
        {hasFilters && (
          <button onClick={clearFilters} className="px-3 h-10 rounded-[12px] bg-sand/40 text-muted text-sm hover:bg-sand/60 transition-colors flex items-center gap-1.5">
            <X size={13} /> {t('families.reset')}
          </button>
        )}
      </div>

      {/* Filters panel */}
      {showFilters && (
        <div className="mb-4 rounded-[16px] bg-canvas p-4 grid grid-cols-2 md:grid-cols-5 gap-3"
             style={{ border: '1px solid rgba(194,184,164,0.60)' }}>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted">{t('families.filter.date_from')}</label>
            <input type="date" value={filters.date_from}
              onChange={e => handleFilter('date_from', e.target.value)}
              className="h-9 rounded-[10px] border border-sand bg-surface px-2 text-sm text-ink outline-none focus:border-primary/50" />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted">{t('families.filter.date_to')}</label>
            <input type="date" value={filters.date_to}
              onChange={e => handleFilter('date_to', e.target.value)}
              className="h-9 rounded-[10px] border border-sand bg-surface px-2 text-sm text-ink outline-none focus:border-primary/50" />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted">{t('families.filter.score_from')}</label>
            <input type="number" min={0} max={100} value={filters.min_score}
              onChange={e => handleFilter('min_score', e.target.value)}
              placeholder="0"
              className="h-9 rounded-[10px] border border-sand bg-surface px-2 text-sm text-ink outline-none focus:border-primary/50" />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted">{t('families.filter.score_to')}</label>
            <input type="number" min={0} max={100} value={filters.max_score}
              onChange={e => handleFilter('max_score', e.target.value)}
              placeholder="100"
              className="h-9 rounded-[10px] border border-sand bg-surface px-2 text-sm text-ink outline-none focus:border-primary/50" />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-semibold text-muted">{t('families.filter.activity')}</label>
            <select value={filters.active} onChange={e => handleFilter('active', e.target.value)}
              className="h-9 rounded-[10px] border border-sand bg-surface px-2 text-sm text-ink outline-none focus:border-primary/50">
              <option value="">{t('families.filter.all')}</option>
              <option value="true">{t('families.filter.active_only')}</option>
            </select>
          </div>
        </div>
      )}

      {/* Table */}
      <div className="rounded-[20px] bg-canvas overflow-hidden"
           style={{ border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }}>
        {isLoading ? (
          <div className="p-4 space-y-2">
            {[...Array(10)].map((_, i) => <div key={i} className="h-12 rounded-xl shimmer" />)}
          </div>
        ) : isError ? (
          <div className="p-10 text-center">
            <p className="text-sm font-semibold text-[#843048]">{t('common.error')}</p>
            <p className="text-xs text-muted mt-1">{t('families.error_hint')}</p>
          </div>
        ) : !data?.results.length ? (
          <div className="p-10 text-center">
            <p className="text-sm text-muted">{t('families.empty')}</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm min-w-[360px]">
              <thead>
                <tr style={{ borderBottom: '1px solid rgba(194,184,164,0.50)', background: 'rgba(232,227,218,0.40)' }}>
                  <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide">{t('families.table.family')}</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide hidden sm:table-cell">{t('families.table.date')}</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide hidden md:table-cell">{t('families.table.diagnostics')}</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide hidden md:table-cell">{t('families.table.practices')}</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide">{t('families.table.index')}</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide hidden sm:table-cell">{t('families.table.crisis')}</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-muted uppercase tracking-wide">{t('families.table.status')}</th>
                </tr>
              </thead>
              <tbody>
                {data?.results.map((f, i) => {
                  const crisis = CRISIS_COLORS[f.crisis_level] ?? CRISIS_COLORS.none
                  return (
                    <tr key={f.id}
                      onClick={() => navigate(`/admin/families/${f.id}`)}
                      className="cursor-pointer transition-colors hover:bg-surface/50"
                      style={{ borderBottom: i < (data.results.length - 1) ? '1px solid rgba(194,184,164,0.30)' : 'none' }}>
                      <td className="px-4 py-3 max-w-[130px] sm:max-w-none">
                        <p className="font-semibold text-ink truncate">{f.partner_a} & {f.partner_b || '—'}</p>
                      </td>
                      <td className="px-4 py-3 text-muted whitespace-nowrap hidden sm:table-cell">{f.created_at}</td>
                      <td className="px-4 py-3 font-medium text-ink hidden md:table-cell">{f.diagnostics_count}</td>
                      <td className="px-4 py-3 font-medium text-ink hidden md:table-cell">{f.practices_count}</td>
                      <td className="px-4 py-3">
                        {f.relationship_score !== null ? (
                          <span className="inline-flex items-center rounded-[10px] px-2 py-0.5 text-sm font-bold"
                            style={{ background: SCORE_BG(f.relationship_score), color: SCORE_COLOR(f.relationship_score) }}>
                            {f.relationship_score}
                          </span>
                        ) : <span className="text-muted">—</span>}
                      </td>
                      <td className="px-4 py-3 hidden sm:table-cell">
                        <span className="inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold whitespace-nowrap"
                          style={{ background: crisis.bg, color: crisis.color }}>
                          {t(`common.crisis.${f.crisis_level}`)}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-semibold whitespace-nowrap ${
                          f.is_active ? 'bg-sage-50 text-sage-700' : 'bg-sand/40 text-muted'
                        }`}>
                          {f.is_active ? t('common.status.active') : t('common.status.inactive')}
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Pagination */}
      {data && data.total_pages > 1 && (
        <div className="flex items-center justify-between mt-4">
          <p className="text-sm text-muted">
            {t('families.pagination', { page: data.page, total: data.total_pages, count: data.count })}
          </p>
          <div className="flex items-center gap-2">
            <button disabled={page <= 1} onClick={() => setPage(p => p - 1)}
              className="flex h-8 w-8 items-center justify-center rounded-[10px] border border-sand disabled:opacity-40 hover:bg-surface transition-colors">
              <ChevronLeft size={14} />
            </button>
            {Array.from({ length: Math.min(5, data.total_pages) }, (_, i) => {
              const p = Math.max(1, Math.min(data.total_pages - 4, page - 2)) + i
              return (
                <button key={p} onClick={() => setPage(p)}
                  className="flex h-8 w-8 items-center justify-center rounded-[10px] text-sm font-semibold transition-colors"
                  style={p === page ? { background: '#3C3888', color: '#fff' } : { color: '#68647C' }}>
                  {p}
                </button>
              )
            })}
            <button disabled={page >= data.total_pages} onClick={() => setPage(p => p + 1)}
              className="flex h-8 w-8 items-center justify-center rounded-[10px] border border-sand disabled:opacity-40 hover:bg-surface transition-colors">
              <ChevronRight size={14} />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
