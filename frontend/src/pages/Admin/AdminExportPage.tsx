import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { Download, FileSpreadsheet, CheckCircle2, AlertCircle } from 'lucide-react'
import { AdminService } from '@/services/admin.service'
import * as XLSX from 'xlsx'

const CRISIS_LABELS: Record<string, Record<string, string>> = {
  ru: { none: 'Норма', warning: 'Внимание', critical: 'Кризис' },
  uz: { none: 'Normal', warning: 'Diqqat',  critical: 'Inqiroz' },
  en: { none: 'Normal', warning: 'Warning',  critical: 'Crisis'  },
}

const LEVEL_NAMES: Record<string, Record<number, string>> = {
  ru: {
    1: 'Основа отношений', 2: 'Коммуникация',  3: 'Доверие',
    4: 'Эм. близость',     5: 'Конфликты',     6: 'Романтика',
    7: 'Финансы',          8: 'Родственники',  9: 'Дети',
    10: 'Будущее семьи',
  },
  uz: {
    1: 'Munosabat asosi',  2: 'Muloqot',       3: 'Ishonch',
    4: 'Hissiy yaqinlik',  5: 'Nizolar',       6: 'Romantika',
    7: 'Moliya',           8: 'Qarindoshlar',  9: 'Bolalar',
    10: 'Oila kelajagi',
  },
  en: {
    1: 'Relationship base', 2: 'Communication', 3: 'Trust',
    4: 'Emotional closeness', 5: 'Conflicts',   6: 'Romance',
    7: 'Finances',           8: 'Relatives',    9: 'Children',
    10: 'Family future',
  },
}

