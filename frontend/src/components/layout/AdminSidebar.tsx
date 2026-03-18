'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Calendar,
  UtensilsCrossed,
  Map,
  ShoppingBag,
  Users,
  Bus,
  ClipboardList,
  Globe,
  UserCog,
  LogOut,
  Compass,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface AdminSidebarProps {
  t: (key: string) => string;
  onLogout: () => void;
}

export default function AdminSidebar({ t, onLogout }: AdminSidebarProps) {
  const pathname = usePathname();

  const menuItems = [
    { href: '/admin', icon: LayoutDashboard, label: t('admin.dashboard'), exact: true },
    { href: '/admin/events', icon: Calendar, label: t('admin.events') },
    { href: '/admin/restaurants', icon: UtensilsCrossed, label: t('admin.restaurants') },
    { href: '/admin/courses', icon: Map, label: t('admin.courses') },
    { href: '/admin/products', icon: ShoppingBag, label: t('admin.products') },
    { href: '/admin/guides', icon: Users, label: t('admin.guides') },
    { href: '/admin/transport', icon: Bus, label: t('admin.transport') },
    { href: '/admin/bookings', icon: ClipboardList, label: t('admin.bookings') },
    { href: '/admin/languages', icon: Globe, label: t('admin.languages') },
    { href: '/admin/users', icon: UserCog, label: t('admin.users') },
  ];

  const isActive = (href: string, exact?: boolean) => {
    if (exact) return pathname === href;
    return pathname.startsWith(href);
  };

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-white dark:bg-dark-sidebar border-r border-gray-200 dark:border-gray-500/40 min-h-screen">
        <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-200 dark:border-gray-500/40">
          <Compass className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
          <span className="text-base font-bold text-gray-900 dark:text-white">Admin Panel</span>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {menuItems.map((item) => {
            const active = isActive(item.href, item.exact);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                  active
                    ? 'bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-white/[0.05]'
                )}
              >
                <item.icon className="w-5 h-5" />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="px-3 py-4 border-t border-gray-200 dark:border-gray-500/40">
          <button
            onClick={onLogout}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-white/[0.05] transition-colors"
          >
            <LogOut className="w-5 h-5" />
            {t('nav.logout')}
          </button>
        </div>
      </aside>

      {/* Mobile Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-dark-main border-t border-gray-200 dark:border-gray-500/40 md:hidden">
        <div className="flex items-center justify-around h-16 px-1">
          {menuItems.slice(0, 5).map((item) => {
            const active = isActive(item.href, item.exact);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex flex-col items-center justify-center gap-0.5 w-full py-1 transition-colors',
                  active
                    ? 'text-indigo-600 dark:text-indigo-400'
                    : 'text-gray-400 dark:text-gray-500'
                )}
              >
                <item.icon className="w-5 h-5" />
                <span className="text-[10px] font-medium truncate max-w-[60px]">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
