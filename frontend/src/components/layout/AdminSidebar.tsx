'use client';

import { useState } from 'react';
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
  Image,
  PartyPopper,
  Palette,
  BookOpen,
  Star,
  Ticket,
  MessageCircle,
  MapPin,
  BarChart3,
  Briefcase,
  ChevronDown,
  ChevronRight,
  FileText,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface AdminSidebarProps {
  t: (key: string) => string;
  onLogout: () => void;
}

export default function AdminSidebar({ t, onLogout }: AdminSidebarProps) {
  const pathname = usePathname();
  const [contentOpen, setContentOpen] = useState(() => {
    const contentPaths = ['/admin/restaurants', '/admin/courses', '/admin/products', '/admin/guides', '/admin/transport', '/admin/festivals', '/admin/themes', '/admin/living-guide'];
    return contentPaths.some((p) => pathname.startsWith(p));
  });

  const contentSubItems = [
    { href: '/admin/restaurants', icon: UtensilsCrossed, label: '맛집' },
    { href: '/admin/courses', icon: Map, label: '코스' },
    { href: '/admin/products', icon: ShoppingBag, label: '상품' },
    { href: '/admin/guides', icon: Users, label: '가이드' },
    { href: '/admin/transport', icon: Bus, label: '교통' },
    { href: '/admin/festivals', icon: PartyPopper, label: '축제' },
    { href: '/admin/themes', icon: Palette, label: '테마' },
    { href: '/admin/living-guide', icon: BookOpen, label: '생활 가이드' },
  ];

  const menuItems = [
    { href: '/admin', icon: LayoutDashboard, label: '대시보드', exact: true },
    { href: '/admin/banners', icon: Image, label: '배너' },
    { href: '/admin/events', icon: Calendar, label: '전시회' },
    { type: 'submenu' as const, icon: FileText, label: '콘텐츠', items: contentSubItems },
    { href: '/admin/bookings', icon: ClipboardList, label: '예약' },
    { href: '/admin/reviews', icon: Star, label: '리뷰' },
    { href: '/admin/coupons', icon: Ticket, label: '쿠폰' },
    { href: '/admin/languages', icon: Globe, label: '언어 관리' },
    { href: '/admin/users', icon: UserCog, label: '회원 관리' },
    { href: '/admin/chat', icon: MessageCircle, label: '채팅 모니터' },
    { href: '/admin/map-settings', icon: MapPin, label: '지도 설정' },
    { href: '/admin/analytics', icon: BarChart3, label: '분석' },
    { href: '/admin/b2b', icon: Briefcase, label: 'B2B 파트너' },
  ];

  const isActive = (href: string, exact?: boolean) => {
    if (exact) return pathname === href;
    return pathname.startsWith(href);
  };

  const isContentActive = contentSubItems.some((item) => pathname.startsWith(item.href));

  const mobileItems = [
    { href: '/admin', icon: LayoutDashboard, label: '대시보드', exact: true },
    { href: '/admin/banners', icon: Image, label: '배너' },
    { href: '/admin/events', icon: Calendar, label: '전시회' },
    { href: '/admin/bookings', icon: ClipboardList, label: '예약' },
    { href: '/admin/analytics', icon: BarChart3, label: '분석' },
  ];

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-white dark:bg-dark-sidebar border-r border-gray-200 dark:border-gray-500/40 min-h-screen flex-shrink-0">
        <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-200 dark:border-gray-500/40">
          <Compass className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
          <span className="text-base font-bold text-gray-900 dark:text-white">관리자 패널</span>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
          {menuItems.map((item, idx) => {
            if ('type' in item && item.type === 'submenu') {
              return (
                <div key={`submenu-${idx}`}>
                  <button
                    onClick={() => setContentOpen(!contentOpen)}
                    className={cn(
                      'flex items-center justify-between w-full gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                      isContentActive
                        ? 'bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-white/[0.05]'
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <item.icon className="w-5 h-5" />
                      {item.label}
                    </div>
                    {contentOpen ? (
                      <ChevronDown className="w-4 h-4" />
                    ) : (
                      <ChevronRight className="w-4 h-4" />
                    )}
                  </button>
                  {contentOpen && (
                    <div className="ml-4 mt-0.5 space-y-0.5 border-l-2 border-gray-200 dark:border-gray-600 pl-2">
                      {item.items.map((sub) => {
                        const active = isActive(sub.href);
                        return (
                          <Link
                            key={sub.href}
                            href={sub.href}
                            className={cn(
                              'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                              active
                                ? 'bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'
                                : 'text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-white/[0.05]'
                            )}
                          >
                            <sub.icon className="w-4 h-4" />
                            {sub.label}
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            }

            if (!('href' in item)) return null;
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
            로그아웃
          </button>
        </div>
      </aside>

      {/* Mobile Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-dark-main border-t border-gray-200 dark:border-gray-500/40 md:hidden">
        <div className="flex items-center justify-around h-16 px-1">
          {mobileItems.map((item) => {
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
