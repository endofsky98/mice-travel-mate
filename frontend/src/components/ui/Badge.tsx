'use client';

import { HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
}

export default function Badge({ className, variant = 'default', children, ...props }: BadgeProps) {
  const variantClasses = {
    default: 'bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300',
    success: 'bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300',
    warning: 'bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
    error: 'bg-red-50 text-red-700 dark:bg-red-900/30 dark:text-red-300',
    info: 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
