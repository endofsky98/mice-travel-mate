'use client';

import { useEffect, useState } from 'react';
import { Search, Star, Check, Trash2, AlertTriangle, Flag } from 'lucide-react';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import Select from '@/components/ui/Select';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';
import { Review } from '@/types';
import { formatDate } from '@/lib/utils';

export default function AdminReviewsPage() {
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Review[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterRating, setFilterRating] = useState('');
  const [filterReported, setFilterReported] = useState('');

  useEffect(() => { fetchItems(); }, [currentPage, search, filterType, filterStatus, filterRating, filterReported]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Review[]; pages: number }>('/api/admin/reviews', {
        page: currentPage,
        per_page: 20,
        search: search || undefined,
        target_type: filterType || undefined,
        status: filterStatus || undefined,
        rating: filterRating || undefined,
        is_reported: filterReported || undefined,
      });
      setItems(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const handleApprove = async (id: string) => {
    try {
      await api.patch(`/api/admin/reviews/${id}`, { status: 'approved' });
      fetchItems();
    } catch { alert('승인에 실패했습니다'); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('이 리뷰를 삭제하시겠습니까?')) return;
    try {
      await api.patch(`/api/admin/reviews/${id}`, { status: 'deleted' });
      fetchItems();
    } catch { alert('삭제에 실패했습니다'); }
  };

  const statusVariant = (status: string) => {
    switch (status) {
      case 'approved': return 'success' as const;
      case 'pending': return 'warning' as const;
      case 'deleted': return 'error' as const;
      default: return 'default' as const;
    }
  };

  const statusLabel = (status: string) => {
    switch (status) {
      case 'approved': return '승인';
      case 'pending': return '대기';
      case 'deleted': return '삭제됨';
      default: return status;
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">리뷰 관리</h1>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-4 flex-wrap">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder="리뷰 검색..." value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
        <Select
          options={[
            { value: '', label: '전체 유형' },
            { value: 'restaurant', label: '맛집' },
            { value: 'course', label: '코스' },
            { value: 'product', label: '상품' },
            { value: 'guide', label: '가이드' },
          ]}
          value={filterType}
          onChange={(e) => { setFilterType(e.target.value); setCurrentPage(1); }}
          className="w-40"
        />
        <Select
          options={[
            { value: '', label: '전체 상태' },
            { value: 'pending', label: '대기' },
            { value: 'approved', label: '승인' },
            { value: 'deleted', label: '삭제됨' },
          ]}
          value={filterStatus}
          onChange={(e) => { setFilterStatus(e.target.value); setCurrentPage(1); }}
          className="w-40"
        />
        <Select
          options={[
            { value: '', label: '전체 별점' },
            { value: '5', label: '5점' },
            { value: '4', label: '4점' },
            { value: '3', label: '3점' },
            { value: '2', label: '2점' },
            { value: '1', label: '1점' },
          ]}
          value={filterRating}
          onChange={(e) => { setFilterRating(e.target.value); setCurrentPage(1); }}
          className="w-36"
        />
        <Select
          options={[
            { value: '', label: '전체 신고' },
            { value: 'true', label: '신고됨' },
            { value: 'false', label: '신고 없음' },
          ]}
          value={filterReported}
          onChange={(e) => { setFilterReported(e.target.value); setCurrentPage(1); }}
          className="w-40"
        />
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={Star} title="리뷰가 없습니다" />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">사용자</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">대상</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">별점</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">내용</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">날짜</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">상태</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">작업</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {items.map((item) => (
                  <tr
                    key={item.id}
                    className={`hover:bg-gray-50 dark:hover:bg-white/[0.02] ${item.is_reported ? 'bg-red-50/50 dark:bg-red-950/10' : ''}`}
                  >
                    <td className="px-6 py-4 text-sm text-gray-900 dark:text-gray-100">
                      <div className="flex items-center gap-2">
                        {item.user_name || item.user_id}
                        {item.is_reported && <Flag className="w-3.5 h-3.5 text-red-500" />}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <Badge>{item.target_type}</Badge>
                      <span className="ml-1 text-gray-500 dark:text-gray-400">{item.target_id}</span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-0.5">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <Star
                            key={i}
                            className={`w-3.5 h-3.5 ${i < item.rating ? 'text-amber-400 fill-amber-400' : 'text-gray-300 dark:text-gray-600'}`}
                          />
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700 dark:text-gray-300 max-w-[300px]">
                      <p className="line-clamp-2">{item.content}</p>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {formatDate(item.created_at)}
                    </td>
                    <td className="px-6 py-4">
                      <Badge variant={statusVariant(item.status)}>{statusLabel(item.status)}</Badge>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        {item.status === 'pending' && (
                          <button onClick={() => handleApprove(item.id)} className="p-1 hover:bg-green-50 dark:hover:bg-green-950/40 rounded" title="승인">
                            <Check className="w-4 h-4 text-green-600" />
                          </button>
                        )}
                        {item.status !== 'deleted' && (
                          <button onClick={() => handleDelete(item.id)} className="p-1 hover:bg-red-50 dark:hover:bg-red-950/40 rounded" title="삭제">
                            <Trash2 className="w-4 h-4 text-red-500" />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-500/40">
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
          </div>
        </Card>
      )}
    </div>
  );
}
