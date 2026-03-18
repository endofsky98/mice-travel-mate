'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Search, UtensilsCrossed, List, Map } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import RestaurantCard from '@/components/restaurant/RestaurantCard';
import RestaurantFilters from '@/components/restaurant/RestaurantFilters';
import Pagination from '@/components/ui/Pagination';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Input from '@/components/ui/Input';
import MapView from '@/components/map/MapView';
import { Restaurant } from '@/types';
import { cn } from '@/lib/utils';

export default function RestaurantsPage() {
  const { t, lt, language } = useLanguage();
  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [priceRange, setPriceRange] = useState('');
  const [sortBy, setSortBy] = useState('recommended');
  const [viewMode, setViewMode] = useState<'list' | 'map'>('list');

  const eventId = searchParams.get('event_id');

  useEffect(() => {
    const fetchRestaurants = async () => {
      setLoading(true);
      try {
        const params: Record<string, string | number | boolean | undefined> = {
          page: currentPage,
          per_page: viewMode === 'map' ? 50 : 12,
          search: search || undefined,
          category: category || undefined,
          price_range: priceRange || undefined,
          sort: sortBy || undefined,
          event_id: eventId || undefined,
        };
        const data = await api.get<{ items: Restaurant[]; pages: number }>('/api/restaurants', params);
        setRestaurants(data.items || []);
        setTotalPages(data.pages || 1);
      } catch {
        setRestaurants([]);
      }
      setLoading(false);
    };
    fetchRestaurants();
  }, [currentPage, search, category, priceRange, sortBy, eventId, language, viewMode]);

  const markers = restaurants
    .filter((r) => (r.lat || r.latitude) && (r.lng || r.longitude))
    .map((r) => ({
      id: r.id,
      lat: r.lat || r.latitude || 0,
      lng: r.lng || r.longitude || 0,
      title: lt(r.name),
      type: 'restaurant',
      rating: r.avg_rating,
    }));

  return (
    <div className="page-container">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t('nav.restaurants')}</h1>
        {/* View Toggle */}
        <div className="flex rounded-lg border border-gray-200 dark:border-gray-500/40 overflow-hidden">
          <button
            onClick={() => setViewMode('list')}
            className={cn(
              'flex items-center gap-1 px-3 py-1.5 text-sm',
              viewMode === 'list'
                ? 'bg-indigo-600 text-white'
                : 'bg-white dark:bg-[#1e1e1e] text-gray-600 dark:text-gray-300'
            )}
          >
            <List className="w-4 h-4" /> {t('common.list') || 'List'}
          </button>
          <button
            onClick={() => setViewMode('map')}
            className={cn(
              'flex items-center gap-1 px-3 py-1.5 text-sm',
              viewMode === 'map'
                ? 'bg-indigo-600 text-white'
                : 'bg-white dark:bg-[#1e1e1e] text-gray-600 dark:text-gray-300'
            )}
          >
            <Map className="w-4 h-4" /> {t('common.map') || 'Map'}
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            placeholder={t('common.search') || 'Search...'}
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setCurrentPage(1);
            }}
            className="pl-10"
          />
        </div>
      </div>

      {/* Filters */}
      <div className="mb-6">
        <RestaurantFilters
          t={t}
          category={category}
          priceRange={priceRange}
          sortBy={sortBy}
          onCategoryChange={(v) => { setCategory(v); setCurrentPage(1); }}
          onPriceRangeChange={(v) => { setPriceRange(v); setCurrentPage(1); }}
          onSortChange={setSortBy}
        />
      </div>

      {/* Results */}
      {loading ? (
        <LoadingSpinner fullPage />
      ) : restaurants.length === 0 ? (
        <EmptyState
          icon={UtensilsCrossed}
          title={t('common.no_results') || 'No results'}
          description={t('common.try_different_filters') || 'Try different filters'}
        />
      ) : viewMode === 'map' ? (
        <div className="h-[calc(100vh-280px)] rounded-xl overflow-hidden">
          <MapView markers={markers} t={t} className="h-full" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {restaurants.map((r) => (
              <RestaurantCard key={r.id} restaurant={r} lt={lt} />
            ))}
          </div>
          <div className="mt-8">
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </div>
        </>
      )}
    </div>
  );
}
