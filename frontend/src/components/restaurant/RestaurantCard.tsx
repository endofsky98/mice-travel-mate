'use client';

import Link from 'next/link';
import { MapPin } from 'lucide-react';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { Restaurant } from '@/types';
import { cn, generatePlaceholderGradient, getPriceRangeSymbol, truncateText } from '@/lib/utils';

interface RestaurantCardProps {
  restaurant: Restaurant;
  lt: (text: string | Record<string, string | undefined> | undefined | null) => string;
}

export default function RestaurantCard({ restaurant, lt }: RestaurantCardProps) {
  const name = lt(restaurant.name);
  const description = lt(restaurant.description);
  const image = restaurant.images && restaurant.images.length > 0 ? restaurant.images[0] : null;

  return (
    <Link href={`/restaurants/${restaurant.id}`}>
      <Card hoverable className="h-full flex flex-col">
        <div className="relative aspect-[4/3] overflow-hidden">
          {image ? (
            <img src={image} alt={name} className="w-full h-full object-cover" />
          ) : (
            <div
              className={cn(
                'w-full h-full bg-gradient-to-br flex items-center justify-center',
                generatePlaceholderGradient(name)
              )}
            >
              <span className="text-white/80 text-xl font-bold">{name.charAt(0)}</span>
            </div>
          )}
          <div className="absolute top-3 left-3">
            <Badge>{restaurant.category}</Badge>
          </div>
        </div>
        <div className="p-4 flex-1 flex flex-col">
          <div className="flex items-start justify-between gap-2 mb-1">
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 line-clamp-1">{name}</h3>
            <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400 whitespace-nowrap">
              {getPriceRangeSymbol(restaurant.price_range)}
            </span>
          </div>
          {description && (
            <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-3 flex-1">
              {truncateText(description, 100)}
            </p>
          )}
          {restaurant.distance_from_venue !== undefined && restaurant.distance_from_venue !== null && (
            <div className="flex items-center gap-1 text-xs text-gray-400 dark:text-gray-500">
              <MapPin className="w-3 h-3" />
              <span>{restaurant.distance_from_venue}m</span>
            </div>
          )}
        </div>
      </Card>
    </Link>
  );
}
