'use client';

import { useEffect, useState } from 'react';
import { Plus, Pencil, Trash2, GripVertical, Image, ToggleLeft, ToggleRight } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Modal from '@/components/ui/Modal';
import Tabs from '@/components/ui/Tabs';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Badge from '@/components/ui/Badge';
import Select from '@/components/ui/Select';
import { RollingBanner, SUPPORTED_LANGUAGES } from '@/types';

export default function AdminBannersPage() {
  const { lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<RollingBanner[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<RollingBanner | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [dragIdx, setDragIdx] = useState<number | null>(null);

  useEffect(() => { fetchItems(); }, []);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: RollingBanner[] }>('/api/admin/banners');
      setItems((data.items || []).sort((a, b) => a.display_order - b.display_order));
    } catch { setItems([]); }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    const data: Record<string, string> = {
      image_url: '',
      link_url: '',
      rolling_interval: '5000',
      event_id: '',
      is_active: 'true',
    };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`title_${l.code}`] = '';
      data[`subtitle_${l.code}`] = '';
    });
    setFormData(data);
    setFormLangTab('en');
    setShowModal(true);
  };

  const openEditModal = (item: RollingBanner) => {
    setEditingItem(item);
    const data: Record<string, string> = {
      image_url: item.image_url || '',
      link_url: item.link_url || '',
      rolling_interval: String(item.rolling_interval || 5000),
      event_id: '',
      is_active: String(item.is_active),
    };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`title_${l.code}`] = typeof item.title === 'object' ? item.title[l.code] || '' : l.code === 'en' ? (item.title as string) : '';
      data[`subtitle_${l.code}`] = typeof item.subtitle === 'object' ? item.subtitle[l.code] || '' : l.code === 'en' ? (item.subtitle as string) : '';
    });
    setFormData(data);
    setFormLangTab('en');
    setShowModal(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const title: Record<string, string> = {};
      const subtitle: Record<string, string> = {};
      SUPPORTED_LANGUAGES.forEach((l) => {
        if (formData[`title_${l.code}`]) title[l.code] = formData[`title_${l.code}`];
        if (formData[`subtitle_${l.code}`]) subtitle[l.code] = formData[`subtitle_${l.code}`];
      });
      const payload = {
        title,
        subtitle,
        image_url: formData.image_url,
        link_url: formData.link_url || undefined,
        rolling_interval: parseInt(formData.rolling_interval) || 5000,
        is_active: formData.is_active === 'true',
        display_order: editingItem ? editingItem.display_order : items.length + 1,
      };
      if (editingItem) {
        await api.put(`/api/admin/banners/${editingItem.id}`, payload);
      } else {
        await api.post('/api/admin/banners', payload);
      }
      setShowModal(false);
      fetchItems();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try { await api.delete(`/api/admin/banners/${id}`); fetchItems(); } catch { alert('삭제에 실패했습니다'); }
  };

  const handleToggleActive = async (item: RollingBanner) => {
    try {
      await api.patch(`/api/admin/banners/${item.id}`, { is_active: !item.is_active });
      fetchItems();
    } catch { alert('업데이트에 실패했습니다'); }
  };

  const handleDragStart = (idx: number) => {
    setDragIdx(idx);
  };

  const handleDragOver = (e: React.DragEvent, idx: number) => {
    e.preventDefault();
    if (dragIdx === null || dragIdx === idx) return;
    const newItems = [...items];
    const [dragged] = newItems.splice(dragIdx, 1);
    newItems.splice(idx, 0, dragged);
    setItems(newItems);
    setDragIdx(idx);
  };

  const handleDragEnd = async () => {
    setDragIdx(null);
    try {
      const orderPayload = items.map((item, idx) => ({ id: item.id, display_order: idx + 1 }));
      await api.put('/api/admin/banners/reorder', { items: orderPayload });
    } catch { /* silent */ }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">배너 관리</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />배너 추가</Button>
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={Image} title="배너가 없습니다" actionLabel="배너 추가" onAction={openCreateModal} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase w-12"></th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase w-12">순서</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase w-20">미리보기</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">제목</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">간격</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">활성</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">작업</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {items.map((item, idx) => (
                  <tr
                    key={item.id}
                    className="hover:bg-gray-50 dark:hover:bg-white/[0.02]"
                    draggable
                    onDragStart={() => handleDragStart(idx)}
                    onDragOver={(e) => handleDragOver(e, idx)}
                    onDragEnd={handleDragEnd}
                  >
                    <td className="px-4 py-3 cursor-grab">
                      <GripVertical className="w-4 h-4 text-gray-400" />
                    </td>
                    <td className="px-4 py-3 text-sm font-mono text-gray-500">{idx + 1}</td>
                    <td className="px-4 py-3">
                      {item.image_url ? (
                        <div className="w-16 h-10 rounded bg-gray-100 dark:bg-gray-800 overflow-hidden">
                          <img src={item.image_url} alt="" className="w-full h-full object-cover" />
                        </div>
                      ) : (
                        <div className="w-16 h-10 rounded bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                          <Image className="w-4 h-4 text-gray-400" />
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-gray-100">{lt(item.title)}</td>
                    <td className="px-4 py-3 text-sm text-gray-500">{(item.rolling_interval || 5000) / 1000}s</td>
                    <td className="px-4 py-3">
                      <button onClick={() => handleToggleActive(item)} className="text-gray-500 hover:text-indigo-600 transition-colors">
                        {item.is_active ? <ToggleRight className="w-6 h-6 text-green-600" /> : <ToggleLeft className="w-6 h-6 text-gray-400" />}
                      </button>
                    </td>
                    <td className="px-4 py-3">
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
        </Card>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? '배너 수정' : '배너 추가'} size="lg">
        <div className="space-y-4">
          <Input label="이미지 URL" value={formData.image_url || ''} onChange={(e) => setFormData((p) => ({ ...p, image_url: e.target.value }))} placeholder="https://example.com/image.jpg" />
          {formData.image_url && (
            <div className="w-full h-40 rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-800">
              <img src={formData.image_url} alt="미리보기" className="w-full h-full object-cover" />
            </div>
          )}
          <Input label="링크 URL" value={formData.link_url || ''} onChange={(e) => setFormData((p) => ({ ...p, link_url: e.target.value }))} placeholder="https://example.com/event" />
          <div className="grid grid-cols-2 gap-4">
            <Input label="롤링 간격 (ms)" type="number" value={formData.rolling_interval || ''} onChange={(e) => setFormData((p) => ({ ...p, rolling_interval: e.target.value }))} />
            <Select
              label="활성"
              options={[{ value: 'true', label: '활성' }, { value: 'false', label: '비활성' }]}
              value={formData.is_active || 'true'}
              onChange={(e) => setFormData((p) => ({ ...p, is_active: e.target.value }))}
            />
          </div>

          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">다국어 콘텐츠</p>
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input label={`제목 (${formLangTab})`} value={formData[`title_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`title_${formLangTab}`]: e.target.value }))} />
              <Input label={`부제목 (${formLangTab})`} value={formData[`subtitle_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`subtitle_${formLangTab}`]: e.target.value }))} />
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
