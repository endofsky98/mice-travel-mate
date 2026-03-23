'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, Calendar, MapPin, ExternalLink, Clock, Share2, Bookmark, BookmarkCheck } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useBookmarks } from '@/hooks/useBookmarks';
import api from '@/lib/api';
import Button from '@/components/ui/Button';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import MapView from '@/components/map/MapView';
import { Festival } from '@/types';
import { formatDateRange } from '@/lib/utils';
import { cn } from '@/lib/utils';

function getDDayText(startDate: string, endDate: string): { text: string; variant: 'ongoing' | 'upcoming' | 'past' } {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const start = new Date(startDate);
  const end = new Date(endDate);

  if (now >= start && now <= end) {
    return { text: 'Ongoing', variant: 'ongoing' };
  }
  if (now < start) {
    const diffDays = Math.ceil((start.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    return { text: `D-${diffDays}`, variant: 'upcoming' };
  }
  return { text: 'Ended', variant: 'past' };
}

export default function FestivalDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { t, lt, language } = useLanguage();
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const [loading, setLoading] = useState(true);
  const [festival, setFestival] = useState<Festival | null>(null);

  useEffect(() => {
    const fetchFestival = async () => {
      setLoading(true);
      try {
        const data = await api.get<Festival>(`/api/festivals/${id}`);
        setFestival(data);
      } catch {
        setFestival(null);
      }
      setLoading(false);
    };
    fetchFestival();
  }, [id, language]);

  useEffect(() => {
    if (festival) document.title = `${lt(festival.name)} | Exporoute`;
  }, [festival, lt]);

  const handleShare = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: festival ? lt(festival.name) : '', url });
      } catch { /* user cancelled */ }
    } else {
      await navigator.clipboard.writeText(url);
      alert('Link copied!');
    }
  };

  if (loading) return <LoadingSpinner fullPage />;
  if (!festival) {
    return (
      <div className="page-container text-center py-20">
        <p className="text-gray-500 dark:text-gray-400">{t('common.no_results') || 'Not found'}</p>
      </div>
    );
  }

  const name = lt(festival.name);
  const description = lt(festival.description);
  const dday = festival.start_date && festival.end_date
    ? getDDayText(festival.start_date, festival.end_date)
    : null;
  const markers = festival.latitude && festival.longitude
    ? [{ id: festival.id, lat: festival.latitude, lng: festival.longitude, title: name }]
    : [];

  const ddayColors = {
    ongoing: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
    upcoming: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300',
    past: 'bg-gray-100 text-gray-500 dark:bg-gray-800 dark:text-gray-400',
  };

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

      {/* Hero Image */}
      <div className="relative aspect-[16/9] rounded-xl overflow-hidden mb-6">
        {festival.image_url ? (
          <img src={festival.image_url} alt={name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-pink-500 to-orange-500 flex items-center justify-center">
            <Calendar className="w-16 h-16 text-white/60" />
          </div>
        )}
        {dday && (
          <span className={cn('absolute top-4 left-4 px-3 py-1.5 rounded-lg text-sm font-semibold', ddayColors[dday.variant])}>
            {dday.text}
          </span>
        )}
        {festival.category && (
          <span className="absolute top-4 right-4 px-3 py-1.5 bg-black/60 backdrop-blur-sm text-white text-sm rounded-lg capitalize">
            {festival.category}
          </span>
        )}
      </div>

      {/* Title & Actions */}
      <div className="flex items-start justify-between mb-4">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex-1">{name}</h1>
        <div className="flex items-center gap-2 ml-4">
          <button
            onClick={handleShare}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/[0.08] text-gray-500 dark:text-gray-400"
          >
            <Share2 className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Date & Location Info */}
      <div className="space-y-3 mb-6">
        {festival.start_date && festival.end_date && (
          <div className="flex items-center gap-3 text-gray-600 dark:text-gray-300">
            <Calendar className="w-5 h-5 text-gray-400 dark:text-gray-500 flex-shrink-0" />
            <span>{formatDateRange(festival.start_date, festival.end_date)}</span>
          </div>
        )}
        {festival.venue_name && (
          <div className="flex items-center gap-3 text-gray-600 dark:text-gray-300">
            <MapPin className="w-5 h-5 text-gray-400 dark:text-gray-500 flex-shrink-0" />
            <div>
              <span className="font-medium">{festival.venue_name}</span>
              {festival.address && <p className="text-sm text-gray-400 dark:text-gray-500">{festival.address}</p>}
            </div>
          </div>
        )}
        {festival.website_url && (
          <a
            href={festival.website_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-3 text-indigo-600 dark:text-indigo-400 hover:underline"
          >
            <ExternalLink className="w-5 h-5 flex-shrink-0" />
            <span>{t('festival.visit_website') || 'Visit Website'}</span>
          </a>
        )}
      </div>

      {/* Description */}
      {description && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            {t('common.description') || 'Description'}
          </h2>
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed whitespace-pre-line">{description}</p>
        </div>
      )}

      {/* Image Gallery */}
      {festival.images && festival.images.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            {t('common.photos') || 'Photos'}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {festival.images.map((img, i) => (
              <div key={i} className="aspect-square rounded-lg overflow-hidden">
                <img src={img} alt={`${name} ${i + 1}`} className="w-full h-full object-cover" />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Map */}
      {markers.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            {t('common.location') || 'Location'}
          </h2>
          <div className="h-[300px] rounded-xl overflow-hidden border border-gray-200 dark:border-gray-500/40">
            <MapView markers={markers} zoom={15} t={t} />
          </div>
          {festival.address && (
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5" /> {festival.address}
            </p>
          )}
        </div>
      )}

      {/* External Links */}
      <div className="flex flex-wrap gap-3">
        {festival.website_url && (
          <a
            href={festival.website_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-400 transition-colors"
          >
            <ExternalLink className="w-4 h-4" />
            {t('festival.visit_website') || 'Visit Website'}
          </a>
        )}
        {festival.latitude && festival.longitude && (
          <a
            href={`https://maps.google.com/?q=${festival.latitude},${festival.longitude}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2.5 border border-gray-200 dark:border-gray-500/40 bg-white dark:bg-[#2a2a2a] text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors"
          >
            <MapPin className="w-4 h-4" />
            {t('common.open_maps') || 'Open in Maps'}
          </a>
        )}
      </div>
    </div>
  );
}
