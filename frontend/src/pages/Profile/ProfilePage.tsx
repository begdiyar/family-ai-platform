import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { User, Users, Heart, Baby, Star, Plus, Trash2, Lock } from 'lucide-react'
import { useTranslation } from 'react-i18next'
import { AuthService } from '@/services/auth.service'
import { CoupleService } from '@/services/couple.service'
import { useAuthStore } from '@/store/auth.store'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { Button } from '@/components/ui/Button'
import { cn } from '@/lib/cn'
import type { Child, FamilyValue } from '@/types/domain.types'

// ── Shared helpers ────────────────────────────────────────────────────────────

const LANG_TO_INTL: Record<string, string> = {
  ru: 'ru',
  en: 'en',
  uz: 'uz',
}
const toIntlLocale = (lang: string) => LANG_TO_INTL[lang] ?? 'ru'

const cardStyle = {
  border: '1px solid rgba(232,227,218,0.6)',
  boxShadow: '0 1px 3px rgba(23,21,42,0.04), 0 6px 20px rgba(23,21,42,0.05)',
}

function SectionHeader({ icon: Icon, label }: { icon: React.ElementType; label: string }) {
  return (
    <div className="flex items-center gap-2 mb-4">
      <div className="flex h-7 w-7 items-center justify-center rounded-xl bg-primary/10">
        <Icon size={14} className="text-primary" />
      </div>
      <p className="label-caps text-muted">{label}</p>
    </div>
  )
}

function ScaleSelector({
  value,
  onChange,
  label,
  hint,
}: {
  value: number | null
  onChange: (v: number) => void
  label: string
  hint?: string
}) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-semibold text-ink/75">{label}</label>
      <div className="flex gap-2">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            className={cn(
              'h-10 w-10 rounded-xl text-sm font-bold border transition-all duration-150',
              value === n
                ? 'bg-primary text-white border-primary shadow-[0_2px_8px_rgba(60,56,136,0.35)]'
                : 'bg-canvas text-ink/60 border-sand hover:border-primary/40 hover:text-ink',
            )}
          >
            {n}
          </button>
        ))}
      </div>
      {hint && <p className="text-xs text-muted">{hint}</p>}
    </div>
  )
}

function NoCoupleNotice({ message }: { message: string }) {
  return (
    <p className="text-sm text-muted text-center py-3 px-4 rounded-xl bg-sand/30">
      {message}
    </p>
  )
}

// ── 1. Personal information ───────────────────────────────────────────────────

type PersonalForm = {
  first_name: string
  last_name: string
  birth_date: string
  gender: string
  native_language: string
  occupation: string
  education_level: string
}

