'use client';

import { useState, useEffect } from 'react';
import { MapPin, Search, Navigation, X } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import FilterChips from '@/components/ui/FilterChips';
import Card from '@/components/ui/Card';
import StarRating from '@/components/ui/StarRating';
import Link from 'next/link';
import { Restaurant, Guide, Festival } from '@/types';

export default function MapPage() {
  const { t, lt, language } = useLanguage();
  const [categoryFilter, setCategoryFilter] = useState('restaurants');
  const [searchQuery, setSearchQuery] = useState('');
  const [items, setItems] = useState<any[]>([]);
  const [selectedItem, setSelectedItem] = useState<any>(null);

  const categoryChips = [
    { key: 'restaurants', label: t('nav.restaurants') || 'Restaurants' },
    { key: 'courses', label: t('nav.courses') || 'Courses' },
    { key: 'guides', label: t('nav.guides') || 'Guides' },
    { key: 'festivals', label: t('home.festivals_events') || 'Festivals' },
  ];

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const endpoint = categoryFilter === 'festivals' ? '/api/festivals' : `/api/${categoryFilter}`;
        const data = await api.get<{ items: any[] }>(endpoint, { per_page: 50 });
        setItems(data.items || []);
      } catch {
        setItems([]);
      }
    };
    fetchItems();
  }, [categoryFilter, language]);

  return (
    <div className="relative h-[calc(100vh-64px)] md:h-[calc(100vh-64px)] flex flex-col">
      {/* Search & Filters Overlay */}
      <div className="absolute top-0 left-0 right-0 z-10 p-4 space-y-2">
        <div className="relative max-w-lg mx-auto">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t('map.search_places') || 'Search places...'}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white dark:bg-[#1e1e1e] shadow-lg border border-gray-200 dark:border-gray-500/40 text-sm outline-none focus:ring-2 focus:ring-indigo-600/20"
          />
        </div>
        <div className="max-w-lg mx-auto">
          <FilterChips chips={categoryChips} selected={categoryFilter} onSelect={(k) => k && setCategoryFilter(k)} />
        </div>
      </div>

      {/* Map Area */}
      <div className="flex-1 bg-gray-100 dark:bg-gray-900 flex items-center justify-center relative">
        <div className="text-center text-gray-400">
          <MapPin className="w-16 h-16 mx-auto mb-4 opacity-30" />
          <p className="text-lg font-medium">{t('map.explore_title') || 'Map Explorer'}</p>
          <p className="text-sm mt-1">{items.length} {categoryFilter} {t('common.found') || 'found'}</p>
        </div>

        {/* Item markers (simplified - shown as cards at bottom) */}
        {items.length > 0 && (
          <div className="absolute bottom-4 left-0 right-0 px-4">
            <div className="flex gap-3 overflow-x-auto scrollbar-hide pb-2">
              {items.slice(0, 10).map((item: any) => (
                <Link
                  key={item.id}
                  href={`/${categoryFilter}/${item.id}`}
                  className="flex-shrink-0 w-[200px]"
                >
                  <Card hoverable className="p-3">
                    <h3 className="font-medium text-sm text-gray-900 dark:text-gray-100 line-clamp-1">
                      {lt(item.name || item.name_en)}
                    </h3>
                    {item.avg_rating > 0 && (
                      <StarRating rating={item.avg_rating} size="sm" showValue />
                    )}
                    <p className="text-xs text-gray-400 mt-1 line-clamp-1">
                      {lt(item.description || item.address || '')}
                    </p>
                  </Card>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* My Location Button */}
      <button className="absolute bottom-24 right-4 w-12 h-12 bg-white dark:bg-[#1e1e1e] rounded-full shadow-lg flex items-center justify-center text-indigo-600 dark:text-indigo-400 z-10">
        <Navigation className="w-5 h-5" />
      </button>
    </div>
  );
}
