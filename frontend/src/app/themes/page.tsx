'use client';

import { useEffect, useState } from 'react';
import { Map, MapPin } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import { ThemeData } from '@/types';

export default function ThemesPage() {
  const { t, lt, language } = useLanguage();
  const [themes, setThemes] = useState<ThemeData[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await api.get<{ items: ThemeData[] }>('/api/themes');
        setThemes(data.items || []);
      } catch {
        setThemes([]);
      }
      setLoading(false);
    };
    fetch();
  }, [language]);

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div className="page-container">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6 flex items-center gap-2">
        <Map className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
        {t('nav.themes') || 'Theme Travel Map'}
      </h1>

      {themes.length === 0 ? (
        <EmptyState icon={Map} title={t('common.no_results') || 'No themes available'} />
      ) : (
        <>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mb-8">
            {themes.map((theme) => (
              <button
                key={theme.id}
                onClick={() => setSelectedTheme(selectedTheme === theme.id ? null : theme.id)}
                className={`text-left rounded-xl p-4 border transition-all ${
                  selectedTheme === theme.id
                    ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20 dark:border-indigo-500'
                    : 'border-gray-200 dark:border-gray-500/40 hover:border-gray-300'
                }`}
              >
                <div className="text-2xl mb-2">{theme.icon || '📍'}</div>
                <h3 className="font-medium text-sm text-gray-900 dark:text-gray-100">{lt(theme.name)}</h3>
                {theme.color && (
                  <div className="w-4 h-4 rounded-full mt-2" style={{ backgroundColor: theme.color }} />
                )}
              </button>
            ))}
          </div>

          {/* Map Placeholder */}
          <div className="h-[400px] rounded-xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <MapPin className="w-12 h-12 mx-auto mb-2" />
              <p className="text-sm">
                {selectedTheme ? 'Showing theme spots on map' : 'Select a theme to see spots'}
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
