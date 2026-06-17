import { api } from './api'
import type { Couple, Invite } from '@/types/domain.types'

export const CoupleService = {
  create: () => api.post<Couple>('/couples/').then(r => r.data),
  getMe: () => api.get<Couple>('/couples/me/').then(r => r.data),
  acceptInvite: (token: string) => api.post<Couple>('/couples/invite/accept/', { token }).then(r => r.data),
  regenerateInvite: () => api.post<Invite>('/couples/invite/regenerate/').then(r => r.data),
}
