import { api } from './api'
import type { FamilyConstitution } from '@/types/domain.types'

export const ConstitutionService = {
  get: () => api.get<FamilyConstitution>('/constitution/').then(r => r.data),
  update: (data: Partial<FamilyConstitution>) => api.put<FamilyConstitution>('/constitution/', data).then(r => r.data),
  generateWithAI: () => api.post<FamilyConstitution>('/constitution/generate/').then(r => r.data),
}
