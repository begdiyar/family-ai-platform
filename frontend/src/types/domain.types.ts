export type User = {
  id: string
  email: string
  first_name: string
  avatar_url: string | null
  is_verified: boolean
  couple: CoupleShort | null
  created_at: string
}

export type CoupleShort = {
  id: string
  status: 'pending' | 'active' | 'paused'
  partner: Partner | null
}

export type Couple = {
  id: string
  status: 'pending' | 'active' | 'paused'
  partner_a: Partner
  partner_b: Partner | null
  diagnostics_status: { partner_a_completed: boolean; partner_b_completed: boolean }
  invite: Invite | null
  has_children: boolean
  children_count: number
  marriage_year: number | null
  created_at: string
}

export type Partner = {
  id: string
  first_name: string
  avatar_url: string | null
}

export type Invite = {
  token: string
  link: string
  expires_at: string
  status: string
}

export type Tokens = {
  access: string
  refresh: string
}

export type Zone = 'communication' | 'trust' | 'intimacy' | 'conflict' | 'values' | 'future'

export type ZoneScoreDetail = {
  zone: Zone
  label: string
  partner_a: { score: number; percent: number }
  partner_b: { score: number; percent: number }
  couple_avg: number
  gap: number
  status: 'strong' | 'growth' | 'attention'
}

export type BridgeAnalysis = {
  partner_a_perspective: string
  partner_b_perspective: string
  common_ground: string
  key_misunderstanding: string
  first_step: string
}

export type StrengthsSummary = {
  headline: string
  strengths: string[]
  achievement: string
  encouragement: string
}

export type ProblemChainItem = {
  step: number
  problem: string
  description: string
}

export type AnalyticsResult = {
  id: string
  overall_score: number
  zone_scores: ZoneScoreDetail[]
  strengths: Zone[]
  attention_zones: Zone[]
  key_insights: string[]
  crisis_level: 'none' | 'warning' | 'critical'
  bridge_analysis: BridgeAnalysis | null
  strengths_summary: StrengthsSummary | null
  problem_chain: ProblemChainItem[] | null
  relatives_index: 'low' | 'medium' | 'high' | null
  finance_index: number | null
  child_environment_index: number | null
  created_at: string
}

export type ConflictSession = {
  id: string
  title: string
  status: 'collecting' | 'analyzing' | 'complete'
  my_entry_submitted: boolean
  partner_entry_submitted: boolean
  ai_analysis: ConflictAnalysis | null
  created_at: string
}

export type ConflictAnalysis = {
  partner_a_position: string
  partner_b_position: string
  common_interests: string[]
  conflict_points: string[]
  compromises: { title: string; description: string }[]
  first_step: string
}

export type FamilyConstitution = {
  id: string
  values: string[]
  goals: string[]
  communication_rules: string[]
  conflict_rules: string[]
  finance_principles: string[]
  parenting_approach: string[]
  is_ai_generated: boolean
  updated_at: string
}

export type PracticeItem = {
  key: string
  content: string
  completed: boolean
}

export type DailyPractice = {
  id: string
  date: string
  is_ai_generated: boolean
  items: PracticeItem[]
}

export type AnalyticsResultShort = {
  id: string
  overall_score: number
  is_latest: boolean
  created_at: string
}

export type DiagnosticSession = {
  id: string
  status: 'in_progress' | 'completed' | 'abandoned'
  started_at: string
  finished_at: string | null
  answers_count: number
  total_questions: number
  progress_percent: number
}

export type Question = {
  id: string
  zone: Zone
  text: string
  question_type: 'scale' | 'choice' | 'text'
  options: string[] | null
  order_index: number
}

export type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export type Conversation = {
  id: string
  title: string | null
  messages_count: number
  created_at: string
  updated_at: string
}

export type PlanTask = {
  id: string
  week_number: number
  day_of_week: number | null
  title: string
  description: string | null
  task_type: 'exercise' | 'question' | 'reading' | 'practice'
  assigned_to: 'both' | 'partner_a' | 'partner_b'
  order_index: number
  completed_by_me: boolean
  completed_by_partner: boolean
}

export type PlanWeek = {
  week: number
  theme: string
  tasks: PlanTask[]
  progress: number
  locked: boolean
}

export type RecoveryPlan = {
  id: string
  title: string
  status: string
  duration_weeks: number
  started_at: string
  overall_progress: number
  current_week: number
  weeks: PlanWeek[]
}

export type Report = {
  id: string
  report_type: 'diagnostic' | 'progress'
  status: 'generating' | 'ready' | 'failed'
  file_url: string | null
  created_at: string
}

// ── Academy ───────────────────────────────────────────────────────────────────

export type AcademyCategory =
  | 'communication' | 'trust' | 'conflict' | 'intimacy' | 'love'
  | 'finance' | 'husband_role' | 'wife_role' | 'relatives' | 'parenting'
  | 'traditions' | 'stress' | 'marriage_prep' | 'crisis_recovery'

export type AcademyDifficulty = 'beginner' | 'intermediate' | 'advanced'

export type AcademySkillType =
  | 'active_listening' | 'emotion_management' | 'gratitude'
  | 'partner_support' | 'constructive_dialogue' | 'conflict_resolution' | 'joint_planning'

export type ArticleSource = {
  name: string
  source_type: 'researcher' | 'organization' | 'book' | 'journal'
  trust_level: 'high' | 'medium'
  url?: string | null
}

export type AcademyArticle = {
  id: string
  slug: string
  category: AcademyCategory
  title: string
  brief: string
  body?: string
  read_time_minutes: number
  difficulty: AcademyDifficulty
  tags: string[]
  sources?: ArticleSource[]
  is_completed: boolean
  order_index: number
}

export type AcademyTraining = {
  id: string
  slug: string
  skill_type: AcademySkillType
  title: string
  description: string
  theory?: string
  exercise_instruction?: string
  completion_check?: string
  duration_minutes: number
  difficulty: AcademyDifficulty
  is_completed: boolean
  status: 'not_started' | 'started' | 'completed'
  reflection_note?: string | null
  order_index: number
}

export type ProgramDayItem = {
  id: string
  day_number: number
  title: string
  material: string
  exercise: string
  reflection_prompt: string
  is_completed: boolean
}

export type AcademyProgram = {
  id: string
  slug: string
  title: string
  description: string
  duration_days: number
  category_focus: string
  cover_gradient: string
  days?: ProgramDayItem[]
  is_enrolled: boolean
  enrollment_status: 'not_enrolled' | 'active' | 'completed' | 'paused'
  current_day: number
  progress_percent: number
  order_index: number
}

export type AcademyMicroPractice = {
  id: string
  title: string
  instruction: string
  category: AcademyCategory
  duration_minutes: number
  is_completed: boolean
}

export type LearningProgress = {
  articles_read: number
  trainings_completed: number
  programs_completed: number
  current_streak: number
  total_minutes: number
  skills: { key: string; name: string; level: number }[]
}

export type AcademyAchievement = {
  id: string
  key: string
  title: string
  description: string
  icon: string
  condition_type: 'articles_count' | 'trainings_count' | 'programs_count' | 'streak_days'
  condition_value: number
}

export type UserAcademyAchievement = {
  achievement: AcademyAchievement
  earned_at: string
}

export type AcademyRecommendation = {
  type: 'article' | 'training' | 'program'
  reason: string
  item: AcademyArticle | AcademyTraining | AcademyProgram
}
