import { api } from './api'
import type { DailyAssignment, FamilyDevelopmentPlan, PracticeStats } from '@/types/domain.types'

export const PracticesService = {
  getToday:   () => api.get<DailyAssignment>('/practices/today/').then(r => r.data),
  complete:   (assignmentId: string, slot: string) =>
    api.post<DailyAssignment>(`/practices/${assignmentId}/complete/${slot}/`).then(r => r.data),
  getPlan:    () => api.get<FamilyDevelopmentPlan>('/practices/plan/').then(r => r.data),
  getStats:   () => api.get<PracticeStats>('/practices/stats/').then(r => r.data),
  getHistory: (limit = 14) =>
    api.get<DailyAssignment[]>(`/practices/history/?limit=${limit}`).then(r => r.data),
}
