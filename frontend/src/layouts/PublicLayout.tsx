import { Outlet } from 'react-router-dom'

export const PublicLayout = () => (
  <div className="min-h-screen bg-surface">
    <Outlet />
  </div>
)
