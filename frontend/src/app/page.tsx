'use client';

import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import {
  ArrowRight,
  Sparkles,
  MapPin,
  Bus,
  ShoppingBag,
  Utensils,
  Globe,
  CreditCard,
  Phone,
  AlertTriangle,
  BookOpen,
  Calendar,
} from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import RollingBanner from '@/components/ui/RollingBanner';
import LocationBar from '@/components/ui/LocationBar';
import SearchBar from '@/components/ui/SearchBar';
import FilterChips from '@/components/ui/FilterChips';
import StarRating from '@/components/ui/StarRating';
import RestaurantCard from '@/components/restaurant/RestaurantCard';
import CourseCard from '@/components/course/CourseCard';
import ProductCard from '@/components/product/ProductCard';
import GuideCard from '@/components/guide/GuideCard';
import Card from '@/components/ui/Card';
import {
  RollingBanner as BannerType,
  Event,
  Restaurant,
  Course,
  Product,
  Guide,
  Festival,
} from '@/types';
import { cn, formatDateRange } from '@/lib/utils';

export default function HomePage() {
  const { t, lt, language } = useLanguage();
  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(true);

  const [banners, setBanners] = useState<BannerType[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [guides, setGuides] = useState<Guide[]>([]);
  const [festivals, setFestivals] = useState<Festival[]>([]);

  const [userLat, setUserLat] = useState(37.5665);
  const [userLng, setUserLng] = useState(126.978);
  const [restaurantFilter, setRestaurantFilter] = useState('');

  const eventSlug = searchParams.get('event');

  const handleLocationChange = useCallback((lat: number, lng: number, label: string) => {
    setUserLat(lat);
    setUserLng(lng);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch banners
        const bannerData = await api.get<{ items: BannerType[] }>('/api/banners', {
          event_id: eventSlug || undefined,
        }).catch(() => ({ items: [] }));
        setBanners(bannerData.items || []);

        // If event slug, fetch event data
        if (eventSlug) {
          try {
            const eventData = await api.get<Event>(`/api/events/${eventSlug}`);
            setSelectedEvent(eventData);
          } catch {
            setSelectedEvent(null);
          }
        }

        // Fetch all section data in parallel
        const [restData, courseData, prodData, guideData, festData] = await Promise.all([
          api.get<{ items: Restaurant[] }>('/api/restaurants', {
            per_page: 10,
            lat: userLat,
            lng: userLng,
            ...(eventSlug ? {} : {}),
          }).catch(() => ({ items: [] })),
          api.get<{ items: Course[] }>('/api/courses', { per_page: 10 }).catch(() => ({ items: [] })),
          api.get<{ items: Product[] }>('/api/products', { per_page: 10 }).catch(() => ({ items: [] })),
          api.get<{ items: Guide[] }>('/api/guides', { per_page: 10 }).catch(() => ({ items: [] })),
          api.get<{ items: Festival[] }>('/api/festivals', { per_page: 6 }).catch(() => ({ items: [] })),
        ]);

        setRestaurants(restData.items || []);
        setCourses(courseData.items || []);
        setProducts(prodData.items || []);
        setGuides(guideData.items || []);
        setFestivals(festData.items || []);
      } catch { /* silently handle */ }
      setLoading(false);
    };

    fetchData();
  }, [eventSlug, language]);

  if (loading) return <LoadingSpinner fullPage />;

  const restaurantCategoryChips = [
    { key: '', label: t('common.all') || 'All' },
    { key: 'korean', label: t('category.korean') || 'Korean' },
    { key: 'japanese', label: t('category.japanese') || 'Japanese' },
    { key: 'chinese', label: t('category.chinese') || 'Chinese' },
    { key: 'western', label: t('category.western') || 'Western' },
    { key: 'cafe', label: t('category.cafe') || 'Cafe' },
    { key: 'street_food', label: t('category.street_food') || 'Street Food' },
  ];

  const livingGuideItems = [
    { href: '/living-guide?cat=transportation', icon: Bus, label: t('living_guide.transportation') || 'Transportation' },
    { href: '/living-guide?cat=food_culture', icon: Utensils, label: t('living_guide.food_culture') || 'Food Culture' },
    { href: '/living-guide?cat=shopping', icon: ShoppingBag, label: t('living_guide.shopping') || 'Shopping' },
    { href: '/living-guide?cat=currency', icon: CreditCard, label: t('living_guide.currency') || 'Currency' },
    { href: '/living-guide?cat=telecom', icon: Phone, label: t('living_guide.telecom') || 'Telecom' },
    { href: '/living-guide?cat=emergency', icon: AlertTriangle, label: t('living_guide.emergency') || 'Emergency' },
    { href: '/living-guide?cat=etiquette', icon: BookOpen, label: t('living_guide.etiquette') || 'Etiquette' },
  ];

  const filteredRestaurants = restaurantFilter
    ? restaurants.filter((r) => r.category === restaurantFilter)
    : restaurants;

  return (
    <div className="pb-20 md:pb-0">
      {/* 1. Rolling Banner */}
      <RollingBanner banners={banners} lt={lt} />

      {/* 2. Location Bar */}
      <LocationBar
        t={t}
        onLocationChange={handleLocationChange}
        eventLat={selectedEvent?.latitude || selectedEvent?.venue_lat}
        eventLng={selectedEvent?.longitude || selectedEvent?.venue_lng}
        eventName={selectedEvent ? lt(selectedEvent.name) : undefined}
      />

      {/* 3. Unified Search Bar */}
      <SearchBar t={t} language={language} />

      {/* 4. Nearby Restaurants Section */}
      {filteredRestaurants.length > 0 && (
        <section className="py-6">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-bold text-gray-900 dark:text-white">
                {t('home.nearby_restaurants') || 'Nearby Restaurants'}
              </h2>
              <Link
                href="/restaurants"
                className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
              >
                {t('common.view_all') || 'View All'}
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <FilterChips
              chips={restaurantCategoryChips}
              selected={restaurantFilter}
              onSelect={setRestaurantFilter}
              className="mb-4"
            />
            <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">
              {filteredRestaurants.slice(0, 8).map((r) => (
                <div key={r.id} className="w-[260px] flex-shrink-0">
                  <RestaurantCard restaurant={r} lt={lt} />
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* 5. Mini Map Section */}
      <section className="py-4 bg-gray-50 dark:bg-[#1a1a1a]">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <MapPin className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
              {t('home.nearby_map') || 'Explore Nearby'}
            </h2>
            <Link
              href="/map"
              className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              {t('common.view_on_map') || 'Full Map'}
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="w-full h-[200px] rounded-xl bg-gray-200 dark:bg-gray-800 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <MapPin className="w-8 h-8 mx-auto mb-2" />
              <p className="text-sm">{t('map.explore_title') || 'Interactive Map'}</p>
              <Link href="/map" className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline mt-1 inline-block">
                {t('common.view_on_map') || 'Open Map'}
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Recommended Courses Section */}
      {courses.length > 0 && (
        <section className="py-6">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-bold text-gray-900 dark:text-white">
                {t('home.recommended_courses') || 'Recommended Courses'}
              </h2>
              <Link href="/courses" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all') || 'View All'} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">
              {courses.map((c) => (
                <div key={c.id} className="w-[280px] flex-shrink-0">
                  <CourseCard course={c} lt={lt} />
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* 7. Travel Products Section */}
      {products.length > 0 && (
        <section className="py-6 bg-gray-50 dark:bg-[#1a1a1a]">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-bold text-gray-900 dark:text-white">
                {t('home.travel_products') || 'Tours & Activities'}
              </h2>
              <Link href="/products" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all') || 'View All'} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">
              {products.map((p) => (
                <div key={p.id} className="w-[280px] flex-shrink-0">
                  <ProductCard product={p} lt={lt} />
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* 8. Guide Recommendations Section */}
      {guides.length > 0 && (
        <section className="py-6">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-bold text-gray-900 dark:text-white">
                {t('home.guide_recommendations') || 'Recommended Guides'}
              </h2>
              <Link href="/guides" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all') || 'View All'} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">
              {guides.map((g) => (
                <div key={g.id} className="w-[260px] flex-shrink-0">
                  <GuideCard guide={g} lt={lt} />
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* 9. Festivals & Events Section */}
      {festivals.length > 0 && (
        <section className="py-6 bg-gray-50 dark:bg-[#1a1a1a]">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <Calendar className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                {t('home.festivals_events') || 'Festivals & Events'}
              </h2>
              <Link href="/festivals" className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                {t('common.view_all') || 'View All'} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="flex gap-4 overflow-x-auto scrollbar-hide pb-2">
              {festivals.map((f) => (
                <Link key={f.id} href={`/festivals/${f.id}`} className="w-[260px] flex-shrink-0">
                  <Card hoverable className="h-full">
                    <div className="relative aspect-[16/10] overflow-hidden">
                      {f.image_url ? (
                        <img src={f.image_url} alt={lt(f.name)} className="w-full h-full object-cover" />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-pink-500 to-orange-500 flex items-center justify-center">
                          <Calendar className="w-10 h-10 text-white/60" />
                        </div>
                      )}
                    </div>
                    <div className="p-3">
                      <h3 className="font-semibold text-sm text-gray-900 dark:text-gray-100 line-clamp-1">{lt(f.name)}</h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        {f.start_date && f.end_date ? formatDateRange(f.start_date, f.end_date) : ''}
                      </p>
                    </div>
                  </Card>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* 10. AI Course Generation Banner */}
      <section className="py-6">
        <div className="max-w-7xl mx-auto px-4">
          <Link href="/ai-course">
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 p-6 md:p-10">
              <div className="relative z-10">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles className="w-6 h-6 text-white" />
                  <span className="text-white/80 text-sm font-medium">AI Powered</span>
                </div>
                <h2 className="text-xl md:text-2xl font-bold text-white mb-2">
                  {t('home.ai_course_banner_title') || 'Create Your Perfect Course'}
                </h2>
                <p className="text-white/80 text-sm md:text-base max-w-md">
                  {t('home.ai_course_banner_desc') || 'Tell us your preferences and we\'ll build a personalized travel course just for you.'}
                </p>
                <div className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 bg-white/20 backdrop-blur-sm rounded-lg text-white text-sm font-medium hover:bg-white/30 transition-colors">
                  {t('button.generate_course') || 'Generate Course'}
                  <ArrowRight className="w-4 h-4" />
                </div>
              </div>
              <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-white/10 to-transparent" />
            </div>
          </Link>
        </div>
      </section>

      {/* 11. Korean Living Guide Section */}
      <section className="py-6 bg-gray-50 dark:bg-[#1a1a1a]">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
            {t('home.living_guide_title') || 'Korea Living Guide'}
          </h2>
          <div className="grid grid-cols-4 sm:grid-cols-7 gap-3">
            {livingGuideItems.map((item) => (
              <Link key={item.href} href={item.href} className="flex flex-col items-center gap-1.5 p-3 rounded-xl hover:bg-white dark:hover:bg-[#1e1e1e] transition-colors">
                <div className="w-11 h-11 rounded-full bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
                  <item.icon className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                </div>
                <span className="text-[11px] text-center font-medium text-gray-600 dark:text-gray-300 line-clamp-1">
                  {item.label}
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
