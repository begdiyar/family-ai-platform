import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import HttpBackend from 'i18next-http-backend'

export const SUPPORTED_LANGS = [
  { code: 'ru',      label: 'RU', name: 'Русский' },
  { code: 'uz',      label: 'UZ', name: "O'zbekcha" },
  { code: 'uz_cyrl', label: 'ЎЗ', name: 'Ўзбекча' },
  { code: 'en',      label: 'EN', name: 'English' },
] as const

export type LangCode = (typeof SUPPORTED_LANGS)[number]['code']

i18n
  .use(HttpBackend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'ru',
    supportedLngs: SUPPORTED_LANGS.map((l) => l.code),
    preload: SUPPORTED_LANGS.map((l) => l.code),
    ns: ['common', 'auth', 'dashboard', 'diagnostics', 'analytics', 'index', 'academy', 'practices', 'ai', 'mediation', 'couple', 'profile'],
    defaultNS: 'common',
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
      lookupLocalStorage: 'lang',
    },
    interpolation: {
      escapeValue: false,
    },
  })

export default i18n
