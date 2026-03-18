'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { User, Settings, UtensilsCrossed, Map, ShoppingBag, Users, ClipboardList, Bookmark } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useAuth } from '@/hooks/useAuth';
import { useBookmarks } from '@/hooks/useBookmarks';
import api from '@/lib/api';
import Tabs from '@/components/ui/Tabs';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Select from '@/components/ui/Select';
import EmptyState from '@/components/ui/EmptyState';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import RestaurantCard from '@/components/restaurant/RestaurantCard';
import CourseCard from '@/components/course/CourseCard';
import ProductCard from '@/components/product/ProductCard';
import GuideCard from '@/components/guide/GuideCard';
import { Booking, Restaurant, Course, Product, Guide } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';

export default function MyPage() {
  const { t, lt, language } = useLanguage();
  const { user, isLoggedIn, isLoading: authLoading } = useAuth();
  const { getBookmarksByType } = useBookmarks();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('bookings');
  const [bookmarkSubTab, setBookmarkSubTab] = useState('restaurants');
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [profileName, setProfileName] = useState('');
  const [profileNationality, setProfileNationality] = useState('');
  const [profileLanguage, setProfileLanguage] = useState('');

  // Bookmark items
  const [bookmarkedRestaurants, setBookmarkedRestaurants] = useState<Restaurant[]>([]);
  const [bookmarkedCourses, setBookmarkedCourses] = useState<Course[]>([]);
  const [bookmarkedProducts, setBookmarkedProducts] = useState<Product[]>([]);
  const [bookmarkedGuides, setBookmarkedGuides] = useState<Guide[]>([]);

  useEffect(() => {
    if (!authLoading && !isLoggedIn) {
      router.push('/auth/login');
    }
  }, [authLoading, isLoggedIn, router]);

  useEffect(() => {
    if (user) {
      setProfileName(user.name);
      setProfileNationality(user.nationality || '');
      setProfileLanguage(user.preferred_language || language);
    }
  }, [user, language]);

  useEffect(() => {
    if (isLoggedIn) {
      fetchBookings();
    }
  }, [isLoggedIn, language]);

  useEffect(() => {
    if (activeTab === 'bookmarks') {
      fetchBookmarkedItems();
    }
  }, [activeTab, bookmarkSubTab]);

  const fetchBookings = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Booking[] }>('/api/bookings/my');
      setBookings(data.items || []);
    } catch {
      setBookings([]);
    }
    setLoading(false);
  };

  const fetchBookmarkedItems = async () => {
    setLoading(true);
    try {
      const ids = getBookmarksByType(bookmarkSubTab as 'restaurant' | 'course' | 'product' | 'guide');
      if (ids.length === 0) {
        setBookmarkedRestaurants([]);
        setBookmarkedCourses([]);
        setBookmarkedProducts([]);
        setBookmarkedGuides([]);
        setLoading(false);
        return;
      }

      const endpoint = `/api/${bookmarkSubTab === 'restaurant' ? 'restaurants' : bookmarkSubTab === 'course' ? 'courses' : bookmarkSubTab === 'product' ? 'products' : 'guides'}`;
      const data = await api.get<{ items: (Restaurant | Course | Product | Guide)[] }>(endpoint, { ids: ids.join(',') });
      const items = data.items || [];

      if (bookmarkSubTab === 'restaurants') setBookmarkedRestaurants(items as Restaurant[]);
      else if (bookmarkSubTab === 'courses') setBookmarkedCourses(items as Course[]);
      else if (bookmarkSubTab === 'products') setBookmarkedProducts(items as Product[]);
      else if (bookmarkSubTab === 'guides') setBookmarkedGuides(items as Guide[]);
    } catch {
      // Silent fail
    }
    setLoading(false);
  };

  const handleSaveProfile = async () => {
    try {
      await api.put('/api/auth/profile', {
        name: profileName,
        nationality: profileNationality,
        preferred_language: profileLanguage,
      });
      setEditMode(false);
    } catch {
      // Handle error
    }
  };

  const statusVariant = (status: string) => {
    switch (status) {
      case 'confirmed': return 'success' as const;
      case 'pending': return 'warning' as const;
      case 'cancelled': return 'error' as const;
      case 'completed': return 'info' as const;
      default: return 'default' as const;
    }
  };

  if (authLoading) return <LoadingSpinner fullPage />;
  if (!isLoggedIn) return null;

  const tabs = [
    { id: 'bookings', label: t('mypage.bookings') },
    { id: 'bookmarks', label: t('mypage.bookmarks') },
  ];

  const bookmarkTabs = [
    { id: 'restaurants', label: t('nav.restaurants') },
    { id: 'courses', label: t('nav.courses') },
    { id: 'products', label: t('nav.products') },
    { id: 'guides', label: t('nav.guides') },
  ];

  const languageOptions = [
    { value: 'en', label: 'English' },
    { value: 'ko', label: '한국어' },
    { value: 'ja', label: '日本語' },
    { value: 'zh-CN', label: '简体中文' },
    { value: 'zh-TW', label: '繁體中文' },
    { value: 'es', label: 'Español' },
  ];

  return (
    <div className="page-container max-w-4xl">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('mypage.title')}</h1>

      {/* Profile Section */}
      <Card className="p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
              <User className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900 dark:text-gray-100">{user?.name}</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">{user?.email}</p>
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={() => setEditMode(!editMode)}>
            <Settings className="w-4 h-4" />
            {t('mypage.edit_profile')}
          </Button>
        </div>

        {editMode && (
          <div className="pt-4 border-t border-gray-200 dark:border-gray-500/40 space-y-4">
            <Input
              label={t('auth.name')}
              value={profileName}
              onChange={(e) => setProfileName(e.target.value)}
            />
            <Input
              label={t('auth.nationality')}
              value={profileNationality}
              onChange={(e) => setProfileNationality(e.target.value)}
            />
            <Select
              label={t('mypage.preferred_language')}
              options={languageOptions}
              value={profileLanguage}
              onChange={(e) => setProfileLanguage(e.target.value)}
            />
            <div className="flex gap-3 justify-end">
              <Button variant="outline" onClick={() => setEditMode(false)}>{t('common.cancel')}</Button>
              <Button onClick={handleSaveProfile}>{t('common.save')}</Button>
            </div>
          </div>
        )}
      </Card>

      {/* Tabs */}
      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

      {/* Bookings Tab */}
      {activeTab === 'bookings' && (
        <div>
          {loading ? (
            <LoadingSpinner fullPage />
          ) : bookings.length === 0 ? (
            <EmptyState icon={ClipboardList} title={t('mypage.no_bookings')} />
          ) : (
            <div className="space-y-3">
              {bookings.map((booking) => (
                <Card key={booking.id} className="p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium text-gray-900 dark:text-gray-100">
                          {booking.item_name || `${booking.type} #${booking.item_id}`}
                        </h3>
                        <Badge variant={statusVariant(booking.status)}>
                          {t(`booking.status_${booking.status}`)}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {formatDate(booking.date)} {booking.time && `| ${booking.time}`}
                      </p>
                      <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                        {t('booking.booking_number')}: {booking.booking_number}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-indigo-600 dark:text-indigo-400">
                        {formatCurrency(booking.total_price, booking.currency)}
                      </p>
                      <p className="text-xs text-gray-400">{booking.participants} {t('booking.participants')}</p>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Bookmarks Tab */}
      {activeTab === 'bookmarks' && (
        <div>
          <Tabs tabs={bookmarkTabs} activeTab={bookmarkSubTab} onChange={setBookmarkSubTab} className="mb-6" />

          {loading ? (
            <LoadingSpinner fullPage />
          ) : (
            <>
              {bookmarkSubTab === 'restaurants' && (
                bookmarkedRestaurants.length === 0 ? (
                  <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks')} />
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedRestaurants.map((r) => <RestaurantCard key={r.id} restaurant={r} lt={lt} />)}
                  </div>
                )
              )}
              {bookmarkSubTab === 'courses' && (
                bookmarkedCourses.length === 0 ? (
                  <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks')} />
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedCourses.map((c) => <CourseCard key={c.id} course={c} lt={lt} />)}
                  </div>
                )
              )}
              {bookmarkSubTab === 'products' && (
                bookmarkedProducts.length === 0 ? (
                  <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks')} />
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedProducts.map((p) => <ProductCard key={p.id} product={p} lt={lt} />)}
                  </div>
                )
              )}
              {bookmarkSubTab === 'guides' && (
                bookmarkedGuides.length === 0 ? (
                  <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks')} />
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedGuides.map((g) => <GuideCard key={g.id} guide={g} lt={lt} />)}
                  </div>
                )
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
