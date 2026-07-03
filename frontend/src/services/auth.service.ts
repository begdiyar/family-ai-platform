import { api } from './api'
import type { User, Tokens, CommunicationPreference } from '@/types/domain.types'

export const AuthService = {
  register: (data: { phone: string; password: string; first_name: string }) =>
    api.post<{ user: User; tokens: Tokens }>('/auth/register/', data).then(r => r.data),

  login: (data: { phone: string; password: string }) =>
    api.post<{ user: User; tokens: Tokens }>('/auth/login/', data).then(r => r.data),

  logout: (refresh: string) =>
    api.post('/auth/logout/', { refresh }),

  getMe: () =>
    api.get<User>('/users/me/').then(r => r.data),

  updateMe: (data: Partial<{
    first_name: string
    last_name: string
    birth_date: string | null
    gender: string
    native_language: string
    occupation: string
    education_level: string
    avatar_url: string
    preferred_language: string
  }>) =>
    api.patch<User>('/users/me/', data).then(r => r.data),

  getCommunicationPref: () =>
    api.get<CommunicationPreference>('/users/me/communication-pref/').then(r => r.data),

  updateCommunicationPref: (data: Partial<{ conflict_style: string; support_style: string }>) =>
    api.patch<CommunicationPreference>('/users/me/communication-pref/', data).then(r => r.data),

  changePassword: (data: { current_password: string; new_password: string }) =>
    api.post('/users/me/change-password/', data).then(r => r.data),
}
