import { api } from './api'
import type { Couple, Invite, Child, FamilyValue } from '@/types/domain.types'

export const CoupleService = {
  create: () => api.post<Couple>('/couples/').then(r => r.data),
  getMe: () => api.get<Couple>('/couples/me/').then(r => r.data),
  acceptInvite: (token: string) => api.post<Couple>('/couples/invite/accept/', { token }).then(r => r.data),
  regenerateInvite: () => api.post<Invite>('/couples/invite/regenerate/').then(r => r.data),

  // Children
  getChildren: () => api.get<Child[]>('/couples/me/children/').then(r => r.data),
  addChild: (data: { birth_date: string; gender: string }) =>
    api.post<Child>('/couples/me/children/', data).then(r => r.data),
  removeChild: (id: string) => api.delete(`/couples/me/children/${id}/`),

  // Family context (relationship + context fields)
  getFamilyContext: () => api.get('/couples/me/family-context/').then(r => r.data),
  updateFamilyContext: (data: Partial<{
    relationship_status: string
    relationship_start_date: string | null
    marriage_date: string | null
    lives_with_parents: boolean
    relatives_influence_level: number | null
    religious_traditions_importance: number | null
    family_values: string[]
  }>) => api.patch('/couples/me/family-context/', data).then(r => r.data),

  // Family values
  getAllFamilyValues: () => api.get<FamilyValue[]>('/couples/family-values/').then(r => r.data),
  getCoupleFamilyValues: () => api.get<FamilyValue[]>('/couples/me/family-values/').then(r => r.data),
  setFamilyValues: (slugs: string[]) =>
    api.put<FamilyValue[]>('/couples/me/family-values/', { slugs }).then(r => r.data),
}
