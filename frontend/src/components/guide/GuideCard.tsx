'use client';

import Link from 'next/link';
import { Star } from 'lucide-react';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { Guide } from '@/types';
import { cn, generatePlaceholderGradient, getInitials } from '@/lib/utils';

interface GuideCardProps {
  guide: Guide;
  lt: (text: string | Record<string, string | undefined> | undefined | null) => string;
}

export default function GuideCard({ guide, lt }: GuideCardProps) {
  const name = lt(guide.name);
  const profileImage = guide.profile_image || guide.profile_image_url;
  const hourlyRate = guide.hourly_rate || guide.price_per_hour_usd;

  return (
    <Link href={`/guides/${guide.id}`}>
      <Card hoverable className="h-full flex flex-col p-4">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">
            {profileImage ? (
              <img
                src={profileImage}
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
            {/* Rating */}
            {guide.avg_rating && guide.avg_rating > 0 && (
              <div className="flex items-center gap-1 mb-2">
                <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                <span className="text-xs font-medium text-gray-700 dark:text-gray-300">{guide.avg_rating.toFixed(1)}</span>
                {guide.review_count !== undefined && guide.review_count > 0 && (
                  <span className="text-xs text-gray-400">({guide.review_count})</span>
                )}
              </div>
            )}
            {guide.languages && guide.languages.length > 0 && (
              <div className="flex flex-wrap gap-1 mb-2">
                {guide.languages.map((lang, idx) => (
                  <Badge key={idx} variant="info">
                    {lang.language}
                    {lang.proficiency && lang.proficiency !== 'native' && (
                      <span className="text-[9px] opacity-70 ml-0.5">
                        ({lang.proficiency === 'fluent' ? 'F' : lang.proficiency === 'intermediate' ? 'I' : 'B'})
                      </span>
                    )}
                  </Badge>
                ))}
              </div>
            )}
            {guide.specialties && guide.specialties.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {guide.specialties.slice(0, 3).map((spec, idx) => (
                  <Badge key={idx}>{spec}</Badge>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="mt-auto pt-3 border-t border-gray-100 dark:border-gray-500/40">
          <div className="flex items-center justify-between">
            {hourlyRate && (
              <span className="text-sm font-bold text-indigo-600 dark:text-indigo-400">
                ${Number(hourlyRate).toFixed(0)}/hr
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
