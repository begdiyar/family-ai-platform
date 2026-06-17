/**
 * SANCTUARY ICON SYSTEM — «Тёплый Дневник»
 *
 * Стиль: hand-drawn illustrations, тонкий карандаш
 * ViewBox: 32×32 · strokeWidth: 1.8 · round caps/joins
 * Линии живые, формы чуть несимметричные, тёплый характер.
 */

export interface IconProps {
  size?: number
  color?: string
  className?: string
}

export const ICON_COLORS = {
  ink:        '#4A4540',
  sage:       '#6B9E84',
  sky:        '#7AAFCA',
  terracotta: '#C4876A',
  olive:      '#8E9E6B',
  lavender:   '#9B8EC4',
  warm:       '#B09080',
  muted:      '#9B9188',
} as const

const S = {
  strokeLinecap:  'round'  as const,
  strokeLinejoin: 'round'  as const,
  strokeWidth:    1.8,
  fill:           'none',
}

/* ─────────────────────────────────────────────────────────────────────
   ЛЮДИ
───────────────────────────────────────────────────────────────────── */

/** Семья — папа, мама и ребёнок, держатся за руки */
export const FamilyIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Ребёнок (центр) */}
    <circle cx="16" cy="8" r="3" stroke={color} {...S} />
    <path d="M16 11 Q15.5 16 16 19" stroke={color} {...S} />
    <path d="M16 14 Q13 13 11 14.5" stroke={color} {...S} />
    <path d="M16 14 Q19 13 21 14.5" stroke={color} {...S} />
    <path d="M16 19 Q14 21.5 13.5 24" stroke={color} {...S} />
    <path d="M16 19 Q18 21.5 18.5 24" stroke={color} {...S} />

    {/* Папа (левее, выше) */}
    <circle cx="7" cy="9" r="3.2" stroke={color} {...S} />
    <path d="M7 12.2 Q6.5 17.5 7 21" stroke={color} {...S} />
    <path d="M7 15.5 Q4 14.5 2.5 16" stroke={color} {...S} />
    <path d="M7 21 Q5.5 23.5 5 26" stroke={color} {...S} />
    <path d="M7 21 Q8.5 23.5 9 26" stroke={color} {...S} />

    {/* Мама (правее, волосы) */}
    <circle cx="25" cy="9" r="3" stroke={color} {...S} />
    <path d="M22.5 7 Q25 5 27.5 7" stroke={color} {...S} />
    {/* юбка */}
    <path d="M25 12 Q23 17.5 21 21" stroke={color} {...S} />
    <path d="M25 12 Q27 17.5 29 21" stroke={color} {...S} />
    <path d="M21 21 Q25 23 29 21" stroke={color} {...S} />
    <path d="M25 15 Q28 14 29.5 15.5" stroke={color} {...S} />

    {/* Руки соединены */}
    <path d="M11 14.5 Q11.5 15.5 13 16" stroke={color} {...S} strokeDasharray="1 1.5" />
    <path d="M21 14.5 Q21.5 15.5 23 16" stroke={color} {...S} strokeDasharray="1 1.5" />
  </svg>
)

/** Муж */
export const HusbandIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    <circle cx="16" cy="8.5" r="4" stroke={color} {...S} />
    {/* тело */}
    <path d="M16 12.5 Q15.5 18 16 22" stroke={color} {...S} />
    {/* плечи широкие */}
    <path d="M16 15.5 Q11 14 8.5 15.5 Q8 19 8.5 22" stroke={color} {...S} />
    <path d="M16 15.5 Q21 14 23.5 15.5 Q24 19 23.5 22" stroke={color} {...S} />
    {/* ноги */}
    <path d="M16 22 Q13.5 25 13 28" stroke={color} {...S} />
    <path d="M16 22 Q18.5 25 19 28" stroke={color} {...S} />
    {/* кроссовки — маленький штрих */}
    <path d="M11 28 Q12.5 28.5 14.5 28" stroke={color} {...S} />
    <path d="M17.5 28 Q19 28.5 21 28" stroke={color} {...S} />
  </svg>
)

/** Жена */
export const WifeIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    <circle cx="16" cy="8.5" r="4" stroke={color} {...S} />
    {/* Волосы */}
    <path d="M12.5 6.5 Q14 4 16 3.5 Q18 4 19.5 6.5" stroke={color} {...S} />
    <path d="M12 7.5 Q11 10 12 12" stroke={color} {...S} />
    <path d="M20 7.5 Q21 10 20 12" stroke={color} {...S} />
    {/* тело */}
    <path d="M16 12.5 Q15.5 16 16 18" stroke={color} {...S} />
    {/* юбка-трапеция */}
    <path d="M16 18 Q12 20 10.5 24 Q13 24.5 16 24" stroke={color} {...S} />
    <path d="M16 18 Q20 20 21.5 24 Q19 24.5 16 24" stroke={color} {...S} />
    {/* ноги */}
    <path d="M13 24 Q12.5 26.5 13 28" stroke={color} {...S} />
    <path d="M19 24 Q19.5 26.5 19 28" stroke={color} {...S} />
    {/* руки */}
    <path d="M16 15 Q12 13.5 10 15" stroke={color} {...S} />
    <path d="M16 15 Q20 13.5 22 15" stroke={color} {...S} />
  </svg>
)

