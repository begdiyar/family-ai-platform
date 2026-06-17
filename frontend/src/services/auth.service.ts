import { api } from './api'
import type { User, Tokens } from '@/types/domain.types'

export const AuthService = {
  register: (data: { email: string; password: string; first_name: string }) =>
    api.post<{ user: User; tokens: Tokens }>('/auth/register/', data).then(r => r.data),

  login: (data: { email: string; password: string }) =>
    api.post<{ user: User; tokens: Tokens }>('/auth/login/', data).then(r => r.data),

  logout: (refresh: string) =>
    api.post('/auth/logout/', { refresh }),

  getMe: () =>
    api.get<User>('/users/me/').then(r => r.data),

  updateMe: (data: Partial<{ first_name: string; avatar_url: string }>) =>
    api.patch<User>('/users/me/', data).then(r => r.data),
}
