import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/cn'

type Variant = 'primary' | 'secondary' | 'ghost' | 'accent' | 'danger' | 'violet'
type Size = 'sm' | 'md' | 'lg'

type Props = {
  variant?: Variant
  size?: Size
  loading?: boolean
  fullWidth?: boolean
} & ButtonHTMLAttributes<HTMLButtonElement>

const variants: Record<Variant, string> = {
  primary:
    'bg-gradient-brand text-white shadow-[0_4px_16px_rgba(60,56,136,0.36)] hover:shadow-[0_6px_24px_rgba(60,56,136,0.46)] hover:brightness-110 active:scale-[0.97]',
  secondary:
    'bg-primary-50 text-primary-700 border border-primary-100 hover:bg-primary-100 active:scale-[0.97]',
  ghost:
    'bg-canvas border border-sand text-muted hover:border-primary-100 hover:text-primary-700 hover:bg-primary-50 active:scale-[0.97]',
  accent:
    'bg-gradient-peach text-white shadow-[0_4px_16px_rgba(136,80,64,0.34)] hover:brightness-110 active:scale-[0.97]',
  danger:
    'bg-danger text-white shadow-[0_4px_14px_rgba(132,48,72,0.34)] hover:brightness-110 active:scale-[0.97]',
  violet:
    'bg-gradient-violet text-white shadow-[0_4px_16px_rgba(56,92,138,0.34)] hover:brightness-110 active:scale-[0.97]',
}

const sizes: Record<Size, string> = {
  sm: 'h-8 px-4 text-xs gap-1.5 rounded-pill',
  md: 'h-10 px-5 text-sm gap-2 rounded-btn',
  lg: 'h-13 px-7 text-[15px] gap-2 rounded-btn',
}

export const Button = forwardRef<HTMLButtonElement, Props>(({
  variant = 'primary',
  size = 'md',
  loading,
  fullWidth,
  children,
  className,
  disabled,
  ...props
}, ref) => (
  <button
    ref={ref}
    className={cn(
      'inline-flex items-center justify-center font-semibold transition-all duration-200',
      'disabled:opacity-50 disabled:cursor-not-allowed select-none',
      variants[variant],
      sizes[size],
      fullWidth && 'w-full',
      className,
    )}
    disabled={loading || disabled}
    {...props}
  >
    {loading ? (
      <span className="h-4 w-4 rounded-full border-2 border-current/25 border-t-current animate-spin" />
    ) : children}
  </button>
))
Button.displayName = 'Button'
