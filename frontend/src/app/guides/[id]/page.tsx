'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Bookmark, BookmarkCheck, Globe, Star, MapPin, DollarSign } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useBookmarks } from '@/hooks/useBookmarks';
import api from '@/lib/api';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { Guide } from '@/types';
import { cn, generatePlaceholderGradient, formatCurrency, getInitials } from '@/lib/utils';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, getDay, isSameMonth, isToday, parseISO } from 'date-fns';

export default function GuideDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { t, lt, language } = useLanguage();
  const { isBookmarked, toggleBookmark } = useBookmarks();
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

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });
  const startDay = getDay(monthStart);
  const availableDates = new Set(guide.availability || []);

  const proficiencyColors: Record<string, string> = {
    native: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
    fluent: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
    conversational: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
    basic: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300',
  };

  return (
    <div className="page-container max-w-4xl">
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      {/* Profile Header */}
      <div className="flex flex-col sm:flex-row items-start gap-6 mb-8">
        <div className="flex-shrink-0">
          {guide.profile_image ? (
            <img src={guide.profile_image} alt={name} className="w-28 h-28 rounded-2xl object-cover" />
          ) : (
            <div
              className={cn(
                'w-28 h-28 rounded-2xl bg-gradient-to-br flex items-center justify-center',
                generatePlaceholderGradient(name)
              )}
            >
              <span className="text-white font-bold text-3xl">{getInitials(name)}</span>
            </div>
          )}
        </div>
        <div className="flex-1">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">{name}</h1>
              {guide.regions && guide.regions.length > 0 && (
                <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400 mb-3">
                  <MapPin className="w-4 h-4" />
                  {guide.regions.join(', ')}
                </div>
              )}
            </div>
            <Button
              variant={bookmarked ? 'default' : 'outline'}
              size="sm"
              onClick={() => toggleBookmark(guide.id, 'guide')}
            >
              {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
            </Button>
          </div>

          {/* Languages */}
          {guide.languages && guide.languages.length > 0 && (
            <div className="mb-3">
              <div className="flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400 mb-2">
                <Globe className="w-4 h-4" />
                {t('guide.languages')}
              </div>
              <div className="flex flex-wrap gap-2">
                {guide.languages.map((lang, idx) => (
                  <span
                    key={idx}
                    className={cn(
                      'px-2.5 py-1 rounded-full text-xs font-medium',
                      proficiencyColors[lang.proficiency] || proficiencyColors.basic
                    )}
                  >
                    {lang.language} ({lang.proficiency})
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Specialties */}
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
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.bio')}</h2>
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{lt(guide.bio)}</p>
        </div>
      )}

      {/* Services */}
      {lt(guide.services) && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.services')}</h2>
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{lt(guide.services)}</p>
        </div>
      )}

      {/* Price Table */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.price')}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {guide.hourly_rate && (
            <Card className="p-4 text-center">
              <DollarSign className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mx-auto mb-2" />
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('guide.hourly_rate')}</p>
              <p className="text-xl font-bold text-gray-900 dark:text-gray-100">
                {formatCurrency(guide.hourly_rate, guide.currency)}
              </p>
            </Card>
          )}
          {guide.half_day_rate && (
            <Card className="p-4 text-center">
              <DollarSign className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mx-auto mb-2" />
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('guide.half_day_rate')}</p>
              <p className="text-xl font-bold text-gray-900 dark:text-gray-100">
                {formatCurrency(guide.half_day_rate, guide.currency)}
              </p>
            </Card>
          )}
          {guide.full_day_rate && (
            <Card className="p-4 text-center">
              <DollarSign className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mx-auto mb-2" />
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('guide.full_day_rate')}</p>
              <p className="text-xl font-bold text-gray-900 dark:text-gray-100">
                {formatCurrency(guide.full_day_rate, guide.currency)}
              </p>
            </Card>
          )}
        </div>
      </div>

      {/* Availability Calendar */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">{t('guide.availability')}</h2>
        <Card className="p-4">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
              className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded-lg"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <span className="font-medium text-gray-900 dark:text-gray-100">
              {format(currentMonth, 'MMMM yyyy')}
            </span>
            <button
              onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
              className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded-lg rotate-180"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
          </div>
          <div className="grid grid-cols-7 gap-1 text-center">
            {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map((day) => (
              <div key={day} className="text-xs font-medium text-gray-400 dark:text-gray-500 py-2">
                {day}
              </div>
            ))}
            {Array.from({ length: startDay }).map((_, i) => (
              <div key={`empty-${i}`} />
            ))}
            {daysInMonth.map((day) => {
              const dateStr = format(day, 'yyyy-MM-dd');
              const isAvailable = availableDates.has(dateStr);
              const today = isToday(day);
              return (
                <div
                  key={dateStr}
                  className={cn(
                    'py-2 rounded-lg text-sm',
                    isAvailable
                      ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 font-medium'
                      : 'text-gray-400 dark:text-gray-600',
                    today && 'ring-2 ring-indigo-600 dark:ring-indigo-400'
                  )}
                >
                  {format(day, 'd')}
                </div>
              );
            })}
          </div>
          <div className="flex items-center gap-4 mt-4 pt-3 border-t border-gray-200 dark:border-gray-500/40">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded bg-green-100 dark:bg-green-900/30" />
              <span className="text-xs text-gray-500 dark:text-gray-400">{t('guide.available')}</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Book Button */}
      <div className="sticky bottom-20 md:bottom-4 bg-white dark:bg-dark-main border-t border-gray-200 dark:border-gray-500/40 -mx-4 px-4 py-4 md:border md:rounded-xl md:mx-0">
        <div className="flex items-center justify-between">
          <div>
            {guide.hourly_rate && (
              <div>
                <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                  {formatCurrency(guide.hourly_rate, guide.currency)}
                </span>
                <span className="text-sm text-gray-400 ml-1">/ hr</span>
              </div>
            )}
          </div>
          <Link href={`/booking/${guide.id}?type=guide`}>
            <Button size="lg">{t('common.book_now')}</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
