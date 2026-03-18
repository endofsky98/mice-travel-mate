'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  BarChart3,
  Users,
  Calendar,
  DollarSign,
  ExternalLink,
  Tag,
  Bell,
  Eye,
  TrendingUp,
  LogOut,
} from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useAuth } from '@/hooks/useAuth';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Tabs from '@/components/ui/Tabs';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';

interface B2BStats {
  total_visits: number;
  total_bookings: number;
  total_revenue: number;
  active_promotions: number;
}

export default function B2BDashboardPage() {
  const { t } = useLanguage();
  const { user, isLoggedIn, isLoading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<B2BStats>({
    total_visits: 0,
    total_bookings: 0,
    total_revenue: 0,
    active_promotions: 0,
  });

  useEffect(() => {
    if (!authLoading && !isLoggedIn) {
      router.push('/auth/login');
      return;
    }
    fetchStats();
  }, [authLoading, isLoggedIn]);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const data = await api.get<B2BStats>('/api/b2b/dashboard/stats');
      setStats(data);
    } catch { /* use defaults */ }
    setLoading(false);
  };

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'landing', label: 'Landing Config' },
    { id: 'promotions', label: 'Promotions' },
    { id: 'notifications', label: 'Notifications' },
  ];

  if (authLoading || loading) return <LoadingSpinner fullPage />;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#141414]">
      {/* Header */}
      <header className="bg-white dark:bg-[#1a1a1a] border-b border-gray-200 dark:border-gray-500/40 px-4 py-3">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="font-bold text-lg text-gray-900 dark:text-gray-100">B2B Partner Dashboard</h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
          </div>
          <button onClick={handleLogout} className="text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400">
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-6">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <Card className="p-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center mb-3">
                  <Eye className="w-5 h-5 text-white" />
                </div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.total_visits.toLocaleString()}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">Total Visits</p>
              </Card>
              <Card className="p-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center mb-3">
                  <Calendar className="w-5 h-5 text-white" />
                </div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.total_bookings}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">Total Bookings</p>
              </Card>
              <Card className="p-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center mb-3">
                  <DollarSign className="w-5 h-5 text-white" />
                </div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">${stats.total_revenue.toLocaleString()}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">Total Revenue</p>
              </Card>
              <Card className="p-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center mb-3">
                  <Tag className="w-5 h-5 text-white" />
                </div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.active_promotions}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400">Active Promotions</p>
              </Card>
            </div>
            <Card className="p-6">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                Performance Trends
              </h3>
              <div className="h-48 flex items-center justify-center text-gray-400 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-xl">
                <BarChart3 className="w-8 h-8 mr-2" /> Charts will appear with data
              </div>
            </Card>
          </div>
        )}

        {/* Landing Config Tab */}
        {activeTab === 'landing' && (
          <Card className="p-6">
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-4">Exhibition Landing Configuration</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
              Configure your exhibition&apos;s landing page with custom banners, recommended content, and promotions.
            </p>
            <div className="space-y-4">
              <div className="p-4 border border-gray-200 dark:border-gray-600 rounded-xl">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Banner Image</h4>
                <div className="h-32 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center text-gray-400">
                  Upload banner image
                </div>
              </div>
              <div className="p-4 border border-gray-200 dark:border-gray-600 rounded-xl">
                <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">Recommended Content</h4>
                <p className="text-sm text-gray-500 dark:text-gray-400">Select restaurants, courses, and products to feature on your landing page.</p>
              </div>
              <div className="flex gap-3 justify-end">
                <Button variant="outline">Preview</Button>
                <Button>Save Configuration</Button>
              </div>
            </div>
          </Card>
        )}

        {/* Promotions Tab */}
        {activeTab === 'promotions' && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100">Promotion Codes</h3>
              <Button size="sm"><Tag className="w-4 h-4 mr-1" /> Create Code</Button>
            </div>
            <EmptyState icon={Tag} title="No promotion codes yet" description="Create promotion codes for your exhibition attendees" />
          </div>
        )}

        {/* Notifications Tab */}
        {activeTab === 'notifications' && (
          <Card className="p-6">
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center gap-2">
              <Bell className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
              Send Notification to Attendees
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Send email notifications to exhibition attendees with travel recommendations.
            </p>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Subject</label>
                <input className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100" placeholder="Notification subject" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Message</label>
                <textarea className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[120px]" placeholder="Write your message..." />
              </div>
              <Button>Send Notification</Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
