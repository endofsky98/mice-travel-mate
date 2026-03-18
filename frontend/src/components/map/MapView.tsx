'use client';

import { MapPin, ExternalLink } from 'lucide-react';
import Button from '@/components/ui/Button';
import { MapMarker } from '@/types';
import { generateGoogleMapsUrl, generateNaverMapUrl } from '@/lib/map-provider';
import { cn } from '@/lib/utils';

interface MapViewProps {
  center?: { lat: number; lng: number };
  zoom?: number;
  markers?: MapMarker[];
  polyline?: { lat: number; lng: number }[];
  className?: string;
  onMarkerClick?: (marker: MapMarker) => void;
  t: (key: string) => string;
}

export default function MapView({ center, markers = [], className, t }: MapViewProps) {
  const mainLat = center?.lat || markers[0]?.lat || 37.5665;
  const mainLng = center?.lng || markers[0]?.lng || 126.978;
  const mainTitle = markers[0]?.title || '';

  return (
    <div
      className={cn(
        'relative rounded-xl border border-gray-200 dark:border-gray-500/40 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 overflow-hidden',
        className
      )}
    >
      <div className="flex flex-col items-center justify-center py-12 px-4">
        <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mb-3">
          <MapPin className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
        </div>
        {markers.length > 0 && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
            {markers.length} {markers.length === 1 ? 'location' : 'locations'}
          </p>
        )}
        <div className="flex flex-col sm:flex-row gap-2">
          <a
            href={generateGoogleMapsUrl(mainLat, mainLng, mainTitle)}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button variant="outline" size="sm">
              <ExternalLink className="w-4 h-4" />
              {t('common.open_in_google_maps')}
            </Button>
          </a>
          <a
            href={generateNaverMapUrl(mainLat, mainLng, mainTitle)}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button variant="outline" size="sm">
              <ExternalLink className="w-4 h-4" />
              {t('common.open_in_naver_map')}
            </Button>
          </a>
        </div>
      </div>
    </div>
  );
}
