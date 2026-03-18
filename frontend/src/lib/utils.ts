import { clsx, type ClassValue } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatCurrency(amount: number, currency: string = 'KRW'): string {
  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
      minimumFractionDigits: currency === 'KRW' ? 0 : 2,
      maximumFractionDigits: currency === 'KRW' ? 0 : 2,
    }).format(amount);
  } catch {
    return `${currency} ${amount.toLocaleString()}`;
  }
}

export function formatDate(dateStr: string, locale: string = 'en'): string {
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString(locale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  } catch {
    return dateStr;
  }
}

export function formatDateShort(dateStr: string): string {
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en', {
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return dateStr;
  }
}

export function formatDateRange(startDate: string, endDate: string): string {
  return `${formatDateShort(startDate)} - ${formatDateShort(endDate)}`;
}

export function getPriceRangeSymbol(range: number): string {
  return '$'.repeat(Math.max(1, Math.min(4, range)));
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
}

export function generatePlaceholderGradient(seed: string | number): string {
  const gradients = [
    'from-indigo-500 to-purple-600',
    'from-blue-500 to-teal-500',
    'from-rose-500 to-orange-500',
    'from-emerald-500 to-cyan-500',
    'from-violet-500 to-fuchsia-500',
    'from-amber-500 to-red-500',
    'from-teal-500 to-blue-600',
    'from-pink-500 to-rose-600',
  ];
  const index = typeof seed === 'number' ? seed : hashString(seed);
  return gradients[Math.abs(index) % gradients.length];
}

function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0;
  }
  return hash;
}

export function debounce<T extends (...args: unknown[]) => unknown>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export function getInitials(name: string): string {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
}
