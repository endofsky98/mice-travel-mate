'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import AdminSidebar from '@/components/layout/AdminSidebar';
import { useLanguage } from '@/hooks/useLanguage';
import { isAuthenticated, getCurrentUser } from '@/lib/auth';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { LogOut, User, ArrowLeft, AlertTriangle } from 'lucide-react';
import Link from 'next/link';
import { User as UserType } from '@/types';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { t, isLoaded } = useLanguage();
  const router = useRouter();
  const pathname = usePathname();
  const [checking, setChecking] = useState(true);
  const [adminUser, setAdminUser] = useState<UserType | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);

  const isLoginPage = pathname === '/admin/login';

  useEffect(() => {
    const checkAdminAccess = async () => {
      if (isLoginPage) {
        setChecking(false);
        return;
      }

      if (!isAuthenticated()) {
        router.replace('/admin/login');
        return;
      }

      try {
        const user = await getCurrentUser();
        if (!user) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          router.replace('/admin/login');
          return;
        }
        if (user.role !== 'admin' && user.role !== 'superadmin' && !user.is_admin) {
          router.replace('/');
          return;
        }
        setAdminUser(user);
      } catch {
        setAuthError('관리자 접근 권한을 확인할 수 없습니다. 다시 시도해 주세요.');
        setChecking(false);
        return;
      }
      setChecking(false);
    };

    checkAdminAccess();
  }, [isLoginPage, router]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/admin/login');
  };

  if (!isLoaded || checking) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-dark-main gap-3">
        <LoadingSpinner size="lg" />
        <p className="text-sm text-gray-500 dark:text-gray-400">로딩 중...</p>
      </div>
    );
  }

  if (authError) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-dark-main gap-4 px-4">
        <AlertTriangle className="w-12 h-12 text-amber-500" />
        <p className="text-gray-700 dark:text-gray-300 text-center">{authError}</p>
        <Link
          href="/admin/login"
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-400 transition-colors"
        >
          관리자 로그인
        </Link>
      </div>
    );
  }

  if (isLoginPage) {
    return <>{children}</>;
  }

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-dark-main">
      <AdminSidebar t={t} onLogout={handleLogout} />
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Top Bar */}
        <header className="h-16 border-b border-gray-200 dark:border-gray-500/40 bg-white dark:bg-dark-main px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="hidden md:flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              홈으로
            </Link>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100 md:hidden">관리자</h1>
          </div>
          <div className="flex items-center gap-3 ml-auto">
            <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
              <User className="w-4 h-4" />
              <span className="hidden sm:inline">{adminUser?.name || '관리자'}</span>
              {adminUser?.role === 'superadmin' && (
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300 font-medium">
                  Super
                </span>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/[0.08] text-gray-500 dark:text-gray-400"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 p-4 md:p-6 pb-24 md:pb-6 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
