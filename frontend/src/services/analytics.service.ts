import { api } from './api'
import type { AnalyticsResult, AnalyticsResultShort, AnalyticsInsight } from '@/types/domain.types'

export const AnalyticsService = {
  list: () => api.get<{ count: number; results: AnalyticsResultShort[] }>('/analytics/results/').then(r => r.data),
  getLatest: (): Promise<AnalyticsResult | null> =>
    api.get<AnalyticsResult>('/analytics/results/latest/')
      .then(r => r.data)
      .catch(e => { if (e?.response?.status === 404) return null; throw e }),
  getById: (id: string) => api.get<AnalyticsResult>(`/analytics/results/${id}/`).then(r => r.data),
  getInsight: (): Promise<AnalyticsInsight | null> =>
    api.get<AnalyticsInsight>('/analytics/results/latest/insight/')
      .then(r => r.data)
      .catch(e => { if (e?.response?.status === 404) return null; throw e }),
  getProgress: () => api.get('/analytics/progress/').then(r => r.data),
}
