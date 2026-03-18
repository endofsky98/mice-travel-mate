'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Menu, X, User, LogOut, Shield } from 'lucide-react';
import { cn } from '@/lib/utils';
import LanguageSwitcher from '@/components/ui/LanguageSwitcher';
import Logo from '@/components/ui/Logo';
import { Language, User as UserType } from '@/types';

interface HeaderProps {
  t: (key: string) => string;
  language: Language;
  onLanguageChange: (lang: Language) => void;
  isLoggedIn: boolean;
  onLogout: () => void;
  user?: UserType | null;
}

export default function Header({ t, language, onLanguageChange, isLoggedIn, onLogout, user }: HeaderProps) {
  const isAdmin = user?.role === 'admin' || user?.role === 'superadmin' || user?.is_admin;
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navLinks = [
    { href: '/restaurants', label: t('nav.restaurants') },
    { href: '/courses', label: t('nav.courses') },
    { href: '/products', label: t('nav.products') },
    { href: '/guides', label: t('nav.guides') },
    { href: '/transport', label: t('nav.transport') },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/80 dark:bg-dark-main/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-500/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Logo href="/" size="md" showText className="hidden sm:flex" />
            <Logo href="/" size="sm" showText={false} className="sm:hidden" />

            <nav className="hidden md:flex items-center gap-1">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>

          <div className="flex items-center gap-3">
            <LanguageSwitcher
              currentLanguage={language}
              onLanguageChange={onLanguageChange}
              compact
            />

            {isLoggedIn ? (
              <div className="hidden md:flex items-center gap-2">
                {isAdmin && (
                  <Link
                    href="/admin"
                    className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 rounded-lg transition-colors"
                  >
                    <Shield className="w-4 h-4" />
                    {t('nav.admin') || 'Admin'}
                  </Link>
                )}
                <Link
                  href="/mypage"
                  className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors"
                >
                  <User className="w-4 h-4" />
                  {t('nav.mypage')}
                </Link>
                <button
                  onClick={onLogout}
                  className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  {t('nav.logout')}
                </button>
              </div>
            ) : (
              <Link
                href="/auth/login"
                className="hidden md:inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-400 rounded-lg transition-colors"
              >
                {t('nav.login')}
              </Link>
            )}

            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/[0.08] transition-colors"
            >
              {isMobileMenuOpen ? (
                <X className="w-5 h-5 text-gray-700 dark:text-gray-300" />
              ) : (
                <Menu className="w-5 h-5 text-gray-700 dark:text-gray-300" />
              )}
            </button>
          </div>
        </div>
      </div>

      {isMobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200 dark:border-gray-500/40 bg-white dark:bg-dark-main">
          <div className="px-4 py-3 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className="block px-3 py-2.5 text-sm text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors"
              >
                {link.label}
              </Link>
            ))}
            <div className="pt-2 border-t border-gray-100 dark:border-gray-500/40">
              {isLoggedIn ? (
                <>
                  {isAdmin && (
                    <Link
                      href="/admin"
                      onClick={() => setIsMobileMenuOpen(false)}
                      className="flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-indigo-600 dark:text-indigo-400 rounded-lg hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors"
                    >
                      <Shield className="w-4 h-4" />
                      {t('nav.admin') || 'Admin'}
                    </Link>
                  )}
                  <Link
                    href="/mypage"
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={cn(
                      'flex items-center gap-2 px-3 py-2.5 text-sm text-gray-600 dark:text-gray-300',
                      'hover:text-indigo-600 dark:hover:text-indigo-400 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors'
                    )}
                  >
                    <User className="w-4 h-4" />
                    {t('nav.mypage')}
                  </Link>
                  <button
                    onClick={() => {
                      setIsMobileMenuOpen(false);
                      onLogout();
                    }}
                    className="flex items-center gap-2 w-full px-3 py-2.5 text-sm text-gray-600 dark:text-gray-300 hover:text-red-600 dark:hover:text-red-400 rounded-lg hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    {t('nav.logout')}
                  </button>
                </>
              ) : (
                <Link
                  href="/auth/login"
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="block px-3 py-2.5 text-sm font-medium text-indigo-600 dark:text-indigo-400"
                >
                  {t('nav.login')}
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
