'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Scale, MapPin, Star, ExternalLink } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import StarRating from '@/components/ui/StarRating';
import Link from 'next/link';

export default function ComparePage() {
  const { t, lt, language } = useLanguage();
  const searchParams = useSearchParams();
  const type = searchParams.get('type') || 'restaurant';
  const ids = (searchParams.get('ids') || '').split(',').filter(Boolean);
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (ids.length === 0) {
      setLoading(false);
      return;
    }
    const fetch = async () => {
      try {
        const endpoint = type === 'restaurant' ? 'restaurants' : type === 'course' ? 'courses' : type === 'product' ? 'products' : 'guides';
        const data = await api.get<{ items: any[] }>(`/api/${endpoint}`, { ids: ids.join(',') });
        setItems(data.items || []);
      } catch {
        setItems([]);
      }
      setLoading(false);
    };
    fetch();
  }, [type, language]);

  if (loading) return <LoadingSpinner fullPage />;

  const typeLabel = type === 'restaurant' ? t('nav.restaurants') : type === 'course' ? t('nav.courses') : type === 'product' ? t('nav.products') : t('nav.guides');

  return (
    <div className="page-container">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6 flex items-center gap-2">
        <Scale className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
        {t('compare.title') || 'Compare'} - {typeLabel}
      </h1>

      {items.length === 0 ? (
        <p className="text-center text-gray-400 py-12">{t('compare.select_items') || 'No items to compare'}</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[600px]">
            <thead>
              <tr>
                <th className="text-left p-3 text-sm text-gray-500 dark:text-gray-400 w-32"></th>
                {items.map((item) => (
                  <th key={item.id} className="p-3 text-center">
                    <div className="space-y-2">
                      {(item.images?.[0] || item.image_url || item.profile_image_url) && (
                        <img src={item.images?.[0] || item.image_url || item.profile_image_url} alt="" className="w-full h-32 object-cover rounded-xl" />
                      )}
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{lt(item.name)}</h3>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {/* Rating */}
              <tr className="border-t border-gray-100 dark:border-gray-500/40">
                <td className="p-3 text-sm text-gray-500">{t('label.rating') || 'Rating'}</td>
                {items.map((item) => (
                  <td key={item.id} className="p-3 text-center">
                    {item.avg_rating > 0 ? (
                      <div className="flex justify-center">
                        <StarRating rating={item.avg_rating} size="sm" showValue reviewCount={item.review_count} />
                      </div>
                    ) : '-'}
                  </td>
                ))}
              </tr>
              {/* Price */}
              <tr className="border-t border-gray-100 dark:border-gray-500/40">
                <td className="p-3 text-sm text-gray-500">{t('label.price') || 'Price'}</td>
                {items.map((item) => (
                  <td key={item.id} className="p-3 text-center font-medium text-indigo-600 dark:text-indigo-400">
                    {item.price_usd ? `$${item.price_usd}` : item.price_per_hour_usd ? `$${item.price_per_hour_usd}/hr` : item.price_range ? '$'.repeat(item.price_range) : '-'}
                  </td>
                ))}
              </tr>
              {/* Category */}
              <tr className="border-t border-gray-100 dark:border-gray-500/40">
                <td className="p-3 text-sm text-gray-500">{t('label.category') || 'Category'}</td>
                {items.map((item) => (
                  <td key={item.id} className="p-3 text-center text-sm text-gray-700 dark:text-gray-300 capitalize">
                    {item.category || item.theme || (item.specialties || []).join(', ') || '-'}
                  </td>
                ))}
              </tr>
              {/* Actions */}
              <tr className="border-t border-gray-100 dark:border-gray-500/40">
                <td className="p-3 text-sm text-gray-500"></td>
                {items.map((item) => {
                  const endpoint = type === 'restaurant' ? 'restaurants' : type === 'course' ? 'courses' : type === 'product' ? 'products' : 'guides';
                  return (
                    <td key={item.id} className="p-3 text-center">
                      <Link href={`/${endpoint}/${item.id}`}>
                        <Button size="sm" variant="outline">
                          {t('button.view_details') || 'Details'}
                        </Button>
                      </Link>
                    </td>
                  );
                })}
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
