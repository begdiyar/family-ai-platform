import { HTMLAttributes } from 'react'
import { cn } from '@/lib/cn'

type Props = HTMLAttributes<HTMLDivElement> & {
  hover?: boolean
  glass?: boolean
  gradient?: boolean
  tinted?: 'lavender' | 'sage' | 'blush' | 'sky'
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

const tints = {
  lavender: 'bg-gradient-to-br from-primary-50 to-violet-light border-primary-100/60',
  sage:     'bg-gradient-to-br from-sage-50 to-primary-50 border-sage-100/60',
  blush:    'bg-gradient-to-br from-accent-light to-primary-50 border-accent/20',
  sky:      'bg-gradient-to-br from-violet-light to-primary-50 border-violet/20',
}

const paddings = {
  none: 'p-0',
  sm:   'p-4',
  md:   'p-6',
  lg:   'p-8',
}

export const Card = ({
  hover,
  glass,
  gradient,
  tinted,
  padding = 'md',
  className,
  children,
  ...props
}: Props) => (
  <div
    className={cn(
      'rounded-card border border-sand/60 bg-canvas shadow-card',
      paddings[padding],
      hover && 'cursor-pointer transition-all duration-[220ms] ease-spring hover:shadow-hover hover:-translate-y-1',
      glass && 'glass border-white/60',
      gradient && 'bg-gradient-rose border-primary-100/40',
      tinted && tints[tinted],
      className,
    )}
    {...props}
  >
    {children}
  </div>
)
