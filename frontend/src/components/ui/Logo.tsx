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

function LogoIcon({ size, variant = 'default' }: { size: number; variant?: 'default' | 'white' }) {
  const primary = variant === 'white' ? '#ffffff' : '#4f46e5';
  const accent = variant === 'white' ? 'rgba(255,255,255,0.7)' : '#818cf8';
  return (
    <svg width={size} height={size} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Globe circle */}
      <circle cx="24" cy="24" r="20" stroke={primary} strokeWidth="2.5" fill="none" />
      {/* Latitude lines */}
      <ellipse cx="24" cy="24" rx="12" ry="20" stroke={accent} strokeWidth="1.5" fill="none" />
      <line x1="4" y1="18" x2="44" y2="18" stroke={accent} strokeWidth="1.5" />
      <line x1="4" y1="30" x2="44" y2="30" stroke={accent} strokeWidth="1.5" />
      {/* Location pin */}
      <g transform="translate(24, 13)">
        <path d="M0 0C-4.5 0 -8 3.5 -8 8C-8 14 0 22 0 22C0 22 8 14 8 8C8 3.5 4.5 0 0 0Z" fill={primary} />
        <circle cx="0" cy="8" r="3" fill="white" />
      </g>
      {/* Airplane */}
      <g transform="translate(36, 10) rotate(30)">
        <path d="M0 -5L2 0L8 2L2 3L0 8L-2 3L-8 2L-2 0Z" fill={primary} opacity="0.8" />
      </g>
    </svg>
  );
}

const sizeMap = {
  sm: { icon: 24, text: 'text-sm' },
  md: { icon: 28, text: 'text-base' },
  lg: { icon: 36, text: 'text-xl' },
  xl: { icon: 48, text: 'text-2xl' },
};

export default function Logo({ size = 'md', className, showText = true, href, variant = 'default' }: LogoProps) {
  const s = sizeMap[size];
  const textColor = variant === 'white' ? 'text-white' : 'text-gray-900 dark:text-white';

  const content = (
    <span className={cn('flex items-center gap-2', className)}>
      <LogoIcon size={s.icon} variant={variant} />
      {showText && (
        <span className={cn('font-bold tracking-tight', s.text, textColor)}>
          Exporum <span className="font-normal text-indigo-600 dark:text-indigo-400">{variant === 'white' ? <span className="text-white/80">Travel Mate</span> : 'Travel Mate'}</span>
        </span>
      )}
    </span>
  );

  if (href) {
    return <Link href={href}>{content}</Link>;
  }

  return content;
}
