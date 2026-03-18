'use client';

import Select from '@/components/ui/Select';

interface ProductFiltersProps {
  t: (key: string) => string;
  category: string;
  sortBy: string;
  onCategoryChange: (value: string) => void;
  onSortChange: (value: string) => void;
}

export default function ProductFilters({
  t,
  category,
  sortBy,
  onCategoryChange,
  onSortChange,
}: ProductFiltersProps) {
  const categoryOptions = [
    { value: '', label: t('common.all') },
    { value: 'tour', label: t('product.tour') },
    { value: 'experience', label: t('product.experience') },
    { value: 'class', label: t('product.class') },
    { value: 'ticket', label: t('product.ticket') },
    { value: 'package', label: t('product.package') },
  ];

  const sortOptions = [
    { value: 'recommended', label: t('common.recommended') },
    { value: 'popular', label: t('common.popular') },
    { value: 'price_low', label: t('common.price_low') },
    { value: 'price_high', label: t('common.price_high') },
    { value: 'newest', label: t('common.newest') },
  ];

  return (
    <div className="flex flex-col sm:flex-row gap-3">
      <div className="flex-1">
        <Select
          options={categoryOptions}
          value={category}
          onChange={(e) => onCategoryChange(e.target.value)}
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
