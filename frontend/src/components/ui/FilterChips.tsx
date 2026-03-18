'use client';

import { cn } from '@/lib/utils';

interface FilterChip {
  key: string;
  label: string;
}

interface FilterChipsProps {
  chips: FilterChip[];
  selected: string;
  onSelect: (key: string) => void;
  className?: string;
}

export default function FilterChips({ chips, selected, onSelect, className }: FilterChipsProps) {
  return (
    <div className={cn('flex gap-2 overflow-x-auto scrollbar-hide pb-1', className)}>
      {chips.map((chip) => (
        <button
          key={chip.key}
          onClick={() => onSelect(chip.key === selected ? '' : chip.key)}
          className={cn(
            'px-3 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors flex-shrink-0',
            chip.key === selected
              ? 'bg-indigo-600 text-white dark:bg-indigo-500'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-[#2a2a2a] dark:text-gray-300 dark:hover:bg-gray-700'
          )}
        >
          {chip.label}
        </button>
      ))}
    </div>
  );
}
