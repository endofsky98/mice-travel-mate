'use client';

import { useEffect, useState } from 'react';
import { Search, ClipboardList } from 'lucide-react';
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
    } catch { alert('상태 변경에 실패했습니다'); }
  };

  const handleRefund = async (bookingId: number) => {
    if (!confirm('환불을 진행하시겠습니까?')) return;
    try {
      await api.post(`/api/admin/bookings/${bookingId}/refund`);
      fetchBookings();
    } catch { alert('환불에 실패했습니다'); }
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
    { value: '', label: '전체' },
    { value: 'pending', label: '대기' },
    { value: 'confirmed', label: '확정' },
    { value: 'cancelled', label: '취소' },
    { value: 'completed', label: '완료' },
  ];

  const changeStatusOptions = [
    { value: 'pending', label: '대기' },
    { value: 'confirmed', label: '확정' },
    { value: 'cancelled', label: '취소' },
    { value: 'completed', label: '완료' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">예약</h1>

      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder="검색어를 입력하세요..." value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
        <div className="w-48">
          <Select options={statusOptions} value={statusFilter} onChange={(e) => { setStatusFilter(e.target.value); setCurrentPage(1); }} />
        </div>
      </div>

      {loading ? <LoadingSpinner fullPage /> : bookings.length === 0 ? (
        <EmptyState icon={ClipboardList} title="결과가 없습니다" />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto"><table className="w-full">
            <thead className="bg-gray-50 dark:bg-dark-input"><tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">예약번호</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">예약자명</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">날짜</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">인원</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">합계</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">상태</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">작업</th>
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
                      환불
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
