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

function CalendarView({ festivals, lt, t }: { festivals: Festival[]; lt: (v: any) => string; t: (key: string) => string }) {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const days = Array.from({ length: firstDay + daysInMonth }, (_, i) => i < firstDay ? null : i - firstDay + 1);
  const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const getFestivalsForDay = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return festivals.filter(f => {
      if (!f.start_date || !f.end_date) return false;
      return dateStr >= f.start_date.slice(0, 10) && dateStr <= f.end_date.slice(0, 10);
    });
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <button onClick={() => setCurrentMonth(new Date(year, month - 1, 1))} className="p-2 hover:bg-gray-100 dark:hover:bg-white/[0.05] rounded-lg text-gray-600 dark:text-gray-300">&lt;</button>
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          {currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
        </h2>
        <button onClick={() => setCurrentMonth(new Date(year, month + 1, 1))} className="p-2 hover:bg-gray-100 dark:hover:bg-white/[0.05] rounded-lg text-gray-600 dark:text-gray-300">&gt;</button>
      </div>
      <div className="grid grid-cols-7 gap-px bg-gray-200 dark:bg-gray-700 rounded-xl overflow-hidden">
        {weekDays.map(d => (
          <div key={d} className="bg-gray-50 dark:bg-[#1a1a1a] p-2 text-center text-xs font-medium text-gray-500 dark:text-gray-400">{d}</div>
        ))}
        {days.map((day, i) => {
          const dayFestivals = day ? getFestivalsForDay(day) : [];
          return (
            <div key={i} className={cn('bg-white dark:bg-[#1e1e1e] min-h-[80px] p-1', !day && 'bg-gray-50 dark:bg-[#141414]')}>
              {day && (
                <>
                  <span className="text-xs text-gray-500 dark:text-gray-400">{day}</span>
                  {dayFestivals.slice(0, 2).map(f => (
                    <Link key={f.id} href={`/festivals/${f.id}`} className="block mt-0.5 px-1 py-0.5 text-[10px] bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-300 rounded truncate hover:bg-pink-200 dark:hover:bg-pink-900/50">
                      {lt(f.name)}
                    </Link>
                  ))}
                  {dayFestivals.length > 2 && <span className="text-[10px] text-gray-400 pl-1">+{dayFestivals.length - 2}</span>}
                </>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function FestivalsPage() {
  const { t, lt, language } = useLanguage();
  const [festivals, setFestivals] = useState<Festival[]>([]);
  const [totalCount, setTotalCount] = useState(0);
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
        const data = await api.get<{ items: Festival[]; total: number }>('/api/festivals', {
          category: categoryFilter || undefined,
          per_page: 100,
        });
        setFestivals(data.items || []);
        setTotalCount(data.total || 0);
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
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {t('home.festivals_events') || 'Festivals & Events'}
          </h1>
          {!loading && totalCount > 0 && (
            <span className="text-sm text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-white/[0.08] px-2 py-0.5 rounded-full">
              {totalCount.toLocaleString()} items
            </span>
          )}
        </div>
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
      ) : viewMode === 'calendar' ? (
        /* Calendar View */
        <CalendarView festivals={festivals} lt={lt} t={t} />
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
