'use client';

import { useEffect, useState } from 'react';
import { Search, ClipboardList } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import Select from '@/components/ui/Select';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';
import { Booking } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';

export default function AdminBookingsPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => { fetchBookings(); }, [currentPage, search, statusFilter]);

  const fetchBookings = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Booking[]; pages: number }>('/api/admin/bookings', {
        page: currentPage, per_page: 20, search: search || undefined, status: statusFilter || undefined,
      });
      setBookings(data.items || []); setTotalPages(data.pages || 1);
    } catch { setBookings([]); }
    setLoading(false);
  };

  const handleStatusChange = async (bookingId: number, newStatus: string) => {
    try {
      await api.patch(`/api/admin/bookings/${bookingId}`, { status: newStatus });
      fetchBookings();
    } catch { alert('Failed to update status'); }
  };

  const handleRefund = async (bookingId: number) => {
    if (!confirm('Process refund?')) return;
    try {
      await api.post(`/api/admin/bookings/${bookingId}/refund`);
      fetchBookings();
    } catch { alert('Refund failed'); }
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

  const statusOptions = [
    { value: '', label: t('common.all') },
    { value: 'pending', label: t('booking.status_pending') },
    { value: 'confirmed', label: t('booking.status_confirmed') },
    { value: 'cancelled', label: t('booking.status_cancelled') },
    { value: 'completed', label: t('booking.status_completed') },
  ];

  const changeStatusOptions = [
    { value: 'pending', label: t('booking.status_pending') },
    { value: 'confirmed', label: t('booking.status_confirmed') },
    { value: 'cancelled', label: t('booking.status_cancelled') },
    { value: 'completed', label: t('booking.status_completed') },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('admin.bookings')}</h1>

      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder={t('admin.search_placeholder')} value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
        <div className="w-48">
          <Select options={statusOptions} value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setCurrentPage(1); }} />
        </div>
      </div>

      {loading ? <LoadingSpinner fullPage /> : bookings.length === 0 ? (
        <EmptyState icon={ClipboardList} title={t('common.no_results')} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto"><table className="w-full">
            <thead className="bg-gray-50 dark:bg-dark-input"><tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('booking.booking_number')}</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('booking.booker_name')}</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('booking.date')}</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('booking.participants')}</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('booking.total')}</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('booking.status')}</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('admin.actions')}</th>
            </tr></thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
              {bookings.map((b) => (
                <tr key={b.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                  <td className="px-4 py-4 text-sm font-mono text-gray-900 dark:text-gray-100">{b.booking_number}</td>
                  <td className="px-4 py-4 text-sm text-gray-900 dark:text-gray-100">
                    <div>{b.booker_name}</div>
                    <div className="text-xs text-gray-400">{b.booker_email}</div>
                  </td>
                  <td className="px-4 py-4 text-sm text-gray-500">{formatDate(b.date)}</td>
                  <td className="px-4 py-4 text-sm text-gray-500">{b.participants}</td>
                  <td className="px-4 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{formatCurrency(b.total_price, b.currency)}</td>
                  <td className="px-4 py-4">
                    <select
                      value={b.status}
                      onChange={(e) => handleStatusChange(b.id, e.target.value)}
                      className="text-xs rounded-lg border border-gray-200 dark:border-gray-500/40 px-2 py-1 bg-transparent dark:bg-dark-input"
                    >
                      {changeStatusOptions.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                    </select>
                  </td>
                  <td className="px-4 py-4">
                    <Button variant="destructive" size="sm" onClick={() => handleRefund(b.id)}>
                      {t('admin.refund')}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table></div>
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-500/40">
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
          </div>
        </Card>
      )}
    </div>
  );
}
