'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, ShoppingBag } from 'lucide-react';
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
import { Product, SUPPORTED_LANGUAGES } from '@/types';
import { formatCurrency } from '@/lib/utils';

export default function AdminProductsPage() {
  const { lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Product[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<Product | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchItems(); }, [currentPage, search]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Product[]; pages: number }>('/api/admin/products', { page: currentPage, per_page: 20, search: search || undefined });
      setItems(data.items || []); setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    const data: Record<string, string> = { category: 'tour', price: '0', currency: 'KRW', duration: '', region: '' };
    SUPPORTED_LANGUAGES.forEach((l) => { data[`name_${l.code}`] = ''; data[`description_${l.code}`] = ''; });
    setFormData(data); setFormLangTab('en'); setShowModal(true);
  };

  const openEditModal = (item: Product) => {
    setEditingItem(item);
    const data: Record<string, string> = { category: item.category, price: String(item.price), currency: item.currency, duration: item.duration || '', region: item.region || '' };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = typeof item.name === 'object' ? item.name[l.code] || '' : l.code === 'en' ? (item.name as string) : '';
      data[`description_${l.code}`] = typeof item.description === 'object' ? (item.description?.[l.code] || '') : l.code === 'en' ? ((item.description as string) || '') : '';
    });
    setFormData(data); setFormLangTab('en'); setShowModal(true);
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
      const payload = { name, description, category: formData.category, price: parseFloat(formData.price), currency: formData.currency, duration: formData.duration, region: formData.region, is_active: true };
      if (editingItem) await api.put(`/api/admin/products/${editingItem.id}`, payload);
      else await api.post('/api/admin/products', payload);
      setShowModal(false); fetchItems();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try { await api.delete(`/api/admin/products/${id}`); fetchItems(); } catch { alert('삭제에 실패했습니다'); }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">상품</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />추가</Button>
      </div>
      <div className="mb-4"><div className="relative max-w-md"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" /><Input placeholder="검색어를 입력하세요..." value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" /></div></div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={ShoppingBag} title="결과가 없습니다" actionLabel="추가" onAction={openCreateModal} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input"><tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">이름</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">카테고리</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">가격</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">상태</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">작업</th>
              </tr></thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4 text-sm text-gray-500">{item.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{lt(item.name)}</td>
                    <td className="px-6 py-4"><Badge>{item.category}</Badge></td>
                    <td className="px-6 py-4 text-sm font-medium text-indigo-600 dark:text-indigo-400">{formatCurrency(item.price, item.currency)}</td>
                    <td className="px-6 py-4"><Badge variant={item.is_active ? 'success' : 'error'}>{item.is_active ? '활성' : '비활성'}</Badge></td>
                    <td className="px-6 py-4"><div className="flex gap-2">
                      <button onClick={() => openEditModal(item)} className="p-1 hover:bg-gray-100 rounded"><Pencil className="w-4 h-4 text-gray-500" /></button>
                      <button onClick={() => handleDelete(item.id)} className="p-1 hover:bg-red-50 rounded"><Trash2 className="w-4 h-4 text-red-500" /></button>
                    </div></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-500/40"><Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} /></div>
        </Card>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? '수정' : '추가'} size="lg">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Select label="카테고리" options={[{ value: 'tour', label: '투어' }, { value: 'experience', label: '체험' }, { value: 'class', label: '클래스' }, { value: 'ticket', label: '티켓' }, { value: 'package', label: '패키지' }]} value={formData.category || ''} onChange={(e) => setFormData((p) => ({ ...p, category: e.target.value }))} />
            <Input label="가격" type="number" value={formData.price || ''} onChange={(e) => setFormData((p) => ({ ...p, price: e.target.value }))} />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <Input label="통화" value={formData.currency || ''} onChange={(e) => setFormData((p) => ({ ...p, currency: e.target.value }))} />
            <Input label="소요시간" value={formData.duration || ''} onChange={(e) => setFormData((p) => ({ ...p, duration: e.target.value }))} />
            <Input label="지역" value={formData.region || ''} onChange={(e) => setFormData((p) => ({ ...p, region: e.target.value }))} />
          </div>
          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">다국어 콘텐츠</p>
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input label={`이름 (${formLangTab})`} value={formData[`name_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`name_${formLangTab}`]: e.target.value }))} />
              <div><label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">설명 ({formLangTab})</label>
              <textarea className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[80px] resize-y" value={formData[`description_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`description_${formLangTab}`]: e.target.value }))} /></div>
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
