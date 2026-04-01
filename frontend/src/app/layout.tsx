'use client';

import { useEffect } from 'react';
import { Inter } from 'next/font/google';
import { usePathname, useRouter } from 'next/navigation';
import Script from 'next/script';
import './globals.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import Header from '@/components/layout/Header';
import BottomNav from '@/components/layout/BottomNav';
import Footer from '@/components/layout/Footer';
import { useLanguage } from '@/hooks/useLanguage';
import { useAuth } from '@/hooks/useAuth';

const inter = Inter({ subsets: ['latin'] });

const HOME_TITLES: Record<string, string> = {
  en: 'Your Expo Travel Mate | Exporoute',
  ko: '당신의 전시회 여행 메이트 | Exporoute',
  ja: 'あなたの展示会トラベルメイト | Exporoute',
  'zh-CN': '您的展会旅行伙伴 | Exporoute',
  'zh-TW': '您的展會旅行夥伴 | Exporoute',
  es: 'Tu Compañero de Viaje de Exposiciones | Exporoute',
  th: 'เพื่อนเที่ยวงานแสดงสินค้าของคุณ | Exporoute',
  vi: 'Bạn Đồng Hành Du Lịch Hội Chợ | Exporoute',
  fr: "Votre Compagnon de Voyage d'Expo | Exporoute",
};

const PAGE_TITLES: Record<string, Record<string, string>> = {
  '/restaurants': { en: 'Restaurants', ko: '맛집', ja: 'レストラン', 'zh-CN': '餐厅', 'zh-TW': '餐廳', es: 'Restaurantes', th: 'ร้านอาหาร', vi: 'Nhà hàng', fr: 'Restaurants' },
  '/courses': { en: 'Travel Courses', ko: '여행 코스', ja: 'トラベルコース', 'zh-CN': '旅游路线', 'zh-TW': '旅遊路線', es: 'Rutas de Viaje', th: 'เส้นทางท่องเที่ยว', vi: 'Lộ trình Du lịch', fr: 'Parcours de Voyage' },
  '/products': { en: 'Tours & Activities', ko: '투어 & 액티비티', ja: 'ツアー＆アクティビティ', 'zh-CN': '旅游活动', 'zh-TW': '旅遊活動', es: 'Tours y Actividades', th: 'ทัวร์และกิจกรรม', vi: 'Tour & Hoạt động', fr: 'Tours & Activités' },
  '/guides': { en: 'Guides', ko: '가이드', ja: 'ガイド', 'zh-CN': '导游', 'zh-TW': '導遊', es: 'Guías', th: 'ไกด์', vi: 'Hướng dẫn viên', fr: 'Guides' },
  '/festivals': { en: 'Festivals & Events', ko: '축제 & 이벤트', ja: '祭り＆イベント', 'zh-CN': '节日活动', 'zh-TW': '節慶活動', es: 'Festivales y Eventos', th: 'เทศกาลและกิจกรรม', vi: 'Lễ hội & Sự kiện', fr: 'Festivals & Événements' },
  '/map': { en: 'Map', ko: '지도', ja: '地図', 'zh-CN': '地图', 'zh-TW': '地圖', es: 'Mapa', th: 'แผนที่', vi: 'Bản đồ', fr: 'Carte' },
  '/transport': { en: 'Transport', ko: '교통', ja: '交通', 'zh-CN': '交通', 'zh-TW': '交通', es: 'Transporte', th: 'การขนส่ง', vi: 'Giao thông', fr: 'Transport' },
  '/ai-course': { en: 'AI Course', ko: 'AI 코스', ja: 'AIコース', 'zh-CN': 'AI路线', 'zh-TW': 'AI路線', es: 'Curso AI', th: 'คอร์ส AI', vi: 'Khóa AI', fr: 'Cours IA' },
  '/themes': { en: 'Themes', ko: '테마', ja: 'テーマ', 'zh-CN': '主题', 'zh-TW': '主題', es: 'Temas', th: 'ธีม', vi: 'Chủ đề', fr: 'Thèmes' },
  '/living-guide': { en: 'Living Guide', ko: '생활 가이드', ja: '生活ガイド', 'zh-CN': '生活指南', 'zh-TW': '生活指南', es: 'Guía de Vida', th: 'คู่มือชีวิต', vi: 'Cẩm nang Sống', fr: 'Guide de Vie' },
  '/mypage': { en: 'My Page', ko: '마이페이지', ja: 'マイページ', 'zh-CN': '我的页面', 'zh-TW': '我的頁面', es: 'Mi Página', th: 'หน้าของฉัน', vi: 'Trang cá nhân', fr: 'Ma Page' },
  '/search': { en: 'Search', ko: '검색', ja: '検索', 'zh-CN': '搜索', 'zh-TW': '搜尋', es: 'Buscar', th: 'ค้นหา', vi: 'Tìm kiếm', fr: 'Recherche' },
  '/chat': { en: 'Chat', ko: '채팅', ja: 'チャット', 'zh-CN': '聊天', 'zh-TW': '聊天', es: 'Chat', th: 'แชท', vi: 'Trò chuyện', fr: 'Chat' },
};

