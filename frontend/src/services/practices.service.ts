import { api } from './api'
import type { DailyPractice } from '@/types/domain.types'

export const PracticesService = {
  getToday: () => api.get<DailyPractice>('/practices/today/').then(r => r.data),
  complete: (practiceId: string, fieldName: string) =>
    api.post(`/practices/${practiceId}/complete/`, { field_name: fieldName }).then(r => r.data),
}