/** Ребёнок */
export const ChildIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* голова побольше относительно тела — детские пропорции */}
    <circle cx="16" cy="10" r="5" stroke={color} {...S} />
    {/* Вихор */}
    <path d="M16 5 Q17.5 3 19 4" stroke={color} {...S} />
    {/* тело */}
    <path d="M16 15 Q15.5 19 16 21.5" stroke={color} {...S} />
    {/* руки */}
    <path d="M16 17 Q12.5 16 11 17.5" stroke={color} {...S} />
    <path d="M16 17 Q19.5 16 21 17.5" stroke={color} {...S} />
    {/* ноги */}
    <path d="M16 21.5 Q14 24 13.5 27" stroke={color} {...S} />
    <path d="M16 21.5 Q18 24 18.5 27" stroke={color} {...S} />
    {/* башмачки */}
    <path d="M11.5 27 Q13 28 15 27.5" stroke={color} {...S} />
    <path d="M17 27.5 Q18.5 28 20.5 27" stroke={color} {...S} />
  </svg>
)

/** Свекровь — взрослая женщина с пучком */
export const MotherInLawIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    <circle cx="16" cy="9" r="4" stroke={color} {...S} />
    {/* пучок на голове */}
    <path d="M14 5.5 Q16 3 18 5.5" stroke={color} {...S} />
    <circle cx="16" cy="3.5" r="2" stroke={color} {...S} />
    {/* очки */}
    <path d="M13 9 Q14.5 8.5 16 9" stroke={color} {...S} />
    <path d="M16 9 Q17.5 8.5 19 9" stroke={color} {...S} />
    {/* юбка пошире */}
    <path d="M16 13 Q15.5 17 16 19" stroke={color} {...S} />
    <path d="M16 19 Q11 21 9 25 Q12 26 16 25.5" stroke={color} {...S} />
    <path d="M16 19 Q21 21 23 25 Q20 26 16 25.5" stroke={color} {...S} />
    {/* руки */}
    <path d="M16 16 Q12 14.5 10 16" stroke={color} {...S} />
    <path d="M16 16 Q20 14.5 22 16" stroke={color} {...S} />
    {/* ноги */}
    <path d="M13.5 25.5 Q13 27.5 13.5 29" stroke={color} {...S} />
    <path d="M18.5 25.5 Q19 27.5 18.5 29" stroke={color} {...S} />
  </svg>
)

/** Родственники — пять фигур разного роста */
export const RelativesIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Фигура 1 — слева, высокая */}
    <circle cx="4.5" cy="10" r="2.5" stroke={color} {...S} />
    <path d="M4.5 12.5 Q4 17.5 4.5 22" stroke={color} {...S} />
    {/* Фигура 2 */}
    <circle cx="10" cy="12" r="2.2" stroke={color} {...S} />
    <path d="M10 14.2 Q9.5 19 10 23" stroke={color} {...S} />
    {/* Фигура 3 — центральная, выше */}
    <circle cx="16" cy="9.5" r="2.8" stroke={color} {...S} />
    <path d="M16 12.3 Q15.5 18 16 23" stroke={color} {...S} />
    {/* Фигура 4 */}
    <circle cx="22" cy="12" r="2.2" stroke={color} {...S} />
    <path d="M22 14.2 Q21.5 19 22 23" stroke={color} {...S} />
    {/* Фигура 5 — справа */}
    <circle cx="27.5" cy="11" r="2.5" stroke={color} {...S} />
    <path d="M27.5 13.5 Q27 18.5 27.5 23" stroke={color} {...S} />
    {/* Земля */}
    <path d="M2 26 Q16 25 30 26" stroke={color} {...S} />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   ЧУВСТВА И ОТНОШЕНИЯ
───────────────────────────────────────────────────────────────────── */

/** Любовь — рукотворное сердце, правый горб чуть выше */
export const LoveIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    <path
      d="M16 27 C12 24.5 3.5 19.5 3 12.5 C2.5 8 5.5 5.5 9 5.5 C11.5 5.5 14 7 16 10 C18 7 20.5 5.5 23 5.5 C26.5 5.5 29.5 8 29 12.5 C28.5 19.5 20 24.5 16 27Z"
      stroke={color} {...S}
    />
    {/* лёгкий блик — одна короткая кривая */}
    <path d="M10 10 Q11.5 8.5 13 9" stroke={color} strokeWidth="1.4" {...S} />
  </svg>
)

/** Объятия — две фигуры в круге объятий, вид условный */
export const HugsIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Левая фигура */}
    <circle cx="10" cy="9" r="3" stroke={color} {...S} />
    <path d="M10 12 Q9.5 15.5 10 18" stroke={color} {...S} />
    {/* Правая фигура */}
    <circle cx="22" cy="9" r="3" stroke={color} {...S} />
    <path d="M22 12 Q22.5 15.5 22 18" stroke={color} {...S} />
    {/* Объятие — руки */}
    <path d="M10 15 Q13 12 16 12.5 Q19 12 22 15" stroke={color} {...S} />
    {/* Большие объятийные руки вокруг */}
    <path d="M7 12 Q3 16 3.5 22 Q5 26 9 27" stroke={color} {...S} />
    <path d="M25 12 Q29 16 28.5 22 Q27 26 23 27" stroke={color} {...S} />
    {/* Ноги вниз */}
    <path d="M10 18 Q8.5 22 8 26" stroke={color} {...S} />
    <path d="M10 18 Q11.5 22 12 26" stroke={color} {...S} />
    <path d="M22 18 Q20.5 22 20 26" stroke={color} {...S} />
    <path d="M22 18 Q23.5 22 24 26" stroke={color} {...S} />
    {/* Маленькое сердечко над объятием */}
    <path d="M16 6 C15 4.5 12.5 4.5 12.5 6.5 C12.5 8.5 16 10 16 10 C16 10 19.5 8.5 19.5 6.5 C19.5 4.5 17 4.5 16 6Z"
      stroke={color} strokeWidth="1.4" {...S} />
  </svg>
)

