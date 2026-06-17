import { InputHTMLAttributes, TextareaHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/cn'

const baseInputCls = [
  'w-full rounded-input border outline-none transition-all duration-200',
  'border-sand bg-canvas text-ink placeholder:text-muted/50',
  'focus:border-primary/50 focus:bg-canvas focus:shadow-[0_0_0_3px_rgba(60,56,136,0.18)]',
].join(' ')

type InputProps = {
  label?: string
  error?: string
  hint?: string
} & InputHTMLAttributes<HTMLInputElement>

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, className, ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm font-semibold text-ink/75">{label}</label>
      )}
      <input
        ref={ref}
        className={cn(
          baseInputCls,
          'h-12 px-4 text-sm',
          error && 'border-danger/50 focus:border-danger focus:shadow-[0_0_0_3px_rgba(132,48,72,0.18)]',
          className,
        )}
        {...props}
      />
      {hint && !error && <p className="text-xs text-muted">{hint}</p>}
      {error && <p className="text-xs font-semibold text-danger">{error}</p>}
    </div>
  )
)
Input.displayName = 'Input'

type TextareaProps = {
  label?: string
  error?: string
  hint?: string
} & TextareaHTMLAttributes<HTMLTextAreaElement>

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, hint, className, ...props }, ref) => (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm font-semibold text-ink/75">{label}</label>
      )}
      <textarea
        ref={ref}
        className={cn(
          baseInputCls,
          'px-4 py-3 text-sm resize-none',
          error && 'border-danger/50 focus:border-danger focus:shadow-[0_0_0_3px_rgba(132,48,72,0.18)]',
          className,
        )}
        {...props}
      />
      {hint && !error && <p className="text-xs text-muted">{hint}</p>}
      {error && <p className="text-xs font-semibold text-danger">{error}</p>}
    </div>
  )
)
Textarea.displayName = 'Textarea'
