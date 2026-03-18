'use client';

import Link from 'next/link';
import { Clock, MapPin, Star, Footprints } from 'lucide-react';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import { Course } from '@/types';
import { cn, generatePlaceholderGradient, truncateText } from '@/lib/utils';

interface CourseCardProps {
  course: Course;
  lt: (text: string | Record<string, string | undefined> | undefined | null) => string;
}

export default function CourseCard({ course, lt }: CourseCardProps) {
  const name = lt(course.name);
  const description = lt(course.description);
  const image = course.image_url || (course.images && course.images.length > 0 ? course.images[0] : null);
  const spotCount = course.spots?.length || 0;
  const duration = course.duration_type || course.duration || '';
  const difficultyLabels: Record<string, string> = { easy: 'Easy', moderate: 'Moderate', hard: 'Active' };

  return (
    <Link href={`/courses/${course.id}`}>
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
          <div className="absolute top-3 left-3 flex gap-2">
            <Badge>{duration}</Badge>
            {course.difficulty && (
              <Badge variant="info">{difficultyLabels[course.difficulty] || course.difficulty}</Badge>
            )}
          </div>
          {course.avg_rating && course.avg_rating > 0 && (
            <div className="absolute top-3 right-3 flex items-center gap-1 bg-black/60 backdrop-blur-sm text-white text-xs px-2 py-1 rounded-lg">
              <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
              {course.avg_rating.toFixed(1)}
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
          <div className="flex items-center gap-4 text-xs text-gray-400 dark:text-gray-500">
            {spotCount > 0 && (
              <span className="flex items-center gap-1">
                <MapPin className="w-3 h-3" />
                {spotCount} spots
              </span>
            )}
            {course.total_duration_minutes && (
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {Math.round(course.total_duration_minutes / 60)}h
              </span>
            )}
            {course.review_count !== undefined && course.review_count > 0 && (
              <span>{course.review_count} reviews</span>
            )}
          </div>
        </div>
      </Card>
    </Link>
  );
}
