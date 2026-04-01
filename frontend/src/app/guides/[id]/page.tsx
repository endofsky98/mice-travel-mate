'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Bookmark, BookmarkCheck, Globe, Star, MapPin, DollarSign, MessageCircle, Share2 } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useBookmarks } from '@/hooks/useBookmarks';
import { useAuth } from '@/hooks/useAuth';
import api from '@/lib/api';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import StarRating from '@/components/ui/StarRating';
import ReviewSection from '@/components/ui/ReviewSection';
import MapView from '@/components/map/MapView';
import { Guide } from '@/types';
import { cn, generatePlaceholderGradient, formatCurrency, getInitials } from '@/lib/utils';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, getDay, isToday } from 'date-fns';

export default function GuideDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { t, lt, language } = useLanguage();
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const { isLoggedIn } = useAuth();
  const [loading, setLoading] = useState(true);
  const [guide, setGuide] = useState<Guide | null>(null);
  const [currentMonth, setCurrentMonth] = useState(new Date());

  useEffect(() => {
    const fetchGuide = async () => {
      setLoading(true);
      try {
        const data = await api.get<Guide>(`/api/guides/${id}`);
        setGuide(data);
      } catch {
        setGuide(null);
      }
      setLoading(false);
    };
    fetchGuide();
  }, [id, language]);

  useEffect(() => {
    if (guide) document.title = `${lt(guide.name)} | Exporoute`;
  }, [guide, lt]);

  const handleShare = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try { await navigator.share({ title: guide ? lt(guide.name) : '', url }); } catch {}
    } else {
      await navigator.clipboard.writeText(url);
    }
  };

  const handleStartChat = async () => {
    if (!isLoggedIn) {
      router.push('/auth/login');
      return;
    }
    try {
      const room = await api.post<{ id: string }>('/api/chat/rooms', { guide_id: id });
      router.push(`/chat/${room.id}`);
    } catch {
      // fallback
      router.push('/chat');
    }
  };

  if (loading) return <LoadingSpinner fullPage />;
  if (!guide) {
    return (
      <div className="page-container text-center py-20">
        <p className="text-gray-500">{t('common.no_results')}</p>
      </div>
    );
  }

  const name = lt(guide.name);
  const bookmarked = isBookmarked(guide.id, 'guide');
  const profileImage = guide.profile_image || guide.profile_image_url;
  const hourlyRate = guide.hourly_rate || guide.price_per_hour_usd;
  const halfDayRate = guide.half_day_rate || guide.price_half_day_usd;
  const fullDayRate = guide.full_day_rate || guide.price_full_day_usd;

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });
  const startDay = getDay(monthStart);
  const availableDates = new Set(guide.availability || []);

  // Approximate coordinates for common Korean regions
  const regionCoords: Record<string, { lat: number; lng: number }> = {
    seoul: { lat: 37.5665, lng: 126.978 },
    busan: { lat: 35.1796, lng: 129.0756 },
    incheon: { lat: 37.4563, lng: 126.7052 },
    daegu: { lat: 35.8714, lng: 128.6014 },
    daejeon: { lat: 36.3504, lng: 127.3845 },
    gwangju: { lat: 35.1595, lng: 126.8526 },
    ulsan: { lat: 35.5384, lng: 129.3114 },
    sejong: { lat: 36.48, lng: 127.0 },
    gyeonggi: { lat: 37.4138, lng: 127.5183 },
    gangwon: { lat: 37.8228, lng: 128.1555 },
    chungbuk: { lat: 36.6358, lng: 127.4913 },
    chungnam: { lat: 36.5184, lng: 126.8 },
    jeonbuk: { lat: 35.8203, lng: 127.1089 },
    jeonnam: { lat: 34.8161, lng: 126.4629 },
    gyeongbuk: { lat: 36.4919, lng: 128.8889 },
    gyeongnam: { lat: 35.4606, lng: 128.2132 },
    jeju: { lat: 33.4996, lng: 126.5312 },
  };

  const regionMarkers = (guide.regions || [])
    .map((region) => {
      const key = region.toLowerCase().replace(/[\s-]/g, '');
      const coords = regionCoords[key];
      return coords ? { id: region, lat: coords.lat, lng: coords.lng, title: region } : null;
    })
    .filter((m): m is { id: string; lat: number; lng: number; title: string } => m !== null);

  const proficiencyColors: Record<string, string> = {
    native: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
    fluent: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
    intermediate: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
    conversational: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
    basic: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300',
  };

  return (
    <div className="page-container max-w-4xl pb-28 md:pb-8">
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        {t('common.back') || 'Back'}
      </button>

      {/* Profile Header */}
      <div className="flex flex-col sm:flex-row items-start gap-6 mb-8">
        <div className="flex-shrink-0">
          {profileImage ? (
            <img src={profileImage} alt={name} className="w-28 h-28 rounded-2xl object-cover" />
          ) : (
            <div className={cn('w-28 h-28 rounded-2xl bg-gradient-to-br flex items-center justify-center', generatePlaceholderGradient(name))}>
              <span className="text-white font-bold text-3xl">{getInitials(name)}</span>
            </div>
          )}
        </div>
        <div className="flex-1">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">{name}</h1>
              {/* Rating */}
              {guide.avg_rating && guide.avg_rating > 0 && (
                <div className="mb-2">
                  <StarRating rating={guide.avg_rating} size="sm" showValue reviewCount={guide.review_count} />
                </div>
              )}
              {guide.regions && guide.regions.length > 0 && (
                <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400 mb-3">
                  <MapPin className="w-4 h-4" />
                  {guide.regions.join(', ')}
                </div>
              )}
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={handleShare}>
                <Share2 className="w-4 h-4" />
              </Button>
              <Button variant={bookmarked ? 'default' : 'outline'} size="sm" onClick={() => toggleBookmark(guide.id, 'guide')}>
                {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
              </Button>
            </div>
          </div>

          {/* Languages with proficiency level */}
          {guide.languages && guide.languages.length > 0 && (
            <div className="mb-3">
              <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400 mb-2">
                <Globe className="w-4 h-4" />
                {t('guide.languages') || 'Languages'}
              </div>
              <div className="flex flex-wrap gap-2">
                {guide.languages.map((lang, idx) => (
                  <span key={idx} className={cn('px-2.5 py-1 rounded-full text-xs font-medium', proficiencyColors[lang.proficiency] || proficiencyColors.basic)}>
                    {lang.language} ({lang.proficiency})
                  </span>
                ))}
              </div>
            </div>
          )}

          {guide.specialties && guide.specialties.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {guide.specialties.map((spec, idx) => (
                <Badge key={idx}>
                  <Star className="w-3 h-3 mr-1" />
                  {spec}
                </Badge>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Bio */}
      {lt(guide.bio) && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.bio') || 'About'}</h2>
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{lt(guide.bio)}</p>
        </div>
      )}

      {/* Services */}
      {lt(guide.services) && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.services') || 'Services'}</h2>
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{lt(guide.services)}</p>
        </div>
      )}

      {/* Price Table */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.price') || 'Pricing'}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {hourlyRate && (
            <Card className="p-4 text-center">
              <DollarSign className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mx-auto mb-2" />
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('guide.hourly_rate') || 'Per Hour'}</p>
              <p className="text-xl font-bold text-gray-900 dark:text-gray-100">${Number(hourlyRate).toFixed(0)}</p>
            </Card>
          )}
          {halfDayRate && (
            <Card className="p-4 text-center">
              <DollarSign className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mx-auto mb-2" />
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('guide.half_day_rate') || 'Half Day (4h)'}</p>
              <p className="text-xl font-bold text-gray-900 dark:text-gray-100">${Number(halfDayRate).toFixed(0)}</p>
            </Card>
          )}
          {fullDayRate && (
            <Card className="p-4 text-center">
              <DollarSign className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mx-auto mb-2" />
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('guide.full_day_rate') || 'Full Day (8h)'}</p>
              <p className="text-xl font-bold text-gray-900 dark:text-gray-100">${Number(fullDayRate).toFixed(0)}</p>
            </Card>
          )}
        </div>
      </div>

      {/* Availability Calendar */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.availability') || 'Availability'}</h2>
        <Card className="p-4">
          <div className="flex items-center justify-between mb-4">
            <button onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded-lg">
              <ArrowLeft className="w-5 h-5" />
            </button>
            <span className="font-medium text-gray-900 dark:text-gray-100">{format(currentMonth, 'MMMM yyyy')}</span>
            <button onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded-lg rotate-180">
              <ArrowLeft className="w-5 h-5" />
            </button>
          </div>
          <div className="grid grid-cols-7 gap-1 text-center">
            {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map((day) => (
              <div key={day} className="text-xs font-medium text-gray-400 dark:text-gray-500 py-2">{day}</div>
            ))}
            {Array.from({ length: startDay }).map((_, i) => (<div key={`empty-${i}`} />))}
            {daysInMonth.map((day) => {
              const dateStr = format(day, 'yyyy-MM-dd');
              const isAvailable = availableDates.has(dateStr);
              const today = isToday(day);
              return (
                <div key={dateStr} className={cn('py-2 rounded-lg text-sm', isAvailable ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 font-medium' : 'text-gray-400 dark:text-gray-600', today && 'ring-2 ring-indigo-600 dark:ring-indigo-400')}>
                  {format(day, 'd')}
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      {/* Activity Regions Map */}
      {regionMarkers.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('guide.activity_regions') || 'Activity Regions'}</h2>
          <MapView markers={regionMarkers} t={t} className="h-64" />
        </div>
      )}

      {/* Reviews */}
      <ReviewSection targetType="guide" targetId={String(id)} t={t} isLoggedIn={isLoggedIn} />

      {/* Fixed Bottom CTA */}
      <div className="fixed bottom-16 md:bottom-0 left-0 right-0 bg-white dark:bg-[#141414] border-t border-gray-200 dark:border-gray-500/40 px-4 py-3 z-30">
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-3">
          <div>
            {hourlyRate && (
              <div>
                <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400">${Number(hourlyRate).toFixed(0)}</span>
                <span className="text-sm text-gray-400 ml-1">/ hr</span>
              </div>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" onClick={handleStartChat}>
              <MessageCircle className="w-4 h-4 mr-1" />
              {t('chat.send_message') || 'Chat'}
            </Button>
            <Link href={`/booking/${guide.id}?type=guide`}>
              <Button>{t('button.book_now') || 'Book Now'}</Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
