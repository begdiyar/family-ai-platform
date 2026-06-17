import { ReactNode } from 'react'
import { Button } from '@/components/ui/Button'

type Props = {
  icon?: ReactNode
  title: string
  description: string
  actionLabel?: string
  onAction?: () => void
}

export const EmptyState = ({ icon, title, description, actionLabel, onAction }: Props) => (
  <div className="flex flex-col items-center justify-center py-16 text-center">
    {/* Lavender orb — спокойный, не кричащий */}
    <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-primary-50 to-violet-light shadow-soft border border-primary-100/60">
      {icon ? (
        <span className="text-primary [&>svg]:h-9 [&>svg]:w-9">{icon}</span>
      ) : (
        <span className="text-3xl">🌿</span>
      )}
    </div>
    <h3 className="mb-2 text-lg font-bold text-ink">{title}</h3>
    <p className="mb-6 max-w-xs text-sm leading-relaxed text-muted">{description}</p>
    {actionLabel && onAction && (
      <Button onClick={onAction} variant="secondary">{actionLabel}</Button>
    )}
  </div>
)
