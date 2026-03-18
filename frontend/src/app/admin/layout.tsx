'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import AdminSidebar from '@/components/layout/AdminSidebar';
import { useLanguage } from '@/hooks/useLanguage';
import { isAuthenticated, getCurrentUser } from '@/lib/auth';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import LanguageSwitcher from '@/components/ui/LanguageSwitcher';
import { LogOut, User, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { User as UserType } from '@/types';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { t, language, setLanguage, isLoaded } = useLanguage();
  const router = useRouter();
  const pathname = usePathname();
  const [checking, setChecking] = useState(true);
  const [adminUser, setAdminUser] = useState<UserType | null>(null);

  const isLoginPage = pathname === '/admin/login';

  useEffect(() => {
    const checkAdminAccess = async () => {
      if (isLoginPage) {
        setChecking(false);
        return;
      }

      if (!isAuthenticated()) {
        router.push('/admin/login');
        setChecking(false);
        return;
      }

      try {
        const user = await getCurrentUser();
        if (!user || (user.role !== 'admin' && user.role !== 'superadmin' && !user.is_admin)) {
          router.push('/');
          setChecking(false);
          return;
        }
        setAdminUser(user);
      } catch {
        router.push('/admin/login');
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

  if (!isLoaded || checking) return <LoadingSpinner fullPage />;

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
              {t('nav.home') || 'Home'}
            </Link>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100 md:hidden">Admin</h1>
          </div>
          <div className="flex items-center gap-3 ml-auto">
            <LanguageSwitcher currentLanguage={language} onLanguageChange={setLanguage} compact />
            <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
              <User className="w-4 h-4" />
              <span className="hidden sm:inline">{adminUser?.name || 'Admin'}</span>
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
