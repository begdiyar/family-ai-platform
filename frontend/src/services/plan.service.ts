import { api } from './api'
import type { RecoveryPlan } from '@/types/domain.types'

export const PlanService = {
  create: (result_id?: string) =>
    api.post<RecoveryPlan>('/plans/', { result_id }).then(r => r.data),
  getCurrent: () =>
    api.get<RecoveryPlan>('/plans/current/').then(r => r.data),
  completeTask: ({ planId, taskId, note }: { planId: string; taskId: string; note?: string }) =>
    api.post(`/plans/${planId}/tasks/${taskId}/complete/`, { note }).then(r => r.data),
  undoTask: ({ planId, taskId }: { planId: string; taskId: string }) =>
    api.delete(`/plans/${planId}/tasks/${taskId}/complete/`),
}
