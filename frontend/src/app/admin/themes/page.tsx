'use client';

import { useEffect, useState } from 'react';
import { Plus, Pencil, Trash2, Palette, Link2 } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Modal from '@/components/ui/Modal';
import Tabs from '@/components/ui/Tabs';
import Select from '@/components/ui/Select';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Badge from '@/components/ui/Badge';
import { ThemeData, ThemeSpot, SUPPORTED_LANGUAGES } from '@/types';

export default function AdminThemesPage() {
  const { lt } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<ThemeData[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [editingItem, setEditingItem] = useState<ThemeData | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);
  const [assignData, setAssignData] = useState({ target_type: 'restaurant', target_id: '' });
  const [selectedTheme, setSelectedTheme] = useState<ThemeData | null>(null);

  useEffect(() => { fetchItems(); }, []);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: ThemeData[] }>('/api/admin/themes');
      setItems(data.items || []);
    } catch { setItems([]); }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    const data: Record<string, string> = { icon: '', color: '#6366f1' };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = '';
      data[`description_${l.code}`] = '';
    });
    setFormData(data);
    setFormLangTab('en');
    setShowModal(true);
  };

  const openEditModal = (item: ThemeData) => {
    setEditingItem(item);
    const data: Record<string, string> = {
      icon: item.icon || '',
      color: item.color || '#6366f1',
    };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`name_${l.code}`] = typeof item.name === 'object' ? item.name[l.code] || '' : l.code === 'en' ? (item.name as string) : '';
      data[`description_${l.code}`] = typeof item.description === 'object' ? (item.description?.[l.code] || '') : l.code === 'en' ? ((item.description as string) || '') : '';
    });
    setFormData(data);
    setFormLangTab('en');
    setShowModal(true);
  };

  const openAssignModal = (theme: ThemeData) => {
    setSelectedTheme(theme);
    setAssignData({ target_type: 'restaurant', target_id: '' });
    setShowAssignModal(true);
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
      const payload = { name, description, icon: formData.icon || undefined, color: formData.color || undefined };
      if (editingItem) {
        await api.put(`/api/admin/themes/${editingItem.id}`, payload);
      } else {
        await api.post('/api/admin/themes', payload);
      }
      setShowModal(false);
      fetchItems();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try { await api.delete(`/api/admin/themes/${id}`); fetchItems(); } catch { alert('삭제에 실패했습니다'); }
  };

  const handleAssignSpot = async () => {
    if (!selectedTheme || !assignData.target_id) return;
    setSaving(true);
    try {
      await api.post(`/api/admin/themes/${selectedTheme.id}/spots`, {
        target_type: assignData.target_type,
        target_id: assignData.target_id,
      });
      setShowAssignModal(false);
      fetchItems();
    } catch { alert('할당에 실패했습니다'); }
    setSaving(false);
  };

  const handleRemoveSpot = async (themeId: string, spotId: string) => {
    try {
      await api.delete(`/api/admin/themes/${themeId}/spots/${spotId}`);
      fetchItems();
    } catch { alert('제거에 실패했습니다'); }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));

  const iconOptions = [
    { value: '', label: '없음' },
    { value: 'utensils', label: '식기' },
    { value: 'camera', label: '카메라' },
    { value: 'mountain', label: '산' },
    { value: 'shopping-bag', label: '쇼핑' },
    { value: 'music', label: '음악' },
    { value: 'palette', label: '예술' },
    { value: 'heart', label: '하트' },
    { value: 'star', label: '별' },
    { value: 'map-pin', label: '지도 핀' },
    { value: 'coffee', label: '커피' },
    { value: 'sunset', label: '일몰' },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">테마 관리</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />테마 추가</Button>
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={Palette} title="테마가 없습니다" actionLabel="테마 추가" onAction={openCreateModal} />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item) => (
            <Card key={item.id} className="p-5">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center text-white text-lg"
                    style={{ backgroundColor: item.color || '#6366f1' }}
                  >
                    {item.icon ? item.icon.charAt(0).toUpperCase() : 'T'}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-gray-100">{lt(item.name)}</h3>
                    {item.icon && <p className="text-xs text-gray-500 dark:text-gray-400">아이콘: {item.icon}</p>}
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  <button onClick={() => openEditModal(item)} className="p-1 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded"><Pencil className="w-4 h-4 text-gray-500" /></button>
                  <button onClick={() => handleDelete(item.id)} className="p-1 hover:bg-red-50 dark:hover:bg-red-950/40 rounded"><Trash2 className="w-4 h-4 text-red-500" /></button>
                </div>
              </div>

              {item.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">{lt(item.description)}</p>
              )}

              {/* Assigned Spots */}
              <div className="border-t border-gray-200 dark:border-gray-500/40 pt-3 mt-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">
                    할당된 스팟 ({item.spots?.length || 0})
                  </span>
                  <button onClick={() => openAssignModal(item)} className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1">
                    <Link2 className="w-3 h-3" /> 할당
                  </button>
                </div>
                {item.spots && item.spots.length > 0 ? (
                  <div className="space-y-1">
                    {item.spots.slice(0, 5).map((spot) => (
                      <div key={spot.id} className="flex items-center justify-between text-sm">
                        <span className="text-gray-700 dark:text-gray-300 truncate flex-1">
                          <Badge className="mr-1 text-[10px]">{spot.target_type}</Badge>
                          {spot.name || spot.target_id}
                        </span>
                        <button onClick={() => handleRemoveSpot(item.id, spot.id)} className="text-red-400 hover:text-red-600 ml-2">
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    ))}
                    {item.spots.length > 5 && (
                      <p className="text-xs text-gray-400">+{item.spots.length - 5}개 더</p>
                    )}
                  </div>
                ) : (
                  <p className="text-xs text-gray-400">할당된 스팟이 없습니다</p>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Create/Edit Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? '테마 수정' : '테마 추가'} size="lg">
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Select label="아이콘" options={iconOptions} value={formData.icon || ''} onChange={(e) => setFormData((p) => ({ ...p, icon: e.target.value }))} />
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">색상</label>
              <div className="flex items-center gap-3">
                <input
                  type="color"
                  value={formData.color || '#6366f1'}
                  onChange={(e) => setFormData((p) => ({ ...p, color: e.target.value }))}
                  className="w-10 h-10 rounded-lg border border-gray-200 dark:border-gray-500/40 cursor-pointer"
                />
                <Input value={formData.color || '#6366f1'} onChange={(e) => setFormData((p) => ({ ...p, color: e.target.value }))} className="flex-1" />
              </div>
            </div>
          </div>

          <div className="pt-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">다국어 콘텐츠</p>
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              <Input label={`이름 (${formLangTab})`} value={formData[`name_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`name_${formLangTab}`]: e.target.value }))} />
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">설명 ({formLangTab})</label>
                <textarea
                  className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[80px] resize-y"
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

      {/* Assign Spot Modal */}
      <Modal isOpen={showAssignModal} onClose={() => setShowAssignModal(false)} title={`"${selectedTheme ? lt(selectedTheme.name) : ''}"에 스팟 할당`} size="sm">
        <div className="space-y-4">
          <Select
            label="대상 유형"
            options={[
              { value: 'restaurant', label: '맛집' },
              { value: 'course', label: '코스' },
              { value: 'product', label: '상품' },
              { value: 'guide', label: '가이드' },
              { value: 'festival', label: '축제' },
            ]}
            value={assignData.target_type}
            onChange={(e) => setAssignData((p) => ({ ...p, target_type: e.target.value }))}
          />
          <Input label="대상 ID" value={assignData.target_id} onChange={(e) => setAssignData((p) => ({ ...p, target_id: e.target.value }))} placeholder="항목 ID를 입력하세요" />
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-500/40">
            <Button variant="outline" onClick={() => setShowAssignModal(false)}>취소</Button>
            <Button onClick={handleAssignSpot} disabled={saving || !assignData.target_id}>{saving ? '로딩 중...' : '할당'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
