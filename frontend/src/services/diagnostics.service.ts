import { api } from './api'
import type { DiagnosticSession, Question, FamilyJourney } from '@/types/domain.types'

type QuestionsResponse = {
  level_number: number
  total: number
  questions: Question[]
}

export const DiagnosticsService = {
  getJourney: () =>
    api.get<FamilyJourney>('/diagnostics/journey/').then(r => r.data),

  getQuestions: (levelNumber: number) =>
    api.get<QuestionsResponse>(`/diagnostics/questions/?level=${levelNumber}`).then(r => r.data),

  startSession: (levelNumber: number) =>
    api.post<DiagnosticSession>('/diagnostics/sessions/', { level_number: levelNumber }).then(r => r.data),

  getCurrentSession: () =>
    api.get<DiagnosticSession>('/diagnostics/sessions/current/').then(r => r.data),

  saveAnswers: (
    sessionId: string,
    answers: Array<{ question_id: string; value_scale?: number; value_choice?: string; value_text?: string }>,
  ) =>
    api.post(`/diagnostics/sessions/${sessionId}/answers/`, { answers }).then(r => r.data),

  completeSession: (sessionId: string) =>
    api.post(`/diagnostics/sessions/${sessionId}/complete/`).then(r => r.data),
}
