'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  Calendar,
  DollarSign,
  CheckCircle,
  XCircle,
  MessageCircle,
  User,
  ChevronLeft,
  ChevronRight,
  LogOut,
} from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useAuth } from '@/hooks/useAuth';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import Tabs from '@/components/ui/Tabs';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import { Booking, ChatRoom } from '@/types';
import { cn, formatDate, formatCurrency } from '@/lib/utils';

interface GuideEarning {
  month: string;
  total: number;
  bookings: { date: string; product_name: string; amount: number }[];
}

export default function GuideDashboardPage() {
  const { t } = useLanguage();
  const { user, isLoggedIn, isLoading: authLoading, logout } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('schedule');
  const [loading, setLoading] = useState(true);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [chatRooms, setChatRooms] = useState<ChatRoom[]>([]);
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [availableDates, setAvailableDates] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (!authLoading && !isLoggedIn) {
      router.push('/auth/login');
      return;
    }
    fetchData();
  }, [authLoading, isLoggedIn]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [bookingData, chatData] = await Promise.all([
        api.get<{ items: Booking[] }>('/api/bookings/my').catch(() => ({ items: [] })),
        api.get<{ items: ChatRoom[] }>('/api/chat/rooms').catch(() => ({ items: [] })),
      ]);
      setBookings(bookingData.items || []);
      setChatRooms(chatData.items || []);
    } catch { /* */ }
    setLoading(false);
  };

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  const toggleDate = (dateStr: string) => {
    const next = new Set(availableDates);
    if (next.has(dateStr)) next.delete(dateStr);
    else next.add(dateStr);
    setAvailableDates(next);
  };

  const pendingBookings = bookings.filter(b => b.status === 'pending');
  const confirmedBookings = bookings.filter(b => b.status === 'confirmed' || b.status === 'completed');

  const tabs = [
    { id: 'schedule', label: 'Schedule' },
    { id: 'bookings', label: `Bookings (${pendingBookings.length})` },
    { id: 'chat', label: 'Chat' },
    { id: 'earnings', label: 'Earnings' },
    { id: 'profile', label: 'Profile' },
  ];

  // Calendar helpers
  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const days = Array.from({ length: firstDay + daysInMonth }, (_, i) => i < firstDay ? null : i - firstDay + 1);
  const weekDays = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

  const getBookingsForDay = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return bookings.filter(b => (b.date || b.booking_date || '').startsWith(dateStr) && b.status === 'confirmed');
  };

  if (authLoading || loading) return <LoadingSpinner fullPage />;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#141414]">
      {/* Header */}
      <header className="bg-white dark:bg-[#1a1a1a] border-b border-gray-200 dark:border-gray-500/40 px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
              <User className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            </div>
            <div>
              <h1 className="font-semibold text-gray-900 dark:text-gray-100">{user?.name || 'Guide'}</h1>
              <p className="text-xs text-gray-500 dark:text-gray-400">Guide Dashboard</p>
            </div>
          </div>
          <button onClick={handleLogout} className="text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400">
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-6">
        <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

        {/* Schedule Tab */}
        {activeTab === 'schedule' && (
          <div>
            <Card className="p-4 mb-4">
              <div className="flex items-center justify-between mb-4">
                <button onClick={() => setCurrentMonth(new Date(year, month - 1, 1))} className="p-1"><ChevronLeft className="w-5 h-5 text-gray-600 dark:text-gray-300" /></button>
                <h2 className="font-semibold text-gray-900 dark:text-gray-100">
                  {currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                </h2>
                <button onClick={() => setCurrentMonth(new Date(year, month + 1, 1))} className="p-1"><ChevronRight className="w-5 h-5 text-gray-600 dark:text-gray-300" /></button>
              </div>
              <div className="grid grid-cols-7 gap-1">
                {weekDays.map(d => (
                  <div key={d} className="text-center text-xs text-gray-400 py-1">{d}</div>
                ))}
                {days.map((day, i) => {
                  if (!day) return <div key={i} />;
                  const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                  const hasBooking = getBookingsForDay(day).length > 0;
                  const isAvailable = availableDates.has(dateStr);
                  return (
                    <button
                      key={i}
                      onClick={() => toggleDate(dateStr)}
                      className={cn(
                        'aspect-square rounded-lg text-sm flex items-center justify-center transition-colors relative',
                        isAvailable ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' : 'hover:bg-gray-100 dark:hover:bg-white/[0.05] text-gray-700 dark:text-gray-300',
                        hasBooking && 'font-bold'
                      )}
                    >
                      {day}
                      {hasBooking && <div className="absolute bottom-0.5 w-1.5 h-1.5 rounded-full bg-indigo-600" />}
                    </button>
                  );
                })}
              </div>
              <p className="text-xs text-gray-400 mt-3">Click dates to toggle availability. Green = available.</p>
            </Card>
          </div>
        )}

        {/* Bookings Tab */}
        {activeTab === 'bookings' && (
          <div className="space-y-4">
            {pendingBookings.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">Pending Requests</h3>
                {pendingBookings.map(b => (
                  <Card key={b.id} className="p-4 mb-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-gray-100">{b.booker_name}</h4>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{formatDate(b.date || b.booking_date || '')}</p>
                        <p className="text-xs text-gray-400 mt-1">{b.participants || b.num_participants} participants</p>
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline" className="text-red-600 border-red-200 hover:bg-red-50 dark:text-red-400 dark:border-red-800">
                          <XCircle className="w-4 h-4 mr-1" /> Decline
                        </Button>
                        <Button size="sm">
                          <CheckCircle className="w-4 h-4 mr-1" /> Accept
                        </Button>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            )}
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">Confirmed Bookings</h3>
              {confirmedBookings.length === 0 ? (
                <EmptyState icon={Calendar} title="No confirmed bookings" />
              ) : (
                confirmedBookings.map(b => (
                  <Card key={b.id} className="p-4 mb-3">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-gray-900 dark:text-gray-100">{b.booker_name}</h4>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{formatDate(b.date || b.booking_date || '')}</p>
                      </div>
                      <Badge variant={b.status === 'completed' ? 'info' : 'success'}>{b.status}</Badge>
                    </div>
                  </Card>
                ))
              )}
            </div>
          </div>
        )}

        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div>
            {chatRooms.length === 0 ? (
              <EmptyState icon={MessageCircle} title="No conversations yet" />
            ) : (
              <div className="space-y-2">
                {chatRooms.map(room => (
                  <Link key={room.id} href={`/chat/${room.id}`}>
                    <Card hoverable className="p-4 flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center flex-shrink-0">
                        <MessageCircle className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-gray-900 dark:text-gray-100 text-sm">{room.guide_name || 'Customer'}</h3>
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

        {/* Earnings Tab */}
        {activeTab === 'earnings' && (
          <div>
            <Card className="p-6 mb-4">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">This Month</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    ${confirmedBookings.reduce((sum, b) => sum + Number(b.total_price || b.total_amount_usd || 0), 0).toFixed(0)}
                  </p>
                </div>
              </div>
            </Card>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">Booking History</h3>
            {confirmedBookings.length === 0 ? (
              <EmptyState icon={DollarSign} title="No earnings yet" />
            ) : (
              <div className="space-y-2">
                {confirmedBookings.map(b => (
                  <Card key={b.id} className="p-4 flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{b.item_name || 'Tour'}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{formatDate(b.date || b.booking_date || '')}</p>
                    </div>
                    <p className="font-bold text-emerald-600 dark:text-emerald-400">${Number(b.total_price || b.total_amount_usd || 0).toFixed(0)}</p>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <Card className="p-6">
            <div className="text-center mb-6">
              <div className="w-20 h-20 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mx-auto mb-3">
                <User className="w-10 h-10 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">{user?.name}</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400">{user?.email}</p>
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
              Profile editing requires admin approval. Contact the administrator to update your guide profile.
            </p>
          </Card>
        )}
      </div>
    </div>
  );
}