function PersonalSection() {
  const { t, i18n } = useTranslation('profile')
  const qc = useQueryClient()
  const setUser = useAuthStore((s) => s.setUser)
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const schema = z.object({
    first_name: z.string().min(2, t('validation_name')),
    last_name: z.string(),
    birth_date: z.string(),
    gender: z.string(),
    native_language: z.string(),
    occupation: z.string(),
    education_level: z.string(),
  })

  const { register, handleSubmit, formState: { errors } } = useForm<PersonalForm>({
    resolver: zodResolver(schema),
    values: {
      first_name: me?.first_name ?? '',
      last_name: me?.last_name ?? '',
      birth_date: me?.birth_date ?? '',
      gender: me?.gender ?? '',
      native_language: me?.native_language ?? '',
      occupation: me?.occupation ?? '',
      education_level: me?.education_level ?? '',
    },
  })

  const mutation = useMutation({
    mutationFn: (data: PersonalForm) =>
      AuthService.updateMe({ ...data, birth_date: data.birth_date || null }),
    onSuccess: (user) => {
      setUser(user)
      qc.setQueryData(['me'], user)
      toast.success(t('toast_updated'))
    },
    onError: () => toast.error(t('toast_error')),
  })

  return (
    <form
      onSubmit={handleSubmit((d) => mutation.mutate(d))}
      className="rounded-[22px] bg-canvas p-5 flex flex-col gap-4"
      style={cardStyle}
    >
      <SectionHeader icon={User} label={t('section_personal')} />

      <div className="grid grid-cols-2 gap-3">
        <Input
          label={t('name_label')}
          placeholder={t('name_placeholder')}
          error={errors.first_name?.message}
          {...register('first_name')}
        />
        <Input
          label={t('last_name_label')}
          placeholder={t('last_name_placeholder')}
          {...register('last_name')}
        />
      </div>

      <Input
        label={t('birth_date_label')}
        type="date"
        max={new Date().toISOString().split('T')[0]}
        {...register('birth_date')}
      />

      <div className="grid grid-cols-2 gap-3">
        <Select label={t('gender_label')} {...register('gender')}>
          <option value="">{t('gender_empty')}</option>
          <option value="male">{t('gender_male')}</option>
          <option value="female">{t('gender_female')}</option>
          <option value="other">{t('gender_other')}</option>
          <option value="prefer_not_to_say">{t('gender_prefer_not')}</option>
        </Select>

        <Select label={t('education_label')} {...register('education_level')}>
          <option value="">{t('edu_empty')}</option>
          <option value="secondary">{t('edu_secondary')}</option>
          <option value="vocational">{t('edu_vocational')}</option>
          <option value="incomplete_higher">{t('edu_incomplete_higher')}</option>
          <option value="higher">{t('edu_higher')}</option>
          <option value="postgraduate">{t('edu_postgraduate')}</option>
        </Select>
      </div>

      <Input
        label={t('occupation_label')}
        placeholder={t('occupation_placeholder')}
        {...register('occupation')}
      />

      <Input
        label={t('native_language_label')}
        placeholder={t('native_language_placeholder')}
        maxLength={10}
        {...register('native_language')}
      />

      <Button type="submit" loading={mutation.isPending} fullWidth>
        {t('save_btn')}
      </Button>
    </form>
  )
}

// ── 2. Change password ────────────────────────────────────────────────────────

type PasswordForm = { current_password: string; new_password: string; confirm_password: string }

function PasswordSection() {
  const { t } = useTranslation('profile')

  const schema = z.object({
    current_password: z.string().min(1, t('pwd_current_required')),
    new_password: z.string().min(8, t('pwd_min_length')),
    confirm_password: z.string(),
  }).refine(d => d.new_password === d.confirm_password, {
    message: t('pwd_mismatch'),
    path: ['confirm_password'],
  })

  const { register, handleSubmit, reset, formState: { errors } } = useForm<PasswordForm>({
    resolver: zodResolver(schema),
  })

  const mutation = useMutation({
    mutationFn: (data: PasswordForm) =>
      AuthService.changePassword({ current_password: data.current_password, new_password: data.new_password }),
    onSuccess: () => { toast.success(t('pwd_changed')); reset() },
    onError: (e: any) => toast.error(e?.response?.data?.current_password?.[0] ?? t('toast_error')),
  })

  return (
    <form
      onSubmit={handleSubmit((d) => mutation.mutate(d))}
      className="rounded-[22px] bg-canvas p-5 flex flex-col gap-4"
      style={cardStyle}
    >
      <SectionHeader icon={Lock} label={t('section_password')} />
      <Input
        label={t('pwd_current_label')}
        type="password"
        placeholder="••••••••"
        error={errors.current_password?.message}
        {...register('current_password')}
      />
      <Input
        label={t('pwd_new_label')}
        type="password"
        placeholder="••••••••"
        error={errors.new_password?.message}
        {...register('new_password')}
      />
      <Input
        label={t('pwd_confirm_label')}
        type="password"
        placeholder="••••••••"
        error={errors.confirm_password?.message}
        {...register('confirm_password')}
      />
      <Button type="submit" loading={mutation.isPending} fullWidth>
        {t('pwd_save_btn')}
      </Button>
    </form>
  )
}

