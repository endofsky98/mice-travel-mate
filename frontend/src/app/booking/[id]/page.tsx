'use client';

import { useEffect, useState } from 'react';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import BookingForm, { BookingFormData } from '@/components/booking/BookingForm';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import Card from '@/components/ui/Card';
import { Product, Guide } from '@/types';
import { formatCurrency } from '@/lib/utils';

export default function BookingPage() {
  const { id } = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const { t, lt, language } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [item, setItem] = useState<Product | Guide | null>(null);

  const type = searchParams.get('type') || 'product';

  useEffect(() => {
    const fetchItem = async () => {
      setLoading(true);
      try {
        if (type === 'guide') {
          const data = await api.get<Guide>(`/api/v1/guides/${id}`);
          setItem(data);
        } else {
          const data = await api.get<Product>(`/api/v1/products/${id}`);
          setItem(data);
        }
      } catch {
        setItem(null);
      }
      setLoading(false);
    };
    fetchItem();
  }, [id, type, language]);

  const handleSubmit = async (data: BookingFormData) => {
    setSubmitting(true);
    try {
      const bookingData = {
        type,
        item_id: Number(id),
        date: data.date,
        time: data.time,
        participants: data.participants,
        booker_name: data.name,
        booker_email: data.email,
        booker_phone: data.phone,
        booker_nationality: data.nationality,
        special_requests: data.specialRequests,
      };
      const result = await api.post<{ booking_number: string }>('/api/v1/bookings', bookingData);
      router.push(`/booking/confirmation?booking_number=${result.booking_number}`);
    } catch {
      alert('Booking failed. Please try again.');
    }
    setSubmitting(false);
  };

  if (loading) return <LoadingSpinner fullPage />;
  if (!item) {
    return (
      <div className="page-container text-center py-20">
        <p className="text-gray-500">{t('common.no_results')}</p>
      </div>
    );
  }

  const name = lt(item.name);
  const isProduct = type === 'product';
  const price = isProduct ? (item as Product).price : (item as Guide).hourly_rate;
  const currency = isProduct ? (item as Product).currency : (item as Guide).currency;

  return (
    <div className="page-container max-w-2xl">
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      {/* Item Summary */}
      <Card className="p-4 mb-6">
        <h2 className="font-semibold text-gray-900 dark:text-gray-100 mb-1">{name}</h2>
        {price && (
          <p className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
            {formatCurrency(price, currency)}
            {!isProduct && <span className="text-sm text-gray-400 font-normal ml-1">/ hr</span>}
            {isProduct && <span className="text-sm text-gray-400 font-normal ml-1">/ {t('product.per_person')}</span>}
          </p>
        )}
      </Card>

      {/* Booking Form */}
      <Card className="p-6">
        <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('common.book_now')}</h1>
        <BookingForm t={t} onSubmit={handleSubmit} isLoading={submitting} />
      </Card>
    </div>
  );
}
