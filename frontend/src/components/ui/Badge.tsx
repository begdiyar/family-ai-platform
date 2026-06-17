import { cn } from '@/lib/cn'

type Variant = 'success' | 'warning' | 'danger' | 'primary' | 'violet' | 'gray' | 'accent'

const variants: Record<Variant, string> = {
  // Sage green — успех, рост
  success: 'bg-sage-50 text-sage-700 border border-sage-100',
  // Amber — внимание
  warning: 'bg-amber-50 text-amber-700 border border-amber-200',
  // Muted red — критично
  danger:  'bg-rose-50 text-rose-700 border border-rose-200',
  // Lavender — основной бренд
  primary: 'bg-primary-50 text-primary-700 border border-primary-100',
  // Sky blue — спокойствие
  violet:  'bg-violet-light text-violet-700 border border-violet/20',
  // Blush — тепло
  accent:  'bg-accent-light text-accent-700 border border-accent/25',
  // Neutral gray
  gray:    'bg-gray-100 text-gray-600 border border-gray-200',
}

export const Badge = ({
  variant = 'gray',
  children,
  className,
}: {
  variant?: Variant
  children: React.ReactNode
  className?: string
}) => (
  <span className={cn(
    'inline-flex items-center rounded-pill px-2.5 py-0.5 text-xs font-semibold',
    variants[variant],
    className,
  )}>
    {children}
  </span>
)
