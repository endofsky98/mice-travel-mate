'use client';

import { useEffect, useState } from 'react';
import { MessageCircle, AlertTriangle, Check, Trash2, ShieldAlert } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';
import { formatDate } from '@/lib/utils';

interface ReportedMessage {
  id: string;
  room_id: string;
  sender_type: 'user' | 'guide';
  sender_id: string;
  sender_name?: string;
  content: string;
  image_url?: string;
  reported_by?: string;
  report_reason?: string;
  status: 'pending' | 'reviewed' | 'dismissed' | 'warned';
  created_at: string;
}

export default function AdminChatMonitorPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState<ReportedMessage[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => { fetchItems(); }, [currentPage]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: ReportedMessage[]; pages: number }>('/api/admin/chat/reports', {
        page: currentPage, per_page: 20,
      });
      setItems(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setItems([]); }
    setLoading(false);
  };

  const handleAction = async (id: string, action: 'reviewed' | 'dismissed' | 'warned') => {
    try {
      await api.patch(`/api/admin/chat/reports/${id}`, { status: action });
      fetchItems();
    } catch { alert('Failed to update'); }
  };

  const handleDeleteMessage = async (id: string) => {
    if (!confirm('Are you sure you want to delete this message?')) return;
    try {
      await api.delete(`/api/admin/chat/messages/${id}`);
      fetchItems();
    } catch { alert('Failed to delete'); }
  };

  const statusVariant = (status: string) => {
    switch (status) {
      case 'reviewed': return 'success' as const;
      case 'dismissed': return 'info' as const;
      case 'warned': return 'error' as const;
      case 'pending': return 'warning' as const;
      default: return 'default' as const;
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Chat Monitor</h1>
        <Badge variant="warning">{items.filter((i) => i.status === 'pending').length} Pending</Badge>
      </div>

      {loading ? <LoadingSpinner fullPage /> : items.length === 0 ? (
        <EmptyState icon={MessageCircle} title="No reported messages" description="All chat messages are clean." />
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <Card key={item.id} className={`p-5 ${item.status === 'pending' ? 'border-l-4 border-l-amber-500' : ''}`}>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                      {item.sender_name || item.sender_id}
                    </span>
                    <Badge>{item.sender_type}</Badge>
                    <Badge variant={statusVariant(item.status)}>{item.status}</Badge>
                    <span className="text-xs text-gray-400">{formatDate(item.created_at)}</span>
                  </div>

                  <div className="bg-gray-50 dark:bg-dark-input rounded-lg p-3 mb-2">
                    {item.image_url ? (
                      <div className="mb-2">
                        <img src={item.image_url} alt="" className="w-32 h-32 rounded object-cover" />
                      </div>
                    ) : null}
                    <p className="text-sm text-gray-800 dark:text-gray-200">{item.content}</p>
                  </div>

                  {item.report_reason && (
                    <div className="flex items-start gap-2 text-sm text-red-600 dark:text-red-400">
                      <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div>
                        <span className="font-medium">Report reason:</span> {item.report_reason}
                        {item.reported_by && <span className="text-gray-400 ml-2">by {item.reported_by}</span>}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-1 ml-4 flex-shrink-0">
                  {item.status === 'pending' && (
                    <>
                      <Button size="sm" variant="outline" onClick={() => handleAction(item.id, 'reviewed')} title="Mark Reviewed">
                        <Check className="w-4 h-4 text-green-600" />
                      </Button>
                      <Button size="sm" variant="outline" onClick={() => handleAction(item.id, 'dismissed')} title="Dismiss">
                        <Trash2 className="w-4 h-4 text-gray-500" />
                      </Button>
                      <Button size="sm" variant="destructive" onClick={() => handleAction(item.id, 'warned')} title="Warn User">
                        <ShieldAlert className="w-4 h-4" />
                      </Button>
                    </>
                  )}
                  <Button size="sm" variant="destructive" onClick={() => handleDeleteMessage(item.id)} title="Delete Message">
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </Card>
          ))}

          <div className="pt-4">
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
          </div>
        </div>
      )}
    </div>
  );
}
