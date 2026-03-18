'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { User, Settings, ClipboardList, Bookmark, MessageCircle, Scale, LogOut } from 'lucide-react';
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
import { Booking, Restaurant, Course, Product, Guide, ChatRoom, SUPPORTED_LANGUAGES } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';

export default function MyPage() {
  const { t, lt, language } = useLanguage();
  const { user, isLoggedIn, isLoading: authLoading, logout } = useAuth();
  const { getBookmarksByType } = useBookmarks();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('bookings');
  const [bookmarkSubTab, setBookmarkSubTab] = useState('restaurants');
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [chatRooms, setChatRooms] = useState<ChatRoom[]>([]);
  const [loading, setLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [profileName, setProfileName] = useState('');
  const [profileNationality, setProfileNationality] = useState('');
  const [profileLanguage, setProfileLanguage] = useState('');
  const [selectedForCompare, setSelectedForCompare] = useState<Set<string>>(new Set());

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
      setSelectedForCompare(new Set());
    } else if (activeTab === 'chat') {
      fetchChatRooms();
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

  const fetchChatRooms = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: ChatRoom[] }>('/api/chat/rooms');
      setChatRooms(data.items || []);
    } catch {
      setChatRooms([]);
    }
    setLoading(false);
  };

  const fetchBookmarkedItems = async () => {
    setLoading(true);
    try {
      const type = bookmarkSubTab.endsWith('s') ? bookmarkSubTab.slice(0, -1) : bookmarkSubTab;
      const ids = getBookmarksByType(type as 'restaurant' | 'course' | 'product' | 'guide');
      if (ids.length === 0) {
        setBookmarkedRestaurants([]);
        setBookmarkedCourses([]);
        setBookmarkedProducts([]);
        setBookmarkedGuides([]);
        setLoading(false);
        return;
      }
      const endpoint = `/api/${bookmarkSubTab === 'restaurants' ? 'restaurants' : bookmarkSubTab === 'courses' ? 'courses' : bookmarkSubTab === 'products' ? 'products' : 'guides'}`;
      const data = await api.get<{ items: (Restaurant | Course | Product | Guide)[] }>(endpoint, { ids: ids.join(',') });
      const items = data.items || [];
      if (bookmarkSubTab === 'restaurants') setBookmarkedRestaurants(items as Restaurant[]);
      else if (bookmarkSubTab === 'courses') setBookmarkedCourses(items as Course[]);
      else if (bookmarkSubTab === 'products') setBookmarkedProducts(items as Product[]);
      else if (bookmarkSubTab === 'guides') setBookmarkedGuides(items as Guide[]);
    } catch { /* */ }
    setLoading(false);
  };

  const toggleCompareItem = (id: string) => {
    const next = new Set(selectedForCompare);
    if (next.has(id)) {
      next.delete(id);
    } else if (next.size < 4) {
      next.add(id);
    }
    setSelectedForCompare(next);
  };

  const handleCompare = () => {
    const ids = Array.from(selectedForCompare).join(',');
    const type = bookmarkSubTab.endsWith('s') ? bookmarkSubTab.slice(0, -1) : bookmarkSubTab;
    router.push(`/compare?type=${type}&ids=${ids}`);
  };

  const handleSaveProfile = async () => {
    try {
      await api.put('/api/auth/profile', { name: profileName, nationality: profileNationality, preferred_language: profileLanguage });
      setEditMode(false);
    } catch { /* */ }
  };

  const handleLogout = async () => {
    await logout();
    router.push('/');
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
    { id: 'bookings', label: t('mypage.bookings') || 'Bookings' },
    { id: 'bookmarks', label: t('mypage.bookmarks') || 'Bookmarks' },
    { id: 'chat', label: t('nav.chat') || 'Chat' },
    { id: 'profile', label: t('mypage.profile') || 'Profile' },
  ];

  const bookmarkTabs = [
    { id: 'restaurants', label: t('nav.restaurants') || 'Restaurants' },
    { id: 'courses', label: t('nav.courses') || 'Courses' },
    { id: 'products', label: t('nav.products') || 'Products' },
    { id: 'guides', label: t('nav.guides') || 'Guides' },
  ];

  const languageOptions = SUPPORTED_LANGUAGES.map(l => ({ value: l.code, label: l.name }));

  return (
    <div className="page-container max-w-4xl pb-20 md:pb-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t('mypage.title') || 'My Page'}</h1>
        <button onClick={handleLogout} className="flex items-center gap-1 text-sm text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400">
          <LogOut className="w-4 h-4" /> {t('button.logout') || 'Logout'}
        </button>
      </div>

      {/* Profile Summary */}
      <Card className="p-4 mb-6">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
            <User className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
          </div>
          <div>
            <h2 className="font-semibold text-gray-900 dark:text-gray-100">{user?.name}</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">{user?.email}</p>
          </div>
        </div>
      </Card>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

      {/* Bookings Tab */}
      {activeTab === 'bookings' && (
        <div>
          {loading ? <LoadingSpinner fullPage /> : bookings.length === 0 ? (
            <EmptyState icon={ClipboardList} title={t('mypage.no_bookings') || 'No bookings yet'} />
          ) : (
            <div className="space-y-3">
              {bookings.map((booking) => (
                <Card key={booking.id} className="p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium text-gray-900 dark:text-gray-100">
                          {booking.item_name || `${booking.type || booking.booking_type} #${booking.item_id || booking.id}`}
                        </h3>
                        <Badge variant={statusVariant(booking.status)}>{booking.status}</Badge>
                      </div>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {formatDate(booking.date || booking.booking_date || '')}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">#{booking.booking_number}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-indigo-600 dark:text-indigo-400">
                        ${Number(booking.total_price || booking.total_amount_usd || 0).toFixed(0)}
                      </p>
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
          <div className="flex items-center justify-between mb-4">
            <Tabs tabs={bookmarkTabs} activeTab={bookmarkSubTab} onChange={setBookmarkSubTab} />
            {selectedForCompare.size >= 2 && (
              <Button size="sm" onClick={handleCompare}>
                <Scale className="w-4 h-4 mr-1" /> {t('common.compare') || 'Compare'} ({selectedForCompare.size})
              </Button>
            )}
          </div>

          {loading ? <LoadingSpinner fullPage /> : (
            <>
              {bookmarkSubTab === 'restaurants' && (
                bookmarkedRestaurants.length === 0 ? <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks') || 'No bookmarks'} /> : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedRestaurants.map((r) => (
                      <div key={r.id} className="relative">
                        <input
                          type="checkbox"
                          checked={selectedForCompare.has(String(r.id))}
                          onChange={() => toggleCompareItem(String(r.id))}
                          className="absolute top-2 left-2 z-10 w-5 h-5 accent-indigo-600"
                        />
                        <RestaurantCard restaurant={r} lt={lt} />
                      </div>
                    ))}
                  </div>
                )
              )}
              {bookmarkSubTab === 'courses' && (
                bookmarkedCourses.length === 0 ? <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks') || 'No bookmarks'} /> : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedCourses.map((c) => (
                      <div key={c.id} className="relative">
                        <input type="checkbox" checked={selectedForCompare.has(String(c.id))} onChange={() => toggleCompareItem(String(c.id))} className="absolute top-2 left-2 z-10 w-5 h-5 accent-indigo-600" />
                        <CourseCard course={c} lt={lt} />
                      </div>
                    ))}
                  </div>
                )
              )}
              {bookmarkSubTab === 'products' && (
                bookmarkedProducts.length === 0 ? <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks') || 'No bookmarks'} /> : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedProducts.map((p) => (
                      <div key={p.id} className="relative">
                        <input type="checkbox" checked={selectedForCompare.has(String(p.id))} onChange={() => toggleCompareItem(String(p.id))} className="absolute top-2 left-2 z-10 w-5 h-5 accent-indigo-600" />
                        <ProductCard product={p} lt={lt} />
                      </div>
                    ))}
                  </div>
                )
              )}
              {bookmarkSubTab === 'guides' && (
                bookmarkedGuides.length === 0 ? <EmptyState icon={Bookmark} title={t('mypage.no_bookmarks') || 'No bookmarks'} /> : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {bookmarkedGuides.map((g) => (
                      <div key={g.id} className="relative">
                        <input type="checkbox" checked={selectedForCompare.has(String(g.id))} onChange={() => toggleCompareItem(String(g.id))} className="absolute top-2 left-2 z-10 w-5 h-5 accent-indigo-600" />
                        <GuideCard guide={g} lt={lt} />
                      </div>
                    ))}
                  </div>
                )
              )}
            </>
          )}
        </div>
      )}

      {/* Chat Tab */}
      {activeTab === 'chat' && (
        <div>
          {loading ? <LoadingSpinner fullPage /> : chatRooms.length === 0 ? (
            <EmptyState icon={MessageCircle} title={t('chat.no_messages') || 'No conversations yet'} description={t('chat.start_chat') || 'Start a chat from a guide page'} />
          ) : (
            <div className="space-y-2">
              {chatRooms.map((room) => (
                <Link key={room.id} href={`/chat/${room.id}`}>
                  <Card hoverable className="p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center flex-shrink-0">
                      {room.guide_image ? (
                        <img src={room.guide_image} alt="" className="w-10 h-10 rounded-full object-cover" />
                      ) : (
                        <MessageCircle className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-gray-900 dark:text-gray-100 text-sm">{room.guide_name || 'Guide'}</h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{room.last_message || '...'}</p>
                    </div>
                    {room.unread_count > 0 && (
                      <div className="w-5 h-5 rounded-full bg-indigo-600 text-white text-xs flex items-center justify-center flex-shrink-0">
                        {room.unread_count}
                      </div>
                    )}
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Profile Tab */}
      {activeTab === 'profile' && (
        <Card className="p-6">
          <div className="space-y-4">
            <Input label={t('auth.name') || 'Name'} value={profileName} onChange={(e) => setProfileName(e.target.value)} />
            <Input label={t('auth.nationality') || 'Nationality'} value={profileNationality} onChange={(e) => setProfileNationality(e.target.value)} />
            <Select label={t('mypage.preferred_language') || 'Preferred Language'} options={languageOptions} value={profileLanguage} onChange={(e) => setProfileLanguage(e.target.value)} />
            <div className="flex gap-3 justify-end pt-4">
              <Button onClick={handleSaveProfile}>{t('common.save') || 'Save'}</Button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
