'use client';

import { useEffect, useState } from 'react';
import { Map, MapPin } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import MapView from '@/components/map/MapView';
import { ThemeData, MapMarker } from '@/types';
import { cn } from '@/lib/utils';

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

  const selectedThemeData = themes.find(t => t.id === selectedTheme);

  const markers: MapMarker[] = selectedThemeData?.spots
    ?.filter(s => s.lat && s.lng)
    .map(s => ({
      id: s.id,
      lat: s.lat!,
      lng: s.lng!,
      title: s.name || lt(selectedThemeData.name),
      type: selectedThemeData.name ? lt(selectedThemeData.name) : 'spot',
    })) || [];

  return (
    <div className="page-container pb-20 md:pb-8">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6 flex items-center gap-2">
        <Map className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
        {t('nav.themes') || 'Theme Travel Map'}
      </h1>

      {themes.length === 0 ? (
        <EmptyState icon={Map} title={t('common.no_results') || 'No themes available'} />
      ) : (
        <>
          {/* Theme Selection */}
          <div className="flex gap-3 overflow-x-auto scrollbar-hide pb-3 mb-4">
            {themes.map((theme) => (
              <button
                key={theme.id}
                onClick={() => setSelectedTheme(selectedTheme === theme.id ? null : theme.id)}
                className={cn(
                  'flex-shrink-0 flex items-center gap-2 px-4 py-2.5 rounded-xl border transition-all text-sm font-medium',
                  selectedTheme === theme.id
                    ? 'border-indigo-600 bg-indigo-50 text-indigo-700 dark:bg-indigo-900/20 dark:border-indigo-500 dark:text-indigo-300'
                    : 'border-gray-200 dark:border-gray-500/40 text-gray-700 dark:text-gray-300 hover:border-gray-300'
                )}
              >
                <span className="text-lg">{theme.icon || '📍'}</span>
                <span>{lt(theme.name)}</span>
                {theme.color && (
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: theme.color }} />
                )}
              </button>
            ))}
          </div>

          {/* Map */}
          <div className="h-[calc(100vh-280px)] min-h-[400px] rounded-xl overflow-hidden">
            {markers.length > 0 ? (
              <MapView
                markers={markers}
                t={t}
                className="h-full w-full rounded-xl"
              />
            ) : (
              <div className="w-full h-full bg-gray-100 dark:bg-[#1a1a1a] rounded-xl flex items-center justify-center">
                <div className="text-center text-gray-400">
                  <MapPin className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p className="text-sm font-medium">
                    {selectedTheme
                      ? t('theme.no_spots') || 'No spots for this theme yet'
                      : t('theme.select_prompt') || 'Select a theme to explore spots on the map'}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Theme Description */}
          {selectedThemeData && lt(selectedThemeData.description) && (
            <div className="mt-4 p-4 bg-gray-50 dark:bg-[#1a1a1a] rounded-xl">
              <p className="text-sm text-gray-600 dark:text-gray-300">{lt(selectedThemeData.description)}</p>
            </div>
          )}

          {/* Spot Count */}
          {selectedThemeData && markers.length > 0 && (
            <p className="mt-3 text-xs text-gray-400">
              {markers.length} {t('theme.spots_found') || 'spots found'}
            </p>
          )}
        </>
      )}
    </div>
  );
}
