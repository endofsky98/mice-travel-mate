'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { Calendar, MapPin, ArrowRight } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import RestaurantCard from '@/components/restaurant/RestaurantCard';
import CourseCard from '@/components/course/CourseCard';
import ProductCard from '@/components/product/ProductCard';
import GuideCard from '@/components/guide/GuideCard';
import { Event, Restaurant, Course, Product, Guide } from '@/types';
import { cn, generatePlaceholderGradient, formatDateRange } from '@/lib/utils';

export default function EventPage() {
  const { slug } = useParams();
  const { t, lt, language } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [event, setEvent] = useState<Event | null>(null);
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [guides, setGuides] = useState<Guide[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const eventData = await api.get<Event>(`/api/events/${slug}`);
        setEvent(eventData);

        const [restData, courseData, prodData, guideData] = await Promise.all([
          api.get<{ items: Restaurant[] }>('/api/restaurants', { event_id: eventData.id, per_page: 6 }).catch(() => ({ items: [] })),
          api.get<{ items: Course[] }>('/api/courses', { event_id: eventData.id, per_page: 6 }).catch(() => ({ items: [] })),
          api.get<{ items: Product[] }>('/api/products', { event_id: eventData.id, per_page: 6 }).catch(() => ({ items: [] })),
          api.get<{ items: Guide[] }>('/api/guides', { event_id: eventData.id, per_page: 6 }).catch(() => ({ items: [] })),
        ]);
        setRestaurants(restData.items || []);
        setCourses(courseData.items || []);
        setProducts(prodData.items || []);
        setGuides(guideData.items || []);
      } catch {
        setEvent(null);
      }
      setLoading(false);
    };
    fetchData();
  }, [slug, language]);

  if (loading) return <LoadingSpinner fullPage />;
  if (!event) {
    return (
      <div className="page-container text-center py-20">
        <p className="text-gray-500">{t('common.no_results')}</p>
      </div>
    );
  }

  return (
    <div className="pb-20 md:pb-0">
      {/* Event Banner */}
      <div className="relative">
        {event.banner_image ? (
          <div className="relative h-64 md:h-80">
            <img src={event.banner_image} alt={lt(event.name)} className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
            <div className="absolute bottom-0 left-0 right-0 p-6">
              <div className="max-w-7xl mx-auto">
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">{lt(event.name)}</h1>
                <div className="flex flex-wrap items-center gap-4 text-white/80">
                  {event.start_date && event.end_date && (
                    <span className="flex items-center gap-1 text-sm">
                      <Calendar className="w-4 h-4" />
                      {formatDateRange(event.start_date, event.end_date)}
                    </span>
                  )}
                  {event.venue_name && (
                    <span className="flex items-center gap-1 text-sm">
                      <MapPin className="w-4 h-4" />
                      {lt(event.venue_name)}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div
            className={cn(
              'h-64 md:h-80 bg-gradient-to-br flex items-end',
              generatePlaceholderGradient(lt(event.name))
            )}
          >
            <div className="w-full p-6 bg-gradient-to-t from-black/60 to-transparent">
              <div className="max-w-7xl mx-auto">
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">{lt(event.name)}</h1>
                <div className="flex flex-wrap items-center gap-4 text-white/80">
                  {event.start_date && event.end_date && (
                    <span className="flex items-center gap-1 text-sm">
                      <Calendar className="w-4 h-4" />
                      {formatDateRange(event.start_date, event.end_date)}
                    </span>
                  )}
                  {event.venue_name && (
                    <span className="flex items-center gap-1 text-sm">
                      <MapPin className="w-4 h-4" />
                      {lt(event.venue_name)}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="page-container">
        {/* Event Description */}
        {lt(event.description) && (
          <div className="mb-8">
            <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{lt(event.description)}</p>
          </div>
        )}

        {/* Restaurants */}
        {restaurants.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-title">{t('nav.restaurants')}</h2>
              <Link href="/restaurants" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all')} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="horizontal-scroll">
              {restaurants.map((r) => (
                <div key={r.id} className="w-[280px]">
                  <RestaurantCard restaurant={r} lt={lt} />
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Courses */}
        {courses.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-title">{t('nav.courses')}</h2>
              <Link href="/courses" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all')} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="horizontal-scroll">
              {courses.map((c) => (
                <div key={c.id} className="w-[280px]">
                  <CourseCard course={c} lt={lt} />
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Products */}
        {products.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-title">{t('nav.products')}</h2>
              <Link href="/products" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all')} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="horizontal-scroll">
              {products.map((p) => (
                <div key={p.id} className="w-[280px]">
                  <ProductCard product={p} lt={lt} />
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Guides */}
        {guides.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-title">{t('nav.guides')}</h2>
              <Link href="/guides" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all')} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {guides.slice(0, 6).map((g) => (
                <GuideCard key={g.id} guide={g} lt={lt} />
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
