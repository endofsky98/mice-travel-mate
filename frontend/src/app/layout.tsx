'use client';

import { Inter } from 'next/font/google';
import { usePathname, useRouter } from 'next/navigation';
import './globals.css';
import Header from '@/components/layout/Header';
import BottomNav from '@/components/layout/BottomNav';
import Footer from '@/components/layout/Footer';
import { useLanguage } from '@/hooks/useLanguage';
import { useAuth } from '@/hooks/useAuth';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const { t, language, setLanguage, isLoaded } = useLanguage();
  const { isLoggedIn, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const isAdminRoute = pathname.startsWith('/admin');
  const isAuthRoute = pathname.startsWith('/auth');

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  return (
    <html lang={language} className={inter.className}>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
        <title>MICE Travel Mate</title>
        <meta name="description" content="Your curated travel companion for MICE exhibition visitors" />
      </head>
      <body className="min-h-screen flex flex-col">
        {!isLoaded ? (
          <div className="flex items-center justify-center min-h-screen">
            <div className="w-8 h-8 border-2 border-gray-200 border-t-indigo-600 rounded-full animate-spin" />
          </div>
        ) : (
          <>
            {!isAdminRoute && !isAuthRoute && (
              <Header
                t={t}
                language={language}
                onLanguageChange={setLanguage}
                isLoggedIn={isLoggedIn}
                onLogout={handleLogout}
              />
            )}
            <main className="flex-1">{children}</main>
            {!isAdminRoute && !isAuthRoute && <Footer t={t} />}
            {!isAdminRoute && !isAuthRoute && <BottomNav t={t} />}
          </>
        )}
      </body>
    </html>
  );
}