// ── 3. Settings (language hint) ───────────────────────────────────────────────
// Language is changed via the sidebar LanguageSwitcher and auto-saved to server.
// No separate form needed here.

// ── 3. Communication style ────────────────────────────────────────────────────

type CommForm = { conflict_style: string; support_style: string }

function CommunicationSection() {
  const { t } = useTranslation('profile')
  const { data: me } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const { register, handleSubmit } = useForm<CommForm>({
    values: {
      conflict_style: me?.communication_pref?.conflict_style ?? '',
      support_style: me?.communication_pref?.support_style ?? '',
    },
  })

  const mutation = useMutation({
    mutationFn: (data: CommForm) => AuthService.updateCommunicationPref(data),
    onSuccess: () => toast.success(t('toast_comm_updated')),
    onError: () => toast.error(t('toast_error')),
  })

  return (
    <form
      onSubmit={handleSubmit((d) => mutation.mutate(d))}
      className="rounded-[22px] bg-canvas p-5 flex flex-col gap-4"
      style={cardStyle}
    >
      <SectionHeader icon={Heart} label={t('section_communication')} />

      <Select label={t('conflict_style_label')} {...register('conflict_style')}>
        <option value="">{t('conflict_empty')}</option>
        <option value="avoidant">{t('conflict_avoidant')}</option>
        <option value="confrontational">{t('conflict_confrontational')}</option>
        <option value="collaborative">{t('conflict_collaborative')}</option>
        <option value="competitive">{t('conflict_competitive')}</option>
        <option value="compromising">{t('conflict_compromising')}</option>
      </Select>

      <Select label={t('support_style_label')} {...register('support_style')}>
        <option value="">{t('support_empty')}</option>
        <option value="advice">{t('support_advice')}</option>
        <option value="empathy">{t('support_empathy')}</option>
        <option value="practical">{t('support_practical')}</option>
        <option value="space">{t('support_space')}</option>
      </Select>

      <Button type="submit" loading={mutation.isPending} fullWidth>
        {t('save_btn')}
      </Button>
    </form>
  )
}

// ── 4. Relationship & family context ─────────────────────────────────────────

type RelForm = {
  relationship_status: string
  relationship_start_date: string
  marriage_date: string
}

