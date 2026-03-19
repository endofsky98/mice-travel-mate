'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { Search, Navigation, X, Heart, MapPin } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import FilterChips from '@/components/ui/FilterChips';
import Card from '@/components/ui/Card';
import StarRating from '@/components/ui/StarRating';

const SAMSUNG_STATION = { lat: 37.5088, lng: 127.0631 };
const DEFAULT_ZOOM = 14;

interface PlaceItem {
  id: number;
  name: string | Record<string, string>;
  description?: string | Record<string, string>;
  address?: string | Record<string, string>;
  category?: string;
  price_range?: number;
  lat?: number;
  lng?: number;
  latitude?: number;
  longitude?: number;
  venue_lat?: number;
  venue_lng?: number;
  avg_rating?: number;
  review_count?: number;
  images?: string[];
  image_url?: string;
  profile_image_url?: string;
}

export default function MapPage() {
  const { t, lt, language } = useLanguage();
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const popupRef = useRef<any>(null);
  const selectedMarkerRef = useRef<any>(null);
  const listContainerRef = useRef<HTMLDivElement>(null);
  const filterByViewportRef = useRef<() => void>(() => {});

  const [categoryFilter, setCategoryFilter] = useState('restaurants');
  const [searchQuery, setSearchQuery] = useState('');
  const [items, setItems] = useState<PlaceItem[]>([]);
  const [visibleItems, setVisibleItems] = useState<PlaceItem[]>([]);
  const [selectedItem, setSelectedItem] = useState<PlaceItem | null>(null);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [mapCenter, setMapCenter] = useState(SAMSUNG_STATION);
  const [mapReady, setMapReady] = useState(false);
  const [mapboxToken, setMapboxToken] = useState<string | null>(null);
  const [gpsStatus, setGpsStatus] = useState<'pending' | 'granted' | 'denied'>('pending');

  const categoryChips = [
    { key: 'restaurants', label: t('nav.restaurants') || 'Restaurants' },
    { key: 'courses', label: t('nav.courses') || 'Courses' },
    { key: 'guides', label: t('nav.guides') || 'Guides' },
    { key: 'festivals', label: t('home.festivals_events') || 'Festivals' },
  ];

  const getCoords = (item: PlaceItem) => {
    const lat = item.lat || item.latitude || item.venue_lat;
    const lng = item.lng || item.longitude || item.venue_lng;
    return lat && lng ? { lat, lng } : null;
  };

  const getImage = (item: PlaceItem) => {
    if (item.images && item.images.length > 0) return item.images[0];
    if (item.image_url) return item.image_url;
    if (item.profile_image_url) return item.profile_image_url;
    return null;
  };

  // B4: Request GPS on mount - fallback to Samsung Station
  useEffect(() => {
    if (!navigator.geolocation) {
      setGpsStatus('denied');
      setMapCenter(SAMSUNG_STATION);
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const loc = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        setUserLocation(loc);
        setMapCenter(loc);
        setGpsStatus('granted');
      },
      () => {
        setGpsStatus('denied');
        setMapCenter(SAMSUNG_STATION);
      },
      { enableHighAccuracy: false, timeout: 15000, maximumAge: 60000 }
    );
  }, []);

  // Load mapbox token
  useEffect(() => {
    const loadToken = async () => {
      const envToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN;
      if (envToken && envToken !== 'pk.placeholder') {
        setMapboxToken(envToken);
        return;
      }
      try {
        const settings = await api.get<{ mapbox_api_key: string }>('/api/map-settings');
        if (settings.mapbox_api_key && settings.mapbox_api_key !== 'pk.placeholder') {
          setMapboxToken(settings.mapbox_api_key);
        }
      } catch { /* */ }
    };
    loadToken();
  }, []);

  // Fetch data when category or language changes
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const endpoint = categoryFilter === 'festivals' ? '/api/festivals' : `/api/${categoryFilter}`;
        const data = await api.get<{ items: PlaceItem[] }>(endpoint, { per_page: 200, lang: language });
        setItems(data.items || []);
      } catch {
        setItems([]);
      }
    };
    fetchItems();
  }, [categoryFilter, language]);

  // B4: Filter items by viewport bounds
  const filterByViewport = useCallback(() => {
    if (!mapRef.current) {
      setVisibleItems(items.filter(i => getCoords(i)));
      return;
    }
    try {
      const bounds = mapRef.current.getBounds();
      const sw = bounds.getSouthWest();
      const ne = bounds.getNorthEast();
      const filtered = items.filter((item) => {
        const coords = getCoords(item);
        if (!coords) return false;
        return coords.lat >= sw.lat && coords.lat <= ne.lat && coords.lng >= sw.lng && coords.lng <= ne.lng;
      });
      setVisibleItems(filtered);
    } catch {
      setVisibleItems(items.filter(i => getCoords(i)));
    }
  }, [items]);

  // Keep ref in sync so moveend handler always uses latest filterByViewport
  useEffect(() => { filterByViewportRef.current = filterByViewport; }, [filterByViewport]);

  // Initialize map
  useEffect(() => {
    if (!mapboxToken || !mapContainerRef.current || gpsStatus === 'pending') return;

    let map: any;
    const initMap = async () => {
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
        center: [mapCenter.lng, mapCenter.lat],
        zoom: DEFAULT_ZOOM,
      });

      map.addControl(new mapboxgl.NavigationControl(), 'top-right');

      // Add user location marker
      if (userLocation) {
        const userEl = document.createElement('div');
        userEl.style.cssText = 'width:16px;height:16px;background:#3b82f6;border-radius:50%;border:3px solid white;box-shadow:0 0 0 2px rgba(59,130,246,0.3);';
        new mapboxgl.Marker(userEl).setLngLat([userLocation.lng, userLocation.lat]).addTo(map);
      }

      // B4: moveend event for viewport-based list filtering (use ref to avoid stale closure)
      map.on('moveend', () => {
        if (mapRef.current) filterByViewportRef.current();
      });

      map.on('load', () => {
        setMapReady(true);
      });

      mapRef.current = map;
    };

    initMap();
    return () => {
      if (map) map.remove();
      mapRef.current = null;
      setMapReady(false);
    };
  }, [mapboxToken, gpsStatus, mapCenter.lat, mapCenter.lng, userLocation]);

  // Update markers when items or mapReady changes
  useEffect(() => {
    if (!mapRef.current || !mapReady) return;

    const updateMarkers = async () => {
      const mapboxgl = (await import('mapbox-gl')).default;
      const map = mapRef.current;

      // Clear old markers
      markersRef.current.forEach(m => m.remove());
      markersRef.current = [];
      if (popupRef.current) { popupRef.current.remove(); popupRef.current = null; }

      const itemsWithCoords = items.filter(i => getCoords(i));

      itemsWithCoords.forEach((item) => {
        const coords = getCoords(item)!;
        const el = document.createElement('div');
        el.className = 'map-marker';
        el.dataset.itemId = String(item.id);
        el.style.cssText = 'width:32px;height:32px;background:#4f46e5;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;';
        el.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>';

        // B5: Marker click -> popup + list highlight
        el.addEventListener('click', (e) => {
          e.stopPropagation();
          handleSelectItem(item, mapboxgl, map);
        });

        const marker = new mapboxgl.Marker(el)
          .setLngLat([coords.lng, coords.lat])
          .addTo(map);

        markersRef.current.push(marker);
      });

      filterByViewport();
    };

    updateMarkers();
  }, [items, mapReady, language]);

  // B5: Handle item selection (from list or marker)
  const handleSelectItem = useCallback(async (item: PlaceItem, mapboxgl?: any, map?: any) => {
    if (!mapboxgl) mapboxgl = (await import('mapbox-gl')).default;
    if (!map) map = mapRef.current;
    if (!map) return;

    const coords = getCoords(item);
    if (!coords) return;

    setSelectedItem(item);

    // Reset previous selected marker
    if (selectedMarkerRef.current) {
      selectedMarkerRef.current.style.background = '#4f46e5';
      selectedMarkerRef.current.style.width = '32px';
      selectedMarkerRef.current.style.height = '32px';
    }

    // Highlight new marker with different color
    const markerEl = document.querySelector(`.map-marker[data-item-id="${item.id}"]`) as HTMLElement;
    if (markerEl) {
      markerEl.style.background = '#dc2626';
      markerEl.style.width = '40px';
      markerEl.style.height = '40px';
      selectedMarkerRef.current = markerEl;
    }

    // Remove old popup
    if (popupRef.current) popupRef.current.remove();

    const image = getImage(item);
    const name = lt(item.name);
    const desc = lt(item.description || item.address || '');
    const detailUrl = `/${categoryFilter}/${item.id}`;

    // B5: Popup with name, image, description, bookmark, detail link
    const popupHtml = `
      <div style="min-width:220px;max-width:280px;font-family:Inter,sans-serif;">
        ${image ? `<img src="${image}" style="width:100%;height:120px;object-fit:cover;border-radius:8px 8px 0 0;" alt="${name}" onerror="this.style.display='none'" />` : ''}
        <div style="padding:10px 12px;">
          <h3 style="font-size:14px;font-weight:600;margin:0 0 4px 0;color:#111;">${name}</h3>
          <p style="font-size:12px;color:#666;margin:0 0 8px 0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">${desc}</p>
          ${item.avg_rating ? `<div style="font-size:12px;color:#f59e0b;margin-bottom:8px;">★ ${item.avg_rating.toFixed(1)}</div>` : ''}
          <div style="display:flex;gap:6px;">
            <button onclick="event.stopPropagation()" style="padding:6px 10px;background:#f3f4f6;border:1px solid #e5e7eb;border-radius:6px;cursor:pointer;display:flex;align-items:center;font-size:12px;" title="${t('common.bookmark') || 'Bookmark'}">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </button>
            <a href="${detailUrl}" style="flex:1;display:inline-flex;align-items:center;justify-content:center;padding:6px 12px;background:#4f46e5;color:white;border-radius:6px;font-size:12px;font-weight:500;text-decoration:none;">${t('common.view_detail') || '상세보기'}</a>
          </div>
        </div>
      </div>
    `;

    const popup = new mapboxgl.Popup({
      offset: 25,
      closeButton: true,
      maxWidth: '300px',
    })
      .setLngLat([coords.lng, coords.lat])
      .setHTML(popupHtml)
      .addTo(map);

    popupRef.current = popup;

    popup.on('close', () => {
      setSelectedItem(null);
      if (selectedMarkerRef.current) {
        selectedMarkerRef.current.style.background = '#4f46e5';
        selectedMarkerRef.current.style.width = '32px';
        selectedMarkerRef.current.style.height = '32px';
        selectedMarkerRef.current = null;
      }
      popupRef.current = null;
    });

    map.flyTo({ center: [coords.lng, coords.lat], zoom: Math.max(map.getZoom(), 15), duration: 500 });

    // B5: Scroll selected item into view in the list
    setTimeout(() => {
      const cardEl = document.querySelector(`[data-list-item-id="${item.id}"]`);
      if (cardEl) {
        cardEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    }, 100);
  }, [categoryFilter, lt, language, t]);

  // B2: My location button handler with GPS permission check
  const handleMyLocation = () => {
    if (!navigator.geolocation) {
      alert(t('map.gps_not_supported') || 'GPS is not supported on this device.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const loc = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        setUserLocation(loc);
        setGpsStatus('granted');
        if (mapRef.current) {
          mapRef.current.flyTo({ center: [loc.lng, loc.lat], zoom: DEFAULT_ZOOM, duration: 800 });
        }
      },
      () => {
        // GPS 거부 시 서울 중심(COEX)으로 이동
        const seoulCenter = { lat: 37.5126, lng: 127.059 };
        setGpsStatus('denied');
        if (mapRef.current) {
          mapRef.current.flyTo({ center: [seoulCenter.lng, seoulCenter.lat], zoom: DEFAULT_ZOOM, duration: 800 });
        }
      },
      { enableHighAccuracy: false, timeout: 15000, maximumAge: 60000 }
    );
  };

  // Search filter
  const displayItems = searchQuery
    ? visibleItems.filter(i => {
        const name = lt(i.name).toLowerCase();
        const desc = lt(i.description || '').toLowerCase();
        const q = searchQuery.toLowerCase();
        return name.includes(q) || desc.includes(q);
      })
    : visibleItems;

  return (
    <div className="relative h-[calc(100vh-64px)] flex flex-col">
      {/* Search & Filter Overlay */}
      <div className="absolute top-0 left-0 right-0 z-20 p-3 space-y-2">
        <div className="relative max-w-lg mx-auto">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t('map.search_places') || 'Search places...'}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white dark:bg-[#1e1e1e] shadow-lg border border-gray-200 dark:border-gray-500/40 text-sm outline-none focus:ring-2 focus:ring-indigo-600/20"
          />
          {searchQuery && (
            <button onClick={() => setSearchQuery('')} className="absolute right-3 top-1/2 -translate-y-1/2">
              <X className="w-4 h-4 text-gray-400" />
            </button>
          )}
        </div>
        <div className="max-w-lg mx-auto">
          <FilterChips chips={categoryChips} selected={categoryFilter} onSelect={(k) => k && setCategoryFilter(k)} />
        </div>
      </div>

      {/* Map Area */}
      <div className="flex-1 relative">
        {mapboxToken ? (
          <div ref={mapContainerRef} className="w-full h-full" />
        ) : (
          <div className="w-full h-full bg-gray-100 dark:bg-[#1a1a1a] flex items-center justify-center">
            <div className="text-center text-gray-500 dark:text-gray-400">
              <MapPin className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p className="text-sm">{t('map.loading') || 'Loading map...'}</p>
            </div>
          </div>
        )}

        {/* B3: Bottom items list with generous padding to avoid GNB overlap */}
        {displayItems.length > 0 && (
          <div className="absolute bottom-0 left-0 right-0 z-10 pb-24 md:pb-4 px-3 pt-2" ref={listContainerRef}>
            <div className="flex gap-3 overflow-x-auto scrollbar-hide pb-2">
              {displayItems.slice(0, 15).map((item) => (
                <button
                  key={item.id}
                  data-list-item-id={item.id}
                  onClick={() => handleSelectItem(item)}
                  className={`flex-shrink-0 w-[200px] text-left transition-all ${
                    selectedItem?.id === item.id
                      ? 'ring-2 ring-red-500 rounded-xl scale-105'
                      : ''
                  }`}
                >
                  <Card hoverable className="p-3">
                    <h3 className="font-medium text-sm text-gray-900 dark:text-gray-100 line-clamp-1">
                      {lt(item.name)}
                    </h3>
                    {item.avg_rating && item.avg_rating > 0 && (
                      <StarRating rating={item.avg_rating} size="sm" showValue />
                    )}
                    <p className="text-xs text-gray-400 mt-1 line-clamp-1">
                      {lt(item.description || item.address || '')}
                    </p>
                  </Card>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Items count badge */}
        <div className="absolute top-24 left-3 z-10 bg-white dark:bg-[#1e1e1e] shadow-md rounded-lg px-3 py-1.5 text-xs text-gray-600 dark:text-gray-300">
          {displayItems.length}{t('map.places_count') || ' places'}
        </div>
      </div>

      {/* B2: My Location Button - positioned above GNB */}
      <button
        onClick={handleMyLocation}
        className="absolute bottom-28 md:bottom-8 right-4 w-12 h-12 bg-white dark:bg-[#1e1e1e] rounded-full shadow-lg flex items-center justify-center text-indigo-600 dark:text-indigo-400 z-20 hover:bg-gray-50 dark:hover:bg-[#2a2a2a] transition-colors active:scale-95"
        title={t('map.my_location') || 'My Location'}
      >
        <Navigation className="w-5 h-5" />
      </button>
    </div>
  );
}
