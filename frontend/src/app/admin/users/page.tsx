'use client';

import { useEffect, useState } from 'react';
import { Search, UserCog, Shield, User as UserIcon } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';
import { User } from '@/types';
import { formatDate } from '@/lib/utils';

export default function AdminUsersPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<User[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');

  useEffect(() => { fetchUsers(); }, [currentPage, search]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: User[]; pages: number }>('/api/admin/users', {
        page: currentPage, per_page: 20, search: search || undefined,
      });
      setUsers(data.items || []); setTotalPages(data.pages || 1);
    } catch { setUsers([]); }
    setLoading(false);
  };

  const toggleAdmin = async (userId: number, isAdmin: boolean) => {
    try {
      await api.patch(`/api/admin/users/${userId}`, { is_admin: !isAdmin });
      setUsers((prev) => prev.map((u) => u.id === userId ? { ...u, is_admin: !isAdmin } : u));
    } catch { alert('Failed to update'); }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('admin.users')}</h1>

      <div className="mb-6">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input placeholder={t('admin.search_placeholder')} value={search} onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }} className="pl-10" />
        </div>
      </div>

      {loading ? <LoadingSpinner fullPage /> : users.length === 0 ? (
        <EmptyState icon={UserCog} title={t('common.no_results')} />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto"><table className="w-full">
            <thead className="bg-gray-50 dark:bg-dark-input"><tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('common.name')}</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('auth.email')}</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('auth.nationality')}</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('admin.role')}</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('admin.created_at')}</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t('admin.actions')}</th>
            </tr></thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                  <td className="px-6 py-4 text-sm text-gray-500">{user.id}</td>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
                        {user.is_admin ? <Shield className="w-4 h-4 text-indigo-600 dark:text-indigo-400" /> : <UserIcon className="w-4 h-4 text-gray-400" />}
                      </div>
                      {user.name}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">{user.email}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{user.nationality || '-'}</td>
                  <td className="px-6 py-4">
                    <Badge variant={user.is_admin ? 'default' : 'info'}>
                      {user.is_admin ? t('admin.admin_role') : t('admin.user_role')}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">{formatDate(user.created_at)}</td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => toggleAdmin(Number(user.id), user.is_admin)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        user.is_admin ? 'bg-indigo-600' : 'bg-gray-300 dark:bg-gray-600'
                      }`}
                      title={t('admin.admin_role')}
                    >
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        user.is_admin ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table></div>
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-500/40">
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
          </div>
        </Card>
      )}
    </div>
  );
}
