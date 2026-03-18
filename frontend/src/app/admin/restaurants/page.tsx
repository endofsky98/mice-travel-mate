'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, UtensilsCrossed } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import Modal from '@/components/ui/Modal';
import Tabs from '@/components/ui/Tabs';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';
import Select from '@/components/ui/Select';
import { Restaurant, SUPPORTED_LANGUAGES } from '@/types';
import { getPriceRangeSymbol } from '@/lib/utils';

export default function AdminRestaurantsPage() {
  const { t, lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Restaurant[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<Restaurant | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchItems(); }, [currentPage, search]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Restaurant[]; pages: number }>('/api/admin/restaurants', {
        page: currentPage, per_page: 20, search: search || undefined,
      });
      setItems(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    const data: Record<string, string> = { category: 'korean', price_range: '2', phone: '' };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = '';
      data[`description_${l.code}`] = '';
      data[`address_${l.code}`] = '';
      data[`hours_${l.code}`] = '';
    });
    setFormData(data);
    setFormLangTab('en');
    setShowModal(true);
  };

  const openEditModal = (item: Restaurant) => {
    setEditingItem(item);
    const data: Record<string, string> = {
      category: item.category,
      price_range: String(item.price_range),
      phone: item.phone || '',
    };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = typeof item.name === 'object' ? item.name[l.code] || '' : l.code === 'en' ? (item.name as string) : '';
      data[`description_${l.code}`] = typeof item.description === 'object' ? (item.description?.[l.code] || '') : l.code === 'en' ? ((item.description as string) || '') : '';
      data[`address_${l.code}`] = typeof item.address === 'object' ? (item.address?.[l.code] || '') : l.code === 'en' ? ((item.address as string) || '') : '';
      data[`hours_${l.code}`] = typeof item.hours === 'object' ? (item.hours?.[l.code] || '') : l.code === 'en' ? ((item.hours as string) || '') : '';
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
      const address: Record<string, string> = {};
      const hours: Record<string, string> = {};
      SUPPORTED_LANGUAGES.forEach((l) => {
        if (formData[`name_${l.code}`]) name[l.code] = formData[`name_${l.code}`];
        if (formData[`description_${l.code}`]) description[l.code] = formData[`description_${l.code}`];
        if (formData[`address_${l.code}`]) address[l.code] = formData[`address_${l.code}`];
        if (formData[`hours_${l.code}`]) hours[l.code] = formData[`hours_${l.code}`];
      });
      const payload = { name, description, address, hours, category: formData.category, price_range: parseInt(formData.price_range), phone: formData.phone, is_active: true };
      if (editingItem) { await api.put(`/api/admin/restaurants/${editingItem.id}`, payload); }
      else { await api.post('/api/admin/restaurants', payload); }
      setShowModal(false);
      fetchItems();
    } catch { alert('Failed to save'); }
    setSaving(false);
  };

  const handleDelete = async (id: number) => {
    if (!confirm(t('admin.confirm_delete'))) return;
    try { await api.delete(`/api/admin/restaurants/${id}`); fetchItems(); } catch { alert('Failed to delete'); }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));
  const categoryOptions = [
    { value: 'korean', label: t('restaurant.korean') }, { value: 'japanese', label: t('restaurant.japanese') },
    { value: 'chinese', label: t('restaurant.chinese') }, { value: 'western', label: t('restaurant.western') },
    { value: 'fusion', label: t('restaurant.fusion') }, { value: 'cafe', label: t('restaurant.cafe') },
    { value: 'bar', label: t('restaurant.bar') }, { value: 'street_food', label: t('restaurant.street_food') },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t('admin.restaurants')}</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />{t('admin.add_new')}</Button>
      </div>
      <div className="mb-4">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder={t('admin.search_placeholder')} value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={UtensilsCrossed} title={t('common.no_results')} actionLabel={t('admin.add_new')} onAction={openCreateModal} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('common.name')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('restaurant.category')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('restaurant.price_range')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('admin.status')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('admin.actions')}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4 text-sm text-gray-500">{item.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{lt(item.name)}</td>
                    <td className="px-6 py-4 text-sm"><Badge>{item.category}</Badge></td>
                    <td className="px-6 py-4 text-sm text-indigo-600 dark:text-indigo-400 font-medium">{getPriceRangeSymbol(item.price_range)}</td>
                    <td className="px-6 py-4"><Badge variant={item.is_active ? 'success' : 'error'}>{item.is_active ? t('admin.active') : t('admin.inactive')}</Badge></td>
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

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? t('common.edit') : t('admin.add_new')} size="lg">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Select label={t('restaurant.category')} options={categoryOptions} value={formData.category || ''} onChange={(e) => setFormData((p) => ({ ...p, category: e.target.value }))} />
            <Select label={t('restaurant.price_range')} options={[{ value: '1', label: '$' }, { value: '2', label: '$$' }, { value: '3', label: '$$$' }, { value: '4', label: '$$$$' }]} value={formData.price_range || ''} onChange={(e) => setFormData((p) => ({ ...p, price_range: e.target.value }))} />
          </div>
          <Input label={t('restaurant.phone')} value={formData.phone || ''} onChange={(e) => setFormData((p) => ({ ...p, phone: e.target.value }))} />
          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('admin.multilingual')}</p>
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input label={`${t('common.name')} (${formLangTab})`} value={formData[`name_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`name_${formLangTab}`]: e.target.value }))} />
              <Input label={`${t('restaurant.address')} (${formLangTab})`} value={formData[`address_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`address_${formLangTab}`]: e.target.value }))} />
              <Input label={`${t('restaurant.hours')} (${formLangTab})`} value={formData[`hours_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`hours_${formLangTab}`]: e.target.value }))} />
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Description ({formLangTab})</label>
                <textarea className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[80px] resize-y" value={formData[`description_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`description_${formLangTab}`]: e.target.value }))} />
              </div>
            </div>
          </div>
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-500/40">
            <Button variant="outline" onClick={() => setShowModal(false)}>{t('common.cancel')}</Button>
            <Button onClick={handleSave} disabled={saving}>{saving ? t('common.loading') : t('common.save')}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
