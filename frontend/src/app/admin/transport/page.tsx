'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, Bus } from 'lucide-react';
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
import { TransportRoute, TransportTip, SUPPORTED_LANGUAGES } from '@/types';

export default function AdminTransportPage() {
  const { lt } = useLanguage();
  const [activeTab, setActiveTab] = useState('routes');
  const [loading, setLoading] = useState(true);
  const [routes, setRoutes] = useState<TransportRoute[]>([]);
  const [tips, setTips] = useState<TransportTip[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<TransportRoute | TransportTip | null>(null);
  const [formLangTab, setFormLangTab] = useState('en');
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchData(); }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [routeData, tipData] = await Promise.all([
        api.get<{ items: TransportRoute[] }>('/api/admin/transport/routes').catch(() => ({ items: [] })),
        api.get<{ items: TransportTip[] }>('/api/admin/transport/tips').catch(() => ({ items: [] })),
      ]);
      setRoutes(routeData.items || []);
      setTips(tipData.items || []);
    } catch { /* silent */ }
    setLoading(false);
  };

  const openCreateModal = () => {
    setEditingItem(null);
    const data: Record<string, string> = { category: 'tmoney' };
    SUPPORTED_LANGUAGES.forEach((l) => {
      data[`from_${l.code}`] = ''; data[`to_${l.code}`] = '';
      data[`title_${l.code}`] = ''; data[`description_${l.code}`] = '';
    });
    setFormData(data); setFormLangTab('en'); setShowModal(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (activeTab === 'routes') {
        const from: Record<string, string> = {};
        const to: Record<string, string> = {};
        SUPPORTED_LANGUAGES.forEach((l) => {
          if (formData[`from_${l.code}`]) from[l.code] = formData[`from_${l.code}`];
          if (formData[`to_${l.code}`]) to[l.code] = formData[`to_${l.code}`];
        });
        const payload = { from, to, modes: [], is_active: true };
        if (editingItem) await api.put(`/api/admin/transport/routes/${editingItem.id}`, payload);
        else await api.post('/api/admin/transport/routes', payload);
      } else {
        const title: Record<string, string> = {};
        const description: Record<string, string> = {};
        SUPPORTED_LANGUAGES.forEach((l) => {
          if (formData[`title_${l.code}`]) title[l.code] = formData[`title_${l.code}`];
          if (formData[`description_${l.code}`]) description[l.code] = formData[`description_${l.code}`];
        });
        const payload = { title, description, category: formData.category, is_active: true };
        if (editingItem) await api.put(`/api/admin/transport/tips/${editingItem.id}`, payload);
        else await api.post('/api/admin/transport/tips', payload);
      }
      setShowModal(false); fetchData();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleDelete = async (type: string, id: number | string) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    try {
      await api.delete(`/api/admin/transport/${type}/${id}`);
      fetchData();
    } catch { alert('삭제에 실패했습니다'); }
  };

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));
  const tabs = [{ id: 'routes', label: '노선' }, { id: 'tips', label: '교통 팁' }];

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">교통</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />추가</Button>
      </div>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

      {activeTab === 'routes' && (
        routes.length === 0 ? <EmptyState icon={Bus} title="결과가 없습니다" actionLabel="추가" onAction={openCreateModal} /> :
        <Card className="overflow-hidden">
          <div className="overflow-x-auto"><table className="w-full">
            <thead className="bg-gray-50 dark:bg-dark-input"><tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">출발</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">도착</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">상태</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">작업</th>
            </tr></thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
              {routes.map((r) => (
                <tr key={r.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                  <td className="px-6 py-4 text-sm text-gray-500">{r.id}</td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-gray-100">{lt(r.from)}</td>
                  <td className="px-6 py-4 text-sm text-gray-900 dark:text-gray-100">{lt(r.to)}</td>
                  <td className="px-6 py-4"><Badge variant={r.is_active ? 'success' : 'error'}>{r.is_active ? '활성' : '비활성'}</Badge></td>
                  <td className="px-6 py-4"><div className="flex gap-2">
                    <button onClick={() => handleDelete('routes', r.id)} className="p-1 hover:bg-red-50 rounded"><Trash2 className="w-4 h-4 text-red-500" /></button>
                  </div></td>
                </tr>
              ))}
            </tbody>
          </table></div>
        </Card>
      )}

      {activeTab === 'tips' && (
        tips.length === 0 ? <EmptyState icon={Bus} title="결과가 없습니다" actionLabel="추가" onAction={openCreateModal} /> :
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {tips.map((tip) => (
            <Card key={tip.id} className="p-4">
              <div className="flex items-start justify-between">
                <div>
                  <Badge className="mb-2">{tip.category}</Badge>
                  <h3 className="font-medium text-gray-900 dark:text-gray-100">{lt(tip.title)}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{lt(tip.description)}</p>
                </div>
                <button onClick={() => handleDelete('tips', tip.id)} className="p-1 hover:bg-red-50 rounded flex-shrink-0"><Trash2 className="w-4 h-4 text-red-500" /></button>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="추가" size="lg">
        <div className="space-y-4">
          {activeTab === 'tips' && (
            <Input label="카테고리" value={formData.category || ''} onChange={(e) => setFormData((p) => ({ ...p, category: e.target.value }))} />
          )}
          <div className="pt-2">
            <Tabs tabs={langTabs} activeTab={formLangTab} onChange={setFormLangTab} className="mb-4" />
            <div className="space-y-3">
              {activeTab === 'routes' ? (
                <>
                  <Input label={`출발 (${formLangTab})`} value={formData[`from_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`from_${formLangTab}`]: e.target.value }))} />
                  <Input label={`도착 (${formLangTab})`} value={formData[`to_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`to_${formLangTab}`]: e.target.value }))} />
                </>
              ) : (
                <>
                  <Input label={`제목 (${formLangTab})`} value={formData[`title_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`title_${formLangTab}`]: e.target.value }))} />
                  <div><label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">설명 ({formLangTab})</label>
                  <textarea className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 min-h-[80px] resize-y" value={formData[`description_${formLangTab}`] || ''} onChange={(e) => setFormData((p) => ({ ...p, [`description_${formLangTab}`]: e.target.value }))} /></div>
                </>
              )}
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
