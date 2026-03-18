'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, Map } from 'lucide-react';
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
import { Course, SUPPORTED_LANGUAGES } from '@/types';

export default function AdminCoursesPage() {
  const { t, lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<Course[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<Course | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchItems(); }, [currentPage, search]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Course[]; pages: number }>('/api/admin/courses', { page: currentPage, per_page: 20, search: search || undefined });
      setItems(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    const data: Record<string, string> = { duration: 'half_day', difficulty: 'easy', theme: 'culture', region: '' };
    SUPPORTED_LANGUAGES.forEach((l) => { data[`name_${l.code}`] = ''; data[`description_${l.code}`] = ''; });
    setFormData(data); setFormLangTab('en'); setShowModal(true);
  };

  const openEditModal = (item: Course) => {
    setEditingItem(item);
    const data: Record<string, string> = { duration: item.duration, difficulty: item.difficulty, theme: item.theme, region: item.region || '' };
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
      const payload = { name, description, duration: formData.duration, difficulty: formData.difficulty, theme: formData.theme, region: formData.region, is_active: true };
      if (editingItem) await api.put(`/api/admin/courses/${editingItem.id}`, payload);
      else await api.post('/api/admin/courses', payload);
      setShowModal(false); fetchItems();
    } catch { alert('Failed to save'); }
    setSaving(false);
  };

  const handleDelete = async (id: number) => {
    if (!confirm(t('admin.confirm_delete'))) return;
    try { await api.delete(`/api/admin/courses/${id}`); fetchItems(); } catch { alert('Failed to delete'); }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t('admin.courses')}</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />{t('admin.add_new')}</Button>
      </div>
      <div className="mb-4"><div className="relative max-w-md"><Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" /><Input placeholder={t('admin.search_placeholder')} value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" /></div></div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={Map} title={t('common.no_results')} actionLabel={t('admin.add_new')} onAction={openCreateModal} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('common.name')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('course.duration')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('course.theme')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('admin.status')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('admin.actions')}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4 text-sm text-gray-500">{item.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{lt(item.name)}</td>
                    <td className="px-6 py-4 text-sm"><Badge>{item.duration}</Badge></td>
                    <td className="px-6 py-4 text-sm"><Badge variant="info">{item.theme}</Badge></td>
                    <td className="px-6 py-4"><Badge variant={item.is_active ? 'success' : 'error'}>{item.is_active ? t('admin.active') : t('admin.inactive')}</Badge></td>
                    <td className="px-6 py-4"><div className="flex items-center gap-2">
                      <button onClick={() => openEditModal(item)} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded"><Pencil className="w-4 h-4 text-gray-500" /></button>
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

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? t('common.edit') : t('admin.add_new')} size="lg">
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <Select label={t('course.duration')} options={[{ value: 'half_day', label: t('course.half_day') }, { value: 'full_day', label: t('course.full_day') }, { value: 'two_days', label: t('course.two_days') }]} value={formData.duration || ''} onChange={(e) => setFormData((p) => ({ ...p, duration: e.target.value }))} />
            <Select label={t('course.difficulty')} options={[{ value: 'easy', label: t('course.easy') }, { value: 'moderate', label: t('course.moderate') }, { value: 'challenging', label: t('course.challenging') }]} value={formData.difficulty || ''} onChange={(e) => setFormData((p) => ({ ...p, difficulty: e.target.value }))} />
            <Select label={t('course.theme')} options={[{ value: 'culture', label: t('course.culture') }, { value: 'food', label: t('course.food') }, { value: 'shopping', label: t('course.shopping') }, { value: 'nature', label: t('course.nature') }, { value: 'history', label: t('course.history') }]} value={formData.theme || ''} onChange={(e) => setFormData((p) => ({ ...p, theme: e.target.value }))} />
          </div>
          <Input label={t('course.region')} value={formData.region || ''} onChange={(e) => setFormData((p) => ({ ...p, region: e.target.value }))} />
          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('admin.multilingual')}</p>
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input label={`${t('common.name')} (${formLangTab})`} value={formData[`name_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`name_${formLangTab}`]: e.target.value }))} />
              <div><label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">Description ({formLangTab})</label>
              <textarea className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[80px] resize-y" value={formData[`description_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`description_${formLangTab}`]: e.target.value }))} /></div>
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
