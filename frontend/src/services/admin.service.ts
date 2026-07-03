import { api } from './api'

export interface AdminOverview {
  total_users: number
  total_couples: number
  active_families_30d: number
  completed_diagnostics: number
  completed_practices: number
  ai_messages: number
  avg_relationship_score: number | null
  new_users_month: number
  crisis_breakdown: { none: number; warning: number; critical: number }
}

export interface TimeSeriesPoint {
  date: string
  count: number
}

export interface ActivityPoint {
  date: string
  diagnostics: number
  practices: number
}

export interface AdminFamily {
  id: string
  partner_a: string
  partner_b: string
  created_at: string
  diagnostics_count: number
  practices_count: number
  relationship_score: number | null
  crisis_level: 'none' | 'warning' | 'critical'
  last_activity: string | null
  is_active: boolean
}

export interface ExportFamily {
  id: string
  a_first_name: string
  a_last_name: string
  a_phone: string
  b_first_name: string
  b_last_name: string
  b_phone: string
  created_at: string
  diagnostics_per_level: Record<number, number>
  diagnostics_total: number
  practices_count: number
  relationship_score: number | null
  crisis_level: 'none' | 'warning' | 'critical'
}

export interface ExportData {
  results: ExportFamily[]
  total: number
  summary: { total: number; normal: number; warning: number; critical: number }
  level_numbers: number[]
}

export interface AdminFamiliesResponse {
  count: number
  page: number
  page_size: number
  total_pages: number
  results: AdminFamily[]
}

export interface ZoneProblem {
  zone: string
  avg_percent: number
  low_count: number
  low_percent: number
}

export interface AdminProblems {
  total_families: number
  zones: ZoneProblem[]
  crisis: { none: number; warning: number; critical: number }
}

export interface FamilyAnalyticsPoint {
  date: string
  overall_score: number | null
  crisis_level: string
  zones: Record<string, number | null>
}

export interface AdminFamilyDetail {
  id: string
  partner_a: { id: string; name: string; email: string }
  partner_b: { id: string; name: string; email: string } | null
  created_at: string
  marriage_year: number | null
  has_children: boolean
  children_count: number
  diagnostics_count: number
  practices_count: number
  last_activity: string | null
  latest_score: number | null
  latest_crisis: string
  analytics_history: FamilyAnalyticsPoint[]
}

export interface ScoreTrendPoint {
  date: string
  avg_score: number
}

export interface ScoreDistPoint {
  range: string
  count: number
  color: string
}

export interface AdminTrends {
  score_trend: ScoreTrendPoint[]
  score_distribution: ScoreDistPoint[]
}

export const AdminService = {
  getOverview: () =>
    api.get<AdminOverview>('/admin-panel/overview/').then(r => r.data),

  getRegistrations: (period: 'day' | 'week' | 'month' = 'day', count = 30) =>
    api.get<TimeSeriesPoint[]>('/admin-panel/registrations/', { params: { period, count } }).then(r => r.data),

  getActivity: (period: 'day' | 'week' | 'month' = 'day', count = 30) =>
    api.get<ActivityPoint[]>('/admin-panel/activity/', { params: { period, count } }).then(r => r.data),

  getFamilies: (params: {
    page?: number
    page_size?: number
    date_from?: string
    date_to?: string
    min_score?: number
    max_score?: number
    active?: boolean
    search?: string
  }) => api.get<AdminFamiliesResponse>('/admin-panel/families/', { params }).then(r => r.data),

  getFamilyDetail: (id: string) =>
    api.get<AdminFamilyDetail>(`/admin-panel/families/${id}/`).then(r => r.data),

  getProblems: () =>
    api.get<AdminProblems>('/admin-panel/problems/').then(r => r.data),

  getTrends: (period: 'day' | 'week' | 'month' = 'day', count = 30) =>
    api.get<AdminTrends>('/admin-panel/trends/', { params: { period, count } }).then(r => r.data),

  getExportData: () =>
    api.get<ExportData>('/admin-panel/export/').then(r => r.data),
}
