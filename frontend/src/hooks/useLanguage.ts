'use client';

import { useState, useEffect, useCallback } from 'react';
import { Language, Translations, SUPPORTED_LANGUAGES } from '@/types';
import { getStoredLanguage, setStoredLanguage, loadTranslations, getTranslation, getLocalizedText } from '@/lib/i18n';

const VALID_LANGUAGES = SUPPORTED_LANGUAGES.map(l => l.code);

export function useLanguage() {
  const [language, setLanguageState] = useState<Language>(() => {
    if (typeof window !== 'undefined') {
      return getStoredLanguage();
    }
    return 'en';
  });
  const [translations, setTranslations] = useState<Translations>({});
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const initLanguage = async () => {
      let lang: Language = 'en';

      if (typeof window !== 'undefined') {
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang') as Language;
        if (urlLang && VALID_LANGUAGES.includes(urlLang)) {
          lang = urlLang;
          setStoredLanguage(lang);
        } else {
          lang = getStoredLanguage();
        }
      }

      setLanguageState(lang);
      const t = await loadTranslations(lang);
      setTranslations(t);
      setIsLoaded(true);
    };

    initLanguage();

    // 언어 변경 브로드캐스트 수신 (같은 탭 내 모든 useLanguage 인스턴스 동기화)
    const handleStorageChange = async (e: StorageEvent) => {
      if (e.key === 'language' && e.newValue && VALID_LANGUAGES.includes(e.newValue as Language)) {
        const lang = e.newValue as Language;
        setLanguageState(lang);
        const t = await loadTranslations(lang);
        setTranslations(t);
      }
    };
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const setLanguage = useCallback(async (lang: Language) => {
    setStoredLanguage(lang);
    setLanguageState(lang);
    const t = await loadTranslations(lang);
    setTranslations(t);
    // Update html lang attribute for accessibility
    if (typeof document !== 'undefined') {
      document.documentElement.lang = lang;
    }
  }, []);

  const t = useCallback(
    (key: string): string => {
      return getTranslation(translations, key);
    },
    [translations]
  );

  const lt = useCallback(
    (text: string | Record<string, string | undefined> | undefined | null): string => {
      return getLocalizedText(text, language);
    },
    [language]
  );

  return { language, setLanguage, t, lt, isLoaded };
}
