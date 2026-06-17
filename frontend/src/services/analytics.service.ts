import { api } from './api'
import type { AnalyticsResult, AnalyticsResultShort } from '@/types/domain.types'

export const AnalyticsService = {
  list: () => api.get<{ count: number; results: AnalyticsResultShort[] }>('/analytics/results/').then(r => r.data),
  getLatest: () => api.get<AnalyticsResult>('/analytics/results/latest/').then(r => r.data),
  getById: (id: string) => api.get<AnalyticsResult>(`/analytics/results/${id}/`).then(r => r.data),
  getProgress: () => api.get('/analytics/progress/').then(r => r.data),
}
