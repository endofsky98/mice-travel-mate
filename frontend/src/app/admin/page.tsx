'use client';

import { useEffect, useState } from 'react';
import {
  Calendar,
  UtensilsCrossed,
  Map,
  ShoppingBag,
  Users,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Eye,
  AlertTriangle,
  Search,
  Star,
} from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { Booking } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';

interface DashboardStats {
  today_bookings: number;
  today_booking_amount: number;
  total_restaurants: number;
  total_courses: number;
  total_products: number;
  total_guides: number;
  today_visitors: number;
  visitor_trend: number;
  untranslated_count: number;
}

interface PendingReview {
  id: string;
  user_name: string;
  target_type: string;
  target_name: string;
  rating: number;
  content: string;
  created_at: string;
}

interface PopularSearch {
  keyword: string;
  count: number;
}

export default function AdminDashboardPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats>({
    today_bookings: 0,
    today_booking_amount: 0,
    total_restaurants: 0,
    total_courses: 0,
    total_products: 0,
    total_guides: 0,
    today_visitors: 0,
    visitor_trend: 0,
    untranslated_count: 0,
  });
  const [recentBookings, setRecentBookings] = useState<Booking[]>([]);
  const [pendingReviews, setPendingReviews] = useState<PendingReview[]>([]);
  const [popularSearches, setPopularSearches] = useState<PopularSearch[]>([]);

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true);
      try {
        const [statsData, bookingsData, reviewsData, searchesData] = await Promise.all([
          api.get<DashboardStats>('/api/admin/dashboard/stats').catch(() => ({
            today_bookings: 0, today_booking_amount: 0, total_restaurants: 0, total_courses: 0,
            total_products: 0, total_guides: 0, today_visitors: 0, visitor_trend: 0, untranslated_count: 0,
          })),
          api.get<{ items: Booking[] }>('/api/admin/bookings', { per_page: 10, sort: 'newest' }).catch(() => ({ items: [] })),
          api.get<{ items: PendingReview[] }>('/api/admin/reviews', { status: 'pending', per_page: 5 }).catch(() => ({ items: [] })),
          api.get<{ items: PopularSearch[] }>('/api/admin/analytics/searches', { per_page: 10 }).catch(() => ({ items: [] })),
        ]);
        setStats(statsData);
        setRecentBookings(bookingsData.items || []);
        setPendingReviews(reviewsData.items || []);
        setPopularSearches(searchesData.items || []);
      } catch {
        // silent
      }
      setLoading(false);
    };
    fetchDashboard();
  }, []);

  const statusVariant = (status: string) => {
    switch (status) {
      case 'confirmed': return 'success' as const;
      case 'pending': return 'warning' as const;
      case 'cancelled': return 'error' as const;
      case 'completed': return 'info' as const;
      default: return 'default' as const;
    }
  };

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('admin.dashboard')}</h1>

      {/* Untranslated Alert */}
      {stats.untranslated_count > 0 && (
        <div className="mb-6 p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0" />
          <p className="text-sm text-amber-800 dark:text-amber-300">
            <span className="font-semibold">{stats.untranslated_count}</span> items have incomplete translations. Please review the Languages section.
          </p>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
        {/* Today's Bookings */}
        <Card className="p-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-blue-500 flex items-center justify-center mb-3">
            <Calendar className="w-5 h-5 text-white" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.today_bookings}</p>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Today&apos;s Bookings</p>
        </Card>

        {/* Today's Booking Amount */}
        <Card className="p-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center mb-3">
            <DollarSign className="w-5 h-5 text-white" />
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{formatCurrency(stats.today_booking_amount, 'KRW')}</p>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Today&apos;s Revenue</p>
        </Card>

        {/* Total Content */}
        <Card className="p-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-500 flex items-center justify-center mb-3">
            <ShoppingBag className="w-5 h-5 text-white" />
          </div>
          <div className="flex items-baseline gap-2 flex-wrap">
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {stats.total_restaurants + stats.total_courses + stats.total_products + stats.total_guides}
            </p>
          </div>
          <div className="flex flex-wrap gap-x-3 gap-y-0.5 mt-1">
            <span className="text-[10px] text-gray-400"><UtensilsCrossed className="w-3 h-3 inline mr-0.5" />{stats.total_restaurants}</span>
            <span className="text-[10px] text-gray-400"><Map className="w-3 h-3 inline mr-0.5" />{stats.total_courses}</span>
            <span className="text-[10px] text-gray-400"><ShoppingBag className="w-3 h-3 inline mr-0.5" />{stats.total_products}</span>
            <span className="text-[10px] text-gray-400"><Users className="w-3 h-3 inline mr-0.5" />{stats.total_guides}</span>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Total Content</p>
        </Card>

        {/* Today's Visitors */}
        <Card className="p-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center mb-3">
            <Eye className="w-5 h-5 text-white" />
          </div>
          <div className="flex items-center gap-2">
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.today_visitors.toLocaleString()}</p>
            {stats.visitor_trend !== 0 && (
              <span className={`flex items-center text-xs font-medium ${stats.visitor_trend > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                {stats.visitor_trend > 0 ? <TrendingUp className="w-3 h-3 mr-0.5" /> : <TrendingDown className="w-3 h-3 mr-0.5" />}
                {Math.abs(stats.visitor_trend)}%
              </span>
            )}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Today&apos;s Visitors</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Recent Bookings */}
        <Card className="overflow-hidden lg:col-span-2">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-500/40">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{t('admin.recent_bookings')}</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    {t('booking.booking_number')}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    {t('booking.booker_name')}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    {t('booking.date')}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    {t('booking.total')}
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    {t('booking.status')}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {recentBookings.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
                      {t('common.no_results')}
                    </td>
                  </tr>
                ) : (
                  recentBookings.map((booking) => (
                    <tr key={booking.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                      <td className="px-6 py-4 text-sm font-mono text-gray-900 dark:text-gray-100">
                        {booking.booking_number}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-900 dark:text-gray-100">
                        {booking.booker_name}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {formatDate(booking.date)}
                      </td>
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">
                        {formatCurrency(booking.total_price, booking.currency)}
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant={statusVariant(booking.status)}>
                          {t(`booking.status_${booking.status}`)}
                        </Badge>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Pending Reviews */}
        <Card className="overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-500/40">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <Star className="w-5 h-5 text-amber-500" />
              Pending Reviews
            </h2>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-500/40">
            {pendingReviews.length === 0 ? (
              <div className="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
                No pending reviews
              </div>
            ) : (
              pendingReviews.map((review) => (
                <div key={review.id} className="px-6 py-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{review.user_name}</span>
                    <div className="flex items-center gap-0.5">
                      {Array.from({ length: 5 }).map((_, i) => (
                        <Star
                          key={i}
                          className={`w-3 h-3 ${i < review.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`}
                        />
                      ))}
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-1">
                    {review.target_type}: {review.target_name}
                  </p>
                  <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">{review.content}</p>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>

      {/* Popular Searches */}
      <Card className="overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-500/40">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <Search className="w-5 h-5 text-indigo-500" />
            Popular Searches (Top 10)
          </h2>
        </div>
        <div className="p-6">
          {popularSearches.length === 0 ? (
            <p className="text-sm text-gray-500 dark:text-gray-400 text-center py-4">No search data available</p>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {popularSearches.map((search, idx) => (
                <div
                  key={search.keyword}
                  className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-dark-input"
                >
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${idx < 3 ? 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300' : 'bg-gray-200 text-gray-600 dark:bg-gray-700 dark:text-gray-400'}`}>
                    {idx + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{search.keyword}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{search.count.toLocaleString()} searches</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