/** Поддержка — рука снизу, поддерживающая фигуру */
export const SupportIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Маленькая фигура сверху */}
    <circle cx="16" cy="8" r="3.2" stroke={color} {...S} />
    <path d="M16 11.2 Q15.5 15 16 17" stroke={color} {...S} />
    <path d="M16 14 Q13 13 11.5 14" stroke={color} {...S} />
    <path d="M16 14 Q19 13 20.5 14" stroke={color} {...S} />
    <path d="M16 17 Q14.5 20 14 22" stroke={color} {...S} />
    <path d="M16 17 Q17.5 20 18 22" stroke={color} {...S} />
    {/* Поддерживающая большая рука */}
    <path d="M5 24 Q8 22 11 22.5 Q13.5 22.5 16 22.5 Q18.5 22.5 21 22.5 Q24 22 27 24" stroke={color} {...S} />
    <path d="M5 24 Q6 26.5 8 26.5 Q10 26.5 11 25 Q13 27.5 16 27.5 Q19 27.5 21 25 Q22 26.5 24 26.5 Q26 26.5 27 24" stroke={color} {...S} />
    {/* большой палец */}
    <path d="M5 24 Q4 22 5.5 21.5" stroke={color} {...S} />
  </svg>
)

/** Доверие — две ладони, тянутся навстречу (почти касаются) */
export const TrustIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Верхняя рука (тянется вниз) */}
    <path d="M9 4 Q9 7 9.5 10" stroke={color} {...S} />
    <path d="M12 4 Q12 7.5 12 10" stroke={color} {...S} />
    <path d="M15 4 Q15 8 14.5 10.5" stroke={color} {...S} />
    <path d="M18 4.5 Q17.5 8 17 10.5" stroke={color} {...S} />
    {/* Ладонь верхней руки */}
    <path d="M8.5 10 Q10.5 13 13.5 13.5 Q16.5 13.5 17.5 11" stroke={color} {...S} />
    {/* Нижняя рука (тянется вверх) */}
    <path d="M14 28 Q14 25 14.5 22" stroke={color} {...S} />
    <path d="M17 28 Q17 24.5 17 22" stroke={color} {...S} />
    <path d="M20 28 Q20 24 20.5 21.5" stroke={color} {...S} />
    <path d="M23 27.5 Q22.5 24 22 21.5" stroke={color} {...S} />
    {/* Ладонь нижней руки */}
    <path d="M13.5 22 Q15.5 19 18.5 18.5 Q21.5 18.5 22.5 21" stroke={color} {...S} />
    {/* Точка встречи — почти касаются */}
    <path d="M15 13.5 Q16 15.5 17 13.5" stroke={color} {...S} strokeDasharray="2 1.5" />
    <path d="M16 18.5 Q16 16.5 16 15.5" stroke={color} {...S} strokeDasharray="1.5 1.5" />
  </svg>
)

/** Примирение — две фигуры, между ними сердце, тянутся навстречу */
export const ReconciliationIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Левая фигура */}
    <circle cx="7" cy="10" r="3" stroke={color} {...S} />
    <path d="M7 13 Q6.5 17 7 21" stroke={color} {...S} />
    <path d="M7 21 Q5.5 23.5 5 26" stroke={color} {...S} />
    <path d="M7 21 Q8.5 23.5 9 26" stroke={color} {...S} />
    {/* Правая фигура */}
    <circle cx="25" cy="10" r="3" stroke={color} {...S} />
    <path d="M25 13 Q25.5 17 25 21" stroke={color} {...S} />
    <path d="M25 21 Q23.5 23.5 23 26" stroke={color} {...S} />
    <path d="M25 21 Q26.5 23.5 27 26" stroke={color} {...S} />
    {/* Руки тянутся навстречу */}
    <path d="M7 16 Q11 15 13.5 16" stroke={color} {...S} />
    <path d="M25 16 Q21 15 18.5 16" stroke={color} {...S} />
    {/* Сердце между ними */}
    <path d="M16 18 C15 16.5 12.5 16.5 12.5 18.5 C12.5 20.5 16 22 16 22 C16 22 19.5 20.5 19.5 18.5 C19.5 16.5 17 16.5 16 18Z"
      stroke={color} {...S} />
  </svg>
)

