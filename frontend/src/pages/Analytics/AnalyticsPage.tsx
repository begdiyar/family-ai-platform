import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { BarChart2, ArrowRight, TrendingUp, TrendingDown, FileText, Download, Loader2 } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AnalyticsService } from '@/services/analytics.service'
import { ReportsService } from '@/services/reports.service'
import { AuthService } from '@/services/auth.service'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { Report } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

const STATUS_BADGE: Record<Report['status'], 'warning' | 'success' | 'danger'> = {
  generating: 'warning',
  ready:      'success',
  failed:     'danger',
}

export const AnalyticsPage = () => {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('analytics')

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const { data, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: AnalyticsService.list,
    retry: false,
  })

  const { data: reports, isLoading: reportsLoading } = useQuery({
    queryKey: ['reports'],
    queryFn: ReportsService.list,
    retry: false,
    enabled: !!me?.couple,
    refetchInterval: (query) =>
      query.state.data?.results?.some((r: Report) => r.status === 'generating') ? 5000 : false,
  })

  const createDiagnosticMutation = useMutation({
    mutationFn: () => ReportsService.create('diagnostic'),
    onSuccess: () => { toast.success(t('toast_creating')); qc.invalidateQueries({ queryKey: ['reports'] }) },
    onError: () => toast.error(t('toast_error_create')),
  })

  const createProgressMutation = useMutation({
    mutationFn: () => ReportsService.create('progress'),
    onSuccess: () => { toast.success(t('toast_creating')); qc.invalidateQueries({ queryKey: ['reports'] }) },
    onError: () => toast.error(t('toast_error_create')),
  })

  const downloadReport = async (report: Report) => {
    if (report.status !== 'ready' || !report.file_url) return
    try {
      const url = await ReportsService.getDownloadUrl(report.id)
      window.open(url, '_blank')
    } catch {
      toast.error(t('toast_error_download'))
    }
  }

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  const statusLabel = (status: Report['status']) => {
    if (status === 'generating') return t('status_generating')
    if (status === 'ready') return t('status_ready')
    return t('status_failed')
  }

  const PageHeader = ({ count }: { count?: number }) => (
    <div className="page-hero px-5 pt-6 pb-5">
      <div className="flex items-center gap-3">
        <div
          className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
          style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.32)' }}
        >
          <BarChart2 size={17} className="text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
          {count !== undefined && <p className="text-xs text-muted mt-0.5">{count} {t('common:sessions', { defaultValue: 'сессий' })}</p>}
        </div>
      </div>
    </div>
  )

  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4 md:px-5 space-y-3">
          {[...Array(3)].map((_, i) => <div key={i} className="h-28 rounded-card shimmer" />)}
        </div>
      </div>
    )
  }

  if (!data?.results?.length) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <PageHeader />
        <div className="px-4 pt-4 md:px-5">
          <EmptyState
            icon={<BarChart2 />}
            title={t('empty_title')}
            description={t('empty_desc')}
            actionLabel={t('empty_btn')}
            onAction={() => navigate('/app/diagnostics')}
          />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      <PageHeader count={data.results.length} />

      <div className="px-4 pt-4 md:px-5">

        <div className="flex flex-col gap-3">
          {data.results.map((r, idx) => {
            const score = Math.round(r.overall_score)
            const prevScore = idx < data.results.length - 1
              ? Math.round(data.results[idx + 1]?.overall_score ?? score)
              : null
            const delta = prevScore !== null ? score - prevScore : null

            return (
              <motion.div
                key={r.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.35, ease, delay: idx * 0.05 }}
                className="rounded-[22px] bg-canvas p-5 cursor-pointer transition-all duration-200 hover:-translate-y-0.5"
                style={{
                  border: r.is_latest ? '1px solid rgba(60,56,136,0.22)' : '1px solid rgba(194,184,164,0.80)',
                  boxShadow: r.is_latest
                    ? '0 4px 20px rgba(60,56,136,0.12), 0 2px 8px rgba(23,21,42,0.06)'
                    : '0 2px 8px rgba(23,21,42,0.06), 0 4px 14px rgba(23,21,42,0.06)',
                }}
                onClick={() => navigate(`/app/analytics/${r.id}`)}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    {r.is_latest && <Badge variant="primary">{t('latest_badge')}</Badge>}
                  </div>
                  <p className="text-xs text-muted">
                    {new Date(r.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'long', year: 'numeric' })}
                  </p>
                </div>

                <div className="flex items-end justify-between mb-3">
                  <div>
                    <p className="text-xs text-muted mb-1">{t('score_label')}</p>
                    <span className="text-4xl font-bold" style={{ color: '#3C3888', letterSpacing: '-0.03em' }}>
                      {score}
                    </span>
                    <span className="text-base font-medium text-muted ml-1">/ 100</span>
                  </div>
                  {delta !== null && (
                    <div className={`flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-pill ${
                      delta > 0 ? 'text-success bg-sage-50' : delta < 0 ? 'text-danger bg-rose-50' : 'text-muted bg-sand/60'
                    }`}>
                      {delta > 0 ? <TrendingUp size={11} /> : delta < 0 ? <TrendingDown size={11} /> : null}
                      {delta > 0 ? '+' : ''}{delta}
                    </div>
                  )}
                </div>

                <div className="h-1.5 w-full rounded-full overflow-hidden bg-sand/60">
                  <div
                    className="h-full rounded-full"
                    style={{ width: `${score}%`, background: 'linear-gradient(90deg, #3C3888, #385C8A)' }}
                  />
                </div>

                <div className="mt-3 flex items-center justify-end gap-1 text-xs font-semibold text-primary">
                  {t('detail_link')} <ArrowRight size={13} />
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* ── PDF-Отчёты ───────────────────────────────────────────── */}
        {me?.couple && (
          <div className="mt-6">
            <div className="flex items-center gap-2 mb-3 px-1">
              <FileText size={13} className="text-muted" />
              <p className="label-caps text-muted">{t('pdf_section')}</p>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-4">
              <div
                className="rounded-[20px] p-4 text-center"
                style={{ background: 'linear-gradient(135deg, #EDEAF8 0%, #EEE4DC 100%)', border: '1px solid rgba(60,56,136,0.12)' }}
              >
                <span className="mb-2 block text-2xl select-none">📊</span>
                <p className="mb-0.5 text-sm font-bold text-ink">{t('pdf_diagnostic_title')}</p>
                <p className="mb-3 text-xs text-muted leading-relaxed">{t('pdf_diagnostic_desc')}</p>
                <Button size="sm" fullWidth onClick={() => createDiagnosticMutation.mutate()} loading={createDiagnosticMutation.isPending}>
                  {t('pdf_create_btn')}
                </Button>
              </div>
              <div
                className="rounded-[20px] p-4 text-center"
                style={{ background: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)', border: '1px solid rgba(56,92,138,0.14)' }}
              >
                <span className="mb-2 block text-2xl select-none">📈</span>
                <p className="mb-0.5 text-sm font-bold text-ink">{t('pdf_progress_title')}</p>
                <p className="mb-3 text-xs text-muted leading-relaxed">{t('pdf_progress_desc')}</p>
                <Button size="sm" variant="secondary" fullWidth onClick={() => createProgressMutation.mutate()} loading={createProgressMutation.isPending}>
                  {t('pdf_create_btn')}
                </Button>
              </div>
            </div>

            {reportsLoading ? (
              <div className="flex flex-col gap-2">
                {[...Array(2)].map((_, i) => <div key={i} className="h-16 rounded-[16px] shimmer" />)}
              </div>
            ) : reports?.results?.length ? (
              <div className="flex flex-col gap-2">
                {reports.results.map((report: Report) => (
                  <div
                    key={report.id}
                    className="rounded-[16px] bg-canvas p-3 flex items-center justify-between"
                    style={{ border: '1px solid rgba(194,184,164,0.80)', boxShadow: '0 2px 8px rgba(23,21,42,0.06)' }}
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-0.5">
                        <span className="text-sm font-semibold text-ink">
                          {report.report_type === 'diagnostic' ? t('pdf_diagnostic_title') : t('pdf_progress_title')}
                        </span>
                        <Badge variant={STATUS_BADGE[report.status]}>{statusLabel(report.status)}</Badge>
                      </div>
                      <p className="text-xs text-muted">
                        {new Date(report.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'short', year: 'numeric' })}
                      </p>
                    </div>
                    {report.status === 'generating' && (
                      <Loader2 size={16} className="animate-spin text-warning" />
                    )}
                    {report.status === 'ready' && (
                      <button
                        onClick={() => downloadReport(report)}
                        className="flex items-center gap-1.5 rounded-[10px] px-3 py-1.5 text-xs font-semibold text-primary transition-colors hover:bg-primary-50"
                      >
                        <Download size={13} /> {t('pdf_download_btn')}
                      </button>
                    )}
                  </div>
                ))}
                {reports.results.some((r: Report) => r.status === 'generating') && (
                  <p className="text-center text-xs text-muted mt-1">{t('pdf_auto_update')}</p>
                )}
              </div>
            ) : null}
          </div>
        )}
      </div>
    </div>
  )
}
