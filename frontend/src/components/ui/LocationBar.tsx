'use client';

import { useState, useEffect } from 'react';
import { MapPin, Navigation } from 'lucide-react';

interface LocationBarProps {
  t: (key: string) => string;
  language?: string;
  onLocationChange?: (lat: number, lng: number, label: string) => void;
  eventLat?: number;
  eventLng?: number;
  eventName?: string;
}

const LANG_MAP: Record<string, string> = {
  'ko': 'ko', 'en': 'en', 'ja': 'ja',
  'zh-CN': 'zh', 'zh-TW': 'zh-TW',
  'es': 'es', 'th': 'th', 'vi': 'vi', 'fr': 'fr',
};

export default function LocationBar({ t, language = 'en', onLocationChange, eventLat, eventLng, eventName }: LocationBarProps) {
  const [locationLabel, setLocationLabel] = useState('');
  const [isLocating, setIsLocating] = useState(false);
  const [useVenue, setUseVenue] = useState(false);
  const [mapboxToken, setMapboxToken] = useState('');

  // Mapbox 토큰 로드
  useEffect(() => {
    fetch('/api/map-settings')
      .then(r => r.json())
      .then(d => { if (d.mapbox_api_key) setMapboxToken(d.mapbox_api_key); })
      .catch(() => {});
  }, []);

  useEffect(() => {
    detectLocation();
  }, []);

  const reverseGeocode = async (lat: number, lng: number): Promise<string> => {
    if (!mapboxToken) return t('home.current_location') || 'Current Location';
    try {
      const lang = LANG_MAP[language] || 'en';
      const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${lng},${lat}.json?access_token=${mapboxToken}&language=${lang}&types=address&limit=1`;
      const res = await fetch(url);
      const data = await res.json();
      if (data.features && data.features.length > 0) {
        return data.features[0].place_name;
      }
    } catch {}
    return t('home.current_location') || 'Current Location';
  };

  const detectLocation = () => {
    if (!navigator.geolocation) {
      fallbackLocation();
      return;
    }

    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;
        onLocationChange?.(latitude, longitude, '');
        const address = await reverseGeocode(latitude, longitude);
        setLocationLabel(address);
        onLocationChange?.(latitude, longitude, address);
        setIsLocating(false);
        setUseVenue(false);
      },
      () => {
        fallbackLocation();
        setIsLocating(false);
      },
      { enableHighAccuracy: false, timeout: 15000, maximumAge: 60000 }
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
    <div className="bg-white dark:bg-[#1e1e1e] border-b border-gray-100 dark:border-gray-500/40 px-4 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-2 min-w-0">
          <MapPin className="w-4 h-4 text-indigo-600 dark:text-indigo-400 flex-shrink-0" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-200 truncate">
            {isLocating ? (t('home.locating') || 'Locating...') : locationLabel}
          </span>
          <button
            onClick={detectLocation}
            className="text-xs text-indigo-600 dark:text-indigo-400 hover:underline flex-shrink-0"
            title="Refresh location"
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
