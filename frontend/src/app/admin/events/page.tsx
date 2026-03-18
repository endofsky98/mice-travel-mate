'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, Calendar } from 'lucide-react';
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
import { Event, SUPPORTED_LANGUAGES } from '@/types';
import { formatDateRange } from '@/lib/utils';

export default function AdminEventsPage() {
  const { t, lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState<Event[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingEvent, setEditingEvent] = useState<Event | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchEvents();
  }, [currentPage, search]);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: Event[]; pages: number }>('/api/admin/events', {
        page: currentPage,
        per_page: 20,
        search: search || undefined,
      });
      setEvents(data.items || []);
      setTotalPages(data.pages || 1);
    } catch {
      setEvents([]);
    }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingEvent(null);
    setFormData({
      slug: '',
      start_date: '',
      end_date: '',
      region: '',
    });
    SUPPORTED_LANGUAGES.forEach((l) => {
      setFormData((prev) => ({
        ...prev,
        [`name_${l.code}`]: '',
        [`description_${l.code}`]: '',
        [`venue_name_${l.code}`]: '',
      }));
    });
    setFormLangTab('en');
    setShowModal(true);
  };

  const openEditModal = (event: Event) => {
    setEditingEvent(event);
    const data: Record<string, string> = {
      slug: event.slug,
      start_date: event.start_date?.split('T')[0] || '',
      end_date: event.end_date?.split('T')[0] || '',
      region: event.region || '',
    };
    SUPPORTED_LANGUAGES.forEach((l) => {
      const name = typeof event.name === 'object' ? event.name[l.code] || '' : l.code === 'en' ? (event.name as string) : '';
      const desc = typeof event.description === 'object' ? event.description[l.code] || '' : l.code === 'en' ? (event.description as string) : '';
      const venue = typeof event.venue_name === 'object' ? (event.venue_name[l.code] || '') : l.code === 'en' ? ((event.venue_name as string) || '') : '';
      data[`name_${l.code}`] = name;
      data[`description_${l.code}`] = desc;
      data[`venue_name_${l.code}`] = venue;
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
      const venue_name: Record<string, string> = {};
      SUPPORTED_LANGUAGES.forEach((l) => {
        if (formData[`name_${l.code}`]) name[l.code] = formData[`name_${l.code}`];
        if (formData[`description_${l.code}`]) description[l.code] = formData[`description_${l.code}`];
        if (formData[`venue_name_${l.code}`]) venue_name[l.code] = formData[`venue_name_${l.code}`];
      });

      const payload = {
        slug: formData.slug,
        name,
        description,
        venue_name,
        start_date: formData.start_date,
        end_date: formData.end_date,
        region: formData.region,
        is_active: true,
      };

      if (editingEvent) {
        await api.put(`/api/admin/events/${editingEvent.id}`, payload);
      } else {
        await api.post('/api/admin/events', payload);
      }
      setShowModal(false);
      fetchEvents();
    } catch {
      alert('Failed to save');
    }
    setSaving(false);
  };

  const handleDelete = async (id: number) => {
    if (!confirm(t('admin.confirm_delete'))) return;
    try {
      await api.delete(`/api/admin/events/${id}`);
      fetchEvents();
    } catch {
      alert('Failed to delete');
    }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t('admin.events')}</h1>
        <Button onClick={openCreateModal}>
          <Plus className="w-4 h-4" />
          {t('admin.add_new')}
        </Button>
      </div>

      <div className="mb-4">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            placeholder={t('admin.search_placeholder')}
            value={search}
            onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }}
            className="pl-10"
          />
        </div>
      </div>

      {loading ? (
        <LoadingSpinner fullPage />
      ) : events.length === 0 ? (
        <EmptyState icon={Calendar} title={t('common.no_results')} actionLabel={t('admin.add_new')} onAction={openCreateModal} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('common.name')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('booking.date')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('admin.status')}</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{t('admin.actions')}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {events.map((event) => (
                  <tr key={event.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4 text-sm text-gray-500">{event.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">{lt(event.name)}</td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {event.start_date && event.end_date ? formatDateRange(event.start_date, event.end_date) : '-'}
                    </td>
                    <td className="px-6 py-4">
                      <Badge variant={event.is_active ? 'success' : 'error'}>
                        {event.is_active ? t('admin.active') : t('admin.inactive')}
                      </Badge>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <button onClick={() => openEditModal(event)} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded">
                          <Pencil className="w-4 h-4 text-gray-500" />
                        </button>
                        <button onClick={() => handleDelete(event.id)} className="p-1 hover:bg-red-50 dark:hover:bg-red-950/40 rounded">
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </button>
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

      {/* Create/Edit Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingEvent ? t('common.edit') : t('admin.add_new')} size="lg">
        <div className="space-y-4">
          <Input label="Slug" value={formData.slug || ''} onChange={(e) => setFormData((p) => ({ ...p, slug: e.target.value }))} />
          <div className="grid grid-cols-2 gap-4">
            <Input type="date" label={t('booking.date') + ' (Start)'} value={formData.start_date || ''} onChange={(e) => setFormData((p) => ({ ...p, start_date: e.target.value }))} />
            <Input type="date" label={t('booking.date') + ' (End)'} value={formData.end_date || ''} onChange={(e) => setFormData((p) => ({ ...p, end_date: e.target.value }))} />
          </div>
          <Input label="Region" value={formData.region || ''} onChange={(e) => setFormData((p) => ({ ...p, region: e.target.value }))} />

          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('admin.multilingual')}</p>
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input
                label={`${t('common.name')} (${formLangTab})`}
                value={formData[`name_${formLangTab}`] || ''}
                onChange={(e) => setFormData((p) => ({ ...p, [`name_${formLangTab}`]: e.target.value }))}
              />
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
                  Description ({formLangTab})
                </label>
                <textarea
                  className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[100px] resize-y"
                  value={formData[`description_${formLangTab}`] || ''}
                  onChange={(e) => setFormData((p) => ({ ...p, [`description_${formLangTab}`]: e.target.value }))}
                />
              </div>
              <Input
                label={`Venue Name (${formLangTab})`}
                value={formData[`venue_name_${formLangTab}`] || ''}
                onChange={(e) => setFormData((p) => ({ ...p, [`venue_name_${formLangTab}`]: e.target.value }))}
              />
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