function getPageTitle(pathname: string, language: string): string {
  // Home page
  if (pathname === '/') {
    return HOME_TITLES[language] || HOME_TITLES['en'];
  }
  // Admin pages
  if (pathname.startsWith('/admin')) {
    return 'Admin | Exporoute';
  }
  // Auth pages
  if (pathname.startsWith('/auth')) {
    return 'Exporoute';
  }
  // Detail pages (e.g. /restaurants/123) - title set by the page itself via document.title
  // Match known section pages
  for (const [path, titles] of Object.entries(PAGE_TITLES)) {
    if (pathname === path || pathname.startsWith(path + '/')) {
      // For detail pages, just return section title - the page will override with item name
      return `${titles[language] || titles['en']} | Exporoute`;
    }
  }
  return 'Exporoute';
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const { t, language, setLanguage, isLoaded } = useLanguage();
  const { user, isLoggedIn, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const isAdminRoute = pathname.startsWith('/admin');
  const isGuideDashboard = pathname.startsWith('/guide-dashboard');
  const isB2B = pathname.startsWith('/b2b');
  const hideMainNav = isAdminRoute || isGuideDashboard || isB2B;

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  // Dynamic page title based on route and language
  useEffect(() => {
    document.title = getPageTitle(pathname, language);
  }, [pathname, language]);

  return (
    <html lang={language} className={inter.className}>
      <head>
        <meta httpEquiv="Content-Security-Policy" content="upgrade-insecure-requests" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
        <title>Exporoute</title>
        <meta name="description" content="Your curated travel companion for MICE exhibition visitors in Korea" />
        <meta property="og:title" content="Exporoute" />
        <meta property="og:site_name" content="Exporoute" />
        <meta property="og:description" content="Your curated travel companion for MICE exhibition visitors in Korea" />
        <meta property="og:image" content="/logo.svg" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="icon" href="/favicon.svg" sizes="any" />
        <link rel="apple-touch-icon" href="/favicon.svg" />
      </head>
      <body className="min-h-screen flex flex-col">
        {!isLoaded ? (
          <div className="flex items-center justify-center min-h-screen">
            <div className="w-8 h-8 border-2 border-gray-200 border-t-indigo-600 rounded-full animate-spin" />
          </div>
        ) : (
          <>
            {!hideMainNav && (
              <Header
                t={t}
                language={language}
                onLanguageChange={setLanguage}
                isLoggedIn={isLoggedIn}
                onLogout={handleLogout}
                user={user}
              />
            )}
            <main className="flex-1">{children}</main>
            {!hideMainNav && <Footer t={t} />}
            {!hideMainNav && <BottomNav t={t} isLoggedIn={isLoggedIn} />}
          </>
        )}
        <Script src="https://guide.runhatch.com/sdk.js?v=3" data-key="bsk_62b54def8bd9562c037055e3d49caba926f463da4eb32191" strategy="afterInteractive" />
      </body>
    </html>
  );
}
