'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, Briefcase, Building2, Phone, Mail, Calendar } from 'lucide-react';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import Modal from '@/components/ui/Modal';
import Select from '@/components/ui/Select';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';

interface B2BPartner {
  id: string;
  company_name: string;
  contact_name: string;
  contact_email: string;
  contact_phone?: string;
  business_type?: string;
  assigned_events?: string[];
  assigned_event_names?: string[];
  status: 'active' | 'inactive' | 'pending';
  total_bookings?: number;
  total_revenue?: number;
  commission_rate?: number;
  notes?: string;
  created_at: string;
}

export default function AdminB2BPage() {
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<B2BPartner[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<B2BPartner | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchItems(); }, [currentPage, search]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: B2BPartner[]; pages: number }>('/api/admin/b2b/partners', {
        page: currentPage, per_page: 20, search: search || undefined,
      });
      setItems(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    setFormData({
      company_name: '',
      contact_name: '',
      contact_email: '',
      contact_phone: '',
      business_type: 'agency',
      status: 'active',
      commission_rate: '10',
      assigned_events: '',
      notes: '',
    });
    setShowModal(true);
  };

  const openEditModal = (item: B2BPartner) => {
    setEditingItem(item);
    setFormData({
      company_name: item.company_name || '',
      contact_name: item.contact_name || '',
      contact_email: item.contact_email || '',
      contact_phone: item.contact_phone || '',
      business_type: item.business_type || 'agency',
      status: item.status || 'active',
      commission_rate: String(item.commission_rate || ''),
      assigned_events: (item.assigned_events || []).join(', '),
      notes: item.notes || '',
    });
    setShowModal(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const payload = {
        company_name: formData.company_name,
        contact_name: formData.contact_name,
        contact_email: formData.contact_email,
        contact_phone: formData.contact_phone || undefined,
        business_type: formData.business_type,
        status: formData.status,
        commission_rate: formData.commission_rate ? parseFloat(formData.commission_rate) : undefined,
        assigned_events: formData.assigned_events ? formData.assigned_events.split(',').map((s) => s.trim()).filter(Boolean) : [],
        notes: formData.notes || undefined,
      };
      if (editingItem) {
        await api.put(`/api/admin/b2b/partners/${editingItem.id}`, payload);
      } else {
        await api.post('/api/admin/b2b/partners', payload);
      }
      setShowModal(false);
      fetchItems();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try { await api.delete(`/api/admin/b2b/partners/${id}`); fetchItems(); } catch { alert('삭제에 실패했습니다'); }
  };

  const statusVariant = (status: string) => {
    switch (status) {
      case 'active': return 'success' as const;
      case 'inactive': return 'error' as const;
      case 'pending': return 'warning' as const;
      default: return 'default' as const;
    }
  };

  const statusLabel = (status: string) => {
    switch (status) {
      case 'active': return '활성';
      case 'inactive': return '비활성';
      case 'pending': return '대기';
      default: return status;
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">B2B 파트너 관리</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />파트너 추가</Button>
      </div>

      <div className="mb-4">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder="파트너 검색..." value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={Briefcase} title="B2B 파트너가 없습니다" actionLabel="파트너 추가" onAction={openCreateModal} />
      ) : (
        <>
          {/* Stats Summary */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <Card className="p-4 text-center">
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{items.length}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">전체 파트너</p>
            </Card>
            <Card className="p-4 text-center">
              <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                {items.filter((i) => i.status === 'active').length}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">활성</p>
            </Card>
            <Card className="p-4 text-center">
              <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                ${items.reduce((sum, i) => sum + (i.total_revenue || 0), 0).toLocaleString()}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">총 매출</p>
            </Card>
          </div>

          <Card className="overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-dark-input">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">회사</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">담당자</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">유형</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">이벤트</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">예약</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">매출</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">상태</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">작업</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                  {items.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <Building2 className="w-4 h-4 text-gray-400" />
                          <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{item.company_name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-900 dark:text-gray-100">{item.contact_name}</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
                          <Mail className="w-3 h-3" />{item.contact_email}
                        </div>
                      </td>
                      <td className="px-6 py-4"><Badge>{item.business_type || 'agency'}</Badge></td>
                      <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {item.assigned_event_names?.length ? (
                          <div className="flex flex-wrap gap-1">
                            {item.assigned_event_names.slice(0, 2).map((name, idx) => (
                              <Badge key={idx} variant="info" className="text-[10px]">{name}</Badge>
                            ))}
                            {(item.assigned_event_names.length || 0) > 2 && (
                              <span className="text-xs text-gray-400">+{item.assigned_event_names.length - 2}</span>
                            )}
                          </div>
                        ) : (
                          <span className="text-xs text-gray-400">-</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-sm text-right text-gray-500 dark:text-gray-400">{(item.total_bookings || 0).toLocaleString()}</td>
                      <td className="px-6 py-4 text-sm text-right font-medium text-emerald-600 dark:text-emerald-400">${(item.total_revenue || 0).toLocaleString()}</td>
                      <td className="px-6 py-4"><Badge variant={statusVariant(item.status)}>{statusLabel(item.status)}</Badge></td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <button onClick={() => openEditModal(item)} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded"><Pencil className="w-4 h-4 text-gray-500" /></button>
                          <button onClick={() => handleDelete(item.id)} className="p-1 hover:bg-red-50 dark:hover:bg-red-950/40 rounded"><Trash2 className="w-4 h-4 text-red-500" /></button>
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
        </>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? '파트너 수정' : '파트너 추가'} size="lg">
        <div className="space-y-4">
          <Input label="회사명" value={formData.company_name || ''} onChange={(e) => setFormData((p) => ({ ...p, company_name: e.target.value }))} />
          <div className="grid grid-cols-2 gap-4">
            <Input label="담당자 이름" value={formData.contact_name || ''} onChange={(e) => setFormData((p) => ({ ...p, contact_name: e.target.value }))} />
            <Input label="담당자 이메일" type="email" value={formData.contact_email || ''} onChange={(e) => setFormData((p) => ({ ...p, contact_email: e.target.value }))} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="담당자 전화번호" value={formData.contact_phone || ''} onChange={(e) => setFormData((p) => ({ ...p, contact_phone: e.target.value }))} />
            <Select
              label="업종"
              options={[
                { value: 'agency', label: '여행사' },
                { value: 'hotel', label: '호텔' },
                { value: 'transport', label: '교통' },
                { value: 'venue', label: '행사장' },
                { value: 'media', label: '미디어' },
                { value: 'other', label: '기타' },
              ]}
              value={formData.business_type || 'agency'}
              onChange={(e) => setFormData((p) => ({ ...p, business_type: e.target.value }))}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="수수료율 (%)" type="number" value={formData.commission_rate || ''} onChange={(e) => setFormData((p) => ({ ...p, commission_rate: e.target.value }))} />
            <Select
              label="상태"
              options={[
                { value: 'active', label: '활성' },
                { value: 'inactive', label: '비활성' },
                { value: 'pending', label: '대기' },
              ]}
              value={formData.status || 'active'}
              onChange={(e) => setFormData((p) => ({ ...p, status: e.target.value }))}
            />
          </div>
          <Input label="할당 이벤트 ID (쉼표로 구분)" value={formData.assigned_events || ''} onChange={(e) => setFormData((p) => ({ ...p, assigned_events: e.target.value }))} placeholder="예: 1, 2, 3" />
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">메모</label>
            <textarea
              className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[80px] resize-y"
              value={formData.notes || ''}
              onChange={(e) => setFormData((p) => ({ ...p, notes: e.target.value }))}
            />
          </div>
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-500/40">
            <Button variant="outline" onClick={() => setShowModal(false)}>취소</Button>
            <Button onClick={handleSave} disabled={saving}>{saving ? '로딩 중...' : '저장'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
