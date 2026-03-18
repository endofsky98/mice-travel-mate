'use client';

import { useEffect, useState } from 'react';
import { Calendar, UtensilsCrossed, Map, ShoppingBag, Users } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { Booking } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';

interface DashboardStats {
  today_bookings: number;
  total_restaurants: number;
  total_courses: number;
  total_products: number;
  total_guides: number;
}

export default function AdminDashboardPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats>({
    today_bookings: 0,
    total_restaurants: 0,
    total_courses: 0,
    total_products: 0,
    total_guides: 0,
  });
  const [recentBookings, setRecentBookings] = useState<Booking[]>([]);

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true);
      try {
        const [statsData, bookingsData] = await Promise.all([
          api.get<DashboardStats>('/api/admin/dashboard/stats').catch(() => ({
            today_bookings: 0, total_restaurants: 0, total_courses: 0, total_products: 0, total_guides: 0,
          })),
          api.get<{ items: Booking[] }>('/api/admin/bookings', { per_page: 10, sort: 'newest' }).catch(() => ({ items: [] })),
        ]);
        setStats(statsData);
        setRecentBookings(bookingsData.items || []);
      } catch {
        // silent
      }
      setLoading(false);
    };
    fetchDashboard();
  }, []);

  const statCards = [
    { label: t('admin.today_bookings'), value: stats.today_bookings, icon: Calendar, color: 'from-indigo-500 to-blue-500' },
    { label: t('admin.total_restaurants'), value: stats.total_restaurants, icon: UtensilsCrossed, color: 'from-orange-500 to-red-500' },
    { label: t('admin.total_courses'), value: stats.total_courses, icon: Map, color: 'from-emerald-500 to-teal-500' },
    { label: t('admin.total_products'), value: stats.total_products, icon: ShoppingBag, color: 'from-violet-500 to-purple-500' },
    { label: t('admin.total_guides'), value: stats.total_guides, icon: Users, color: 'from-amber-500 to-orange-500' },
  ];

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

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
        {statCards.map((stat) => (
          <Card key={stat.label} className="p-4">
            <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center mb-3`}>
              <stat.icon className="w-5 h-5 text-white" />
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stat.value}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{stat.label}</p>
          </Card>
        ))}
      </div>

      {/* Recent Bookings */}
      <Card className="overflow-hidden">
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
    </div>
  );
}
