'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { MapPin, ExternalLink } from 'lucide-react';
import Button from '@/components/ui/Button';
import { MapMarker } from '@/types';
import { generateGoogleMapsUrl, generateNaverMapUrl } from '@/lib/map-provider';
import { cn } from '@/lib/utils';
import api from '@/lib/api';

interface MapViewProps {
  center?: { lat: number; lng: number };
  zoom?: number;
  markers?: MapMarker[];
  polyline?: { lat: number; lng: number }[];
  className?: string;
  onMarkerClick?: (marker: MapMarker) => void;
  t: (key: string) => string;
}

interface MapSettingsResponse {
  map_engine: string;
  mapbox_api_key: string;
  google_maps_api_key: string;
  default_center_lat: number;
  default_center_lng: number;
  default_zoom: number;
}

let googleMapsLoadPromise: Promise<void> | null = null;

function loadGoogleMapsScript(apiKey: string): Promise<void> {
  if (googleMapsLoadPromise) return googleMapsLoadPromise;
  if (typeof window !== 'undefined' && (window as any).google?.maps) {
    return Promise.resolve();
  }
  googleMapsLoadPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=marker`;
    script.async = true;
    script.defer = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Google Maps'));
    document.head.appendChild(script);
  });
  return googleMapsLoadPromise;
}

export default function MapView({ center, zoom, markers = [], polyline, className, onMarkerClick, t }: MapViewProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const [mapEngine, setMapEngine] = useState<string | null>(null);
  const [mapboxToken, setMapboxToken] = useState<string | null>(null);
  const [googleApiKey, setGoogleApiKey] = useState<string | null>(null);
  const [settingsLoaded, setSettingsLoaded] = useState(false);

  const mainLat = center?.lat || markers[0]?.lat || 37.5665;
  const mainLng = center?.lng || markers[0]?.lng || 126.978;
  const mainTitle = markers[0]?.title || '';

  // Load map settings
  useEffect(() => {
    const loadSettings = async () => {
      // Try env var first for mapbox
      const envToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;

      try {
        const settings = await api.get<MapSettingsResponse>('/api/map-settings');
        const engine = settings.map_engine || 'mapbox';
        setMapEngine(engine);

        if (engine === 'google' && settings.google_maps_api_key) {
          setGoogleApiKey(settings.google_maps_api_key);
        } else if (engine === 'mapbox') {
          const token = settings.mapbox_api_key && settings.mapbox_api_key !== 'pk.placeholder'
            ? settings.mapbox_api_key
            : (envToken && envToken !== 'pk.placeholder' ? envToken : null);
          setMapboxToken(token);
        }
      } catch {
        // Fallback to env var
        if (envToken && envToken !== 'pk.placeholder') {
          setMapEngine('mapbox');
          setMapboxToken(envToken);
        }
      }
      setSettingsLoaded(true);
    };
    loadSettings();
  }, []);

  // Initialize Mapbox
  useEffect(() => {
    if (!settingsLoaded || mapEngine !== 'mapbox' || !mapboxToken || !mapContainerRef.current) return;

    let map: any;
    const initMap = async () => {
      try {
        const mapboxgl = (await import('mapbox-gl')).default;

        if (!document.getElementById('mapbox-gl-css')) {
          const link = document.createElement('link');
          link.id = 'mapbox-gl-css';
          link.rel = 'stylesheet';
          link.href = 'https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.css';
          document.head.appendChild(link);
        }

        (mapboxgl as any).accessToken = mapboxToken;

        map = new mapboxgl.Map({
          container: mapContainerRef.current!,
          style: 'mapbox://styles/mapbox/streets-v12',
          center: [mainLng, mainLat],
          zoom: zoom || 13,
        });

        map.addControl(new mapboxgl.NavigationControl(), 'top-right');

        markers.forEach((marker) => {
          const el = document.createElement('div');
          el.className = 'mapbox-custom-marker';
          el.style.cssText = 'width:32px;height:32px;background:#4f46e5;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);cursor:pointer;display:flex;align-items:center;justify-content:center;';
          el.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>';

          const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
            `<div style="padding:4px 8px;"><strong style="font-size:14px;">${marker.title || ''}</strong>${marker.description ? `<p style="font-size:12px;color:#666;margin-top:4px;">${marker.description}</p>` : ''}</div>`
          );

          new mapboxgl.Marker(el)
            .setLngLat([marker.lng, marker.lat])
            .setPopup(popup)
            .addTo(map);

          if (onMarkerClick) {
            el.addEventListener('click', () => onMarkerClick(marker));
          }
        });

        if (polyline && polyline.length > 1) {
          map.on('load', () => {
            map.addSource('route', {
              type: 'geojson',
              data: {
                type: 'Feature',
                properties: {},
                geometry: {
                  type: 'LineString',
                  coordinates: polyline.map(p => [p.lng, p.lat]),
                },
              },
            });
            map.addLayer({
              id: 'route',
              type: 'line',
              source: 'route',
              layout: { 'line-join': 'round', 'line-cap': 'round' },
              paint: { 'line-color': '#4f46e5', 'line-width': 4 },
            });
          });
        }

        if (markers.length > 1) {
          const bounds = new mapboxgl.LngLatBounds();
          markers.forEach(m => bounds.extend([m.lng, m.lat]));
          map.fitBounds(bounds, { padding: 50, maxZoom: 15 });
        }

        mapRef.current = map;
      } catch (err) {
        console.error('Failed to initialize Mapbox:', err);
      }
    };

    initMap();
    return () => { if (map) map.remove(); };
  }, [settingsLoaded, mapEngine, mapboxToken, mainLat, mainLng, zoom, markers, polyline, onMarkerClick]);

  // Initialize Google Maps
  useEffect(() => {
    if (!settingsLoaded || mapEngine !== 'google' || !googleApiKey || !mapContainerRef.current) return;

    let map: any;
    const initGoogleMap = async () => {
      try {
        await loadGoogleMapsScript(googleApiKey);
        const google = (window as any).google;

        map = new google.maps.Map(mapContainerRef.current!, {
          center: { lat: mainLat, lng: mainLng },
          zoom: zoom || 13,
          mapId: 'exporoute-map',
        });

        markers.forEach((marker) => {
          const gMarker = new google.maps.Marker({
            position: { lat: marker.lat, lng: marker.lng },
            map,
            title: marker.title || '',
          });

          if (marker.title || marker.description) {
            const infoWindow = new google.maps.InfoWindow({
              content: `<div style="padding:4px 8px;"><strong style="font-size:14px;">${marker.title || ''}</strong>${marker.description ? `<p style="font-size:12px;color:#666;margin-top:4px;">${marker.description}</p>` : ''}</div>`,
            });
            gMarker.addListener('click', () => {
              infoWindow.open(map, gMarker);
              if (onMarkerClick) onMarkerClick(marker);
            });
          }
        });

        if (polyline && polyline.length > 1) {
          new google.maps.Polyline({
            path: polyline.map(p => ({ lat: p.lat, lng: p.lng })),
            geodesic: true,
            strokeColor: '#4f46e5',
            strokeWeight: 4,
            map,
          });
        }

        if (markers.length > 1) {
          const bounds = new google.maps.LatLngBounds();
          markers.forEach(m => bounds.extend({ lat: m.lat, lng: m.lng }));
          map.fitBounds(bounds);
        }

        mapRef.current = map;
      } catch (err) {
        console.error('Failed to initialize Google Maps:', err);
      }
    };

    initGoogleMap();
    return () => { map = null; };
  }, [settingsLoaded, mapEngine, googleApiKey, mainLat, mainLng, zoom, markers, polyline, onMarkerClick]);

  // Fallback: no token/key available
  if (settingsLoaded && !mapboxToken && !googleApiKey) {
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
            <a href={generateGoogleMapsUrl(mainLat, mainLng, mainTitle)} target="_blank" rel="noopener noreferrer">
              <Button variant="outline" size="sm">
                <ExternalLink className="w-4 h-4" />
                {t('common.open_in_google_maps') || 'Google Maps'}
              </Button>
            </a>
            <a href={generateNaverMapUrl(mainLat, mainLng, mainTitle)} target="_blank" rel="noopener noreferrer">
              <Button variant="outline" size="sm">
                <ExternalLink className="w-4 h-4" />
                {t('common.open_in_naver_map') || 'Naver Map'}
              </Button>
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        'relative rounded-xl border border-gray-200 dark:border-gray-500/40 overflow-hidden',
        className
      )}
    >
      <div ref={mapContainerRef} className="w-full h-full" style={{ minHeight: '200px' }} />
      <div className="absolute bottom-2 right-2 flex gap-1 z-10">
        <a
          href={generateGoogleMapsUrl(mainLat, mainLng, mainTitle)}
          target="_blank"
          rel="noopener noreferrer"
          className="px-2 py-1 bg-white/90 dark:bg-black/70 rounded text-[10px] text-gray-600 dark:text-gray-300 hover:bg-white dark:hover:bg-black/90 shadow-sm"
        >
          Google Maps
        </a>
        <a
          href={generateNaverMapUrl(mainLat, mainLng, mainTitle)}
          target="_blank"
          rel="noopener noreferrer"
          className="px-2 py-1 bg-white/90 dark:bg-black/70 rounded text-[10px] text-gray-600 dark:text-gray-300 hover:bg-white dark:hover:bg-black/90 shadow-sm"
        >
          Naver Map
        </a>
      </div>
    </div>
  );
}
