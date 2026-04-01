'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Clock, Users, MapPin, Bookmark, BookmarkCheck, Check, X, CircleDot, Share2 } from 'lucide-react';
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
import { Product } from '@/types';
import { formatCurrency } from '@/lib/utils';

export default function ProductDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { t, lt, language } = useLanguage();
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const { isLoggedIn } = useAuth();
  const [loading, setLoading] = useState(true);
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => {
    const fetchProduct = async () => {
      setLoading(true);
      try {
        const data = await api.get<Product>(`/api/products/${id}`);
        setProduct(data);
      } catch {
        setProduct(null);
      }
      setLoading(false);
    };
    fetchProduct();
  }, [id, language]);

  useEffect(() => {
    if (product) document.title = `${lt(product.name)} | Exporoute`;
  }, [product, lt]);

  if (loading) return <LoadingSpinner fullPage />;
  if (!product) {
    return (
      <div className="page-container text-center py-20">
        <p className="text-gray-500">{t('common.no_results')}</p>
      </div>
    );
  }

  const handleShare = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: lt(product.name), url });
      } catch { /* user cancelled */ }
    } else {
      await navigator.clipboard.writeText(url);
      alert('Link copied!');
    }
  };

  const name = lt(product.name);
  const bookmarked = isBookmarked(product.id, 'product');
  const meetingLat = product.meeting_point_lat || product.lat;
  const meetingLng = product.meeting_point_lng || product.lng;
  const markers = meetingLat && meetingLng
    ? [{ id: product.id, lat: meetingLat, lng: meetingLng, title: lt(product.meeting_point) || name }]
    : [];

  return (
    <div className="page-container max-w-4xl">
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      <ImageGallery images={product.images || []} alt={name} className="mb-6" />

      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Badge>{product.category}</Badge>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">{name}</h1>
          <div className="flex items-center gap-4">
            <span className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
              {formatCurrency(product.price, product.currency)}
            </span>
            <span className="text-sm text-gray-400">/ {t('product.per_person')}</span>
          </div>
          {product.avg_rating && product.avg_rating > 0 && (
            <div className="mt-2">
              <StarRating
                rating={product.avg_rating}
                size="sm"
                showValue
                reviewCount={product.review_count}
              />
            </div>
          )}
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
            onClick={() => toggleBookmark(product.id, 'product')}
          >
            {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      {/* Quick Info */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
        {product.duration && (
          <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
            <Clock className="w-5 h-5 text-gray-400 mx-auto mb-1" />
            <p className="text-xs text-gray-500 dark:text-gray-400">{t('product.duration')}</p>
            <p className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{product.duration}</p>
          </div>
        )}
        {product.min_participants && (
          <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
            <Users className="w-5 h-5 text-gray-400 mx-auto mb-1" />
            <p className="text-xs text-gray-500 dark:text-gray-400">{t('product.min_participants')}</p>
            <p className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{product.min_participants}</p>
          </div>
        )}
        {product.max_participants && (
          <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
            <Users className="w-5 h-5 text-gray-400 mx-auto mb-1" />
            <p className="text-xs text-gray-500 dark:text-gray-400">{t('product.max_participants')}</p>
            <p className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{product.max_participants}</p>
          </div>
        )}
        {product.region && (
          <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
            <MapPin className="w-5 h-5 text-gray-400 mx-auto mb-1" />
            <p className="text-xs text-gray-500 dark:text-gray-400">{t('product.region')}</p>
            <p className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{product.region}</p>
          </div>
        )}
      </div>

      {/* Description */}
      {lt(product.description) && (
        <div className="mb-8">
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{lt(product.description)}</p>
        </div>
      )}

      {/* Includes / Excludes */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {product.includes && product.includes.length > 0 && (
          <div className="p-4 rounded-xl border border-green-200 dark:border-green-800/40 bg-green-50/50 dark:bg-green-950/20">
            <h3 className="font-semibold text-green-700 dark:text-green-400 mb-3">{t('product.includes')}</h3>
            <ul className="space-y-2">
              {product.includes.map((item, idx) => (
                <li key={idx} className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <Check className="w-4 h-4 text-green-500 flex-shrink-0" />
                  {lt(item as string)}
                </li>
              ))}
            </ul>
          </div>
        )}
        {product.excludes && product.excludes.length > 0 && (
          <div className="p-4 rounded-xl border border-red-200 dark:border-red-800/40 bg-red-50/50 dark:bg-red-950/20">
            <h3 className="font-semibold text-red-700 dark:text-red-400 mb-3">{t('product.excludes')}</h3>
            <ul className="space-y-2">
              {product.excludes.map((item, idx) => (
                <li key={idx} className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                  <X className="w-4 h-4 text-red-500 flex-shrink-0" />
                  {lt(item as string)}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Itinerary */}
      {product.itinerary && product.itinerary.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('product.itinerary')}</h2>
          <div className="space-y-0">
            {product.itinerary.map((item, idx) => (
              <div key={idx} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <CircleDot className="w-5 h-5 text-indigo-600 dark:text-indigo-400 flex-shrink-0" />
                  {idx < product.itinerary!.length - 1 && (
                    <div className="w-0.5 flex-1 bg-indigo-200 dark:bg-indigo-800 my-1" />
                  )}
                </div>
                <div className="pb-6">
                  <span className="text-xs font-medium text-indigo-600 dark:text-indigo-400">{item.time}</span>
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">{lt(item.title)}</h3>
                  {lt(item.description) && (
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{lt(item.description)}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Meeting / Dismissal */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {lt(product.meeting_point) && (
          <div className="flex items-start gap-3 p-4 rounded-xl bg-gray-50 dark:bg-dark-card">
            <MapPin className="w-5 h-5 text-indigo-600 dark:text-indigo-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{t('product.meeting_point')}</p>
              <p className="text-gray-900 dark:text-gray-100">{lt(product.meeting_point)}</p>
            </div>
          </div>
        )}
        {lt(product.dismissal_point) && (
          <div className="flex items-start gap-3 p-4 rounded-xl bg-gray-50 dark:bg-dark-card">
            <MapPin className="w-5 h-5 text-emerald-600 dark:text-emerald-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">{t('product.dismissal_point')}</p>
              <p className="text-gray-900 dark:text-gray-100">{lt(product.dismissal_point)}</p>
            </div>
          </div>
        )}
      </div>

      {/* Meeting Point Map */}
      {markers.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('product.meeting_point_map') || 'Meeting Point'}</h2>
          <MapView markers={markers} t={t} className="h-64" />
        </div>
      )}

      {/* Cancellation Policy */}
      {lt(product.cancellation_policy) && (
        <div className="mb-8 p-4 rounded-xl bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800/40">
          <h3 className="font-semibold text-amber-700 dark:text-amber-400 mb-2">{t('booking.cancellation_policy')}</h3>
          <p className="text-sm text-amber-600 dark:text-amber-300">{lt(product.cancellation_policy)}</p>
        </div>
      )}

      {/* Reviews Section */}
      <ReviewSection
        targetType="product"
        targetId={String(id)}
        t={t}
        isLoggedIn={isLoggedIn}
      />

      {/* Book Now */}
      <div className="sticky bottom-20 md:bottom-4 bg-white dark:bg-dark-main border-t border-gray-200 dark:border-gray-500/40 -mx-4 px-4 py-4 md:border md:rounded-xl md:mx-0">
        <div className="flex items-center justify-between">
          <div>
            <span className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
              {formatCurrency(product.price, product.currency)}
            </span>
            <span className="text-sm text-gray-400 ml-1">/ {t('product.per_person')}</span>
          </div>
          <Link href={`/booking/${product.id}?type=product`}>
            <Button size="lg">{t('common.book_now')}</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
