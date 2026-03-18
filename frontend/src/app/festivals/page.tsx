'use client';

import { useEffect, useState } from 'react';
import { Calendar, List, MapPin } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import FilterChips from '@/components/ui/FilterChips';
import { Festival } from '@/types';
import { formatDateRange } from '@/lib/utils';
import { cn } from '@/lib/utils';
import Link from 'next/link';

export default function FestivalsPage() {
  const { t, lt, language } = useLanguage();
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'list' | 'calendar'>('list');
  const [categoryFilter, setCategoryFilter] = useState('');

  const categories = [
    { key: '', label: t('common.all') || 'All' },
    { key: 'festival', label: t('festival.type_festival') || 'Festival' },
    { key: 'performance', label: t('festival.type_performance') || 'Performance' },
    { key: 'market', label: t('festival.type_market') || 'Market' },
    { key: 'exhibition', label: t('festival.type_exhibition') || 'Exhibition' },
  ];

  useEffect(() => {
    const fetch = async () => {
      setLoading(true);
      try {
        const data = await api.get<{ items: Festival[] }>('/api/festivals', {
          category: categoryFilter || undefined,
          per_page: 50,
        });
        setFestivals(data.items || []);
      } catch {
        setFestivals([]);
      }
      setLoading(false);
    };
    fetch();
  }, [language, categoryFilter]);

  return (
    <div className="page-container">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          {t('home.festivals_events') || 'Festivals & Events'}
        </h1>
        <div className="flex rounded-lg border border-gray-200 dark:border-gray-500/40 overflow-hidden">
          <button onClick={() => setViewMode('list')} className={cn('flex items-center gap-1 px-3 py-1.5 text-sm', viewMode === 'list' ? 'bg-indigo-600 text-white' : 'bg-white dark:bg-[#1e1e1e] text-gray-600 dark:text-gray-300')}>
            <List className="w-4 h-4" />
          </button>
          <button onClick={() => setViewMode('calendar')} className={cn('flex items-center gap-1 px-3 py-1.5 text-sm', viewMode === 'calendar' ? 'bg-indigo-600 text-white' : 'bg-white dark:bg-[#1e1e1e] text-gray-600 dark:text-gray-300')}>
            <Calendar className="w-4 h-4" />
          </button>
        </div>
      </div>

      <FilterChips chips={categories} selected={categoryFilter} onSelect={setCategoryFilter} className="mb-6" />

      {loading ? <LoadingSpinner fullPage /> : festivals.length === 0 ? (
        <EmptyState icon={Calendar} title={t('common.no_results') || 'No festivals found'} />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {festivals.map((f) => (
            <Link key={f.id} href={`/festivals/${f.id}`}>
              <Card hoverable className="h-full">
                <div className="relative aspect-[16/10] overflow-hidden">
                  {f.image_url ? (
                    <img src={f.image_url} alt={lt(f.name)} className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-pink-500 to-orange-500 flex items-center justify-center">
                      <Calendar className="w-10 h-10 text-white/60" />
                    </div>
                  )}
                  {f.category && (
                    <span className="absolute top-3 left-3 px-2 py-1 bg-black/60 backdrop-blur-sm text-white text-xs rounded-lg">
                      {f.category}
                    </span>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">{lt(f.name)}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                    {f.start_date && f.end_date ? formatDateRange(f.start_date, f.end_date) : ''}
                  </p>
                  {f.venue_name && (
                    <p className="text-xs text-gray-400 flex items-center gap-1">
                      <MapPin className="w-3 h-3" /> {f.venue_name}
                    </p>
                  )}
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
