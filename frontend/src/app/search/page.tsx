'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Search } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Tabs from '@/components/ui/Tabs';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import StarRating from '@/components/ui/StarRating';
import Link from 'next/link';

export default function SearchPage() {
  const { t, lt, language } = useLanguage();
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';
  const [activeTab, setActiveTab] = useState('all');
  const [results, setResults] = useState<any>({});
  const [loading, setLoading] = useState(true);

  const tabs = [
    { id: 'all', label: t('common.all') || 'All' },
    { id: 'restaurants', label: t('nav.restaurants') || 'Restaurants' },
    { id: 'courses', label: t('nav.courses') || 'Courses' },
    { id: 'products', label: t('nav.products') || 'Products' },
    { id: 'guides', label: t('nav.guides') || 'Guides' },
    { id: 'festivals', label: t('home.festivals_events') || 'Festivals' },
  ];

  useEffect(() => {
    if (!query) return;
    const fetchResults = async () => {
      setLoading(true);
      try {
        const data = await api.get<any>('/api/search', { q: query, category: activeTab === 'all' ? undefined : activeTab });
        setResults(data);
      } catch {
        setResults({});
      }
      setLoading(false);
    };
    fetchResults();
  }, [query, activeTab, language]);

  const allItems = [
    ...(results.restaurants || []).map((r: any) => ({ ...r, _type: 'restaurants' })),
    ...(results.courses || []).map((c: any) => ({ ...c, _type: 'courses' })),
    ...(results.products || []).map((p: any) => ({ ...p, _type: 'products' })),
    ...(results.guides || []).map((g: any) => ({ ...g, _type: 'guides' })),
    ...(results.festivals || []).map((f: any) => ({ ...f, _type: 'festivals' })),
  ];

  const displayItems = activeTab === 'all' ? allItems : (results[activeTab] || []).map((item: any) => ({ ...item, _type: activeTab }));

  return (
    <div className="page-container">
      <div className="flex items-center gap-3 mb-6">
        <Search className="w-6 h-6 text-gray-400" />
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          "{query}"
        </h1>
        <span className="text-sm text-gray-400">
          {displayItems.length} {t('common.results') || 'results'}
        </span>
      </div>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

      {loading ? <LoadingSpinner fullPage /> : displayItems.length === 0 ? (
        <EmptyState icon={Search} title={t('common.no_results') || 'No results found'} />
      ) : (
        <div className="space-y-3">
          {displayItems.map((item: any, i: number) => (
            <Link key={`${item._type}-${item.id}-${i}`} href={`/${item._type}/${item.id}`}>
              <Card hoverable className="p-4 flex gap-4">
                {(item.images?.[0] || item.image_url || item.profile_image_url) && (
                  <img
                    src={item.images?.[0] || item.image_url || item.profile_image_url}
                    alt=""
                    className="w-20 h-20 rounded-lg object-cover flex-shrink-0"
                  />
                )}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 capitalize">
                      {item._type}
                    </span>
                  </div>
                  <h3 className="font-medium text-gray-900 dark:text-gray-100 line-clamp-1">
                    {lt(item.name) || lt(item.name_en)}
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-1 mt-0.5">
                    {lt(item.description) || lt(item.description_en) || ''}
                  </p>
                  {item.avg_rating > 0 && (
                    <StarRating rating={item.avg_rating} size="sm" showValue reviewCount={item.review_count} />
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
