'use client';

import { useState } from 'react';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { cn } from '@/lib/utils';

interface BookingFormProps {
  t: (key: string) => string;
  onSubmit: (data: BookingFormData) => void;
  isLoading?: boolean;
}

export interface BookingFormData {
  date: string;
  time: string;
  participants: number;
  name: string;
  email: string;
  phone: string;
  nationality: string;
  specialRequests: string;
}

export default function BookingForm({ t, onSubmit, isLoading }: BookingFormProps) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<BookingFormData>({
    date: '',
    time: '',
    participants: 1,
    name: '',
    email: '',
    phone: '',
    nationality: '',
    specialRequests: '',
  });

  const steps = [
    { id: 1, label: t('booking.step_date') },
    { id: 2, label: t('booking.step_details') },
    { id: 3, label: t('booking.step_payment') },
    { id: 4, label: t('booking.step_confirmation') },
  ];

  const updateField = (field: keyof BookingFormData, value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (step < 3) setStep(step + 1);
    else if (step === 3) onSubmit(formData);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <div>
      {/* Step Indicator */}
      <div className="flex items-center justify-between mb-8">
        {steps.map((s, idx) => (
          <div key={s.id} className="flex items-center flex-1">
            <div className="flex flex-col items-center">
              <div
                className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium border-2 transition-colors',
                  step >= s.id
                    ? 'bg-indigo-600 border-indigo-600 text-white dark:bg-indigo-500 dark:border-indigo-500'
                    : 'border-gray-300 text-gray-400 dark:border-gray-600 dark:text-gray-500'
                )}
              >
                {s.id}
              </div>
              <span
                className={cn(
                  'mt-1 text-xs font-medium hidden sm:block',
                  step >= s.id ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-400 dark:text-gray-500'
                )}
              >
                {s.label}
              </span>
            </div>
            {idx < steps.length - 1 && (
              <div
                className={cn(
                  'flex-1 h-0.5 mx-2',
                  step > s.id ? 'bg-indigo-600 dark:bg-indigo-500' : 'bg-gray-200 dark:bg-gray-700'
                )}
              />
            )}
          </div>
        ))}
      </div>

      {/* Step 1: Date & Participants */}
      {step === 1 && (
        <div className="space-y-4">
          <Input
            type="date"
            label={t('booking.select_date')}
            value={formData.date}
            onChange={(e) => updateField('date', e.target.value)}
          />
          <Input
            type="time"
            label={t('booking.time')}
            value={formData.time}
            onChange={(e) => updateField('time', e.target.value)}
          />
          <Input
            type="number"
            label={t('booking.participant_count')}
            min={1}
            max={20}
            value={formData.participants}
            onChange={(e) => updateField('participants', parseInt(e.target.value) || 1)}
          />
        </div>
      )}

      {/* Step 2: Personal Details */}
      {step === 2 && (
        <div className="space-y-4">
          <Input
            label={t('booking.booker_name')}
            placeholder={t('booking.booker_name')}
            value={formData.name}
            onChange={(e) => updateField('name', e.target.value)}
          />
          <Input
            type="email"
            label={t('booking.booker_email')}
            placeholder={t('booking.booker_email')}
            value={formData.email}
            onChange={(e) => updateField('email', e.target.value)}
          />
          <Input
            type="tel"
            label={t('booking.booker_phone')}
            placeholder={t('booking.booker_phone')}
            value={formData.phone}
            onChange={(e) => updateField('phone', e.target.value)}
          />
          <Input
            label={t('booking.booker_nationality')}
            placeholder={t('booking.booker_nationality')}
            value={formData.nationality}
            onChange={(e) => updateField('nationality', e.target.value)}
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
              {t('booking.special_requests')}
            </label>
            <textarea
              className="w-full px-4 py-3 rounded-lg border border-gray-200 bg-transparent outline-none transition focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 placeholder:text-gray-400 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-100 dark:focus:ring-indigo-400/30 dark:focus:border-indigo-400 min-h-[100px] resize-y"
              placeholder={t('booking.special_requests')}
              value={formData.specialRequests}
              onChange={(e) => updateField('specialRequests', e.target.value)}
            />
          </div>
        </div>
      )}

      {/* Step 3: Payment */}
      {step === 3 && (
        <div className="space-y-6">
          <div className="bg-gray-50 dark:bg-dark-input rounded-xl p-6">
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-4">
              {t('booking.order_summary')}
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500 dark:text-gray-400">{t('booking.date')}</span>
                <span className="text-gray-900 dark:text-gray-100">{formData.date}</span>
              </div>
              {formData.time && (
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">{t('booking.time')}</span>
                  <span className="text-gray-900 dark:text-gray-100">{formData.time}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span className="text-gray-500 dark:text-gray-400">{t('booking.participants')}</span>
                <span className="text-gray-900 dark:text-gray-100">{formData.participants}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500 dark:text-gray-400">{t('booking.booker_name')}</span>
                <span className="text-gray-900 dark:text-gray-100">{formData.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500 dark:text-gray-400">{t('booking.booker_email')}</span>
                <span className="text-gray-900 dark:text-gray-100">{formData.email}</span>
              </div>
            </div>
          </div>
          <div className="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl text-center text-gray-500 dark:text-gray-400">
            Stripe Checkout Integration
          </div>
        </div>
      )}

      {/* Navigation Buttons */}
      <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-200 dark:border-gray-500/40">
        {step > 1 ? (
          <Button variant="outline" onClick={handleBack}>
            {t('common.previous')}
          </Button>
        ) : (
          <div />
        )}
        <Button onClick={handleNext} disabled={isLoading}>
          {step === 3 ? t('booking.pay_now') : t('common.next')}
        </Button>
      </div>
    </div>
  );
}
