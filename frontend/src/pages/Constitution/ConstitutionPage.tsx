import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { motion } from 'framer-motion'
import { ScrollText, Sparkles, Pencil, Check, X, Plus } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { ConstitutionService } from '@/services/constitution.service'
import { Card } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { EmptyState } from '@/components/feedback/EmptyState'
import type { FamilyConstitution } from '@/types/domain.types'

const ease: [number, number, number, number] = [0.16, 1, 0.3, 1]

type SectionStatic = {
  key: keyof Omit<FamilyConstitution, 'id' | 'is_ai_generated' | 'updated_at'>
  icon: string
  bg: string
  accent: string
  dotHex: string
}

type Section = SectionStatic & { label: string; placeholder: string }

const SECTION_STATICS: SectionStatic[] = [
  { key: 'values',              icon: '🌟', bg: 'linear-gradient(135deg, #FDF4E8 0%, #E8E2D4 100%)', accent: '#886028', dotHex: '#886028' },
  { key: 'goals',               icon: '🎯', bg: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)', accent: '#385C8A', dotHex: '#385C8A' },
  { key: 'communication_rules', icon: '💬', bg: 'linear-gradient(135deg, #EDEAF8 0%, #EEE4DC 100%)', accent: '#3C3888', dotHex: '#3C3888' },
  { key: 'conflict_rules',      icon: '⚖️', bg: 'linear-gradient(135deg, #DDE8F2 0%, #EDEAF8 100%)', accent: '#385C8A', dotHex: '#385C8A' },
  { key: 'finance_principles',  icon: '💰', bg: 'linear-gradient(135deg, #E2EDE8 0%, #DDE8F2 100%)', accent: '#386858', dotHex: '#386858' },
  { key: 'parenting_approach',  icon: '👨‍👩‍👧', bg: 'linear-gradient(135deg, #EEE4DC 0%, #FDF4E8 100%)', accent: '#885040', dotHex: '#885040' },
]

