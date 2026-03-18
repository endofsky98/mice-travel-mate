'use client';

import { useEffect, useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  Users,
  Eye,
  ShoppingBag,
  Search,
  Calendar,
} from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import Select from '@/components/ui/Select';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

interface VisitorStats {
  today: number;
  yesterday: number;
  this_week: number;
  this_month: number;
  trend_percent: number;
}

interface SearchKeyword {
  keyword: string;
  count: number;
  trend: 'up' | 'down' | 'stable';
}

interface ContentPopularity {
  id: string;
  name: string;
  type: string;
  views: number;
  bookmarks: number;
  reviews: number;
}

interface BookingStats {
  total_bookings: number;
  total_revenue: number;
  avg_order_value: number;
  conversion_rate: number;
  top_products: { name: string; count: number; revenue: number }[];
}

interface EventComparison {
  event_name: string;
  visitors: number;
  bookings: number;
  revenue: number;
  avg_rating: number;
}

export default function AdminAnalyticsPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('7d');
  const [visitorStats, setVisitorStats] = useState<VisitorStats>({
    today: 0, yesterday: 0, this_week: 0, this_month: 0, trend_percent: 0,
  });
  const [searchKeywords, setSearchKeywords] = useState<SearchKeyword[]>([]);
  const [contentPopularity, setContentPopularity] = useState<ContentPopularity[]>([]);
  const [bookingStats, setBookingStats] = useState<BookingStats>({
    total_bookings: 0, total_revenue: 0, avg_order_value: 0, conversion_rate: 0, top_products: [],
  });
  const [eventComparison, setEventComparison] = useState<EventComparison[]>([]);

  useEffect(() => { fetchAnalytics(); }, [period]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const [visitors, searches, content, bookings, events] = await Promise.all([
        api.get<VisitorStats>('/api/admin/analytics/visitors', { period }).catch(() => ({
          today: 0, yesterday: 0, this_week: 0, this_month: 0, trend_percent: 0,
        })),
        api.get<{ items: SearchKeyword[] }>('/api/admin/analytics/searches', { period, per_page: 15 }).catch(() => ({ items: [] })),
        api.get<{ items: ContentPopularity[] }>('/api/admin/analytics/content', { period, per_page: 10 }).catch(() => ({ items: [] })),
        api.get<BookingStats>('/api/admin/analytics/bookings', { period }).catch(() => ({
          total_bookings: 0, total_revenue: 0, avg_order_value: 0, conversion_rate: 0, top_products: [],
        })),
        api.get<{ items: EventComparison[] }>('/api/admin/analytics/events', { period }).catch(() => ({ items: [] })),
      ]);
      setVisitorStats(visitors);
      setSearchKeywords(searches.items || []);
      setContentPopularity(content.items || []);
      setBookingStats(bookings);
      setEventComparison(events.items || []);
    } catch {
      // silent
    }
    setLoading(false);
  };

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Analytics Dashboard</h1>
        <Select
          options={[
            { value: '1d', label: 'Today' },
            { value: '7d', label: 'Last 7 Days' },
            { value: '30d', label: 'Last 30 Days' },
            { value: '90d', label: 'Last 90 Days' },
          ]}
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          className="w-40"
        />
      </div>

      {/* Visitor Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <Card className="p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
              <Eye className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400">Today</span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{visitorStats.today.toLocaleString()}</p>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <Users className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400">Yesterday</span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{visitorStats.yesterday.toLocaleString()}</p>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400">This Week</span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{visitorStats.this_week.toLocaleString()}</p>
        </Card>
        <Card className="p-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-8 h-8 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
              <Calendar className="w-4 h-4 text-amber-600 dark:text-amber-400" />
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400">This Month</span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{visitorStats.this_month.toLocaleString()}</p>
        </Card>
      </div>

      {/* Chart Placeholder */}
      <Card className="p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Visitor Trend</h2>
        <div className="h-64 bg-gray-50 dark:bg-dark-input rounded-xl flex items-center justify-center">
          <div className="text-center">
            <BarChart3 className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-2" />
            <p className="text-sm text-gray-500 dark:text-gray-400">Chart visualization</p>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
              {visitorStats.trend_percent >= 0 ? '+' : ''}{visitorStats.trend_percent}% vs previous period
            </p>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Search Keyword Ranking */}
        <Card className="overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-500/40">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <Search className="w-5 h-5 text-indigo-500" />
              Search Keywords
            </h2>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-500/40">
            {searchKeywords.length === 0 ? (
              <div className="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400">No search data</div>
            ) : (
              searchKeywords.map((kw, idx) => (
                <div key={kw.keyword} className="flex items-center justify-between px-6 py-3">
                  <div className="flex items-center gap-3">
                    <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${idx < 3 ? 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300' : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'}`}>
                      {idx + 1}
                    </span>
                    <span className="text-sm text-gray-900 dark:text-gray-100">{kw.keyword}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{kw.count.toLocaleString()}</span>
                    <Badge variant={kw.trend === 'up' ? 'success' : kw.trend === 'down' ? 'error' : 'default'} className="text-[10px]">
                      {kw.trend === 'up' ? 'UP' : kw.trend === 'down' ? 'DOWN' : '-'}
                    </Badge>
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>

        {/* Content Popularity */}
        <Card className="overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-500/40">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <ShoppingBag className="w-5 h-5 text-violet-500" />
              Content Popularity
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Type</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Views</th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Reviews</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {contentPopularity.length === 0 ? (
                  <tr><td colSpan={4} className="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400">No data</td></tr>
                ) : (
                  contentPopularity.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                      <td className="px-6 py-3 text-sm font-medium text-gray-900 dark:text-gray-100 truncate max-w-[200px]">{item.name}</td>
                      <td className="px-6 py-3"><Badge>{item.type}</Badge></td>
                      <td className="px-4 py-3 text-sm text-right text-gray-500 dark:text-gray-400">{item.views.toLocaleString()}</td>
                      <td className="px-4 py-3 text-sm text-right text-gray-500 dark:text-gray-400">{item.reviews}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      {/* Booking Stats */}
      <Card className="p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Booking Summary</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center p-3 bg-gray-50 dark:bg-dark-input rounded-xl">
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{bookingStats.total_bookings.toLocaleString()}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Total Bookings</p>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-dark-input rounded-xl">
            <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">${bookingStats.total_revenue.toLocaleString()}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Total Revenue</p>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-dark-input rounded-xl">
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">${bookingStats.avg_order_value.toFixed(0)}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Avg Order Value</p>
          </div>
          <div className="text-center p-3 bg-gray-50 dark:bg-dark-input rounded-xl">
            <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{bookingStats.conversion_rate}%</p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Conversion Rate</p>
          </div>
        </div>
        {bookingStats.top_products.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">Top Products</h3>
            <div className="space-y-2">
              {bookingStats.top_products.map((product, idx) => (
                <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-dark-input rounded-lg">
                  <span className="text-sm text-gray-900 dark:text-gray-100">{product.name}</span>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-gray-500">{product.count} bookings</span>
                    <span className="font-medium text-emerald-600 dark:text-emerald-400">${product.revenue.toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>

      {/* Event Comparison */}
      <Card className="overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-500/40">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Event Comparison</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-dark-input">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Event</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Visitors</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Bookings</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Revenue</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Avg Rating</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
              {eventComparison.length === 0 ? (
                <tr><td colSpan={5} className="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400">No event data</td></tr>
              ) : (
                eventComparison.map((event, idx) => (
                  <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{event.event_name}</td>
                    <td className="px-6 py-4 text-sm text-right text-gray-500 dark:text-gray-400">{event.visitors.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-right text-gray-500 dark:text-gray-400">{event.bookings.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-right font-medium text-emerald-600 dark:text-emerald-400">${event.revenue.toLocaleString()}</td>
                    <td className="px-6 py-4 text-sm text-right text-amber-600 dark:text-amber-400">{event.avg_rating.toFixed(1)}</td>
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
