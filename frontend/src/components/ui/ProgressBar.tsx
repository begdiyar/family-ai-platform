import { cn } from '@/lib/cn'

type Props = {
  value: number
  className?: string
  color?: 'primary' | 'violet' | 'accent' | 'success' | 'warning' | 'danger' | string
  label?: string
  showValue?: boolean
  size?: 'xs' | 'sm' | 'md' | 'lg'
}

const colorMap: Record<string, string> = {
  primary: 'bg-gradient-brand',    // lavender→sky
  violet:  'bg-gradient-violet',   // sky→lavender
  accent:  'bg-gradient-peach',    // terracotta→lavender
  success: 'bg-gradient-sage',     // sage→sky
  warning: 'bg-gradient-gold',     // amber→blush
  danger:  'bg-danger',
}

const heights: Record<string, string> = {
  xs: 'h-1',
  sm: 'h-1.5',
  md: 'h-2.5',
  lg: 'h-3.5',
}

export const ProgressBar = ({
  value,
  className,
  color = 'primary',
  label,
  showValue,
  size = 'md',
}: Props) => {
  const fill = colorMap[color] ?? color
  const pct = Math.min(100, Math.max(0, value))
  return (
    <div className={cn('w-full', className)}>
      {(label || showValue) && (
        <div className="mb-1.5 flex justify-between text-xs font-semibold text-muted">
          {label && <span>{label}</span>}
          {showValue && <span>{Math.round(pct)}%</span>}
        </div>
      )}
      <div className={cn(
        'w-full overflow-hidden rounded-full',
        heights[size],
        // Тёплый бежевый трек вместо холодного серого
        'bg-sand/70',
      )}>
        <div
          className={cn('h-full rounded-full transition-all duration-700 ease-out', fill)}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
