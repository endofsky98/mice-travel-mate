'use client';

import { cn } from '@/lib/utils';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  fullPage?: boolean;
}

export default function LoadingSpinner({ size = 'md', className, fullPage = false }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  const spinner = (
    <div
      className={cn(
        'border-2 border-gray-200 border-t-indigo-600 rounded-full animate-spin dark:border-gray-700 dark:border-t-indigo-400',
        sizeClasses[size],
        className
      )}
    />
  );

  if (fullPage) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        {spinner}
      </div>
    );
  }

  return spinner;
}
