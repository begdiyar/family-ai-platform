import { api } from './api'
import type {
  AcademyArticle, AcademyTraining, AcademyProgram, AcademyMicroPractice,
  LearningProgress, UserAcademyAchievement, AcademyRecommendation,
} from '@/types/domain.types'

type ListResponse<T> = { count: number; results: T[] }

export const AcademyService = {
  // Articles
  listArticles: (params?: { category?: string; difficulty?: string; search?: string }) =>
    api.get<ListResponse<AcademyArticle>>('/academy/articles/', { params }).then(r => r.data),

  getArticle: (slug: string) =>
    api.get<AcademyArticle>(`/academy/articles/${slug}/`).then(r => r.data),

  completeArticle: (slug: string) =>
    api.post<{ completed: boolean; newly_completed: boolean }>(`/academy/articles/${slug}/complete/`).then(r => r.data),

  reflectArticle: (slug: string, payload: { question_key: 'understood' | 'try' | 'apply'; answer: string }) =>
    api.post<{
      question_key: string; answer: string; ai_response: string;
      next_question_key: string | null; next_question: string | null;
    }>(`/academy/articles/${slug}/reflect/`, payload).then(r => r.data),

  // Trainings
  listTrainings: () =>
    api.get<ListResponse<AcademyTraining>>('/academy/trainings/').then(r => r.data),

  getTraining: (slug: string) =>
    api.get<AcademyTraining>(`/academy/trainings/${slug}/`).then(r => r.data),

  startTraining: (slug: string) =>
    api.post<{ status: string }>(`/academy/trainings/${slug}/start/`).then(r => r.data),

  completeTraining: (slug: string, reflection_note?: string) =>
    api.post<AcademyTraining>(`/academy/trainings/${slug}/complete/`, { reflection_note }).then(r => r.data),

  // Programs
  listPrograms: () =>
    api.get<ListResponse<AcademyProgram>>('/academy/programs/').then(r => r.data),

  getProgram: (slug: string) =>
    api.get<AcademyProgram>(`/academy/programs/${slug}/`).then(r => r.data),

  getActiveProgram: () =>
    api.get<{ active_program: AcademyProgram | null }>('/academy/programs/active/').then(r => r.data),

  enrollProgram: (slug: string) =>
    api.post<AcademyProgram>(`/academy/programs/${slug}/enroll/`).then(r => r.data),

  completeProgramDay: (slug: string, dayNumber: number, reflection?: string) =>
    api.post<AcademyProgram>(`/academy/programs/${slug}/days/${dayNumber}/complete/`, { reflection }).then(r => r.data),

  // Micro practice
  getTodayMicroPractice: () =>
    api.get<{ practice: AcademyMicroPractice | null; is_completed: boolean }>('/academy/micro-practice/today/').then(r => r.data),

  completeMicroPractice: (id: string) =>
    api.post<{ completed: boolean }>(`/academy/micro-practice/${id}/complete/`).then(r => r.data),

  // Progress & recommendations
  getProgress: () =>
    api.get<LearningProgress>('/academy/progress/').then(r => r.data),

  getRecommendations: () =>
    api.get<ListResponse<AcademyRecommendation>>('/academy/recommendations/').then(r => r.data),

  getAchievements: () =>
    api.get<ListResponse<UserAcademyAchievement>>('/academy/achievements/').then(r => r.data),
}
