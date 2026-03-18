'use client';

import Link from 'next/link';
import { Clock, Star } from 'lucide-react';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { Product } from '@/types';
import { cn, generatePlaceholderGradient, formatCurrency, truncateText } from '@/lib/utils';

interface ProductCardProps {
  product: Product;
  lt: (text: string | Record<string, string | undefined> | undefined | null) => string;
}

export default function ProductCard({ product, lt }: ProductCardProps) {
  const name = lt(product.name);
  const description = lt(product.description);
  const image = product.images && product.images.length > 0 ? product.images[0] : null;
  const price = product.price_usd || product.price || 0;

  return (
    <Link href={`/products/${product.id}`}>
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
            <Badge>{product.category}</Badge>
          </div>
          {product.avg_rating && product.avg_rating > 0 && (
            <div className="absolute top-3 right-3 flex items-center gap-1 bg-black/60 backdrop-blur-sm text-white text-xs px-2 py-1 rounded-lg">
              <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
              {product.avg_rating.toFixed(1)}
            </div>
          )}
        </div>
        <div className="p-4 flex-1 flex flex-col">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 line-clamp-1 mb-1">{name}</h3>
          {description && (
            <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-3 flex-1">
              {truncateText(description, 100)}
            </p>
          )}
          <div className="flex items-center justify-between">
            <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
              ${price}
            </span>
            <div className="flex items-center gap-2 text-xs text-gray-400">
              {(product.duration_hours || product.duration) && (
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {product.duration_hours ? `${product.duration_hours}h` : product.duration}
                </span>
              )}
              {product.review_count !== undefined && product.review_count > 0 && (
                <span>({product.review_count})</span>
              )}
            </div>
          </div>
        </div>
      </Card>
    </Link>
  );
}
