'use client';

import { useState } from 'react';
import { Search, ClipboardList } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { Booking } from '@/types';
import { formatCurrency, formatDate } from '@/lib/utils';

export default function BookingLookupPage() {
  const { t } = useLanguage();
  const [bookingNumber, setBookingNumber] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [booking, setBooking] = useState<Booking | null>(null);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

  const handleSearch = async () => {
    if (!bookingNumber || !email) return;
    setLoading(true);
    setError('');
    setBooking(null);
    try {
      const data = await api.get<Booking>('/api/bookings/lookup', {
        booking_number: bookingNumber,
        email,
      });
      setBooking(data);
    } catch {
      setError(t('common.no_results'));
    }
    setSearched(true);
    setLoading(false);
  };

  const statusVariant = (status: string) => {
    switch (status) {
      case 'confirmed': return 'success';
      case 'pending': return 'warning';
      case 'cancelled': return 'error';
      case 'completed': return 'info';
      default: return 'default';
    }
  };

  return (
    <div className="page-container max-w-lg">
      <div className="text-center mb-8">
        <div className="w-16 h-16 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mx-auto mb-4">
          <Search className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">{t('booking.lookup_title')}</h1>
        <p className="text-gray-500 dark:text-gray-400">{t('booking.lookup_subtitle')}</p>
      </div>

      <Card className="p-6 mb-6">
        <div className="space-y-4">
          <Input
            label={t('booking.booking_number')}
            placeholder="BK-XXXXXX"
            value={bookingNumber}
            onChange={(e) => setBookingNumber(e.target.value)}
          />
          <Input
            type="email"
            label={t('auth.email')}
            placeholder="your@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Button onClick={handleSearch} disabled={loading} className="w-full">
            {loading ? t('common.loading') : t('booking.lookup_button')}
          </Button>
        </div>
      </Card>

      {error && searched && (
        <Card className="p-6 text-center">
          <ClipboardList className="w-10 h-10 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
          <p className="text-gray-500 dark:text-gray-400">{error}</p>
        </Card>
      )}

      {booking && (
        <Card className="p-6">
          <h2 className="font-semibold text-gray-900 dark:text-gray-100 mb-4">{t('booking.booking_details')}</h2>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-500 dark:text-gray-400">{t('booking.booking_number')}</span>
              <span className="font-mono font-medium text-gray-900 dark:text-gray-100">{booking.booking_number}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500 dark:text-gray-400">{t('booking.status')}</span>
              <Badge variant={statusVariant(booking.status)}>
                {t(`booking.status_${booking.status}`)}
              </Badge>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500 dark:text-gray-400">{t('booking.date')}</span>
              <span className="text-gray-900 dark:text-gray-100">{formatDate(booking.date)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-500 dark:text-gray-400">{t('booking.participants')}</span>
              <span className="text-gray-900 dark:text-gray-100">{booking.participants}</span>
            </div>
            <div className="flex justify-between pt-3 border-t border-gray-200 dark:border-gray-500/40">
              <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{t('booking.total')}</span>
              <span className="font-bold text-indigo-600 dark:text-indigo-400">
                {formatCurrency(booking.total_price, booking.currency)}
              </span>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
