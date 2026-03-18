'use client';

import { Compass } from 'lucide-react';

interface FooterProps {
  t: (key: string) => string;
}

export default function Footer({ t }: FooterProps) {
  return (
    <footer className="hidden md:block border-t border-gray-200 dark:border-gray-500/40 bg-white dark:bg-dark-main">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Compass className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <span className="text-sm font-semibold text-gray-900 dark:text-white">MICE Travel Mate</span>
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
            &copy; 2024 MICE Travel Mate. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
