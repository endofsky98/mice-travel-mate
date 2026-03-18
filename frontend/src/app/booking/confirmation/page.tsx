'use client';

import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { CheckCircle, Home, ClipboardList } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

export default function BookingConfirmationPage() {
  const { t } = useLanguage();
  const searchParams = useSearchParams();
  const bookingNumber = searchParams.get('booking_number') || 'N/A';

  return (
    <div className="page-container max-w-lg">
      <Card className="p-8 text-center">
        <div className="w-16 h-16 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center mx-auto mb-4">
          <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {t('booking.confirmation')}
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mb-6">
          {t('booking.booking_success')}
        </p>

        <div className="bg-gray-50 dark:bg-dark-input rounded-xl p-4 mb-6">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">{t('booking.booking_number')}</p>
          <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 font-mono">
            {bookingNumber}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <Link href="/" className="flex-1">
            <Button variant="outline" className="w-full">
              <Home className="w-4 h-4" />
              {t('nav.home')}
            </Button>
          </Link>
          <Link href="/mypage" className="flex-1">
            <Button className="w-full">
              <ClipboardList className="w-4 h-4" />
              {t('mypage.bookings')}
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
