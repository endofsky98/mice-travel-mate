'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, MapPin, Clock, Phone, Bookmark, BookmarkCheck, Share2, ExternalLink, Map } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useBookmarks } from '@/hooks/useBookmarks';
import { useAuth } from '@/hooks/useAuth';
import api from '@/lib/api';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import ImageGallery from '@/components/ui/ImageGallery';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import StarRating from '@/components/ui/StarRating';
import ReviewSection from '@/components/ui/ReviewSection';
import MapView from '@/components/map/MapView';
import { Restaurant } from '@/types';
import { getPriceRangeSymbol } from '@/lib/utils';

export default function RestaurantDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { t, lt, language } = useLanguage();
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const { isLoggedIn } = useAuth();
  const [loading, setLoading] = useState(true);
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);

  useEffect(() => {
    const fetchRestaurant = async () => {
      setLoading(true);
      try {
        const data = await api.get<Restaurant>(`/api/restaurants/${id}`);
        setRestaurant(data);
      } catch {
        setRestaurant(null);
      }
      setLoading(false);
    };
    fetchRestaurant();
  }, [id, language]);

  useEffect(() => {
    if (restaurant) document.title = `${lt(restaurant.name)} | Exporoute`;
  }, [restaurant, lt]);

  const handleShare = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: restaurant ? lt(restaurant.name) : '', url });
      } catch { /* user cancelled */ }
    } else {
      await navigator.clipboard.writeText(url);
      alert('Link copied!');
    }
  };

  if (loading) return <LoadingSpinner fullPage />;
  if (!restaurant) {
    return (
      <div className="page-container text-center py-20">
        <p className="text-gray-500">{t('common.no_results')}</p>
      </div>
    );
  }

  const name = lt(restaurant.name);
  const bookmarked = isBookmarked(restaurant.id, 'restaurant');
  const lat = restaurant.lat || restaurant.latitude;
  const lng = restaurant.lng || restaurant.longitude;
  const markers = lat && lng ? [{ id: restaurant.id, lat, lng, title: name }] : [];

  return (
    <div className="page-container max-w-4xl pb-20 md:pb-8">
      {/* Back Button */}
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        {t('common.back') || 'Back'}
      </button>

      {/* Image Gallery */}
      <ImageGallery images={restaurant.images || []} alt={name} className="mb-6" />

      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{name}</h1>
            <Badge>{restaurant.category}</Badge>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-lg font-medium text-indigo-600 dark:text-indigo-400">
              {getPriceRangeSymbol(restaurant.price_range)}
            </span>
            {restaurant.avg_rating && restaurant.avg_rating > 0 && (
              <StarRating
                rating={restaurant.avg_rating}
                size="sm"
                showValue
                reviewCount={restaurant.review_count}
              />
            )}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleShare}
          >
            <Share2 className="w-4 h-4" />
          </Button>
          <Button
            variant={bookmarked ? 'default' : 'outline'}
            size="sm"
            onClick={() => toggleBookmark(restaurant.id, 'restaurant')}
          >
            {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      {/* Description */}
      {lt(restaurant.description) && (
        <p className="text-gray-600 dark:text-gray-300 leading-relaxed mb-6">{lt(restaurant.description)}</p>
      )}

      {/* Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {lt(restaurant.address) && (
          <div className="flex items-start gap-3 p-4 rounded-xl bg-gray-50 dark:bg-[#1e1e1e]">
            <MapPin className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{t('restaurant.address') || 'Address'}</p>
              <p className="text-gray-900 dark:text-gray-100">{lt(restaurant.address)}</p>
            </div>
          </div>
        )}
        {lt(restaurant.hours) && (
          <div className="flex items-start gap-3 p-4 rounded-xl bg-gray-50 dark:bg-[#1e1e1e]">
            <Clock className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{t('restaurant.hours') || 'Hours'}</p>
              <p className="text-gray-900 dark:text-gray-100">{lt(restaurant.hours)}</p>
            </div>
          </div>
        )}
        {restaurant.phone && (
          <div className="flex items-start gap-3 p-4 rounded-xl bg-gray-50 dark:bg-[#1e1e1e]">
            <Phone className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{t('restaurant.phone') || 'Phone'}</p>
              <a href={`tel:${restaurant.phone}`} className="text-indigo-600 dark:text-indigo-400">{restaurant.phone}</a>
            </div>
          </div>
        )}
      </div>

      {/* Menu Highlights */}
      {restaurant.menu_highlights && restaurant.menu_highlights.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('restaurant.menu_highlights') || 'Menu Highlights'}</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {restaurant.menu_highlights.map((item, idx) => (
              <div key={idx} className="flex items-center gap-3 p-3 rounded-xl border border-gray-200 dark:border-gray-500/40">
                {item.image && (
                  <img src={item.image} alt={lt(item.name)} className="w-16 h-16 rounded-lg object-cover" />
                )}
                <div className="flex-1">
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">{lt(item.name)}</h3>
                  {item.description && (
                    <p className="text-sm text-gray-500 dark:text-gray-400">{lt(item.description)}</p>
                  )}
                </div>
                {item.price && (
                  <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400">{item.price}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Map */}
      {markers.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('common.view_on_map') || 'Location'}</h2>
          <MapView markers={markers} t={t} className="h-64" />
          {/* External map links */}
          <div className="flex gap-3 mt-3">
            <a
              href={`https://map.naver.com/v5/search/${encodeURIComponent(lt(restaurant.address) || name)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-xs text-gray-500 hover:text-indigo-600"
            >
              <ExternalLink className="w-3 h-3" /> Naver Map
            </a>
            <a
              href={`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-xs text-gray-500 hover:text-indigo-600"
            >
              <ExternalLink className="w-3 h-3" /> Google Maps
            </a>
          </div>
        </div>
      )}

      {/* Reviews Section */}
      <ReviewSection
        targetType="restaurant"
        targetId={String(id)}
        t={t}
        isLoggedIn={isLoggedIn}
      />
    </div>
  );
}
