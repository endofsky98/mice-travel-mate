'use client';

import { useEffect, useRef } from 'react';
import { usePathname } from 'next/navigation';

/**
 * 페이지 이탈 시 스크롤 위치 저장, 복귀 시 복원.
 * 사용: useScrollRestore() — 복원 대상 페이지에 추가.
 */
export function useScrollRestore() {
  const pathname = usePathname();
  const scrollKey = `scroll:${pathname}`;
  const savedRef = useRef(false);

  // 복원: 페이지 마운트 후 저장된 위치로 이동
  useEffect(() => {
    if (typeof window === 'undefined') return;

    // history.state에 스크롤 위치가 있으면 복원 (뒤로가기 감지)
    const saved = sessionStorage.getItem(scrollKey);
    if (saved) {
      const { y, x } = JSON.parse(saved);
      // 데이터 로드 후 복원되도록 약간 지연
      requestAnimationFrame(() => {
        setTimeout(() => {
          window.scrollTo({ top: y, left: x, behavior: 'instant' as ScrollBehavior });
        }, 100);
      });
    }
    savedRef.current = false;

    // 이탈 시 저장
    const saveScroll = () => {
      if (!savedRef.current) {
        sessionStorage.setItem(scrollKey, JSON.stringify({ y: window.scrollY, x: window.scrollX }));
        savedRef.current = true;
      }
    };

    window.addEventListener('beforeunload', saveScroll);
    return () => {
      saveScroll();
      window.removeEventListener('beforeunload', saveScroll);
    };
  }, [scrollKey]);
}
