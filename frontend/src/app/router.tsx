import { createBrowserRouter, Navigate } from 'react-router-dom'
import { AppLayout } from '@/layouts/AppLayout'
import { PublicLayout } from '@/layouts/PublicLayout'
import { ProtectedRoute } from '@/lib/ProtectedRoute'
import { AdminRoute } from '@/lib/AdminRoute'
import { AdminRedirectGuard } from '@/lib/AdminRedirectGuard'

import { ProfileGuard } from '@/lib/ProfileGuard'
import { ProfileSetupPage } from '@/pages/Profile/ProfileSetupPage'

import { AdminLayout } from '@/pages/Admin/AdminLayout'
import { AdminDashboard } from '@/pages/Admin/AdminDashboard'
import { FamiliesPage } from '@/pages/Admin/FamiliesPage'
import { FamilyDetailPage } from '@/pages/Admin/FamilyDetailPage'
import { ProblemsPage } from '@/pages/Admin/ProblemsPage'
import { AdminStatisticsPage } from '@/pages/Admin/AdminStatisticsPage'
import { AdminExportPage } from '@/pages/Admin/AdminExportPage'
import { AdminSettingsPage } from '@/pages/Admin/AdminSettingsPage'

import { LoginPage } from '@/pages/Auth/LoginPage'
import { RegisterPage } from '@/pages/Auth/RegisterPage'
import { InviteAcceptPage } from '@/pages/Auth/InviteAcceptPage'
import { DashboardPage } from '@/pages/Dashboard/DashboardPage'
import { CouplePage } from '@/pages/Couple/CouplePage'
import { DiagnosticsPage } from '@/pages/Diagnostics/DiagnosticsPage'
import { DiagnosticsStartPage } from '@/pages/Diagnostics/DiagnosticsStartPage'
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
  // ── Public routes ────────────────────────────────────────────────
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      { index: true, element: <Navigate to="/login" replace /> },
      { path: 'login',           element: <LoginPage /> },
      { path: 'register',        element: <RegisterPage /> },
      { path: 'invite/:token',   element: <InviteAcceptPage /> },
    ],
  },

  // ── Profile setup (protected, no app layout) ─────────────────────
  {
    path: '/setup',
    element: (
      <ProtectedRoute>
        <ProfileSetupPage />
      </ProtectedRoute>
    ),
  },

  // ── User app (regular users) ─────────────────────────────────────
  {
    path: '/app',
    element: (
      <ProtectedRoute>
        <AdminRedirectGuard>
          <ProfileGuard>
            <AppLayout />
          </ProfileGuard>
        </AdminRedirectGuard>
      </ProtectedRoute>
    ),
    children: [
      { index: true,                                element: <DashboardPage /> },
      { path: 'couple',                             element: <CouplePage /> },
      { path: 'diagnostics',                        element: <DiagnosticsPage /> },
      { path: 'diagnostics/start',                  element: <DiagnosticsStartPage /> },
      { path: 'analytics',                          element: <Navigate to="/app/index" replace /> },
      { path: 'analytics/:resultId',                element: <Navigate to="/app/index" replace /> },
      { path: 'ai',                                 element: <AIChatPage /> },
      { path: 'ai/:convId',                         element: <AIChatPage /> },
      { path: 'plan',                               element: <Navigate to="/app/practices" replace /> },
      { path: 'practices',                          element: <PracticesPage /> },
      { path: 'mediation',                          element: <MediationPage /> },
      { path: 'constitution',                       element: <Navigate to="/app/index" replace /> },
      { path: 'index',                              element: <RelationshipIndexPage /> },
      { path: 'bridge',                             element: <Navigate to="/app/index" replace /> },
      { path: 'reports',                             element: <Navigate to="/app/index" replace /> },
      { path: 'academy',                            element: <AcademyPage /> },
      { path: 'academy/articles/:slug',             element: <ArticleDetailPage /> },
      { path: 'academy/trainings/:slug',            element: <TrainingDetailPage /> },
      { path: 'academy/programs/:slug',             element: <ProgramDetailPage /> },
      { path: 'profile',                            element: <ProfilePage /> },
    ],
  },

  // ── Admin panel (staff / superuser only) ─────────────────────────
  {
    path: '/admin',
    element: <AdminRoute><AdminLayout /></AdminRoute>,
    children: [
      { index: true,                 element: <AdminDashboard /> },
      { path: 'families',            element: <FamiliesPage /> },
      { path: 'families/:id',        element: <FamilyDetailPage /> },
      { path: 'problems',            element: <ProblemsPage /> },
      { path: 'statistics',          element: <AdminStatisticsPage /> },
      { path: 'export',              element: <AdminExportPage /> },
      { path: 'settings',            element: <AdminSettingsPage /> },
    ],
  },

  { path: '*', element: <Navigate to="/login" replace /> },
])
