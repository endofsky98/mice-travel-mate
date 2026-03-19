'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

export function useScrollRestore() {
  const pathname = usePathname();
  const scrollKey = `scroll:${pathname}`;

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // 복원
    const saved = sessionStorage.getItem(scrollKey);
    if (saved) {
      const { y, horizontals } = JSON.parse(saved);
      setTimeout(() => {
        window.scrollTo({ top: y, behavior: 'instant' as ScrollBehavior });
        // 가로 스크롤 복원
        if (horizontals) {
          Object.entries(horizontals).forEach(([idx, left]) => {
            const els = document.querySelectorAll('.overflow-x-auto');
            const el = els[Number(idx)] as HTMLElement;
            if (el) el.scrollLeft = left as number;
          });
        }
      }, 150);
    }

    // 이탈 시 저장
    const saveScroll = () => {
      const horizontals: Record<number, number> = {};
      document.querySelectorAll('.overflow-x-auto').forEach((el, i) => {
        if ((el as HTMLElement).scrollLeft > 0) {
          horizontals[i] = (el as HTMLElement).scrollLeft;
        }
      });
      sessionStorage.setItem(scrollKey, JSON.stringify({
        y: window.scrollY,
        horizontals,
      }));
    };

    window.addEventListener('beforeunload', saveScroll);
    // Next.js Link 클릭 시 beforeunload 안 뜨므로 pagehide도 등록
    window.addEventListener('pagehide', saveScroll);

    return () => {
      saveScroll();
      window.removeEventListener('beforeunload', saveScroll);
      window.removeEventListener('pagehide', saveScroll);
    };
  }, [scrollKey]);
}
