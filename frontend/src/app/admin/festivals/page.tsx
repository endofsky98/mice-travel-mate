'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, PartyPopper, Calendar } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import Modal from '@/components/ui/Modal';
import Tabs from '@/components/ui/Tabs';
import Select from '@/components/ui/Select';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';
import { Festival, SUPPORTED_LANGUAGES } from '@/types';
import { formatDateRange } from '@/lib/utils';

export default function AdminFestivalsPage() {
  const { lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Festival[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<Festival | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchItems(); }, [currentPage, search, filterCategory]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Festival[]; pages: number }>('/api/admin/festivals', {
        page: currentPage, per_page: 20, search: search || undefined, category: filterCategory || undefined,
      });
      setItems(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    const data: Record<string, string> = {
      category: 'cultural',
      start_date: '',
      end_date: '',
      latitude: '',
      longitude: '',
      image_url: '',
      venue_name: '',
      address: '',
      website_url: '',
      is_active: 'true',
    };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = '';
      data[`description_${l.code}`] = '';
    });
    setFormData(data);
    setFormLangTab('en');
    setShowModal(true);
  };

  const openEditModal = (item: Festival) => {
    setEditingItem(item);
    const data: Record<string, string> = {
      category: item.category || 'cultural',
      start_date: item.start_date?.split('T')[0] || '',
      end_date: item.end_date?.split('T')[0] || '',
      latitude: String(item.latitude || ''),
      longitude: String(item.longitude || ''),
      image_url: item.image_url || '',
      venue_name: item.venue_name || '',
      address: item.address || '',
      website_url: item.website_url || '',
      is_active: String(item.is_active),
    };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = typeof item.name === 'object' ? item.name[l.code] || '' : l.code === 'en' ? (item.name as string) : '';
      data[`description_${l.code}`] = typeof item.description === 'object' ? (item.description?.[l.code] || '') : l.code === 'en' ? ((item.description as string) || '') : '';
    });
    setFormData(data);
    setFormLangTab('en');
    setShowModal(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const name: Record<string, string> = {};
      const description: Record<string, string> = {};
      SUPPORTED_LANGUAGES.forEach((l) => {
        if (formData[`name_${l.code}`]) name[l.code] = formData[`name_${l.code}`];
        if (formData[`description_${l.code}`]) description[l.code] = formData[`description_${l.code}`];
      });
      const payload = {
        name,
        description,
        category: formData.category,
        start_date: formData.start_date,
        end_date: formData.end_date,
        latitude: formData.latitude ? parseFloat(formData.latitude) : undefined,
        longitude: formData.longitude ? parseFloat(formData.longitude) : undefined,
        image_url: formData.image_url || undefined,
        venue_name: formData.venue_name || undefined,
        address: formData.address || undefined,
        website_url: formData.website_url || undefined,
        is_active: formData.is_active === 'true',
      };
      if (editingItem) {
        await api.put(`/api/admin/festivals/${editingItem.id}`, payload);
      } else {
        await api.post('/api/admin/festivals', payload);
      }
      setShowModal(false);
      fetchItems();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try { await api.delete(`/api/admin/festivals/${id}`); fetchItems(); } catch { alert('삭제에 실패했습니다'); }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));
  const categoryOptions = [
    { value: 'cultural', label: '문화' },
    { value: 'music', label: '음악' },
    { value: 'food', label: '음식' },
    { value: 'traditional', label: '전통' },
    { value: 'seasonal', label: '계절' },
    { value: 'art', label: '예술' },
    { value: 'sports', label: '스포츠' },
    { value: 'other', label: '기타' },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">축제 관리</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />축제 추가</Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder="축제 검색..." value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
        <Select
          options={[{ value: '', label: '전체 카테고리' }, ...categoryOptions]}
          value={filterCategory}
          onChange={(e) => { setFilterCategory(e.target.value); setCurrentPage(1); }}
          className="w-48"
        />
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={PartyPopper} title="축제가 없습니다" actionLabel="축제 추가" onAction={openCreateModal} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">이름</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">카테고리</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">기간</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">상태</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">작업</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4 text-sm text-gray-500">{item.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{lt(item.name)}</td>
                    <td className="px-6 py-4 text-sm"><Badge>{item.category}</Badge></td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {formatDateRange(item.start_date, item.end_date)}
                    </td>
                    <td className="px-6 py-4"><Badge variant={item.is_active ? 'success' : 'error'}>{item.is_active ? '활성' : '비활성'}</Badge></td>
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
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? '축제 수정' : '축제 추가'} size="lg">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Select label="카테고리" options={categoryOptions} value={formData.category || ''} onChange={(e) => setFormData((p) => ({ ...p, category: e.target.value }))} />
            <Select
              label="상태"
              options={[{ value: 'true', label: '활성' }, { value: 'false', label: '비활성' }]}
              value={formData.is_active || 'true'}
              onChange={(e) => setFormData((p) => ({ ...p, is_active: e.target.value }))}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="시작일" type="date" value={formData.start_date || ''} onChange={(e) => setFormData((p) => ({ ...p, start_date: e.target.value }))} />
            <Input label="종료일" type="date" value={formData.end_date || ''} onChange={(e) => setFormData((p) => ({ ...p, end_date: e.target.value }))} />
          </div>
          <Input label="장소명" value={formData.venue_name || ''} onChange={(e) => setFormData((p) => ({ ...p, venue_name: e.target.value }))} />
          <Input label="주소" value={formData.address || ''} onChange={(e) => setFormData((p) => ({ ...p, address: e.target.value }))} />
          <div className="grid grid-cols-2 gap-4">
            <Input label="위도" type="number" step="any" value={formData.latitude || ''} onChange={(e) => setFormData((p) => ({ ...p, latitude: e.target.value }))} />
            <Input label="경도" type="number" step="any" value={formData.longitude || ''} onChange={(e) => setFormData((p) => ({ ...p, longitude: e.target.value }))} />
          </div>
          <Input label="이미지 URL" value={formData.image_url || ''} onChange={(e) => setFormData((p) => ({ ...p, image_url: e.target.value }))} />
          <Input label="웹사이트 URL" value={formData.website_url || ''} onChange={(e) => setFormData((p) => ({ ...p, website_url: e.target.value }))} />

          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">다국어 콘텐츠</p>
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input label={`이름 (${formLangTab})`} value={formData[`name_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`name_${formLangTab}`]: e.target.value }))} />
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">설명 ({formLangTab})</label>
                <textarea
                  className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[100px] resize-y"
                  value={formData[`description_${formLangTab}`] || ''}
                  onChange={(e) => setFormData((p) => ({ ...p, [`description_${formLangTab}`]: e.target.value }))}
                />
              </div>
            </div>
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