/** Конфликт — две фигуры отвернулись, молния между ними */
export const ConflictIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Левая фигура (отвернулась влево) */}
    <circle cx="7.5" cy="9" r="3" stroke={color} {...S} />
    <path d="M7.5 12 Q7 17 7.5 21" stroke={color} {...S} />
    <path d="M7.5 15.5 Q4.5 14.5 3 16" stroke={color} {...S} />
    <path d="M7.5 21 Q6 23.5 5.5 26" stroke={color} {...S} />
    <path d="M7.5 21 Q9 23.5 9.5 26" stroke={color} {...S} />
    {/* Правая фигура (отвернулась вправо) */}
    <circle cx="24.5" cy="9" r="3" stroke={color} {...S} />
    <path d="M24.5 12 Q25 17 24.5 21" stroke={color} {...S} />
    <path d="M24.5 15.5 Q27.5 14.5 29 16" stroke={color} {...S} />
    <path d="M24.5 21 Q23 23.5 22.5 26" stroke={color} {...S} />
    <path d="M24.5 21 Q26 23.5 26.5 26" stroke={color} {...S} />
    {/* Молния между ними */}
    <path d="M17 6 L14.5 14 L17.5 14 L15 23" stroke={color} {...S} strokeWidth="1.6" />
  </svg>
)

/** Благодарность — руки, из которых вырастает цветок */
export const GratitudeIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Руки-чаша */}
    <path d="M4 22 Q6 20 9 20.5 Q12.5 21 16 21 Q19.5 21 23 20.5 Q26 20 28 22" stroke={color} {...S} />
    <path d="M4 22 Q5 25 8 25.5 Q12 26 16 26 Q20 26 24 25.5 Q27 25 28 22" stroke={color} {...S} />
    {/* большой палец левой */}
    <path d="M4 22 Q3 20 4.5 19.5" stroke={color} {...S} />
    {/* большой палец правой */}
    <path d="M28 22 Q29 20 27.5 19.5" stroke={color} {...S} />
    {/* Стебель */}
    <path d="M16 21 Q15.5 15 16 9" stroke={color} {...S} />
    {/* Листья */}
    <path d="M16 14 Q12.5 11.5 11 13 Q12 15 15.5 14.5" stroke={color} {...S} />
    <path d="M16 11 Q19.5 8.5 21 10 Q20 12 16.5 11.5" stroke={color} {...S} />
    {/* Цветок */}
    <circle cx="16" cy="7" r="2.5" stroke={color} {...S} />
    <path d="M16 4.5 Q16.5 3 16 2" stroke={color} {...S} />
    <path d="M18 5.5 Q19.5 4.5 20.5 4" stroke={color} {...S} />
    <path d="M18.5 7 Q19.5 8.5 20.5 9" stroke={color} {...S} />
    <path d="M14 5.5 Q12.5 4.5 11.5 4" stroke={color} {...S} />
    <path d="M13.5 7 Q12.5 8.5 11.5 9" stroke={color} {...S} />
  </svg>
)

/** Счастье — улыбающееся солнышко */
export const HappinessIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Круг */}
    <circle cx="16" cy="16" r="8" stroke={color} {...S} />
    {/* Закрытые глаза-дуги */}
    <path d="M12 14 Q13 12.5 14 14" stroke={color} {...S} strokeWidth="1.6" />
    <path d="M18 14 Q19 12.5 20 14" stroke={color} {...S} strokeWidth="1.6" />
    {/* Улыбка */}
    <path d="M12 18 Q16 21.5 20 18" stroke={color} {...S} />
    {/* Лучи (неровные) */}
    <path d="M16 6 Q16.3 5 16 3.5" stroke={color} {...S} />
    <path d="M22 8 Q23 7.5 24.5 6.5" stroke={color} {...S} />
    <path d="M25.5 14 Q26.5 14.5 28 14" stroke={color} {...S} />
    <path d="M24 21 Q25 22 26.5 23" stroke={color} {...S} />
    <path d="M16 26 Q15.7 27 16 28.5" stroke={color} {...S} />
    <path d="M10 23.5 Q9 24.5 7.5 25.5" stroke={color} {...S} />
    <path d="M6.5 17.5 Q5.5 17 4 17" stroke={color} {...S} />
    <path d="M8 10 Q7 9 5.5 8" stroke={color} {...S} />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   КОММУНИКАЦИЯ
───────────────────────────────────────────────────────────────────── */

/** Общение — два пузыря, один с точками */
export const CommunicationIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Верхний пузырь (левый) */}
    <path d="M3 5 Q3 4 4 4 L20 4 Q21 4 21 5 L21 14 Q21 15 20 15 L9 15 L6.5 18 L6.5 15 L4 15 Q3 15 3 14 Z"
      stroke={color} {...S} />
    {/* три точки */}
    <circle cx="10" cy="9.5" r="1" fill={color} />
    <circle cx="14" cy="9.5" r="1" fill={color} />
    <circle cx="18" cy="9.5" r="1" fill={color} />
    {/* Нижний пузырь (правый) */}
    <path d="M11 19 Q11 18 12 18 L28 18 Q29 18 29 19 L29 27 Q29 28 28 28 L18 28 L25.5 28 L25.5 28 M11 27 L11 19"
      stroke={color} {...S} />
    <path d="M11 18.5 Q11 18 12 18 L28 18 Q29 18 29 19 L29 27 Q29 28 28 28 L20.5 28 L18 30.5 L18 28 L12 28 Q11 28 11 27 Z"
      stroke={color} {...S} />
    {/* одиночная точка — задумчивость */}
    <circle cx="20" cy="23" r="1" fill={color} />
  </svg>
)

