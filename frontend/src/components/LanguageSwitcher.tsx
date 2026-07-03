import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Globe } from 'lucide-react'
import { useQueryClient } from '@tanstack/react-query'
import { SUPPORTED_LANGS, type LangCode } from '@/i18n'
import { cn } from '@/lib/cn'
import { useAuthStore } from '@/store/auth.store'
import { AuthService } from '@/services/auth.service'

export const LanguageSwitcher = ({
  compact = false,
  dropDirection = 'up',
  dark = false,
}: {
  compact?: boolean
  dropDirection?: 'up' | 'down'
  dark?: boolean
}) => {
  const { i18n } = useTranslation()
  const [open, setOpen] = useState(false)
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  const setUser = useAuthStore((s) => s.setUser)
  const queryClient = useQueryClient()

  const current = SUPPORTED_LANGS.find((l) => l.code === i18n.language) ?? SUPPORTED_LANGS[0]

  const handleChange = async (code: LangCode) => {
    i18n.changeLanguage(code)
    setOpen(false)
    if (isAuthenticated) {
      try {
        const user = await AuthService.updateMe({ preferred_language: code })
        setUser(user)
        // Invalidate all queries — X-Language header is already updated in the
        // axios interceptor, so every refetch returns content in the new language
        await queryClient.invalidateQueries()
      } catch {
        // silent — UI language already changed locally
      }
    }
  }

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className={cn(
          'flex items-center gap-1.5 rounded-[12px] px-2.5 py-1.5 text-xs font-bold transition-all duration-150',
          dark
            ? 'text-[#9B99C8] hover:bg-white/10 hover:text-white'
            : 'text-muted hover:bg-surface hover:text-ink',
        )}
        aria-label="Change language"
      >
        {compact ? (
          <Globe size={15} />
        ) : (
          <>
            <Globe size={13} />
            <span>{current.label}</span>
          </>
        )}
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div
            className={cn(
              'absolute z-50 min-w-[140px] rounded-[16px] bg-white py-1.5 shadow-[0_8px_32px_rgba(23,21,42,0.14)] border border-sand/60',
              dropDirection === 'down' ? 'top-full left-0 mt-1' : 'bottom-full left-0 mb-1',
            )}
          >
            {SUPPORTED_LANGS.map((lang) => (
              <button
                key={lang.code}
                onClick={() => handleChange(lang.code)}
                className={cn(
                  'flex w-full items-center gap-2.5 px-3.5 py-2 text-sm font-medium transition-colors',
                  i18n.language === lang.code
                    ? 'text-primary bg-primary-50'
                    : 'text-ink hover:bg-surface',
                )}
              >
                <span className="w-8 text-[11px] font-bold text-muted">{lang.label}</span>
                <span>{lang.name}</span>
                {i18n.language === lang.code && (
                  <span className="ml-auto h-1.5 w-1.5 rounded-full bg-primary" />
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
