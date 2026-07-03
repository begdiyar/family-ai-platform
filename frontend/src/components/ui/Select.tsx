import { SelectHTMLAttributes, forwardRef } from 'react'
import { ChevronDown } from 'lucide-react'
import { cn } from '@/lib/cn'

type SelectProps = {
  label?: string
  error?: string
  hint?: string
} & SelectHTMLAttributes<HTMLSelectElement>

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, hint, className, children, ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm font-semibold text-ink/75">{label}</label>
      )}
      <div className="relative">
        <select
          ref={ref}
          className={cn(
            'w-full appearance-none rounded-input border outline-none transition-all duration-200',
            'border-sand bg-canvas text-ink',
            'focus:border-primary/50 focus:bg-canvas focus:shadow-[0_0_0_3px_rgba(60,56,136,0.18)]',
            'h-12 px-4 pr-10 text-sm cursor-pointer',
            error && 'border-danger/50 focus:border-danger focus:shadow-[0_0_0_3px_rgba(132,48,72,0.18)]',
            className,
          )}
          {...props}
        >
          {children}
        </select>
        <ChevronDown
          size={15}
          className="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-muted/60"
        />
      </div>
      {hint && !error && <p className="text-xs text-muted">{hint}</p>}
      {error && <p className="text-xs font-semibold text-danger">{error}</p>}
    </div>
  )
)
Select.displayName = 'Select'
