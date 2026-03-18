'use client';

import { useState, useEffect } from 'react';
import { MapPin, Navigation, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LocationBarProps {
  t: (key: string) => string;
  onLocationChange?: (lat: number, lng: number, label: string) => void;
  eventLat?: number;
  eventLng?: number;
  eventName?: string;
}

export default function LocationBar({ t, onLocationChange, eventLat, eventLng, eventName }: LocationBarProps) {
  const [locationLabel, setLocationLabel] = useState('');
  const [isLocating, setIsLocating] = useState(false);
  const [useVenue, setUseVenue] = useState(false);

  useEffect(() => {
    detectLocation();
  }, []);

  const detectLocation = () => {
    if (!navigator.geolocation) {
      fallbackLocation();
      return;
    }

    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const label = t('home.location_nearby') || 'Nearby';
        setLocationLabel(label);
        onLocationChange?.(pos.coords.latitude, pos.coords.longitude, label);
        setIsLocating(false);
        setUseVenue(false);
      },
      () => {
        fallbackLocation();
        setIsLocating(false);
      },
      { timeout: 5000 }
    );
  };

  const fallbackLocation = () => {
    if (eventLat && eventLng && eventName) {
      setLocationLabel(eventName);
      onLocationChange?.(eventLat, eventLng, eventName);
      setUseVenue(true);
    } else {
      const label = 'Seoul';
      setLocationLabel(label);
      onLocationChange?.(37.5665, 126.978, label);
    }
  };

  const switchToVenue = () => {
    if (eventLat && eventLng && eventName) {
      setLocationLabel(eventName);
      onLocationChange?.(eventLat, eventLng, eventName);
      setUseVenue(true);
    }
  };

  return (
    <div className="bg-white dark:bg-[#1e1e1e] border-b border-gray-100 dark:border-gray-500/40 px-4 py-2.5">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-2 min-w-0">
          <MapPin className="w-4 h-4 text-indigo-600 dark:text-indigo-400 flex-shrink-0" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-200 truncate">
            {isLocating ? '...' : locationLabel}
          </span>
          <button
            onClick={detectLocation}
            className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline flex-shrink-0"
          >
            <Navigation className="w-3.5 h-3.5" />
          </button>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          {eventName && !useVenue && (
            <button
              onClick={switchToVenue}
              className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline whitespace-nowrap"
            >
              {t('home.venue_based') || 'Venue-based'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
