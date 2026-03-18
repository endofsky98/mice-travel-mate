'use client';

import { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn, generatePlaceholderGradient } from '@/lib/utils';

interface ImageGalleryProps {
  images: string[];
  alt?: string;
  className?: string;
}

export default function ImageGallery({ images, alt = 'Image', className }: ImageGalleryProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const hasImages = images && images.length > 0;
  const displayImages = hasImages ? images : ['placeholder'];

  const goNext = () => {
    setCurrentIndex((prev) => (prev + 1) % displayImages.length);
  };

  const goPrev = () => {
    setCurrentIndex((prev) => (prev - 1 + displayImages.length) % displayImages.length);
  };

  return (
    <div className={cn('relative overflow-hidden rounded-xl', className)}>
      <div className="relative aspect-[16/9]">
        {hasImages ? (
          <img
            src={displayImages[currentIndex]}
            alt={`${alt} ${currentIndex + 1}`}
            className="w-full h-full object-cover"
          />
        ) : (
          <div
            className={cn(
              'w-full h-full bg-gradient-to-br flex items-center justify-center',
              generatePlaceholderGradient(alt)
            )}
          >
            <span className="text-white/80 text-lg font-medium">{alt}</span>
          </div>
        )}
      </div>

      {displayImages.length > 1 && (
        <>
          <button
            onClick={goPrev}
            className="absolute left-2 top-1/2 -translate-y-1/2 p-1.5 rounded-full bg-white/80 dark:bg-black/50 shadow-sm hover:bg-white dark:hover:bg-black/70 transition"
          >
            <ChevronLeft className="w-5 h-5 text-gray-700 dark:text-gray-200" />
          </button>
          <button
            onClick={goNext}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded-full bg-white/80 dark:bg-black/50 shadow-sm hover:bg-white dark:hover:bg-black/70 transition"
          >
            <ChevronRight className="w-5 h-5 text-gray-700 dark:text-gray-200" />
          </button>
          <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-1.5">
            {displayImages.map((_, idx) => (
              <button
                key={idx}
                onClick={() => setCurrentIndex(idx)}
                className={cn(
                  'w-2 h-2 rounded-full transition',
                  idx === currentIndex ? 'bg-white' : 'bg-white/50'
                )}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