export const AdminExportPage = () => {
  const { t, i18n } = useTranslation('admin')
  const lang = (i18n.language || 'ru').split('-')[0] as 'ru' | 'uz' | 'en'
  const [exportStatus, setExportStatus] = useState<'idle' | 'loading' | 'done' | 'error'>('idle')

  const { data: overview } = useQuery({
    queryKey: ['admin-overview'],
    queryFn: AdminService.getOverview,
    staleTime: 60_000,
  })

  const crisisLabels = CRISIS_LABELS[lang] ?? CRISIS_LABELS.ru
  const levelNames   = LEVEL_NAMES[lang]   ?? LEVEL_NAMES.ru

  const exportXLSX = async () => {
    setExportStatus('loading')
    try {
      const data = await AdminService.getExportData()
      const levels = data.level_numbers
      const wb = XLSX.utils.book_new()

      // ── Sheet 1: Families ─────────────────────────────────────
      const colHeaders: Record<string, string> = {
        ru: { aFirst: 'Имя (А)', aLast: 'Фамилия (А)', aPhone: 'Телефон (А)',
              bFirst: 'Имя (Б)', bLast: 'Фамилия (Б)', bPhone: 'Телефон (Б)',
              date:   'Дата регистрации', total: 'Всего диагностик',
              prac:   'Практик выполнено', score: 'Индекс отношений', status: 'Статус' },
        uz:  { aFirst: 'Ism (A)', aLast: 'Familiya (A)', aPhone: 'Telefon (A)',
              bFirst: 'Ism (B)', bLast: 'Familiya (B)', bPhone: 'Telefon (B)',
              date:   'Ro\'yxatdan o\'tgan sana', total: 'Jami diagnostika',
              prac:   'Bajarilgan amaliyotlar', score: 'Munosabat indeksi', status: 'Holat' },
        en:  { aFirst: 'First name (A)', aLast: 'Last name (A)', aPhone: 'Phone (A)',
              bFirst: 'First name (B)', bLast: 'Last name (B)', bPhone: 'Phone (B)',
              date:   'Registered', total: 'Total diagnostics',
              prac:   'Practices done', score: 'Relationship index', status: 'Status' },
      }
      const col = (colHeaders[lang] ?? colHeaders.ru) as Record<string, string>

      const rows = data.results.map(f => {
        const row: Record<string, string | number> = {
          [col.aFirst]: f.a_first_name,
          [col.aLast]:  f.a_last_name || '—',
          [col.aPhone]: f.a_phone || '—',
          [col.bFirst]: f.b_first_name || '—',
          [col.bLast]:  f.b_last_name  || '—',
          [col.bPhone]: f.b_phone      || '—',
          [col.date]:   f.created_at,
        }
        // Diagnostics per level
        levels.forEach(lvl => {
          const header = lang === 'ru' ? `Уровень ${lvl} — ${levelNames[lvl]}`
                       : lang === 'uz' ? `${lvl}-daraja — ${levelNames[lvl]}`
                       : `Level ${lvl} — ${levelNames[lvl]}`
          row[header] = f.diagnostics_per_level[lvl] ?? 0
        })
        row[col.total] = f.diagnostics_total
        row[col.prac]  = f.practices_count
        row[col.score] = f.relationship_score ?? '—'
        row[col.status] = crisisLabels[f.crisis_level] ?? f.crisis_level
        return row
      })

      const familiesWs = XLSX.utils.json_to_sheet(rows)
      // Auto column width
      const colWidths = rows.reduce<number[]>((acc, row) => {
        Object.values(row).forEach((v, i) => {
          acc[i] = Math.max(acc[i] ?? 10, String(v).length + 2)
        })
        return acc
      }, [])
      familiesWs['!cols'] = colWidths.map(w => ({ wch: Math.min(w, 40) }))

      const sheetName = lang === 'ru' ? 'Семьи' : lang === 'uz' ? 'Oilalar' : 'Families'
      XLSX.utils.book_append_sheet(wb, familiesWs, sheetName)

      // ── Sheet 2: Summary ──────────────────────────────────────
      const s = data.summary
      const summaryRows =
        lang === 'ru' ? [
          { 'Показатель': 'Всего семей',                  'Значение': s.total },
          { 'Показатель': 'В норме (индекс ≥ 75)',        'Значение': s.normal },
          { 'Показатель': 'Требуют внимания (50–75)',     'Значение': s.warning },
          { 'Показатель': 'В кризисе (< 50)',             'Значение': s.critical },
          { 'Показатель': 'Средний индекс',               'Значение': overview?.avg_relationship_score ?? '—' },
          { 'Показатель': 'Всего диагностик пройдено',   'Значение': overview?.completed_diagnostics ?? '—' },
          { 'Показатель': 'Всего практик выполнено',     'Значение': overview?.completed_practices ?? '—' },
        ]
        : lang === 'uz' ? [
          { 'Ko\'rsatkich': 'Jami oilalar',               'Qiymat': s.total },
          { 'Ko\'rsatkich': 'Normal (indeks ≥ 75)',        'Qiymat': s.normal },
          { 'Ko\'rsatkich': 'Diqqat talab qiladi (50–75)', 'Qiymat': s.warning },
          { 'Ko\'rsatkich': 'Inqirozda (< 50)',            'Qiymat': s.critical },
          { 'Ko\'rsatkich': "O'rtacha indeks",             'Qiymat': overview?.avg_relationship_score ?? '—' },
          { 'Ko\'rsatkich': 'Jami o\'tilgan diagnostika',  'Qiymat': overview?.completed_diagnostics ?? '—' },
          { 'Ko\'rsatkich': 'Jami bajarilgan amaliyot',    'Qiymat': overview?.completed_practices ?? '—' },
        ]
        : [
          { 'Indicator': 'Total families',                 'Value': s.total },
          { 'Indicator': 'Normal (index ≥ 75)',            'Value': s.normal },
          { 'Indicator': 'Need attention (50–75)',         'Value': s.warning },
          { 'Indicator': 'In crisis (< 50)',               'Value': s.critical },
          { 'Indicator': 'Average index',                  'Value': overview?.avg_relationship_score ?? '—' },
          { 'Indicator': 'Total diagnostics completed',   'Value': overview?.completed_diagnostics ?? '—' },
          { 'Indicator': 'Total practices completed',     'Value': overview?.completed_practices ?? '—' },
        ]

      const summaryWs = XLSX.utils.json_to_sheet(summaryRows)
      summaryWs['!cols'] = [{ wch: 36 }, { wch: 12 }]
      const summarySheetName = lang === 'ru' ? 'Сводка' : lang === 'uz' ? 'Xulosa' : 'Summary'
      XLSX.utils.book_append_sheet(wb, summaryWs, summarySheetName)

      XLSX.writeFile(wb, `oila_ai_export_${new Date().toISOString().slice(0, 10)}.xlsx`)
      setExportStatus('done')
    } catch {
      setExportStatus('error')
    }
    setTimeout(() => setExportStatus('idle'), 3000)
  }

  const CARD       = 'rounded-[20px] bg-canvas p-4 md:p-6'
  const CARD_STYLE = { border: '1px solid rgba(194,184,164,0.60)', boxShadow: '0 2px 12px rgba(23,21,42,0.08)' }

  const stats = [
    { labelKey: 'export.stats.families',    value: overview?.total_couples ?? '—' },
    { labelKey: 'export.stats.diagnostics', value: overview?.completed_diagnostics ?? '—' },
    { labelKey: 'export.stats.practices',   value: overview?.completed_practices ?? '—' },
    { labelKey: 'export.stats.users',       value: overview?.total_users ?? '—' },
  ]

  const fields = t('export.families_card.fields', { returnObjects: true }) as string[]

  const btnLabel =
    exportStatus === 'loading' ? t('export.families_card.btn_loading')
    : exportStatus === 'done'  ? t('export.families_card.btn_done')
    : exportStatus === 'error' ? t('export.families_card.btn_error')
    : t('export.families_card.btn_idle')

  return (
    <div className="min-h-full bg-surface p-4 md:p-6 space-y-5">
      <div>
        <h1 className="text-xl md:text-2xl font-bold text-ink">{t('export.title')}</h1>
        <p className="text-sm text-muted mt-0.5">{t('export.subtitle')}</p>
      </div>

      {/* Stats preview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {stats.map(s => (
          <div key={s.labelKey} className={CARD} style={CARD_STYLE}>
            <p className="text-2xl font-bold text-ink">{s.value}</p>
            <p className="text-xs text-muted mt-1">{t(s.labelKey)}</p>
          </div>
        ))}
      </div>

      {/* Export cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className={CARD} style={CARD_STYLE}>
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-[#E2EDE8]">
              <FileSpreadsheet size={22} className="text-[#386858]" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-bold text-ink">{t('export.families_card.title')}</p>
              <p className="text-xs text-muted mt-1">{t('export.families_card.desc')}</p>
              <ul className="mt-2 space-y-0.5">
                {(Array.isArray(fields) ? fields : []).map((l: string) => (
                  <li key={l} className="flex items-center gap-1.5 text-xs text-muted">
                    <span className="h-1 w-1 rounded-full bg-muted/60 shrink-0" />
                    {l}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <button
            onClick={exportXLSX}
            disabled={exportStatus === 'loading'}
            className="mt-5 flex w-full items-center justify-center gap-2 rounded-[14px] px-4 py-2.5 text-sm font-semibold transition-all"
            style={{
              background: exportStatus === 'done' ? '#E2EDE8' : exportStatus === 'error' ? '#F5DDE4' : '#3C3888',
              color: exportStatus === 'done' ? '#386858' : exportStatus === 'error' ? '#843048' : '#fff',
              opacity: exportStatus === 'loading' ? 0.7 : 1,
            }}
          >
            {exportStatus === 'loading' && <span className="h-4 w-4 rounded-full border-2 border-white/40 border-t-white animate-spin" />}
            {exportStatus === 'done'    && <CheckCircle2 size={15} />}
            {exportStatus === 'error'   && <AlertCircle size={15} />}
            {exportStatus === 'idle'    && <Download size={15} />}
            {btnLabel}
          </button>
        </div>

        <div className={CARD} style={{ ...CARD_STYLE, opacity: 0.6 }}>
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-[#EDEAF8]">
              <FileSpreadsheet size={22} className="text-[#3C3888]" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <p className="font-bold text-ink">{t('export.reports_card.title')}</p>
                <span className="rounded-full bg-sand px-2 py-0.5 text-[10px] font-bold text-muted">{t('export.reports_card.badge')}</span>
              </div>
              <p className="text-xs text-muted mt-1">{t('export.reports_card.desc')}</p>
            </div>
          </div>
          <div className="mt-5 h-10 rounded-[14px] bg-sand/40" />
        </div>
      </div>
    </div>
  )
}