export const ConstitutionPage = () => {
  const qc = useQueryClient()
  const navigate = useNavigate()
  const { t, i18n } = useTranslation('common')
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState<Record<string, string[]>>({})

  const dateLocale = i18n.language === 'en' ? 'en-US' : 'ru-RU'

  const sections: Section[] = SECTION_STATICS.map((s) => ({
    ...s,
    label: t(`constitution_${s.key}_label`, {
      defaultValue: {
        values: 'Семейные ценности',
        goals: 'Цели и мечты',
        communication_rules: 'Правила общения',
        conflict_rules: 'Правила конфликтов',
        finance_principles: 'Финансовые принципы',
        parenting_approach: 'Подход к воспитанию',
      }[s.key] ?? s.key,
    }),
    placeholder: t(`constitution_${s.key}_placeholder`, {
      defaultValue: {
        values: 'Что важно для нашей семьи...',
        goals: 'Куда мы движемся вместе...',
        communication_rules: 'Как мы говорим друг с другом...',
        conflict_rules: 'Как мы разрешаем разногласия...',
        finance_principles: 'Как мы управляем деньгами...',
        parenting_approach: 'Наши принципы воспитания...',
      }[s.key] ?? '',
    }),
  }))

  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })
  const { data: constitution, isLoading } = useQuery({
    queryKey: ['constitution'],
    queryFn: ConstitutionService.get,
    enabled: me?.couple?.status === 'active',
    retry: false,
  })

  const generateMutation = useMutation({
    mutationFn: ConstitutionService.generateWithAI,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['constitution'] })
      toast.success(t('constitution_generated', { defaultValue: 'Конституция сгенерирована AI' }))
    },
    onError: () => toast.error(t('constitution_generate_error', { defaultValue: 'Ошибка генерации' })),
  })

  const saveMutation = useMutation({
    mutationFn: () => ConstitutionService.update(draft as any),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['constitution'] })
      setEditing(false)
      toast.success(t('constitution_saved', { defaultValue: 'Конституция сохранена' }))
    },
    onError: () => toast.error(t('constitution_save_error', { defaultValue: 'Ошибка сохранения' })),
  })

  const startEditing = (c: FamilyConstitution) => {
    const d: Record<string, string[]> = {}
    sections.forEach((s) => { d[s.key] = [...(c[s.key] as string[])] })
    setDraft(d)
    setEditing(true)
  }

  if (me?.couple?.status === 'pending') {
    return (
      <div className="p-6">
        <EmptyState
          icon={<ScrollText />}
          title={t('pending_couple_title')}
          description={t('invite_partner_first')}
          actionLabel={t('invite_partner_btn')}
          onAction={() => navigate('/app/couple')}
        />
      </div>
    )
  }

  if (!me?.couple) {
    return (
      <div className="p-6">
        <EmptyState
          icon={<ScrollText />}
          title={t('constitution_no_couple_title', { defaultValue: 'Сначала создайте пару' })}
          description={t('constitution_no_couple_desc', { defaultValue: 'Конституция доступна только для пары' })}
        />
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">
      {/* Header */}
      <div className="page-hero px-5 pt-6 pb-5">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div
              className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
              style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
            >
              <ScrollText size={17} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-ink">{t('constitution_title', { defaultValue: 'Семейная конституция' })}</h1>
              <p className="text-xs text-muted mt-0.5">{t('constitution_subtitle', { defaultValue: 'Совместные правила и ценности' })}</p>
            </div>
          </div>
          {constitution && !editing && (
            <Button size="sm" variant="secondary" onClick={() => startEditing(constitution)}>
              <Pencil size={14} /> {t('constitution_edit_btn', { defaultValue: 'Изменить' })}
            </Button>
          )}
        </div>
      </div>

      <div className="px-4 pt-4 md:px-5 max-w-2xl">
        {isLoading ? (
          <div className="flex flex-col gap-4">
            {[...Array(6)].map((_, i) => <div key={i} className="h-32 rounded-card shimmer" />)}
          </div>
        ) : !constitution || sections.every(s => !(constitution[s.key] as string[])?.length) ? (
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, ease }}>
            <div
              className="mb-5 rounded-[22px] p-5"
              style={{
                background: 'linear-gradient(145deg, #DAD6EE 0%, #D2DDF0 50%, #D6E8E2 100%)',
                border: '1px solid rgba(60,56,136,0.12)',
              }}
            >
              <div className="flex gap-4">
                <span className="text-3xl shrink-0">📜</span>
                <div>
                  <p className="font-bold text-ink">{t('constitution_doc_title', { defaultValue: 'Документ ваших правил' })}</p>
                  <p className="mt-1 text-sm text-muted leading-relaxed">
                    {t('constitution_doc_desc', { defaultValue: 'Конституция — живой документ: ценности, цели, правила общения и многое другое. AI создаст первую версию на основе вашей диагностики.' })}
                  </p>
                </div>
              </div>
            </div>
            <Button fullWidth onClick={() => generateMutation.mutate()} loading={generateMutation.isPending}>
              <Sparkles size={16} /> {t('constitution_generate_btn', { defaultValue: 'Создать конституцию с AI' })}
            </Button>
          </motion.div>
        ) : editing ? (
          <EditView
            sections={sections}
            draft={draft}
            setDraft={setDraft}
            onSave={() => saveMutation.mutate()}
            onCancel={() => setEditing(false)}
            saving={saveMutation.isPending}
          />
        ) : (
          <ViewMode
            sections={sections}
            constitution={constitution}
            dateLocale={dateLocale}
            onGenerate={() => generateMutation.mutate()}
            generating={generateMutation.isPending}
          />
        )}
      </div>
    </div>
  )
}

