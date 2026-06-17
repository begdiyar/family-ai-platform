import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { FileText, Download, Loader2 } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { ReportsService } from '@/services/reports.service'
import { AuthService } from '@/services/auth.service'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { Report } from '@/types/domain.types'

const STATUS_BADGE: Record<Report['status'], 'warning' | 'success' | 'danger'> = {
  generating: 'warning',
  ready:      'success',
  failed:     'danger',
}

export const ReportsPage = () => {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const { t, i18n } = useTranslation('analytics')

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  const statusLabel = (status: Report['status']) => {
    if (status === 'generating') return t('status_generating')
    if (status === 'ready') return t('status_ready')
    return t('status_failed')
  }

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data, isLoading } = useQuery({
    queryKey: ['reports'],
    queryFn: ReportsService.list,
    retry: false,
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

  const pageHeader = (
    <div className="page-hero px-5 pt-6 pb-5">
      <div className="flex items-center gap-3">
        <div
          className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
          style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
        >
          <FileText size={17} className="text-white" />
        </div>
        <h1 className="text-xl font-bold text-ink">{t('reports_title', { defaultValue: 'Отчёты' })}</h1>
      </div>
    </div>
  )

  if (!me?.couple) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        {pageHeader}
        <div className="px-4 pt-4 md:px-5">
          <EmptyState
            icon={<FileText />}
            title={t('reports_no_couple_title', { defaultValue: 'Сначала создайте пару' })}
            description={t('reports_no_couple_desc', { defaultValue: 'Отчёты доступны после прохождения диагностики вместе с партнёром' })}
            actionLabel={t('reports_invite_btn', { defaultValue: 'Пригласить партнёра' })}
            onAction={() => navigate('/app/couple')}
          />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {pageHeader}

      <div className="px-4 pt-4 md:px-5">
        {/* Create cards */}
        <div className="mb-5 grid grid-cols-2 gap-3">
          <div
            className="rounded-[20px] p-4 text-center"
            style={{
              background: 'linear-gradient(135deg, #EDEAF8 0%, #EEE4DC 100%)',
              border: '1px solid rgba(60,56,136,0.12)',
            }}
          >
            <span className="mb-2 block text-3xl select-none">📊</span>
            <p className="mb-1 text-sm font-bold text-ink">{t('pdf_diagnostic_title')}</p>
            <p className="mb-3 text-xs text-muted leading-relaxed">{t('pdf_diagnostic_desc')}</p>
            <Button
              size="sm"
              fullWidth
              onClick={() => createDiagnosticMutation.mutate()}
              loading={createDiagnosticMutation.isPending}
            >
              {t('pdf_create_btn')}
            </Button>
          </div>
          <div
            className="rounded-[20px] p-4 text-center"
            style={{
              background: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)',
              border: '1px solid rgba(56,92,138,0.12)',
            }}
          >
            <span className="mb-2 block text-3xl select-none">📈</span>
            <p className="mb-1 text-sm font-bold text-ink">{t('pdf_progress_title')}</p>
            <p className="mb-3 text-xs text-muted leading-relaxed">{t('pdf_progress_desc')}</p>
            <Button
              size="sm"
              variant="secondary"
              fullWidth
              onClick={() => createProgressMutation.mutate()}
              loading={createProgressMutation.isPending}
            >
              {t('pdf_create_btn')}
            </Button>
          </div>
        </div>

        {/* History */}
        <p className="label-caps text-muted mb-3 px-1">{t('reports_history_label', { defaultValue: 'История отчётов' })}</p>

        {isLoading && (
          <div className="flex flex-col gap-3">
            {[...Array(2)].map((_, i) => <div key={i} className="h-20 rounded-card shimmer" />)}
          </div>
        )}

        {!isLoading && !data?.results?.length && (
          <EmptyState
            icon={<FileText />}
            title={t('reports_empty_title', { defaultValue: 'Отчётов пока нет' })}
            description={t('reports_empty_desc', { defaultValue: 'Создайте первый PDF-отчёт, нажав на одну из кнопок выше' })}
          />
        )}

        <div className="flex flex-col gap-3">
          {data?.results?.map((report: Report) => (
            <div
              key={report.id}
              className="rounded-[20px] bg-canvas p-4"
              style={{
                border: '1px solid rgba(232,227,218,0.6)',
                boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 4px 12px rgba(23,21,42,0.04)',
              }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="mb-1 flex items-center gap-2">
                    <span className="font-semibold text-ink text-sm">
                      {report.report_type === 'diagnostic' ? t('pdf_diagnostic_title') : t('pdf_progress_title')}
                    </span>
                    <Badge variant={STATUS_BADGE[report.status]}>{statusLabel(report.status)}</Badge>
                  </div>
                  <p className="text-xs text-muted">
                    {new Date(report.created_at).toLocaleDateString(dateLocale, { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
                <div className="flex gap-2 items-center">
                  {report.status === 'generating' && (
                    <div className="flex items-center gap-1.5 text-xs text-warning">
                      <Loader2 size={13} className="animate-spin" /> {t('status_generating')}
                    </div>
                  )}
                  {report.status === 'ready' && (
                    <Button size="sm" onClick={() => downloadReport(report)}>
                      <Download size={13} /> {t('pdf_download_btn')}
                    </Button>
                  )}
                  {report.status === 'failed' && (
                    <p className="text-xs font-medium text-danger">{t('status_failed')}</p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {data?.results?.some((r: Report) => r.status === 'generating') && (
          <p className="mt-4 text-center text-xs text-muted">
            {t('pdf_auto_update')}
          </p>
        )}
      </div>
    </div>
  )
}