function RelationshipSection() {
  const { t } = useTranslation('profile')
  const qc = useQueryClient()

  const { data: ctx } = useQuery({
    queryKey: ['couple-context'],
    queryFn: CoupleService.getFamilyContext,
  })

  const [livesWith, setLivesWith] = useState<boolean>(ctx?.lives_with_parents ?? false)
  const [relInfluence, setRelInfluence] = useState<number | null>(ctx?.relatives_influence_level ?? null)
  const [religiousImportance, setReligiousImportance] = useState<number | null>(
    ctx?.religious_traditions_importance ?? null,
  )

  const { register, handleSubmit } = useForm<RelForm>({
    values: {
      relationship_status: ctx?.relationship_status ?? '',
      relationship_start_date: ctx?.relationship_start_date ?? '',
      marriage_date: ctx?.marriage_date ?? '',
    },
  })

  const mutation = useMutation({
    mutationFn: (data: RelForm) =>
      CoupleService.updateFamilyContext({
        relationship_status: data.relationship_status || undefined,
        relationship_start_date: data.relationship_start_date || null,
        marriage_date: data.marriage_date || null,
        lives_with_parents: livesWith,
        relatives_influence_level: relInfluence,
        religious_traditions_importance: religiousImportance,
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['couple-context'] })
      qc.invalidateQueries({ queryKey: ['couple'] })
      toast.success(t('toast_context_updated'))
    },
    onError: () => toast.error(t('toast_error')),
  })

  return (
    <form
      onSubmit={handleSubmit((d) => mutation.mutate(d))}
      className="rounded-[22px] bg-canvas p-5 flex flex-col gap-4"
      style={cardStyle}
    >
      <SectionHeader icon={Heart} label={t('section_relationship')} />

      <Select label={t('relationship_status_label')} {...register('relationship_status')}>
        <option value="">{t('rel_empty')}</option>
        <option value="dating">{t('rel_dating')}</option>
        <option value="engaged">{t('rel_engaged')}</option>
        <option value="cohabitating">{t('rel_cohabitating')}</option>
        <option value="married">{t('rel_married')}</option>
        <option value="separated">{t('rel_separated')}</option>
      </Select>

      <div className="grid grid-cols-2 gap-3">
        <Input
          label={t('relationship_start_date_label')}
          type="date"
          max={new Date().toISOString().split('T')[0]}
          {...register('relationship_start_date')}
        />
        <Input
          label={t('marriage_date_label')}
          type="date"
          max={new Date().toISOString().split('T')[0]}
          {...register('marriage_date')}
        />
      </div>

      {/* ── Family context ─────────────────────────────────────── */}
      <div className="border-t border-sand/60 pt-4 flex flex-col gap-4">
        <p className="label-caps text-muted">{t('section_family_context')}</p>

        {/* lives_with_parents — toggle pills */}
        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-semibold text-ink/75">{t('lives_with_parents_label')}</label>
          <div className="flex gap-2">
            {([true, false] as const).map((val) => (
              <button
                key={String(val)}
                type="button"
                onClick={() => setLivesWith(val)}
                className={cn(
                  'px-5 py-2 rounded-full text-sm font-semibold border transition-all duration-150',
                  livesWith === val
                    ? 'bg-primary text-white border-primary shadow-[0_2px_8px_rgba(60,56,136,0.28)]'
                    : 'bg-canvas text-ink/60 border-sand hover:border-primary/40',
                )}
              >
                {val ? t('yes') : t('no')}
              </button>
            ))}
          </div>
        </div>

        <ScaleSelector
          value={relInfluence}
          onChange={setRelInfluence}
          label={t('relatives_influence_label')}
          hint={t('scale_hint')}
        />

        <ScaleSelector
          value={religiousImportance}
          onChange={setReligiousImportance}
          label={t('religious_importance_label')}
          hint={t('scale_hint')}
        />
      </div>

      <Button type="submit" loading={mutation.isPending} fullWidth>
        {t('save_btn')}
      </Button>
    </form>
  )
}

// ── 5. Children ───────────────────────────────────────────────────────────────

