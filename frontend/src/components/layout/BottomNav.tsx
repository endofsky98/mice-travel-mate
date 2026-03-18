'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, UtensilsCrossed, Map, ShoppingBag, Users } from 'lucide-react';
import { cn } from '@/lib/utils';

interface BottomNavProps {
  t: (key: string) => string;
}

export default function BottomNav({ t }: BottomNavProps) {
  const pathname = usePathname();

  const tabs = [
    { href: '/', icon: Home, label: t('nav.home'), match: '/' },
    { href: '/restaurants', icon: UtensilsCrossed, label: t('nav.restaurants'), match: '/restaurants' },
    { href: '/courses', icon: Map, label: t('nav.courses'), match: '/courses' },
    { href: '/products', icon: ShoppingBag, label: t('nav.products'), match: '/products' },
    { href: '/guides', icon: Users, label: t('nav.guides'), match: '/guides' },
  ];

  const isActive = (match: string) => {
    if (match === '/') return pathname === '/';
    return pathname.startsWith(match);
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-dark-main border-t border-gray-200 dark:border-gray-500/40 md:hidden">
      <div className="flex items-center justify-around h-16 px-2">
        {tabs.map((tab) => {
          const active = isActive(tab.match);
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={cn(
                'flex flex-col items-center justify-center gap-0.5 w-full py-1 transition-colors',
                active
                  ? 'text-indigo-600 dark:text-indigo-400'
                  : 'text-gray-400 dark:text-gray-500'
              )}
            >
              <tab.icon className="w-5 h-5" />
              <span className="text-[10px] font-medium">{tab.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
