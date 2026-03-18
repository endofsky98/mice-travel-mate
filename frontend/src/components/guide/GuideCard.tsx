'use client';

import Link from 'next/link';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { Guide } from '@/types';
import { cn, generatePlaceholderGradient, formatCurrency, getInitials } from '@/lib/utils';

interface GuideCardProps {
  guide: Guide;
  lt: (text: string | Record<string, string | undefined> | undefined | null) => string;
}

export default function GuideCard({ guide, lt }: GuideCardProps) {
  const name = lt(guide.name);

  return (
    <Link href={`/guides/${guide.id}`}>
      <Card hoverable className="h-full flex flex-col p-4">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            {guide.profile_image ? (
              <img
                src={guide.profile_image}
                alt={name}
                className="w-16 h-16 rounded-full object-cover"
              />
            ) : (
              <div
                className={cn(
                  'w-16 h-16 rounded-full bg-gradient-to-br flex items-center justify-center',
                  generatePlaceholderGradient(name)
                )}
              >
                <span className="text-white font-bold text-lg">{getInitials(name)}</span>
              </div>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 line-clamp-1 mb-1">{name}</h3>
            {guide.languages && guide.languages.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-2">
                {guide.languages.map((lang, idx) => (
                  <Badge key={idx} variant="info">
                    {lang.language}
                  </Badge>
                ))}
              </div>
            )}
            {guide.specialties && guide.specialties.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-3">
                {guide.specialties.slice(0, 3).map((spec, idx) => (
                  <Badge key={idx}>{spec}</Badge>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="mt-auto pt-3 border-t border-gray-100 dark:border-gray-500/40">
          <div className="flex items-center justify-between">
            {guide.hourly_rate && (
              <span className="text-sm font-bold text-indigo-600 dark:text-indigo-400">
                {formatCurrency(guide.hourly_rate, guide.currency)}/hr
              </span>
            )}
            {guide.regions && guide.regions.length > 0 && (
              <span className="text-xs text-gray-400 dark:text-gray-500">
                {guide.regions.join(', ')}
              </span>
            )}
          </div>
        </div>
      </Card>
    </Link>
  );
}
