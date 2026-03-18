'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, Clock, MapPin, Bookmark, BookmarkCheck, ArrowDown, Bus, Footprints, Car, Train, Share2 } from 'lucide-react';
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
import { Course } from '@/types';
import { cn, generatePlaceholderGradient } from '@/lib/utils';

const transportIcons: Record<string, typeof Bus> = {
  bus: Bus,
  walk: Footprints,
  taxi: Car,
  subway: Train,
};

export default function CourseDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { t, lt, language } = useLanguage();
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const { isLoggedIn } = useAuth();
  const [loading, setLoading] = useState(true);
  const [course, setCourse] = useState<Course | null>(null);

  useEffect(() => {
    const fetchCourse = async () => {
      setLoading(true);
      try {
        const data = await api.get<Course>(`/api/v1/courses/${id}`);
        setCourse(data);
      } catch {
        setCourse(null);
      }
      setLoading(false);
    };
    fetchCourse();
  }, [id, language]);

  if (loading) return <LoadingSpinner fullPage />;
  if (!course) {
    return (
      <div className="page-container text-center py-20">
        <p className="text-gray-500">{t('common.no_results')}</p>
      </div>
    );
  }

  const name = lt(course.name);
  const bookmarked = isBookmarked(course.id, 'course');
  const spots = course.spots || [];

  const handleShare = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title: name, url });
      } catch { /* user cancelled */ }
    } else {
      await navigator.clipboard.writeText(url);
      alert('Link copied!');
    }
  };
  const markers = spots
    .filter((s) => s.lat && s.lng)
    .map((s) => ({ id: s.id, lat: s.lat!, lng: s.lng!, title: lt(s.name) }));

  return (
    <div className="page-container max-w-4xl pb-20 md:pb-8">
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      <ImageGallery images={course.images || []} alt={name} className="mb-6" />

      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">{name}</h1>
          {course.avg_rating && course.avg_rating > 0 && (
            <div className="mb-2">
              <StarRating
                rating={course.avg_rating}
                size="sm"
                showValue
                reviewCount={course.review_count}
              />
            </div>
          )}
          <div className="flex flex-wrap gap-2">
            <Badge>{course.duration}</Badge>
            <Badge variant="info">{course.theme}</Badge>
            <Badge variant={course.difficulty === 'easy' ? 'success' : course.difficulty === 'challenging' ? 'warning' : 'default'}>
              {course.difficulty}
            </Badge>
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
            onClick={() => toggleBookmark(course.id, 'course')}
          >
            {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      {/* Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
        <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('course.duration')}</p>
          <p className="font-semibold text-gray-900 dark:text-gray-100">{course.duration}</p>
        </div>
        <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('course.spots')}</p>
          <p className="font-semibold text-gray-900 dark:text-gray-100">{spots.length}</p>
        </div>
        <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('course.difficulty')}</p>
          <p className="font-semibold text-gray-900 dark:text-gray-100">{course.difficulty}</p>
        </div>
        {course.transport_cost && (
          <div className="p-3 rounded-xl bg-gray-50 dark:bg-dark-card text-center">
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">{t('course.transport_cost')}</p>
            <p className="font-semibold text-gray-900 dark:text-gray-100">{course.transport_cost}</p>
          </div>
        )}
      </div>

      {lt(course.description) && (
        <p className="text-gray-600 dark:text-gray-300 leading-relaxed mb-8">{lt(course.description)}</p>
      )}

      {/* Spot List */}
      {spots.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('course.spot_list')}</h2>
          <div className="space-y-4">
            {spots.map((spot, idx) => (
              <div key={spot.id || idx}>
                <div className="flex gap-4 p-4 rounded-xl border border-gray-200 dark:border-gray-500/40">
                  <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-indigo-600 dark:bg-indigo-500 flex items-center justify-center text-white font-bold text-sm">
                      {idx + 1}
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start gap-3">
                      {spot.image ? (
                        <img src={spot.image} alt={lt(spot.name)} className="w-20 h-20 rounded-lg object-cover flex-shrink-0" />
                      ) : (
                        <div className={cn('w-20 h-20 rounded-lg bg-gradient-to-br flex-shrink-0 flex items-center justify-center', generatePlaceholderGradient(lt(spot.name)))}>
                          <MapPin className="w-6 h-6 text-white/60" />
                        </div>
                      )}
                      <div>
                        <h3 className="font-medium text-gray-900 dark:text-gray-100">{lt(spot.name)}</h3>
                        {lt(spot.description) && (
                          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{lt(spot.description)}</p>
                        )}
                        {spot.duration && (
                          <span className="inline-flex items-center gap-1 text-xs text-gray-400 mt-2">
                            <Clock className="w-3 h-3" /> {spot.duration}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Transition */}
                {spot.transition && idx < spots.length - 1 && (
                  <div className="flex items-center gap-3 py-3 pl-9">
                    <ArrowDown className="w-4 h-4 text-gray-300 dark:text-gray-600" />
                    <div className="flex items-center gap-2 text-xs text-gray-400 dark:text-gray-500">
                      {(() => {
                        const Icon = transportIcons[spot.transition.mode] || Bus;
                        return <Icon className="w-4 h-4" />;
                      })()}
                      <span>{spot.transition.mode}</span>
                      <span className="text-gray-300 dark:text-gray-600">|</span>
                      <span>{spot.transition.duration}</span>
                      {spot.transition.distance && (
                        <>
                          <span className="text-gray-300 dark:text-gray-600">|</span>
                          <span>{spot.transition.distance}</span>
                        </>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Map */}
      {markers.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('common.view_on_map')}</h2>
          <MapView markers={markers} t={t} className="h-64" />
        </div>
      )}

      {/* Reviews Section */}
      <ReviewSection
        targetType="course"
        targetId={String(id)}
        t={t}
        isLoggedIn={isLoggedIn}
      />
    </div>
  );
}