function ChildrenSection() {
  const { t, i18n } = useTranslation('profile')
  const qc = useQueryClient()
  const [adding, setAdding] = useState(false)
  const [birthDate, setBirthDate] = useState('')
  const [gender, setGender] = useState('')

  const { data: children = [] } = useQuery<Child[]>({
    queryKey: ['couple-children'],
    queryFn: CoupleService.getChildren,
  })

  const addMutation = useMutation({
    mutationFn: () => CoupleService.addChild({ birth_date: birthDate, gender }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['couple-children'] })
      qc.invalidateQueries({ queryKey: ['couple'] })
      setBirthDate('')
      setGender('')
      setAdding(false)
      toast.success(t('toast_child_added'))
    },
    onError: () => toast.error(t('toast_error')),
  })

  const removeMutation = useMutation({
    mutationFn: (id: string) => CoupleService.removeChild(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['couple-children'] })
      qc.invalidateQueries({ queryKey: ['couple'] })
      toast.success(t('toast_child_removed'))
    },
    onError: () => toast.error(t('toast_error')),
  })

  return (
    <div className="rounded-[22px] bg-canvas p-5 flex flex-col gap-4" style={cardStyle}>
      <SectionHeader icon={Baby} label={t('section_children')} />

      {children.length === 0 && !adding && (
        <p className="text-sm text-muted text-center py-2">{t('no_children')}</p>
      )}

      {children.map((child) => (
        <div
          key={child.id}
          className="flex items-center justify-between rounded-xl bg-surface px-4 py-3"
        >
          <div>
            <p className="text-sm font-semibold text-ink">
              {new Intl.DateTimeFormat(toIntlLocale(i18n.language), { day: 'numeric', month: 'long', year: 'numeric' }).format(
                new Date(child.birth_date),
              )}
            </p>
            <p className="text-xs text-muted mt-0.5">
              {child.gender === 'male'
                ? t('child_gender_male')
                : child.gender === 'female'
                ? t('child_gender_female')
                : t('child_gender_empty')}
            </p>
          </div>
          <button
            type="button"
            onClick={() => removeMutation.mutate(child.id)}
            disabled={removeMutation.isPending}
            className="h-8 w-8 flex items-center justify-center rounded-lg text-danger/60 hover:bg-danger/10 hover:text-danger transition-colors"
          >
            <Trash2 size={14} />
          </button>
        </div>
      ))}

      {adding && (
        <div className="rounded-xl border border-sand bg-surface/60 p-4 flex flex-col gap-3">
          <Input
            label={t('child_birth_date')}
            type="date"
            max={new Date().toISOString().split('T')[0]}
            value={birthDate}
            onChange={(e) => setBirthDate(e.target.value)}
          />
          <Select
            label={t('child_gender')}
            value={gender}
            onChange={(e) => setGender(e.target.value)}
          >
            <option value="">{t('child_gender_empty')}</option>
            <option value="male">{t('child_gender_male')}</option>
            <option value="female">{t('child_gender_female')}</option>
          </Select>
          <div className="flex gap-2">
            <Button
              type="button"
              size="sm"
              loading={addMutation.isPending}
              disabled={!birthDate}
              onClick={() => addMutation.mutate()}
            >
              {t('add_child_save')}
            </Button>
            <Button
              type="button"
              size="sm"
              variant="ghost"
              onClick={() => { setAdding(false); setBirthDate(''); setGender('') }}
            >
              {t('add_child_cancel')}
            </Button>
          </div>
        </div>
      )}

      {!adding && (
        <button
          type="button"
          onClick={() => setAdding(true)}
          className="flex items-center justify-center gap-2 h-10 rounded-xl border border-dashed border-primary/30 text-sm text-primary/70 hover:border-primary/60 hover:text-primary hover:bg-primary/5 transition-all"
        >
          <Plus size={14} />
          {t('add_child_btn')}
        </button>
      )}
    </div>
  )
}

// ── 6. Family values ──────────────────────────────────────────────────────────

function FamilyValuesSection() {
  const { t } = useTranslation('profile')
  const qc = useQueryClient()

  const { data: allValues = [] } = useQuery<FamilyValue[]>({
    queryKey: ['family-values-all'],
    queryFn: CoupleService.getAllFamilyValues,
  })

  const { data: selected = [] } = useQuery<FamilyValue[]>({
    queryKey: ['couple-family-values'],
    queryFn: CoupleService.getCoupleFamilyValues,
  })

  const selectedSlugs = new Set(selected.map((v) => v.slug))

  const mutation = useMutation({
    mutationFn: (slugs: string[]) => CoupleService.setFamilyValues(slugs),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['couple-family-values'] })
      qc.invalidateQueries({ queryKey: ['couple'] })
      toast.success(t('toast_values_updated'))
    },
    onError: () => toast.error(t('toast_error')),
  })

  const toggle = (slug: string) => {
    const next = new Set(selectedSlugs)
    if (next.has(slug)) next.delete(slug)
    else next.add(slug)
    mutation.mutate(Array.from(next))
  }

  return (
    <div className="rounded-[22px] bg-canvas p-5 flex flex-col gap-4" style={cardStyle}>
      <SectionHeader icon={Star} label={t('section_family_values')} />
      <p className="text-xs text-muted -mt-2">{t('family_values_hint')}</p>

      <div className="flex flex-wrap gap-2">
        {allValues.map((v) => {
          const active = selectedSlugs.has(v.slug)
          return (
            <button
              key={v.slug}
              type="button"
              onClick={() => toggle(v.slug)}
              disabled={mutation.isPending}
              className={cn(
                'px-3.5 py-1.5 rounded-full text-sm font-medium border transition-all duration-150',
                active
                  ? 'bg-primary text-white border-primary shadow-[0_2px_8px_rgba(60,56,136,0.28)]'
                  : 'bg-canvas text-ink/70 border-sand hover:border-primary/40 hover:text-primary',
              )}
            >
              {t(`fv_${v.slug}`)}
            </button>
          )
        })}
      </div>
    </div>
  )
}

