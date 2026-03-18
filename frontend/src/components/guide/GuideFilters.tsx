'use client';

import Select from '@/components/ui/Select';

interface GuideFiltersProps {
  t: (key: string) => string;
  language: string;
  specialty: string;
  sortBy: string;
  onLanguageChange: (value: string) => void;
  onSpecialtyChange: (value: string) => void;
  onSortChange: (value: string) => void;
}

export default function GuideFilters({
  t,
  language,
  specialty,
  sortBy,
  onLanguageChange,
  onSpecialtyChange,
  onSortChange,
}: GuideFiltersProps) {
  const languageOptions = [
    { value: '', label: t('common.all') },
    { value: 'English', label: 'English' },
    { value: 'Korean', label: 'Korean' },
    { value: 'Japanese', label: 'Japanese' },
    { value: 'Chinese', label: 'Chinese' },
    { value: 'Spanish', label: 'Spanish' },
  ];

  const specialtyOptions = [
    { value: '', label: t('common.all') },
    { value: 'culture', label: t('course.culture') },
    { value: 'food', label: t('course.food') },
    { value: 'shopping', label: t('course.shopping') },
    { value: 'history', label: t('course.history') },
    { value: 'nightlife', label: t('course.nightlife') },
  ];

  const sortOptions = [
    { value: 'recommended', label: t('common.recommended') },
    { value: 'price_low', label: t('common.price_low') },
    { value: 'price_high', label: t('common.price_high') },
  ];

  return (
    <div className="flex flex-col sm:flex-row gap-3">
      <div className="flex-1">
        <Select
          options={languageOptions}
          value={language}
          onChange={(e) => onLanguageChange(e.target.value)}
        />
      </div>
      <div className="flex-1">
        <Select
          options={specialtyOptions}
          value={specialty}
          onChange={(e) => onSpecialtyChange(e.target.value)}
        />
      </div>
      <div className="flex-1">
        <Select
          options={sortOptions}
          value={sortBy}
          onChange={(e) => onSortChange(e.target.value)}
        />
      </div>
    </div>
  );
}
