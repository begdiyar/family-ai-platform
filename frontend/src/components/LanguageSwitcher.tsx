import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Globe } from 'lucide-react'
import { SUPPORTED_LANGS, type LangCode } from '@/i18n'
import { cn } from '@/lib/cn'

export const LanguageSwitcher = ({ compact = false }: { compact?: boolean }) => {
  const { i18n } = useTranslation()
  const [open, setOpen] = useState(false)

  const current = SUPPORTED_LANGS.find((l) => l.code === i18n.language) ?? SUPPORTED_LANGS[0]

  const handleChange = (code: LangCode) => {
    i18n.changeLanguage(code)
    setOpen(false)
  }

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className={cn(
          'flex items-center gap-1.5 rounded-[12px] px-2.5 py-1.5 text-xs font-bold transition-all duration-150',
          'text-muted hover:bg-surface hover:text-ink',
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
            className="absolute bottom-full left-0 z-50 mb-1 min-w-[140px] rounded-[16px] bg-white py-1.5 shadow-[0_8px_32px_rgba(23,21,42,0.14)] border border-sand/60"
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
