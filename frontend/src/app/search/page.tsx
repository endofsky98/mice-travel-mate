'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Search, Utensils, Map, ShoppingBag, Users, Calendar } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Link from 'next/link';

interface SearchItem {
  type: string;
  id: string;
  name: string;
  description?: string;
  image_url?: string;
  category?: string;
  price_usd?: number;
  start_date?: string;
  end_date?: string;
  latitude?: number;
  longitude?: number;
}

interface SearchResponse {
  query: string;
  items: SearchItem[];
  total: number;
  page: number;
  per_page: number;
}

const typeConfig: Record<string, { href: string; icon: typeof Search; color: string }> = {
  restaurant: { href: '/restaurants', icon: Utensils, color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400' },
  course: { href: '/courses', icon: Map, color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' },
  product: { href: '/products', icon: ShoppingBag, color: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400' },
  guide: { href: '/guides', icon: Users, color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400' },
  festival: { href: '/festivals', icon: Calendar, color: 'bg-pink-100 text-pink-600 dark:bg-pink-900/30 dark:text-pink-400' },
};

export default function SearchPage() {
  const { t, language } = useLanguage();
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';
  const [activeTab, setActiveTab] = useState('all');
  const [results, setResults] = useState<SearchItem[]>([]);
  const [loading, setLoading] = useState(true);

  const tabs = [
    { id: 'all', label: t('search.category_all') || t('common.all') || 'All' },
    { id: 'restaurant', label: t('search.category_restaurant') || t('nav.restaurants') || 'Restaurants' },
    { id: 'course', label: t('search.category_course') || t('nav.courses') || 'Courses' },
    { id: 'product', label: t('search.category_product') || t('nav.products') || 'Products' },
    { id: 'guide', label: t('search.category_guide') || t('nav.guides') || 'Guides' },
    { id: 'festival', label: t('search.category_festival') || t('nav.festivals') || 'Festivals' },
  ];

  useEffect(() => {
    if (!query) {
      setLoading(false);
      return;
    }
    const fetchResults = async () => {
      setLoading(true);
      try {
        const data = await api.get<SearchResponse>('/api/search', { q: query });
        setResults(data.items || []);
      } catch {
        setResults([]);
      }
      setLoading(false);
    };
    fetchResults();
  }, [query, language]);

  const displayItems = activeTab === 'all'
    ? results
    : results.filter((item) => item.type === activeTab);

  const getItemHref = (item: SearchItem) => {
    const config = typeConfig[item.type];
    return config ? `${config.href}/${item.id}` : '#';
  };

  const getTypeLabel = (type: string) => {
    const labelMap: Record<string, string> = {
      restaurant: t('nav.restaurants') || 'Restaurants',
      course: t('nav.courses') || 'Courses',
      product: t('nav.products') || 'Products',
      guide: t('nav.guides') || 'Guides',
      festival: t('nav.festivals') || 'Festivals',
    };
    return labelMap[type] || type;
  };

  if (!query) {
    return (
      <div className="pb-20 md:pb-0">
        <div className="max-w-3xl mx-auto px-4 py-12">
          <EmptyState
            icon={Search}
            title={t('home.search_placeholder') || 'Search restaurants, courses, guides...'}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="pb-20 md:pb-0">
      <div className="max-w-3xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center gap-3 mb-4">
          <Search className="w-5 h-5 text-gray-400" />
          <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
            &ldquo;{query}&rdquo;
          </h1>
          {!loading && (
            <span className="text-sm text-gray-400">
              {displayItems.length} {t('common.results') || 'results'}
            </span>
          )}
        </div>

        {/* Category tabs */}
        <div className="flex gap-2 overflow-x-auto scrollbar-hide mb-6 pb-1">
          {tabs.map((tab) => {
            const count = tab.id === 'all'
              ? results.length
              : results.filter((r) => r.type === tab.id).length;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-indigo-600 text-white dark:bg-indigo-500'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-[#2a2a2a] dark:text-gray-300 dark:hover:bg-[#333]'
                }`}
              >
                {tab.label} {count > 0 && `(${count})`}
              </button>
            );
          })}
        </div>

        {/* Results */}
        {loading ? (
          <LoadingSpinner fullPage />
        ) : displayItems.length === 0 ? (
          <EmptyState
            icon={Search}
            title={`${t('search.no_results') || 'No results found for'} "${query}"`}
            description={t('search.try_again') || 'Try different keywords'}
          />
        ) : (
          <div className="space-y-3">
            {displayItems.map((item, i) => {
              const config = typeConfig[item.type] || { href: '#', icon: Search, color: 'bg-gray-100 text-gray-600' };
              const Icon = config.icon;
              return (
                <Link key={`${item.type}-${item.id}-${i}`} href={getItemHref(item)}>
                  <Card hoverable className="p-4 flex gap-4">
                    {item.image_url ? (
                      <img
                        src={item.image_url}
                        alt={item.name}
                        className="w-20 h-20 rounded-lg object-cover flex-shrink-0"
                      />
                    ) : (
                      <div className="w-20 h-20 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center flex-shrink-0">
                        <Icon className="w-8 h-8 text-gray-300 dark:text-gray-600" />
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${config.color}`}>
                          {getTypeLabel(item.type)}
                        </span>
                        {item.category && (
                          <span className="text-xs text-gray-400 dark:text-gray-500">
                            {item.category}
                          </span>
                        )}
                      </div>
                      <h3 className="font-medium text-gray-900 dark:text-gray-100 line-clamp-1">
                        {item.name}
                      </h3>
                      {item.description && (
                        <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-1 mt-0.5">
                          {item.description}
                        </p>
                      )}
                      {item.price_usd && (
                        <p className="text-sm font-medium text-indigo-600 dark:text-indigo-400 mt-1">
                          ${item.price_usd.toFixed(0)}
                        </p>
                      )}
                    </div>
                  </Card>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
