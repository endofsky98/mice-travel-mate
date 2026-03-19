'use client';

import Link from 'next/link';
import { cn } from '@/lib/utils';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  showText?: boolean;
  href?: string;
  variant?: 'default' | 'white';
}

const sizeMap = {
  sm: { full: 36, icon: 32 },
  md: { full: 44, icon: 36 },
  lg: { full: 48, icon: 40 },
  xl: { full: 56, icon: 48 },
};

export default function Logo({ size = 'md', className, showText = true, href, variant = 'default' }: LogoProps) {
  const s = sizeMap[size];

  const content = (
    <span className={cn('flex items-center gap-2', className)}>
      {showText ? (
        <>
          {/* Color logo for light mode */}
          <img
            src={variant === 'white' ? '/logo-white.svg' : '/logo.svg'}
            alt="Exporum Travel Mate"
            style={{ height: s.full }}
            className={cn(
              'w-auto flex-shrink-0 max-w-[160px] sm:max-w-none',
              variant === 'default' && 'block dark:hidden'
            )}
          />
          {/* White logo for dark mode (only when variant is default) */}
          {variant === 'default' && (
            <img
              src="/logo-white.svg"
              alt="Exporum Travel Mate"
              style={{ height: s.full }}
              className="w-auto flex-shrink-0 max-w-[160px] sm:max-w-none hidden dark:block"
            />
          )}
        </>
      ) : (
        <img
          src="/favicon.svg"
          alt="Exporum Travel Mate"
          width={s.icon}
          height={s.icon}
          className="flex-shrink-0"
        />
      )}
    </span>
  );

  if (href) {
    return <Link href={href}>{content}</Link>;
  }

  return content;
}
