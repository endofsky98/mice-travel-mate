'use client';

import { useRef, useEffect, useCallback } from 'react';

/**
 * 가로 드래그 스크롤 + 3초마다 2개씩 자동 스크롤
 * @param itemWidth 카드 1개 너비(px) + gap
 * @param autoScrollItems 한 번에 스크롤할 카드 수 (기본 2)
 * @param autoScrollInterval 자동 스크롤 간격 ms (기본 3000)
 */
export function useDragScroll(
  itemWidth = 276,
  autoScrollItems = 2,
  autoScrollInterval = 3000
) {
  const ref = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);
  const startX = useRef(0);
  const scrollLeft = useRef(0);
  const autoTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const userInteracting = useRef(false);
  const interactTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const pauseAuto = useCallback(() => {
    userInteracting.current = true;
    if (interactTimer.current) clearTimeout(interactTimer.current);
    interactTimer.current = setTimeout(() => {
      userInteracting.current = false;
    }, 5000); // 사용자 조작 후 5초 뒤 자동 재개
  }, []);

  // 드래그 이벤트
  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const onMouseDown = (e: MouseEvent) => {
      isDragging.current = true;
      startX.current = e.pageX - el.offsetLeft;
      scrollLeft.current = el.scrollLeft;
      el.style.cursor = 'grabbing';
      el.style.userSelect = 'none';
      pauseAuto();
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging.current) return;
      e.preventDefault();
      const x = e.pageX - el.offsetLeft;
      const walk = (x - startX.current) * 1.2;
      el.scrollLeft = scrollLeft.current - walk;
    };

    const onMouseUp = () => {
      isDragging.current = false;
      el.style.cursor = 'grab';
      el.style.userSelect = '';
    };

    const onTouchStart = (e: TouchEvent) => {
      startX.current = e.touches[0].pageX - el.offsetLeft;
      scrollLeft.current = el.scrollLeft;
      pauseAuto();
    };

    const onTouchMove = (e: TouchEvent) => {
      const x = e.touches[0].pageX - el.offsetLeft;
      const walk = (x - startX.current) * 1;
      el.scrollLeft = scrollLeft.current - walk;
    };

    el.style.cursor = 'grab';
    el.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    el.addEventListener('touchstart', onTouchStart, { passive: true });
    el.addEventListener('touchmove', onTouchMove, { passive: true });

    return () => {
      el.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      el.removeEventListener('touchstart', onTouchStart);
      el.removeEventListener('touchmove', onTouchMove);
    };
  }, [pauseAuto]);

  // 자동 스크롤
  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    autoTimer.current = setInterval(() => {
      if (userInteracting.current) return;
      const scrollAmount = itemWidth * autoScrollItems;
      const maxScroll = el.scrollWidth - el.clientWidth;

      if (el.scrollLeft + scrollAmount >= maxScroll) {
        // 끝에 도달하면 처음으로
        el.scrollTo({ left: 0, behavior: 'smooth' });
      } else {
        el.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      }
    }, autoScrollInterval);

    return () => {
      if (autoTimer.current) clearInterval(autoTimer.current);
    };
  }, [itemWidth, autoScrollItems, autoScrollInterval]);

  return ref;
}
