import { Language, Translations } from '@/types';

const translationCache: Record<string, Translations> = {};

export function getStoredLanguage(): Language {
  if (typeof window === 'undefined') return 'en';
  const stored = localStorage.getItem('language') as Language;
  if (stored) return stored;

  const browserLang = navigator.language;
  if (browserLang.startsWith('ko')) return 'ko';
  if (browserLang.startsWith('ja')) return 'ja';
  if (browserLang === 'zh-CN' || browserLang === 'zh-Hans') return 'zh-CN';
  if (browserLang === 'zh-TW' || browserLang === 'zh-Hant' || browserLang.startsWith('zh')) return 'zh-TW';
  if (browserLang.startsWith('es')) return 'es';

  return 'en';
}

export function setStoredLanguage(lang: Language): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('language', lang);
}

export async function loadTranslations(lang: Language): Promise<Translations> {
  if (translationCache[lang]) {
    return translationCache[lang];
  }

  try {
    const response = await fetch(`/locales/${lang}/common.json`);
    if (!response.ok) {
      throw new Error(`Failed to load translations for ${lang}`);
    }
    const data = await response.json();
    translationCache[lang] = data;
    return data;
  } catch {
    if (lang !== 'en') {
      return loadTranslations('en');
    }
    return {};
  }
}

export function getTranslation(translations: Translations, key: string): string {
  const keys = key.split('.');
  let current: unknown = translations;

  for (const k of keys) {
    if (current && typeof current === 'object' && k in (current as Record<string, unknown>)) {
      current = (current as Record<string, unknown>)[k];
    } else {
      return key;
    }
  }

  if (typeof current === 'string') {
    return current;
  }

  return key;
}

export function getLocalizedText(
  text: string | Record<string, string | undefined> | undefined | null,
  lang: Language
): string {
  if (!text) return '';
  if (typeof text === 'string') return text;
  return text[lang] || text['en'] || Object.values(text).find((v) => v) || '';
}
