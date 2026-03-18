'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Search, UtensilsCrossed } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import RestaurantCard from '@/components/restaurant/RestaurantCard';
import RestaurantFilters from '@/components/restaurant/RestaurantFilters';
import Pagination from '@/components/ui/Pagination';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Input from '@/components/ui/Input';
import { Restaurant } from '@/types';

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
  const [sortBy, setSortBy] = useState('distance');

  const eventId = searchParams.get('event_id');

  useEffect(() => {
    const fetchRestaurants = async () => {
      setLoading(true);
      try {
        const params: Record<string, string | number | boolean | undefined> = {
          page: currentPage,
          per_page: 12,
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
  }, [currentPage, search, category, priceRange, sortBy, eventId, language]);

  return (
    <div className="page-container">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('nav.restaurants')}</h1>

      {/* Search */}
      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            placeholder={t('common.search')}
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
          title={t('common.no_results')}
          description={t('common.no_results')}
        />
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
