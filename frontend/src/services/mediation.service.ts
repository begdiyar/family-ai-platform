import { api } from './api'
import type { ConflictSession } from '@/types/domain.types'

export const MediationService = {
  list: () => api.get<ConflictSession[]>('/mediation/').then(r => r.data),
  create: (title: string) => api.post<ConflictSession>('/mediation/', { title }).then(r => r.data),
  get: (id: string) => api.get<ConflictSession>(`/mediation/${id}/`).then(r => r.data),
  submitEntry: (sessionId: string, data: { description: string; feelings?: string; desired_outcome?: string }) =>
    api.post(`/mediation/${sessionId}/submit/`, data).then(r => r.data),
}