/** Диалог — два пузыря, обращённых навстречу */
export const DialogueIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Левый пузырь */}
    <path d="M2 5 Q2 4 3 4 L16 4 Q17 4 17 5 L17 13 Q17 14 16 14 L8 14 L5.5 17 L5.5 14 L3 14 Q2 14 2 13 Z"
      stroke={color} {...S} />
    <path d="M6 9 Q9.5 9 13 9" stroke={color} {...S} />
    <path d="M6 11.5 Q8.5 11.5 11 11.5" stroke={color} {...S} />
    {/* Правый пузырь */}
    <path d="M30 19 Q30 18 29 18 L16 18 Q15 18 15 19 L15 27 Q15 28 16 28 L24 28 L26.5 31 L26.5 28 L29 28 Q30 28 30 27 Z"
      stroke={color} {...S} />
    <path d="M19 22.5 Q22.5 22.5 26 22.5" stroke={color} {...S} />
    <path d="M19 25 Q21.5 25 24 25" stroke={color} {...S} />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   ДОМ И ПРОСТРАНСТВО
───────────────────────────────────────────────────────────────────── */

/** Дом — уютный домик с дымком */
export const HomeIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Крыша */}
    <path d="M3.5 17 Q9 8.5 16 5.5 Q23 8.5 28.5 17" stroke={color} {...S} />
    {/* Стены */}
    <path d="M6.5 16 L6.5 28 L25.5 28 L25.5 16" stroke={color} {...S} />
    {/* Дверь с аркой */}
    <path d="M13 28 L13 22 Q16 20 19 22 L19 28" stroke={color} {...S} />
    {/* Окошко */}
    <path d="M20.5 18.5 Q22 18 23.5 18.5 Q24 20 23.5 21.5 Q22 22 20.5 21.5 Q20 20 20.5 18.5Z" stroke={color} {...S} />
    {/* крест на окне */}
    <path d="M22 18.5 L22 21.5" stroke={color} strokeWidth="1.2" />
    <path d="M20.5 20 L23.5 20" stroke={color} strokeWidth="1.2" />
    {/* Труба */}
    <path d="M20.5 11 L20.5 7 L23.5 7 L23.5 12" stroke={color} {...S} />
    {/* Дымок */}
    <path d="M21.5 7 Q20.5 5 22 3.5 Q23.5 5 22.5 3" stroke={color} strokeWidth="1.4" {...S} />
  </svg>
)

/** Безопасность — органичный щит с сердцем */
export const SafetyIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Щит */}
    <path d="M16 3.5 Q12 4 8 6 Q5.5 8 5.5 12 Q5.5 20 16 28 Q26.5 20 26.5 12 Q26.5 8 24 6 Q20 4 16 3.5Z"
      stroke={color} {...S} />
    {/* Сердечко внутри */}
    <path d="M16 20 C13.5 18 9.5 16 9.5 12.5 C9.5 10.5 11 9.5 12.5 9.5 C13.5 9.5 15 10.5 16 12 C17 10.5 18.5 9.5 19.5 9.5 C21 9.5 22.5 10.5 22.5 12.5 C22.5 16 18.5 18 16 20Z"
      stroke={color} {...S} />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   ПРОГРЕСС И ПЛАНИРОВАНИЕ
───────────────────────────────────────────────────────────────────── */

/** Прогресс — росток с листьями */
export const ProgressIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Земля */}
    <path d="M5 27 Q16 25.5 27 27" stroke={color} {...S} />
    {/* Стебель с изгибом */}
    <path d="M16 27 Q15.5 22 16 16 Q16.5 12 16 7" stroke={color} {...S} />
    {/* Лист левый (побольше) */}
    <path d="M16 16 Q11 13 9 15 Q11 18 15.5 17" stroke={color} {...S} />
    {/* Лист правый (поменьше) */}
    <path d="M16 11.5 Q21 9 23 11 Q21 13.5 16.5 12.5" stroke={color} {...S} />
    {/* Бутон вверху */}
    <path d="M16 7 Q14 5 14 3.5 Q16 4 16 4 Q16 4 18 3.5 Q18 5 16 7Z" stroke={color} {...S} />
  </svg>
)

/** Календарь с отметкой-сердечком */
export const CalendarIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Основа */}
    <path d="M4 9 Q4 7.5 5.5 7.5 L26.5 7.5 Q28 7.5 28 9 L28 27 Q28 28.5 26.5 28.5 L5.5 28.5 Q4 28.5 4 27 Z"
      stroke={color} {...S} />
    {/* Шапка */}
    <path d="M4 12.5 Q16 12 28 12.5" stroke={color} {...S} />
    {/* Крепления */}
    <path d="M10 5.5 L10 9.5" stroke={color} {...S} strokeWidth="2" />
    <path d="M22 5.5 L22 9.5" stroke={color} {...S} strokeWidth="2" />
    {/* Сетка дней (точки) */}
    <circle cx="9" cy="17" r="0.8" fill={color} />
    <circle cx="14" cy="17" r="0.8" fill={color} />
    <circle cx="24" cy="17" r="0.8" fill={color} />
    <circle cx="9" cy="22" r="0.8" fill={color} />
    <circle cx="14" cy="22" r="0.8" fill={color} />
    <circle cx="19" cy="22" r="0.8" fill={color} />
    <circle cx="24" cy="22" r="0.8" fill={color} />
    {/* Сердечко на выбранном дне */}
    <path d="M19 17 C18.2 15.8 16 15.8 16 17.5 C16 19.2 19 21 19 21 C19 21 22 19.2 22 17.5 C22 15.8 19.8 15.8 19 17Z"
      stroke={color} {...S} />
  </svg>
)

