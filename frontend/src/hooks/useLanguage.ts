'use client';

import { useState, useEffect, useCallback } from 'react';
import { Language, Translations } from '@/types';
import { getStoredLanguage, setStoredLanguage, loadTranslations, getTranslation, getLocalizedText } from '@/lib/i18n';

export function useLanguage() {
  const [language, setLanguageState] = useState<Language>('en');
  const [translations, setTranslations] = useState<Translations>({});
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const initLanguage = async () => {
      let lang: Language = 'en';

      if (typeof window !== 'undefined') {
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang') as Language;
        if (urlLang && ['en', 'ko', 'ja', 'zh-CN', 'zh-TW', 'es'].includes(urlLang)) {
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
  }, []);

  const setLanguage = useCallback(async (lang: Language) => {
    setStoredLanguage(lang);
    setLanguageState(lang);
    const t = await loadTranslations(lang);
    setTranslations(t);
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
