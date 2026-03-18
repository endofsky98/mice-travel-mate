'use client';

import Link from 'next/link';
import { Clock, MapPin } from 'lucide-react';
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
  const image = course.images && course.images.length > 0 ? course.images[0] : null;
  const spotCount = course.spots?.length || 0;

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
            <Badge>{course.duration}</Badge>
          </div>
        </div>
        <div className="p-4 flex-1 flex flex-col">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 line-clamp-1 mb-1">{name}</h3>
          {description && (
            <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2 mb-3 flex-1">
              {truncateText(description, 100)}
            </p>
          )}
          <div className="flex items-center gap-4 text-xs text-gray-400 dark:text-gray-500">
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {spotCount} spots
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {course.duration}
            </span>
          </div>
        </div>
      </Card>
    </Link>
  );
}