/** План восстановления — тропинка с шагами */
export const RecoveryPlanIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Тропинка */}
    <path d="M5 28 Q8 24 11 20 Q16 14 19 10 Q22 6 26 4" stroke={color} {...S} strokeDasharray="3 2" />
    {/* Шаг 1 — Галочка */}
    <circle cx="8.5" cy="25" r="3.5" stroke={color} {...S} />
    <path d="M6.5 25 L8 26.5 L10.5 23.5" stroke={color} {...S} strokeWidth="1.6" />
    {/* Шаг 2 — Галочка */}
    <circle cx="17" cy="15.5" r="3.5" stroke={color} {...S} />
    <path d="M15 15.5 L16.5 17 L19 14" stroke={color} {...S} strokeWidth="1.6" />
    {/* Шаг 3 — пустой (впереди) */}
    <circle cx="25" cy="5.5" r="3.5" stroke={color} {...S} />
    <path d="M23.5 5.5 Q25 7 26.5 5.5" stroke={color} {...S} strokeDasharray="1.5 1" />
  </svg>
)

/** Достижения — медаль на ленте */
export const AchievementsIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Лента */}
    <path d="M12 4 L12 14 Q16 17 20 14 L20 4" stroke={color} {...S} />
    <path d="M12 4 Q14 6 16 4 Q18 6 20 4" stroke={color} {...S} />
    {/* Медаль */}
    <circle cx="16" cy="22" r="7.5" stroke={color} {...S} />
    <circle cx="16" cy="22" r="5" stroke={color} strokeWidth="1.2" />
    {/* Звёздочка внутри */}
    <path d="M16 18.5 L17 21 L19.5 21 L17.5 22.5 L18.5 25 L16 23.5 L13.5 25 L14.5 22.5 L12.5 21 L15 21 Z"
      stroke={color} strokeWidth="1.2" {...S} />
  </svg>
)

/** Память семьи — фоторамка с сердцем */
export const FamilyMemoryIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Рамка (чуть наклонена для живости) */}
    <path d="M5 5.5 Q5 4.5 6 4.5 L26 4.5 Q27 4.5 27 5.5 L27 26.5 Q27 27.5 26 27.5 L6 27.5 Q5 27.5 5 26.5 Z"
      stroke={color} {...S} />
    {/* Внутренняя рамочка */}
    <path d="M8 8 L8 24 L24 24 L24 8 Z" stroke={color} strokeWidth="1.2" {...S} />
    {/* Уголки рамки */}
    <path d="M8 8 L10 10" stroke={color} strokeWidth="1" />
    <path d="M24 8 L22 10" stroke={color} strokeWidth="1" />
    <path d="M8 24 L10 22" stroke={color} strokeWidth="1" />
    <path d="M24 24 L22 22" stroke={color} strokeWidth="1" />
    {/* Сердечко внутри */}
    <path d="M16 20 C13 17.5 9 16 9 12 C9 9.5 11 8 13 8 C14.5 8 16 9 16 9 C16 9 17.5 8 19 8 C21 8 23 9.5 23 12 C23 16 19 17.5 16 20Z"
      stroke={color} {...S} />
  </svg>
)

/** Семейные цели — рукотворная звезда с сердечком */
export const FamilyGoalsIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Звезда (5 лучей, чуть неровная) */}
    <path d="M16 3 L18.5 11 L27.5 11 L20 16.5 L22.5 25 L16 20 L9.5 25 L12 16.5 L4.5 11 L13.5 11 Z"
      stroke={color} {...S} />
    {/* Сердечко внутри */}
    <path d="M16 17 C15 15.5 13 15.5 13 17 C13 18.5 16 20 16 20 C16 20 19 18.5 19 17 C19 15.5 17 15.5 16 17Z"
      stroke={color} {...S} />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   СОВМЕСТНОЕ ВРЕМЯ
───────────────────────────────────────────────────────────────────── */

/** Совместное время — часы с сердечком на стрелках */
export const TogetherTimeIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    <circle cx="16" cy="17" r="12" stroke={color} {...S} />
    {/* Деления */}
    <path d="M16 6.5 L16 8" stroke={color} strokeWidth="2" />
    <path d="M16 26 L16 27.5" stroke={color} strokeWidth="2" />
    <path d="M5.5 17 L7 17" stroke={color} strokeWidth="2" />
    <path d="M25 17 L26.5 17" stroke={color} strokeWidth="2" />
    {/* Стрелки в виде сердца */}
    <path d="M16 17 Q16 12 16 10" stroke={color} {...S} strokeWidth="2" />
    <path d="M16 17 Q20 17 22 17" stroke={color} {...S} strokeWidth="2" />
    {/* Центр */}
    <circle cx="16" cy="17" r="1.5" fill={color} />
    {/* Маленькое сердечко вместо 12 */}
    <path d="M16 7 C15.5 6.2 14 6.2 14 7.2 C14 8.2 16 9.5 16 9.5 C16 9.5 18 8.2 18 7.2 C18 6.2 16.5 6.2 16 7Z"
      stroke={color} strokeWidth="1.3" {...S} />
  </svg>
)

