'use client';

import Link from 'next/link';
import Image from 'next/image';
import { cn } from '@/lib/utils';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  showText?: boolean;
  href?: string;
  variant?: 'default' | 'white';
}

const sizeMap = {
  sm: { icon: 28, text: 'text-sm' },
  md: { icon: 32, text: 'text-base' },
  lg: { icon: 40, text: 'text-xl' },
  xl: { icon: 52, text: 'text-2xl' },
};

export default function Logo({ size = 'md', className, showText = true, href, variant = 'default' }: LogoProps) {
  const s = sizeMap[size];
  const textColor = variant === 'white' ? 'text-white' : 'text-gray-900 dark:text-white';

  const content = (
    <span className={cn('flex items-center gap-2', className)}>
      <Image
        src="/logo.svg"
        alt="Exporum Travel Mate"
        width={s.icon}
        height={s.icon}
        className={cn('flex-shrink-0', variant === 'white' && 'brightness-0 invert')}
        priority
      />
      {showText && (
        <span className={cn('font-bold tracking-tight', s.text, textColor)}>
          Exporum{' '}
          <span className={cn('font-normal', variant === 'white' ? 'text-white/80' : 'text-indigo-600 dark:text-indigo-400')}>
            Travel Mate
          </span>
        </span>
      )}
    </span>
  );

  if (href) {
    return <Link href={href}>{content}</Link>;
  }

  return content;
}
