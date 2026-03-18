'use client';

import Select from '@/components/ui/Select';

interface RestaurantFiltersProps {
  t: (key: string) => string;
  category: string;
  priceRange: string;
  sortBy: string;
  onCategoryChange: (value: string) => void;
  onPriceRangeChange: (value: string) => void;
  onSortChange: (value: string) => void;
}

export default function RestaurantFilters({
  t,
  category,
  priceRange,
  sortBy,
  onCategoryChange,
  onPriceRangeChange,
  onSortChange,
}: RestaurantFiltersProps) {
  const categoryOptions = [
    { value: '', label: t('restaurant.all_categories') },
    { value: 'korean', label: t('restaurant.korean') },
    { value: 'japanese', label: t('restaurant.japanese') },
    { value: 'chinese', label: t('restaurant.chinese') },
    { value: 'western', label: t('restaurant.western') },
    { value: 'fusion', label: t('restaurant.fusion') },
    { value: 'cafe', label: t('restaurant.cafe') },
    { value: 'bar', label: t('restaurant.bar') },
    { value: 'street_food', label: t('restaurant.street_food') },
  ];

  const priceOptions = [
    { value: '', label: t('common.all') },
    { value: '1', label: '$' },
    { value: '2', label: '$$' },
    { value: '3', label: '$$$' },
    { value: '4', label: '$$$$' },
  ];

  const sortOptions = [
    { value: 'distance', label: t('common.distance') },
    { value: 'name', label: t('common.name') },
    { value: 'price_low', label: t('common.price_low') },
    { value: 'price_high', label: t('common.price_high') },
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
          options={priceOptions}
          value={priceRange}
          onChange={(e) => onPriceRangeChange(e.target.value)}
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