/** Прогулка — две фигуры идут рядом */
export const WalkIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Фигура 1 (левее, шаг левой ногой) */}
    <circle cx="10" cy="7" r="3" stroke={color} {...S} />
    <path d="M10 10 Q9.5 14.5 10 17" stroke={color} {...S} />
    <path d="M10 13 Q7 12 5.5 13.5" stroke={color} {...S} />
    <path d="M10 13 Q12.5 12 13.5 13" stroke={color} {...S} />
    <path d="M10 17 Q8 20 7.5 24" stroke={color} {...S} />
    <path d="M10 17 Q12.5 20.5 13 24" stroke={color} {...S} />
    <path d="M6 24 Q7 25.5 9 25" stroke={color} {...S} />
    <path d="M12 24 Q13.5 25.5 15.5 25" stroke={color} {...S} />
    {/* Фигура 2 (правее) */}
    <circle cx="22" cy="7" r="3" stroke={color} {...S} />
    <path d="M22 7.5 Q21 5.5 22.5 4.5" stroke={color} {...S} />
    <path d="M22 10 Q22.5 14.5 22 17" stroke={color} {...S} />
    <path d="M22 13 Q19.5 12 18.5 13.5" stroke={color} {...S} />
    <path d="M22 13 Q25 12 26.5 13.5" stroke={color} {...S} />
    <path d="M22 17 Q20.5 20.5 20 24" stroke={color} {...S} />
    <path d="M22 17 Q24 20 24.5 24" stroke={color} {...S} />
    <path d="M19 24 Q20 25.5 22 25" stroke={color} {...S} />
    <path d="M23.5 24 Q24.5 25.5 26.5 25" stroke={color} {...S} />
    {/* Земля и трава */}
    <path d="M2 27 Q16 26 30 27" stroke={color} {...S} />
    <path d="M5 27 Q5.5 25.5 6 24 M8 27 Q8.5 25 9 24 M23 27 Q23.5 25 24 24 M26 27 Q26.5 25.5 27 24" stroke={color} strokeWidth="1.3" />
  </svg>
)

/** Путешествие — чемодан с наклейкой-сердечком */
export const TravelIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Ручка */}
    <path d="M11 10 L11 7 Q11 5.5 13 5.5 L19 5.5 Q21 5.5 21 7 L21 10" stroke={color} {...S} />
    {/* Корпус чемодана */}
    <path d="M4 11 Q4 9.5 5.5 9.5 L26.5 9.5 Q28 9.5 28 11 L28 26 Q28 27.5 26.5 27.5 L5.5 27.5 Q4 27.5 4 26 Z"
      stroke={color} {...S} />
    {/* Застёжка */}
    <path d="M4 18.5 L28 18.5" stroke={color} {...S} />
    <path d="M14.5 17 L14.5 20 Q16 21 17.5 20 L17.5 17" stroke={color} {...S} />
    {/* Сердечко-наклейка */}
    <path d="M22 13 C21 11.8 19 11.8 19 13.5 C19 15.2 22 17 22 17 C22 17 25 15.2 25 13.5 C25 11.8 23 11.8 22 13Z"
      stroke={color} {...S} />
    {/* Колёсики */}
    <circle cx="9" cy="27.5" r="2" stroke={color} {...S} />
    <circle cx="23" cy="27.5" r="2" stroke={color} {...S} />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   ФИНАНСЫ
───────────────────────────────────────────────────────────────────── */

/** Финансы — монеты стопочкой */
export const FinancesIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Три монеты */}
    {/* Нижняя */}
    <path d="M6 24 Q16 22 26 24 Q16 26.5 6 24Z" stroke={color} {...S} />
    <path d="M6 24 L6 27 Q16 29.5 26 27 L26 24" stroke={color} {...S} />
    {/* Средняя */}
    <path d="M7 18 Q16 16 25 18 Q16 20.5 7 18Z" stroke={color} {...S} />
    <path d="M7 18 L7 21 Q16 23.5 25 21 L25 18" stroke={color} {...S} />
    {/* Верхняя */}
    <path d="M8 12 Q16 10 24 12 Q16 14.5 8 12Z" stroke={color} {...S} />
    <path d="M8 12 L8 15 Q16 17.5 24 15 L24 12" stroke={color} {...S} />
    {/* Знак валюты на верхней монете */}
    <path d="M15 12 Q16 10.5 17 12 Q16 13.5 15 12Z" stroke={color} strokeWidth="1.2" />
    {/* Блеск */}
    <path d="M10 12.5 Q11 11.5 12.5 12" stroke={color} strokeWidth="1.2" />
  </svg>
)

