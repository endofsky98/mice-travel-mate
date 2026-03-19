'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import Link from 'next/link';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { RollingBanner as BannerType, BannerTransitionType } from '@/types';
import { cn } from '@/lib/utils';

interface RollingBannerProps {
  banners: BannerType[];
  lt: (text: any) => string;
  interval?: number;
}

export default function RollingBanner({ banners, lt, interval = 4000 }: RollingBannerProps) {
  const [current, setCurrent] = useState(0);
  const [prev, setPrev] = useState<number | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [direction, setDirection] = useState<'next' | 'prev'>('next');
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);
  const touchStartX = useRef(0);
  const touchEndX = useRef(0);
  const mouseStartX = useRef(0);
  const isDragging = useRef(false);

  const transitionType: BannerTransitionType = banners[current]?.transition_type || 'slide';

  const goTo = useCallback((index: number, dir?: 'next' | 'prev') => {
    if (isAnimating || banners.length <= 1) return;
    const newIndex = (index + banners.length) % banners.length;
    if (newIndex === current) return;
    setDirection(dir || (newIndex > current ? 'next' : 'prev'));
    setPrev(current);
    setCurrent(newIndex);
    setIsAnimating(true);
    setTimeout(() => {
      setPrev(null);
      setIsAnimating(false);
    }, 700);
  }, [current, banners.length, isAnimating]);

  const goNext = useCallback(() => goTo(current + 1, 'next'), [current, goTo]);
  const goPrev = useCallback(() => goTo(current - 1, 'prev'), [current, goTo]);

  useEffect(() => {
    if (!isAutoPlaying || banners.length <= 1) return;
    const timer = setInterval(goNext, interval);
    return () => clearInterval(timer);
  }, [isAutoPlaying, goNext, interval, banners.length]);

  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
    setIsAutoPlaying(false);
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    touchEndX.current = e.changedTouches[0].clientX;
    const diff = touchStartX.current - touchEndX.current;
    if (Math.abs(diff) > 50) {
      diff > 0 ? goNext() : goPrev();
    }
    setTimeout(() => setIsAutoPlaying(true), 5000);
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    mouseStartX.current = e.clientX;
    isDragging.current = true;
    setIsAutoPlaying(false);
  };

  const handleMouseUp = (e: React.MouseEvent) => {
    if (!isDragging.current) return;
    isDragging.current = false;
    const diff = mouseStartX.current - e.clientX;
    if (Math.abs(diff) > 50) {
      diff > 0 ? goNext() : goPrev();
    }
    setTimeout(() => setIsAutoPlaying(true), 5000);
  };

  const handleMouseLeave = (e: React.MouseEvent) => {
    if (!isDragging.current) return;
    isDragging.current = false;
    const diff = mouseStartX.current - e.clientX;
    if (Math.abs(diff) > 50) {
      diff > 0 ? goNext() : goPrev();
    }
    setTimeout(() => setIsAutoPlaying(true), 5000);
  };

  if (!banners.length) return null;

  const renderBannerContent = (banner: BannerType, isActive: boolean) => {
    const title = lt(banner.title);
    const subtitle = lt(banner.subtitle);

    const inner = (
      <>
        <h2 className="text-2xl md:text-4xl font-bold text-white mb-2 drop-shadow-lg">
          {title}
        </h2>
        <p className="text-base md:text-lg text-white/90 max-w-xl drop-shadow">
          {subtitle}
        </p>
      </>
    );

    if (banner.link_url) {
      return (
        <Link href={banner.link_url} className="relative h-full flex flex-col justify-end p-6 md:p-12 max-w-7xl mx-auto cursor-pointer">
          {inner}
        </Link>
      );
    }
    return (
      <div className="relative h-full flex flex-col justify-end p-6 md:p-12 max-w-7xl mx-auto">
        {inner}
      </div>
    );
  };

  const getSlideStyle = (index: number, isCurrentSlide: boolean): React.CSSProperties => {
    const tt = transitionType;

    if (tt === 'fade') {
      return {
        position: 'absolute',
        inset: 0,
        opacity: isCurrentSlide ? 1 : 0,
        transition: 'opacity 0.7s ease-in-out',
        zIndex: isCurrentSlide ? 2 : 1,
      };
    }

    if (tt === 'zoom') {
      return {
        position: 'absolute',
        inset: 0,
        opacity: isCurrentSlide ? 1 : 0,
        transform: isCurrentSlide ? 'scale(1)' : 'scale(1.15)',
        transition: 'opacity 0.7s ease-in-out, transform 0.7s ease-in-out',
        zIndex: isCurrentSlide ? 2 : 1,
      };
    }

    if (tt === 'flip') {
      return {
        position: 'absolute',
        inset: 0,
        opacity: isCurrentSlide ? 1 : 0,
        transform: isCurrentSlide ? 'perspective(1200px) rotateY(0deg)' : `perspective(1200px) rotateY(${direction === 'next' ? '-90' : '90'}deg)`,
        transition: 'opacity 0.7s ease-in-out, transform 0.7s ease-in-out',
        zIndex: isCurrentSlide ? 2 : 1,
        backfaceVisibility: 'hidden' as const,
      };
    }

    // slide (default)
    if (isCurrentSlide) {
      return {
        position: 'absolute',
        inset: 0,
        transform: isAnimating
          ? 'translateX(0)'
          : 'translateX(0)',
        transition: 'transform 0.7s ease-in-out',
        zIndex: 2,
      };
    }
    // prev slide exiting
    return {
      position: 'absolute',
      inset: 0,
      transform: direction === 'next' ? 'translateX(-100%)' : 'translateX(100%)',
      transition: 'transform 0.7s ease-in-out',
      zIndex: 1,
    };
  };

  const getSlideEnterStyle = (): React.CSSProperties => {
    if (transitionType === 'slide' && isAnimating) {
      return {
        position: 'absolute',
        inset: 0,
        transform: 'translateX(0)',
        transition: 'transform 0.7s ease-in-out',
        zIndex: 2,
      };
    }
    return {};
  };

  // For slide transition, we need a different approach
  const renderSlideTransition = () => {
    if (transitionType === 'slide') {
      return (
        <div className="absolute inset-0 overflow-hidden">
          {/* Previous banner (sliding out) */}
          {prev !== null && (
            <div
              style={{
                position: 'absolute',
                inset: 0,
                transform: direction === 'next' ? 'translateX(-100%)' : 'translateX(100%)',
                transition: 'transform 0.7s ease-in-out',
                zIndex: 1,
              }}
            >
              <div
                className="absolute inset-0 bg-cover bg-center"
                style={{ backgroundImage: `url(${banners[prev].image_url})` }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
              {renderBannerContent(banners[prev], false)}
            </div>
          )}
          {/* Current banner (sliding in) */}
          <div
            style={{
              position: 'absolute',
              inset: 0,
              transform: 'translateX(0)',
              transition: isAnimating ? 'transform 0.7s ease-in-out' : 'none',
              zIndex: 2,
            }}
          >
            <div
              className="absolute inset-0 bg-cover bg-center"
              style={{ backgroundImage: `url(${banners[current].image_url})` }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
            {renderBannerContent(banners[current], true)}
          </div>
        </div>
      );
    }

    // For fade, zoom, flip - render all banners with CSS transitions
    return (
      <div className="absolute inset-0" style={{ perspective: '1200px' }}>
        {banners.map((banner, i) => {
          const isActive = i === current;
          return (
            <div key={banner.id || i} style={getSlideStyle(i, isActive)}>
              <div
                className="absolute inset-0 bg-cover bg-center"
                style={{ backgroundImage: `url(${banner.image_url})` }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
              {renderBannerContent(banner, isActive)}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div
      className="relative w-full h-[280px] md:h-[480px] lg:h-[560px] overflow-hidden cursor-grab active:cursor-grabbing select-none"
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseLeave}
      onMouseEnter={() => setIsAutoPlaying(false)}
      onMouseLeave={() => setIsAutoPlaying(true)}
    >
      {renderSlideTransition()}

      {/* Navigation Arrows */}
      {banners.length > 1 && (
        <>
          <button
            onClick={goPrev}
            className="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center text-white hover:bg-black/50 transition-colors hidden md:flex z-10"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button
            onClick={goNext}
            className="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center text-white hover:bg-black/50 transition-colors hidden md:flex z-10"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </>
      )}

      {/* Indicators */}
      {banners.length > 1 && (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-10">
          {banners.map((_, i) => (
            <button
              key={i}
              onClick={() => goTo(i)}
              className={cn(
                'w-2 h-2 rounded-full transition-all',
                i === current ? 'bg-white w-6' : 'bg-white/50 hover:bg-white/70'
              )}
            />
          ))}
        </div>
      )}
    </div>
  );
}
