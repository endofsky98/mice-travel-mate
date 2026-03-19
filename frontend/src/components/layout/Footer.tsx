'use client';

import Logo from '@/components/ui/Logo';

interface FooterProps {
  t: (key: string) => string;
}

export default function Footer({ t }: FooterProps) {
  return (
    <footer className="hidden md:block border-t border-gray-200 dark:border-gray-500/40 bg-white dark:bg-dark-main">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Logo size="sm" href="/" />
            <span className="text-xs text-gray-400 dark:text-gray-500">powered by exporum</span>
          </div>
          <nav className="flex items-center gap-6">
            <a href="/restaurants" className="text-sm text-gray-500 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              {t('nav.restaurants')}
            </a>
            <a href="/courses" className="text-sm text-gray-500 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              {t('nav.courses')}
            </a>
            <a href="/products" className="text-sm text-gray-500 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              {t('nav.products')}
            </a>
            <a href="/guides" className="text-sm text-gray-500 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              {t('nav.guides')}
            </a>
          </nav>
          <p className="text-xs text-gray-400 dark:text-gray-500">
            &copy; 2026 exporum. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