const ViewMode = ({ sections, constitution, dateLocale, onGenerate, generating }: {
  sections: Section[]
  constitution: FamilyConstitution
  dateLocale: string
  onGenerate: () => void
  generating: boolean
}) => {
  const { t } = useTranslation('common')
  return (
    <div className="flex flex-col gap-3">
      {constitution.is_ai_generated && (
        <div className="flex items-center gap-2 rounded-2xl px-4 py-2.5" style={{ background: '#DDE8F2' }}>
          <Sparkles size={14} className="text-violet" />
          <span className="text-xs font-medium text-violet">{t('constitution_ai_badge', { defaultValue: 'Создана AI на основе диагностики' })}</span>
          <span className="ml-auto text-xs text-muted">
            {new Date(constitution.updated_at).toLocaleDateString(dateLocale)}
          </span>
        </div>
      )}

      {sections.map((section, idx) => {
        const items = constitution[section.key] as string[]
        if (!items?.length) return null
        return (
          <motion.div
            key={section.key}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease, delay: idx * 0.05 }}
            className="rounded-[20px] p-5"
            style={{ background: section.bg, border: '1px solid rgba(232,227,218,0.5)' }}
          >
            <div className="mb-3 flex items-center gap-2.5">
              <span className="text-xl select-none">{section.icon}</span>
              <h2 className="font-bold text-sm" style={{ color: section.accent }}>{section.label}</h2>
            </div>
            <ul className="flex flex-col gap-2">
              {items.map((item, i) => (
                <li key={i} className="flex items-start gap-2.5 text-sm text-ink leading-relaxed">
                  <span
                    className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full"
                    style={{ background: section.dotHex }}
                  />
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
        )
      })}

      <Button variant="secondary" onClick={onGenerate} loading={generating} fullWidth>
        <Sparkles size={15} /> {t('constitution_update_btn', { defaultValue: 'Обновить с AI' })}
      </Button>
    </div>
  )
}

const EditView = ({ sections, draft, setDraft, onSave, onCancel, saving }: {
  sections: Section[]
  draft: Record<string, string[]>
  setDraft: (d: Record<string, string[]>) => void
  onSave: () => void
  onCancel: () => void
  saving: boolean
}) => {
  const { t } = useTranslation('common')

  const updateItem = (key: string, index: number, value: string) => {
    const nd = { ...draft, [key]: [...(draft[key] ?? [])] }
    nd[key][index] = value
    setDraft(nd)
  }

  const addItem = (key: string) => setDraft({ ...draft, [key]: [...(draft[key] ?? []), ''] })

  const removeItem = (key: string, index: number) =>
    setDraft({ ...draft, [key]: draft[key].filter((_, i) => i !== index) })

  return (
    <div className="flex flex-col gap-4">
      {sections.map((section) => (
        <Card key={section.key}>
          <div className="mb-3 flex items-center gap-2.5">
            <span className="text-xl">{section.icon}</span>
            <h2 className="font-bold text-ink">{section.label}</h2>
          </div>
          <div className="flex flex-col gap-2">
            {(draft[section.key] ?? []).map((item, i) => (
              <div key={i} className="flex gap-2">
                <Input
                  value={item}
                  placeholder={section.placeholder}
                  onChange={(e) => updateItem(section.key, i, e.target.value)}
                  className="h-10 text-sm"
                />
                <button
                  onClick={() => removeItem(section.key, i)}
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-input border border-gray-200 text-muted hover:border-danger/50 hover:text-danger transition-colors"
                >
                  <X size={15} />
                </button>
              </div>
            ))}
            <button
              onClick={() => addItem(section.key)}
              className="mt-1 flex items-center gap-1.5 text-xs font-semibold text-primary hover:underline"
            >
              <Plus size={13} /> {t('constitution_add_item', { defaultValue: 'Добавить' })}
            </button>
          </div>
        </Card>
      ))}

      <div className="flex gap-3">
        <Button variant="ghost" fullWidth onClick={onCancel}><X size={15} /> {t('btn.cancel', { defaultValue: 'Отмена' })}</Button>
        <Button fullWidth onClick={onSave} loading={saving}><Check size={15} /> {t('btn.save', { defaultValue: 'Сохранить' })}</Button>
      </div>
    </div>
  )
}
