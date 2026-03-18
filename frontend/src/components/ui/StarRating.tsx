'use client';

import { Star } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StarRatingProps {
  rating: number;
  size?: 'sm' | 'md' | 'lg';
  interactive?: boolean;
  onChange?: (rating: number) => void;
  showValue?: boolean;
  reviewCount?: number;
}

export default function StarRating({
  rating,
  size = 'sm',
  interactive = false,
  onChange,
  showValue = false,
  reviewCount,
}: StarRatingProps) {
  const sizeMap = { sm: 'w-3.5 h-3.5', md: 'w-5 h-5', lg: 'w-6 h-6' };
  const iconSize = sizeMap[size];

  return (
    <div className="flex items-center gap-1">
      <div className="flex">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            disabled={!interactive}
            onClick={() => interactive && onChange?.(star)}
            className={cn(
              'transition-colors',
              interactive ? 'cursor-pointer hover:scale-110' : 'cursor-default'
            )}
          >
            <Star
              className={cn(
                iconSize,
                star <= Math.round(rating)
                  ? 'fill-amber-400 text-amber-400'
                  : 'fill-gray-200 text-gray-200 dark:fill-gray-600 dark:text-gray-600'
              )}
            />
          </button>
        ))}
      </div>
      {showValue && (
        <span className={cn(
          'font-medium text-gray-700 dark:text-gray-300',
          size === 'sm' ? 'text-xs' : size === 'md' ? 'text-sm' : 'text-base'
        )}>
          {rating > 0 ? rating.toFixed(1) : '-'}
        </span>
      )}
      {reviewCount !== undefined && (
        <span className="text-xs text-gray-400">({reviewCount})</span>
      )}
    </div>
  );
}