// ── Main ProfilePage ──────────────────────────────────────────────────────────

export const ProfilePage = () => {
  const { t, i18n } = useTranslation('profile')

  const { data: me, isLoading } = useQuery({ queryKey: ['me'], queryFn: AuthService.getMe })

  const fullName = [me?.first_name, me?.last_name].filter(Boolean).join(' ')
  const memberSince = me?.created_at
    ? new Intl.DateTimeFormat(toIntlLocale(i18n.language), { month: 'long', year: 'numeric' }).format(
        new Date(me.created_at),
      )
    : ''

  const hasCouple = !!me?.couple?.id

  if (isLoading) {
    return (
      <div className="min-h-full bg-surface pb-24 md:pb-8">
        <div className="page-hero px-5 pt-6 pb-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-2xl shimmer" />
            <div className="h-6 w-32 rounded-xl shimmer" />
          </div>
        </div>
        <div className="px-4 pt-2 md:px-5 max-w-md space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 rounded-[22px] shimmer" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-full bg-surface pb-24 md:pb-8">

      {/* ── Header ──────────────────────────────────────────────── */}
      <div className="page-hero px-5 pt-6 pb-4">
        <div className="flex items-center gap-3">
          <div
            className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-brand"
            style={{ boxShadow: '0 4px 14px rgba(60,56,136,0.28)' }}
          >
            <User size={17} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-ink">{t('title')}</h1>
            <p className="text-xs text-muted mt-0.5">{t('subtitle')}</p>
          </div>
        </div>
      </div>

      <div className="px-4 pt-2 md:px-5 max-w-md space-y-4">

        {/* ── Profile summary card ─────────────────────────────── */}
        <div className="rounded-[22px] bg-canvas p-5" style={cardStyle}>
          <div className="flex items-center gap-4">
            <div
              className="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-gradient-brand text-2xl font-bold text-white"
              style={{ boxShadow: '0 4px 16px rgba(60,56,136,0.35)' }}
            >
              {me?.first_name?.[0]?.toUpperCase() ?? '?'}
            </div>
            <div className="min-w-0">
              <p className="font-bold text-ink leading-tight truncate">
                {fullName || me?.email}
              </p>
              <p className="text-sm text-muted truncate mt-0.5">{me?.email}</p>
              {memberSince && (
                <p className="text-xs text-muted/60 mt-1.5">
                  {t('member_since')} {memberSince}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* ── 1. Personal information ──────────────────────────── */}
        <PersonalSection />

        {/* ── 2. Change password ───────────────────────────────── */}
        <PasswordSection />

        {/* ── 3. Communication style ───────────────────────────── */}
        <CommunicationSection />

        {/* ── Couple-only sections ─────────────────────────────── */}
        {hasCouple ? (
          <>
            {/* ── 4. Relationship & family context ─────────────── */}
            <RelationshipSection />

            {/* ── 5. Children ──────────────────────────────────── */}
            <ChildrenSection />

            {/* ── 6. Family values ─────────────────────────────── */}
            <FamilyValuesSection />
          </>
        ) : (
          <div className="rounded-[22px] bg-canvas p-5" style={cardStyle}>
            <div className="flex items-center gap-2 mb-3">
              <div className="flex h-7 w-7 items-center justify-center rounded-xl bg-primary/10">
                <Users size={14} className="text-primary" />
              </div>
              <p className="label-caps text-muted">Для пары</p>
            </div>
            <NoCoupleNotice message={t('no_couple')} />
          </div>
        )}

      </div>
    </div>
  )
}
