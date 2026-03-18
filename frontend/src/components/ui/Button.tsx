'use client';

import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', children, disabled, ...props }, ref) => {
    const baseClasses =
      'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';

    const variantClasses = {
      default:
        'bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500 dark:bg-indigo-500 dark:hover:bg-indigo-400',
      outline:
        'border border-gray-200 bg-white hover:bg-gray-50 text-gray-700 focus:ring-indigo-500 dark:border-gray-500/40 dark:bg-[#2a2a2a] dark:text-gray-200 dark:hover:bg-[#333]',
      ghost:
        'hover:bg-gray-100 text-gray-700 dark:text-gray-200 dark:hover:bg-white/[0.08]',
      destructive:
        'bg-red-50 text-red-600 hover:bg-red-100 focus:ring-red-500 dark:bg-red-950/40 dark:text-red-300 dark:hover:bg-red-950/60',
    };

    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm gap-1.5',
      md: 'px-4 py-2.5 text-sm gap-2',
      lg: 'px-6 py-3 text-base gap-2',
    };

    return (
      <button
        ref={ref}
        className={cn(baseClasses, variantClasses[variant], sizeClasses[size], className)}
        disabled={disabled}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
