import { api } from './api'
import type { Report } from '@/types/domain.types'

export const ReportsService = {
  list: () => api.get<{ count: number; results: Report[] }>('/reports/').then(r => r.data),
  create: (report_type: 'diagnostic' | 'progress', result_id?: string) =>
    api.post<Report>('/reports/', { report_type, result_id }).then(r => r.data),
  getById: (id: string) => api.get<Report>(`/reports/${id}/`).then(r => r.data),
  getDownloadUrl: (id: string) =>
    api.get<{ download_url: string }>(`/reports/${id}/download/`).then(r => r.data.download_url),
  share: (id: string) =>
    api.post<{ share_token: string; share_url: string; expires_at: string }>(`/reports/${id}/share/`).then(r => r.data),
}