/** Бюджет — баночка с монеткой */
export const BudgetIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Банка */}
    <path d="M9 11 Q9 9.5 10.5 9.5 L21.5 9.5 Q23 9.5 23 11 L23 26 Q23 27.5 21.5 27.5 L10.5 27.5 Q9 27.5 9 26 Z"
      stroke={color} {...S} />
    {/* Крышка */}
    <path d="M8 9.5 Q8 8 9 8 L23 8 Q24 8 24 9.5 L24 11 L8 11 Z" stroke={color} {...S} />
    {/* Прорезь для монеты */}
    <path d="M14.5 8 L17.5 8" stroke={color} strokeWidth="2.5" />
    {/* Монетка летит в банку */}
    <path d="M19 4 C19.5 3.5 21 3.5 21 5 C21 6.5 19 7 19 7 C19 7 17 6.5 17 5 C17 3.5 18.5 3.5 19 4Z"
      stroke={color} {...S} />
    <path d="M19 7 L19 8" stroke={color} {...S} />
    {/* Линии — уровень накоплений */}
    <path d="M12 20 Q16 19.5 20 20" stroke={color} {...S} strokeWidth="1.2" strokeDasharray="2 1.5" />
    <path d="M12 23 Q16 22.5 20 23" stroke={color} {...S} strokeWidth="1.2" strokeDasharray="2 1.5" />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   МОСТ, AI, ОСОБЫЕ
───────────────────────────────────────────────────────────────────── */

/** Мост понимания — арка, две фигуры, сердечко */
export const BridgeIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Арка моста */}
    <path d="M3 22 Q3 10 16 8 Q29 10 29 22" stroke={color} {...S} />
    {/* Пролёт моста */}
    <path d="M3 22 L29 22" stroke={color} {...S} />
    {/* Опоры */}
    <path d="M9.5 22 L9.5 27" stroke={color} {...S} />
    <path d="M22.5 22 L22.5 27" stroke={color} {...S} />
    {/* Вода */}
    <path d="M2 27 Q8 25.5 16 27 Q24 25.5 30 27" stroke={color} {...S} />
    <path d="M2 29.5 Q8 28 16 29.5 Q24 28 30 29.5" stroke={color} strokeWidth="1.2" />
    {/* Фигурка слева */}
    <circle cx="5" cy="17.5" r="2" stroke={color} {...S} />
    <path d="M5 19.5 Q4.5 21.5 5 22" stroke={color} {...S} />
    {/* Фигурка справа */}
    <circle cx="27" cy="17.5" r="2" stroke={color} {...S} />
    <path d="M27 19.5 Q27.5 21.5 27 22" stroke={color} {...S} />
    {/* Сердечко над мостом */}
    <path d="M16 5 C15.2 3.8 13.5 3.8 13.5 5.5 C13.5 7.2 16 9 16 9 C16 9 18.5 7.2 18.5 5.5 C18.5 3.8 16.8 3.8 16 5Z"
      stroke={color} {...S} />
  </svg>
)

/** AI-консультант — пузырь с тремя звёздочками */
export const AiConsultantIcon = ({ size = 32, color = '#3C3888', className }: IconProps) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" className={className}>
    {/* Пузырь (органичный) */}
    <path d="M4 5.5 Q4 4 5.5 4 L26.5 4 Q28 4 28 5.5 L28 20.5 Q28 22 26.5 22 L18 22 L14.5 27 L14.5 22 L5.5 22 Q4 22 4 20.5 Z"
      stroke={color} {...S} />
    {/* Три звёздочки ✦ */}
    {/* Звёздочка 1 (крупная, в центре) */}
    <path d="M16 8 L16.8 11.2 L19.5 11 L17 13 L18 16 L16 14 L14 16 L15 13 L12.5 11 L15.2 11.2 Z"
      stroke={color} strokeWidth="1.3" {...S} />
    {/* Звёздочка 2 (маленькая, слева вверху) */}
    <path d="M8 8 L8.4 9.5 L10 9.4 L8.8 10.4 L9.3 12 L8 11.1 L6.7 12 L7.2 10.4 L6 9.4 L7.6 9.5 Z"
      stroke={color} strokeWidth="1.2" {...S} />
    {/* Звёздочка 3 (маленькая, справа) */}
    <path d="M23.5 13 L23.8 14.2 L25 14.1 L24.1 14.8 L24.5 16 L23.5 15.3 L22.5 16 L22.9 14.8 L22 14.1 L23.2 14.2 Z"
      stroke={color} strokeWidth="1.2" {...S} />
  </svg>
)

/* ─────────────────────────────────────────────────────────────────────
   ЭКСПОРТ — именованный справочник
───────────────────────────────────────────────────────────────────── */

export const ICONS = {
  family:         FamilyIcon,
  husband:        HusbandIcon,
  wife:           WifeIcon,
  child:          ChildIcon,
  motherInLaw:    MotherInLawIcon,
  relatives:      RelativesIcon,
  love:           LoveIcon,
  hugs:           HugsIcon,
  support:        SupportIcon,
  trust:          TrustIcon,
  reconciliation: ReconciliationIcon,
  conflict:       ConflictIcon,
  gratitude:      GratitudeIcon,
  happiness:      HappinessIcon,
  communication:  CommunicationIcon,
  dialogue:       DialogueIcon,
  home:           HomeIcon,
  safety:         SafetyIcon,
  progress:       ProgressIcon,
  calendar:       CalendarIcon,
  recoveryPlan:   RecoveryPlanIcon,
  achievements:   AchievementsIcon,
  familyMemory:   FamilyMemoryIcon,
  familyGoals:    FamilyGoalsIcon,
  togetherTime:   TogetherTimeIcon,
  walk:           WalkIcon,
  travel:         TravelIcon,
  finances:       FinancesIcon,
  budget:         BudgetIcon,
  bridge:         BridgeIcon,
  aiConsultant:   AiConsultantIcon,
} as const

export type IconName = keyof typeof ICONS
