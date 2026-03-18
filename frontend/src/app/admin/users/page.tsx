'use client';

import { useEffect, useState } from 'react';
import { Search, UserCog, Shield, ShieldCheck, User as UserIcon } from 'lucide-react';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Pagination from '@/components/ui/Pagination';
import Select from '@/components/ui/Select';
import { User } from '@/types';
import { formatDate } from '@/lib/utils';

export default function AdminUsersPage() {
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<User[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');

  useEffect(() => { fetchUsers(); }, [currentPage, search, roleFilter]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const params: Record<string, string | number> = { page: currentPage, per_page: 20 };
      if (search) params.search = search;
      if (roleFilter) params.role = roleFilter;
      const data = await api.get<{ items: User[]; pages: number }>('/api/admin/users', params);
      setUsers(data.items || []);
      setTotalPages(data.pages || 1);
    } catch { setUsers([]); }
    setLoading(false);
  };

  const changeRole = async (userId: number | string, newRole: string) => {
    if (!confirm(`이 사용자의 역할을 "${newRole}"(으)로 변경하시겠습니까?`)) return;
    try {
      await api.patch(`/api/admin/users/${userId}`, { role: newRole });
      fetchUsers();
    } catch { alert('역할 변경에 실패했습니다'); }
  };

  const getRoleIcon = (role?: string) => {
    switch (role) {
      case 'superadmin': return <ShieldCheck className="w-4 h-4 text-amber-500" />;
      case 'admin': return <Shield className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />;
      default: return <UserIcon className="w-4 h-4 text-gray-400" />;
    }
  };

  const getRoleBadge = (role?: string) => {
    switch (role) {
      case 'superadmin': return <Badge variant="warning">슈퍼 관리자</Badge>;
      case 'admin': return <Badge variant="default">관리자</Badge>;
      default: return <Badge variant="info">사용자</Badge>;
    }
  };

  const roleOptions = [
    { value: '', label: '전체 역할' },
    { value: 'user', label: '사용자' },
    { value: 'admin', label: '관리자' },
    { value: 'superadmin', label: '슈퍼 관리자' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">회원 관리</h1>

      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            placeholder="검색어를 입력하세요..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }}
            className="pl-10"
          />
        </div>
        <div className="w-40">
          <Select
            options={roleOptions}
            value={roleFilter}
            onChange={(e) => { setRoleFilter(e.target.value); setCurrentPage(1); }}
          />
        </div>
      </div>

      {loading ? <LoadingSpinner fullPage /> : users.length === 0 ? (
        <EmptyState icon={UserCog} title="결과가 없습니다" />
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">이름</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">이메일</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">국적</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">역할</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">생성일</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">작업</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-gray-100">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                          {getRoleIcon(user.role)}
                        </div>
                        {user.name}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{user.email}</td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{user.nationality || '-'}</td>
                    <td className="px-6 py-4">{getRoleBadge(user.role)}</td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{formatDate(user.created_at)}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-1">
                        {user.role === 'user' && (
                          <button
                            onClick={() => changeRole(user.id, 'admin')}
                            className="px-2.5 py-1 text-xs font-medium text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/20 rounded-md hover:bg-indigo-100 dark:hover:bg-indigo-900/40 transition-colors"
                          >
                            관리자 지정
                          </button>
                        )}
                        {user.role === 'admin' && (
                          <>
                            <button
                              onClick={() => changeRole(user.id, 'superadmin')}
                              className="px-2.5 py-1 text-xs font-medium text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 rounded-md hover:bg-amber-100 dark:hover:bg-amber-900/40 transition-colors"
                            >
                              승격
                            </button>
                            <button
                              onClick={() => changeRole(user.id, 'user')}
                              className="px-2.5 py-1 text-xs font-medium text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 rounded-md hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors"
                            >
                              해제
                            </button>
                          </>
                        )}
                        {user.role === 'superadmin' && (
                          <button
                            onClick={() => changeRole(user.id, 'admin')}
                            className="px-2.5 py-1 text-xs font-medium text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                          >
                            강등
                          </button>
                        )}
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
    </div>
  );
}
