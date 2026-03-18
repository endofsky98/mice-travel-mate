'use client';

import { useEffect, useState } from 'react';
import { Plus, Search, Pencil, Trash2, Ticket, ToggleLeft, ToggleRight, Copy, RefreshCw } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
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
import { Coupon } from '@/types';

interface CouponFull extends Coupon {
  start_date?: string;
  end_date?: string;
  max_uses?: number;
  used_count?: number;
  max_uses_per_user?: number;
  event_id?: string;
  created_at?: string;
}

export default function AdminCouponsPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<CouponFull[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState<CouponFull | null>(null);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchItems(); }, [currentPage, search]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: CouponFull[]; pages: number }>('/api/admin/coupons', {
        page: currentPage, per_page: 20, search: search || undefined,
      });
      setItems(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const generateCode = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 8; i++) code += chars.charAt(Math.floor(Math.random() * chars.length));
    return code;
  };

  const openCreateModal = () => {
    setEditingItem(null);
    setFormData({
      code: generateCode(),
      name: '',
      discount_type: 'percentage',
      discount_value: '10',
      max_discount_usd: '',
      min_order_usd: '',
      start_date: '',
      end_date: '',
      max_uses: '',
      max_uses_per_user: '1',
      event_id: '',
      is_valid: 'true',
    });
    setShowModal(true);
  };

  const openEditModal = (item: CouponFull) => {
    setEditingItem(item);
    setFormData({
      code: item.code,
      name: item.name || '',
      discount_type: item.discount_type,
      discount_value: String(item.discount_value),
      max_discount_usd: String(item.max_discount_usd || ''),
      min_order_usd: String(item.min_order_usd || ''),
      start_date: item.start_date?.split('T')[0] || '',
      end_date: item.end_date?.split('T')[0] || '',
      max_uses: String(item.max_uses || ''),
      max_uses_per_user: String(item.max_uses_per_user || ''),
      event_id: item.event_id || '',
      is_valid: String(item.is_valid),
    });
    setShowModal(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const payload = {
        code: formData.code,
        name: formData.name,
        discount_type: formData.discount_type,
        discount_value: parseFloat(formData.discount_value),
        max_discount_usd: formData.max_discount_usd ? parseFloat(formData.max_discount_usd) : undefined,
        min_order_usd: formData.min_order_usd ? parseFloat(formData.min_order_usd) : undefined,
        start_date: formData.start_date || undefined,
        end_date: formData.end_date || undefined,
        max_uses: formData.max_uses ? parseInt(formData.max_uses) : undefined,
        max_uses_per_user: formData.max_uses_per_user ? parseInt(formData.max_uses_per_user) : undefined,
        event_id: formData.event_id || undefined,
        is_valid: formData.is_valid === 'true',
      };
      if (editingItem) {
        await api.put(`/api/admin/coupons/${editingItem.id}`, payload);
      } else {
        await api.post('/api/admin/coupons', payload);
      }
      setShowModal(false);
      fetchItems();
    } catch { alert('Failed to save'); }
    setSaving(false);
  };

  const handleDelete = async (id: string) => {
    if (!confirm(t('admin.confirm_delete'))) return;
    try { await api.delete(`/api/admin/coupons/${id}`); fetchItems(); } catch { alert('Failed to delete'); }
  };

  const handleToggleActive = async (item: CouponFull) => {
    try {
      await api.patch(`/api/admin/coupons/${item.id}`, { is_valid: !item.is_valid });
      fetchItems();
    } catch { alert('Failed to update'); }
  };

  const copyCode = (code: string) => {
    navigator.clipboard.writeText(code);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Coupon Management</h1>
        <Button onClick={openCreateModal}><Plus className="w-4 h-4" />Add Coupon</Button>
      </div>

      <div className="mb-4">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder="Search coupons..." value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={Ticket} title="No coupons found" actionLabel="Add Coupon" onAction={openCreateModal} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Code</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Discount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Usage</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Period</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Active</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-mono font-semibold text-indigo-600 dark:text-indigo-400">{item.code}</span>
                        <button onClick={() => copyCode(item.code)} className="p-0.5 hover:bg-gray-100 dark:hover:bg-white/[0.08] rounded">
                          <Copy className="w-3.5 h-3.5 text-gray-400" />
                        </button>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 dark:text-gray-100">{item.name}</td>
                    <td className="px-6 py-4 text-sm">
                      <Badge variant={item.discount_type === 'percentage' ? 'info' : item.discount_type === 'fixed' ? 'success' : 'default'}>
                        {item.discount_type === 'percentage' ? `${item.discount_value}%` :
                          item.discount_type === 'fixed' ? `$${item.discount_value}` : item.discount_type}
                      </Badge>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {item.used_count || 0} / {item.max_uses || '-'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {item.start_date && item.end_date ? (
                        <span>{item.start_date.split('T')[0]} ~ {item.end_date.split('T')[0]}</span>
                      ) : (
                        <span>No limit</span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      <button onClick={() => handleToggleActive(item)} className="text-gray-500 hover:text-indigo-600 transition-colors">
                        {item.is_valid ? <ToggleRight className="w-6 h-6 text-green-600" /> : <ToggleLeft className="w-6 h-6 text-gray-400" />}
                      </button>
                    </td>
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

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editingItem ? 'Edit Coupon' : 'Add Coupon'} size="lg">
        <div className="space-y-4">
          <div className="flex items-end gap-3">
            <Input label="Code" value={formData.code || ''} onChange={(e) => setFormData((p) => ({ ...p, code: e.target.value.toUpperCase() }))} className="flex-1 font-mono" />
            {!editingItem && (
              <Button variant="outline" onClick={() => setFormData((p) => ({ ...p, code: generateCode() }))} className="mb-0">
                <RefreshCw className="w-4 h-4" />Auto
              </Button>
            )}
          </div>
          <Input label="Name" value={formData.name || ''} onChange={(e) => setFormData((p) => ({ ...p, name: e.target.value }))} />
          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Discount Type"
              options={[
                { value: 'percentage', label: 'Percentage (%)' },
                { value: 'fixed', label: 'Fixed Amount ($)' },
                { value: 'upgrade', label: 'Upgrade' },
              ]}
              value={formData.discount_type || ''}
              onChange={(e) => setFormData((p) => ({ ...p, discount_type: e.target.value }))}
            />
            <Input label="Discount Value" type="number" value={formData.discount_value || ''} onChange={(e) => setFormData((p) => ({ ...p, discount_value: e.target.value }))} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Max Discount (USD)" type="number" value={formData.max_discount_usd || ''} onChange={(e) => setFormData((p) => ({ ...p, max_discount_usd: e.target.value }))} placeholder="Optional" />
            <Input label="Min Order (USD)" type="number" value={formData.min_order_usd || ''} onChange={(e) => setFormData((p) => ({ ...p, min_order_usd: e.target.value }))} placeholder="Optional" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Start Date" type="date" value={formData.start_date || ''} onChange={(e) => setFormData((p) => ({ ...p, start_date: e.target.value }))} />
            <Input label="End Date" type="date" value={formData.end_date || ''} onChange={(e) => setFormData((p) => ({ ...p, end_date: e.target.value }))} />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <Input label="Max Total Uses" type="number" value={formData.max_uses || ''} onChange={(e) => setFormData((p) => ({ ...p, max_uses: e.target.value }))} placeholder="Unlimited" />
            <Input label="Max Per User" type="number" value={formData.max_uses_per_user || ''} onChange={(e) => setFormData((p) => ({ ...p, max_uses_per_user: e.target.value }))} />
            <Input label="Event ID" value={formData.event_id || ''} onChange={(e) => setFormData((p) => ({ ...p, event_id: e.target.value }))} placeholder="Optional" />
          </div>
          <Select
            label="Status"
            options={[{ value: 'true', label: 'Active' }, { value: 'false', label: 'Inactive' }]}
            value={formData.is_valid || 'true'}
            onChange={(e) => setFormData((p) => ({ ...p, is_valid: e.target.value }))}
          />
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200 dark:border-gray-500/40">
            <Button variant="outline" onClick={() => setShowModal(false)}>{t('common.cancel')}</Button>
            <Button onClick={handleSave} disabled={saving}>{saving ? t('common.loading') : t('common.save')}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
