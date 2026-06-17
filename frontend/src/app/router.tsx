import { createBrowserRouter, Navigate } from 'react-router-dom'
import { AppLayout } from '@/layouts/AppLayout'
import { PublicLayout } from '@/layouts/PublicLayout'
import { ProtectedRoute } from '@/lib/ProtectedRoute'

import { LoginPage } from '@/pages/Auth/LoginPage'
import { RegisterPage } from '@/pages/Auth/RegisterPage'
import { InviteAcceptPage } from '@/pages/Auth/InviteAcceptPage'
import { DashboardPage } from '@/pages/Dashboard/DashboardPage'
import { CouplePage } from '@/pages/Couple/CouplePage'
import { DiagnosticsPage } from '@/pages/Diagnostics/DiagnosticsPage'
import { DiagnosticsStartPage } from '@/pages/Diagnostics/DiagnosticsStartPage'
import { AnalyticsPage } from '@/pages/Analytics/AnalyticsPage'
import { AnalyticsDetailPage } from '@/pages/Analytics/AnalyticsDetailPage'
import { AIChatPage } from '@/pages/AIChat/AIChatPage'
import { ProfilePage } from '@/pages/Profile/ProfilePage'
import { PracticesPage } from '@/pages/Practices/PracticesPage'
import { MediationPage } from '@/pages/Mediation/MediationPage'
import { RelationshipIndexPage } from '@/pages/Index/RelationshipIndexPage'
import { AcademyPage } from '@/pages/Academy/AcademyPage'
import { ArticleDetailPage } from '@/pages/Academy/ArticleDetailPage'
import { TrainingDetailPage } from '@/pages/Academy/TrainingDetailPage'
import { ProgramDetailPage } from '@/pages/Academy/ProgramDetailPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      { index: true, element: <Navigate to="/login" replace /> },
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
      { path: 'invite/:token', element: <InviteAcceptPage /> },
    ],
  },
  {
    path: '/app',
    element: <ProtectedRoute><AppLayout /></ProtectedRoute>,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'couple', element: <CouplePage /> },
      { path: 'diagnostics', element: <DiagnosticsPage /> },
      { path: 'diagnostics/start', element: <DiagnosticsStartPage /> },
      { path: 'analytics', element: <AnalyticsPage /> },
      { path: 'analytics/:resultId', element: <AnalyticsDetailPage /> },
      { path: 'ai', element: <AIChatPage /> },
      { path: 'ai/:convId', element: <AIChatPage /> },
      { path: 'plan', element: <Navigate to="/app/practices" replace /> },
      { path: 'practices', element: <PracticesPage /> },
      { path: 'mediation', element: <MediationPage /> },
      { path: 'constitution', element: <Navigate to="/app/index" replace /> },
      { path: 'index', element: <RelationshipIndexPage /> },
      { path: 'bridge', element: <Navigate to="/app/index" replace /> },
      { path: 'reports', element: <Navigate to="/app/analytics" replace /> },
      { path: 'academy', element: <AcademyPage /> },
      { path: 'academy/articles/:slug', element: <ArticleDetailPage /> },
      { path: 'academy/trainings/:slug', element: <TrainingDetailPage /> },
      { path: 'academy/programs/:slug', element: <ProgramDetailPage /> },
      { path: 'profile', element: <ProfilePage /> },
    ],
  },
  { path: '*', element: <Navigate to="/login" replace /> },
])
