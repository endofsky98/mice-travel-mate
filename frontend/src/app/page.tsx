'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  UtensilsCrossed,
  Map,
  ShoppingBag,
  Users,
  Bus,
  Calendar,
  ArrowRight,
  Compass,
} from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import RestaurantCard from '@/components/restaurant/RestaurantCard';
import CourseCard from '@/components/course/CourseCard';
import ProductCard from '@/components/product/ProductCard';
import { Event, Restaurant, Course, Product } from '@/types';
import { cn, generatePlaceholderGradient, formatDateRange } from '@/lib/utils';

export default function HomePage() {
  const { t, lt, language } = useLanguage();
  const searchParams = useSearchParams();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState<Event[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [products, setProducts] = useState<Product[]>([]);

  const eventSlug = searchParams.get('event');

  useEffect(() => {
    const langParam = searchParams.get('lang');
    if (langParam) {
      // Language already handled by useLanguage hook
    }
  }, [searchParams]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        if (eventSlug) {
          try {
            const eventData = await api.get<Event>(`/api/events/${eventSlug}`);
            setSelectedEvent(eventData);
            const [restData, courseData, prodData] = await Promise.all([
              api.get<{ items: Restaurant[] }>('/api/restaurants', { event_id: eventData.id, per_page: 6 }).catch(() => ({ items: [] })),
              api.get<{ items: Course[] }>('/api/courses', { event_id: eventData.id, per_page: 6 }).catch(() => ({ items: [] })),
              api.get<{ items: Product[] }>('/api/products', { event_id: eventData.id, per_page: 6 }).catch(() => ({ items: [] })),
            ]);
            setRestaurants(restData.items || []);
            setCourses(courseData.items || []);
            setProducts(prodData.items || []);
          } catch {
            setSelectedEvent(null);
          }
        } else {
          try {
            const eventData = await api.get<{ items: Event[] }>('/api/events', { per_page: 10 });
            setEvents(eventData.items || []);
          } catch {
            setEvents([]);
          }
          const [restData, courseData, prodData] = await Promise.all([
            api.get<{ items: Restaurant[] }>('/api/restaurants', { per_page: 6 }).catch(() => ({ items: [] })),
            api.get<{ items: Course[] }>('/api/courses', { per_page: 6 }).catch(() => ({ items: [] })),
            api.get<{ items: Product[] }>('/api/products', { per_page: 6 }).catch(() => ({ items: [] })),
          ]);
          setRestaurants(restData.items || []);
          setCourses(courseData.items || []);
          setProducts(prodData.items || []);
        }
      } catch {
        // Silently handle errors
      }
      setLoading(false);
    };

    fetchData();
  }, [eventSlug, language]);

  if (loading) return <LoadingSpinner fullPage />;

  const categories = [
    { href: '/restaurants', icon: UtensilsCrossed, label: t('home.explore_restaurants'), color: 'from-orange-500 to-red-500' },
    { href: '/courses', icon: Map, label: t('home.explore_courses'), color: 'from-emerald-500 to-teal-500' },
    { href: '/products', icon: ShoppingBag, label: t('home.explore_products'), color: 'from-violet-500 to-purple-500' },
    { href: '/guides', icon: Users, label: t('home.explore_guides'), color: 'from-blue-500 to-indigo-500' },
    { href: '/transport', icon: Bus, label: t('home.view_transport'), color: 'from-amber-500 to-orange-500' },
  ];

  return (
    <div className="pb-20 md:pb-0">
      {/* Hero Section */}
      {selectedEvent ? (
        <div className="relative bg-gradient-to-br from-indigo-600 to-purple-700 dark:from-indigo-800 dark:to-purple-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 md:py-20">
            <div className="max-w-2xl">
              <h1 className="text-3xl md:text-4xl font-bold text-white mb-3">
                {lt(selectedEvent.name)}
              </h1>
              {selectedEvent.start_date && selectedEvent.end_date && (
                <div className="flex items-center gap-2 text-indigo-200 mb-4">
                  <Calendar className="w-4 h-4" />
                  <span className="text-sm">
                    {formatDateRange(selectedEvent.start_date, selectedEvent.end_date)}
                  </span>
                </div>
              )}
              <p className="text-indigo-100 text-lg">
                {lt(selectedEvent.description) || t('home.hero_subtitle')}
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="relative bg-gradient-to-br from-indigo-600 via-indigo-700 to-purple-700 dark:from-indigo-800 dark:via-indigo-900 dark:to-purple-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 md:py-20">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="flex-1 text-center md:text-left">
                <div className="flex items-center gap-2 justify-center md:justify-start mb-4">
                  <Compass className="w-8 h-8 text-indigo-200" />
                  <span className="text-indigo-200 font-medium">MICE Travel Mate</span>
                </div>
                <h1 className="text-3xl md:text-5xl font-bold text-white mb-4 text-balance">
                  {t('home.hero_title')}
                </h1>
                <p className="text-indigo-100 text-lg max-w-lg mx-auto md:mx-0">
                  {t('home.hero_subtitle')}
                </p>
              </div>
              <div className="hidden md:block flex-shrink-0">
                <div className="w-64 h-64 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center">
                  <Compass className="w-32 h-32 text-white/40" />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Categories */}
      <div className="page-container">
        <h2 className="section-title mb-4">{t('home.categories')}</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
          {categories.map((cat) => (
            <Link key={cat.href} href={cat.href}>
              <Card hoverable className="p-4 text-center">
                <div
                  className={cn(
                    'w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center mx-auto mb-3',
                    cat.color
                  )}
                >
                  <cat.icon className="w-6 h-6 text-white" />
                </div>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{cat.label}</span>
              </Card>
            </Link>
          ))}
        </div>

        {/* Events Grid (when no event selected) */}
        {!selectedEvent && events.length > 0 && (
          <div className="mt-10">
            <h2 className="section-title mb-4">{t('home.featured_events')}</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {events.map((event) => (
                <button
                  key={event.id}
                  onClick={() => router.push(`/?event=${event.slug}&lang=${language}`)}
                  className="text-left"
                >
                  <Card hoverable className="h-full">
                    <div className="relative aspect-[16/9] overflow-hidden">
                      {event.banner_image ? (
                        <img src={event.banner_image} alt={lt(event.name)} className="w-full h-full object-cover" />
                      ) : (
                        <div
                          className={cn(
                            'w-full h-full bg-gradient-to-br flex items-center justify-center',
                            generatePlaceholderGradient(lt(event.name))
                          )}
                        >
                          <Calendar className="w-12 h-12 text-white/60" />
                        </div>
                      )}
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">{lt(event.name)}</h3>
                      {event.start_date && event.end_date && (
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {formatDateRange(event.start_date, event.end_date)}
                        </p>
                      )}
                      {event.venue_name && (
                        <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">{lt(event.venue_name)}</p>
                      )}
                    </div>
                  </Card>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Restaurants Section */}
        {restaurants.length > 0 && (
          <div className="mt-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-title">{t('nav.restaurants')}</h2>
              <Link
                href="/restaurants"
                className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
              >
                {t('common.view_all')}
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="horizontal-scroll">
              {restaurants.map((r) => (
                <div key={r.id} className="w-[280px]">
                  <RestaurantCard restaurant={r} lt={lt} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Courses Section */}
        {courses.length > 0 && (
          <div className="mt-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-title">{t('nav.courses')}</h2>
              <Link
                href="/courses"
                className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
              >
                {t('common.view_all')}
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="horizontal-scroll">
              {courses.map((c) => (
                <div key={c.id} className="w-[280px]">
                  <CourseCard course={c} lt={lt} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Products Section */}
        {products.length > 0 && (
          <div className="mt-10">
            <div className="flex items-center justify-between mb-4">
              <h2 className="section-title">{t('nav.products')}</h2>
              <Link
                href="/products"
                className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
              >
                {t('common.view_all')}
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="horizontal-scroll">
              {products.map((p) => (
                <div key={p.id} className="w-[280px]">
                  <ProductCard product={p} lt={lt} />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
