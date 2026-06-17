import { api } from './api'
import type { DiagnosticSession, Question } from '@/types/domain.types'

type QuestionsResponse = { total: number; zones: Array<{ zone: string; label: string; questions: Question[] }> }

export const DiagnosticsService = {
  getQuestions: () => api.get<QuestionsResponse>('/diagnostics/questions/').then(r => r.data),
  startSession: () => api.post<DiagnosticSession>('/diagnostics/sessions/').then(r => r.data),
  getCurrentSession: () => api.get<DiagnosticSession>('/diagnostics/sessions/current/').then(r => r.data),
  saveAnswers: (sessionId: string, answers: Array<{ question_id: string; value_scale?: number; value_choice?: string; value_text?: string }>) =>
    api.post(`/diagnostics/sessions/${sessionId}/answers/`, { answers }).then(r => r.data),
  completeSession: (sessionId: string) =>
    api.post(`/diagnostics/sessions/${sessionId}/complete/`).then(r => r.data),
}
