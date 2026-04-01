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

export default function MapPage() {
  const { t, lt, language } = useLanguage();
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const userMarkerRef = useRef<any>(null);
  const popupRef = useRef<any>(null);
  const itemsRef = useRef<PlaceItem[]>([]);
  const listContainerRef = useRef<HTMLDivElement>(null);
  const filterByViewportRef = useRef<() => void>(() => {});
  const selectedIdRef = useRef<number | null>(null);
  const googleMarkersRef = useRef<any[]>([]);
  const googleInfoWindowRef = useRef<any>(null);

  const [categoryFilter, setCategoryFilter] = useState('restaurants');
  const [searchQuery, setSearchQuery] = useState('');
  const [items, setItems] = useState<PlaceItem[]>([]);
  const [visibleItems, setVisibleItems] = useState<PlaceItem[]>([]);
  const [selectedItem, setSelectedItem] = useState<PlaceItem | null>(null);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [mapCenter, setMapCenter] = useState(SAMSUNG_STATION);
  const [mapReady, setMapReady] = useState(false);
  const [mapEngine, setMapEngine] = useState<string | null>(null);
  const [mapboxToken, setMapboxToken] = useState<string | null>(null);
  const [googleApiKey, setGoogleApiKey] = useState<string | null>(null);
  const [settingsLoaded, setSettingsLoaded] = useState(false);
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

  // Keep itemsRef in sync
  useEffect(() => { itemsRef.current = items; }, [items]);

  // Build GeoJSON from items (for Mapbox)
  const buildGeoJSON = useCallback((data: PlaceItem[], selectedId: number | null) => {
    return {
      type: 'FeatureCollection' as const,
      features: data.filter(i => getCoords(i)).map(item => {
        const coords = getCoords(item)!;
        return {
          type: 'Feature' as const,
          geometry: { type: 'Point' as const, coordinates: [coords.lng, coords.lat] },
          properties: { itemId: item.id, selected: item.id === selectedId },
        };
      }),
    };
  }, []);

  // Update GeoJSON source on the map (Mapbox only)
  const updateSource = useCallback((selectedId?: number | null) => {
    const map = mapRef.current;
    if (!map || !map.getSource || !map.getSource('places')) return;
    const sid = selectedId !== undefined ? selectedId : selectedIdRef.current;
    map.getSource('places').setData(buildGeoJSON(itemsRef.current, sid));
  }, [buildGeoJSON]);

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

  // Load map settings (engine + keys)
  useEffect(() => {
    const loadSettings = async () => {
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
        // Fallback to env var for mapbox
        if (envToken && envToken !== 'pk.placeholder') {
          setMapEngine('mapbox');
          setMapboxToken(envToken);
        }
      }
      setSettingsLoaded(true);
    };
    loadSettings();
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

  // B4: Filter items by viewport bounds (engine-aware)
  const filterByViewport = useCallback(() => {
    if (!mapRef.current) {
      setVisibleItems(items.filter(i => getCoords(i)));
      return;
    }
    try {
      const map = mapRef.current;
      let swLat: number, swLng: number, neLat: number, neLng: number;

      if (mapEngine === 'google') {
        const bounds = map.getBounds();
        if (!bounds) { setVisibleItems(items.filter(i => getCoords(i))); return; }
        const sw = bounds.getSouthWest();
        const ne = bounds.getNorthEast();
        swLat = sw.lat(); swLng = sw.lng();
        neLat = ne.lat(); neLng = ne.lng();
      } else {
        const bounds = map.getBounds();
        const sw = bounds.getSouthWest();
        const ne = bounds.getNorthEast();
        swLat = sw.lat; swLng = sw.lng;
        neLat = ne.lat; neLng = ne.lng;
      }

      const filtered = items.filter((item) => {
        const coords = getCoords(item);
        if (!coords) return false;
        return coords.lat >= swLat && coords.lat <= neLat && coords.lng >= swLng && coords.lng <= neLng;
      });
      setVisibleItems(filtered);
    } catch {
      setVisibleItems(items.filter(i => getCoords(i)));
    }
  }, [items, mapEngine]);

  // Keep ref in sync so moveend/idle handler always uses latest filterByViewport
  useEffect(() => { filterByViewportRef.current = filterByViewport; }, [filterByViewport]);

  // Ref for stable access to categoryFilter and lt
  const categoryFilterRef = useRef(categoryFilter);
  useEffect(() => { categoryFilterRef.current = categoryFilter; }, [categoryFilter]);
  const ltRef = useRef(lt);
  useEffect(() => { ltRef.current = lt; }, [lt]);
  const tRef = useRef(t);
  useEffect(() => { tRef.current = t; }, [t]);

  // Build popup/infowindow HTML content
  const buildPopupHtml = useCallback((item: PlaceItem) => {
    const image = getImage(item);
    const name = ltRef.current(item.name);
    const desc = ltRef.current(item.description || item.address || '');
    const detailUrl = `/${categoryFilterRef.current}/${item.id}`;

    return `
      <div style="min-width:220px;max-width:280px;font-family:Inter,sans-serif;">
        ${image ? `<img src="${image}" style="width:100%;height:120px;object-fit:cover;border-radius:8px 8px 0 0;" alt="${name}" onerror="this.style.display='none'" />` : ''}
        <div style="padding:10px 12px;">
          <h3 style="font-size:14px;font-weight:600;margin:0 0 4px 0;color:#111;">${name}</h3>
          <p style="font-size:12px;color:#666;margin:0 0 8px 0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">${desc}</p>
          ${item.avg_rating ? `<div style="font-size:12px;color:#f59e0b;margin-bottom:8px;">★ ${item.avg_rating.toFixed(1)}</div>` : ''}
          <div style="display:flex;gap:6px;">
            <button onclick="event.stopPropagation()" style="padding:6px 10px;background:#f3f4f6;border:1px solid #e5e7eb;border-radius:6px;cursor:pointer;display:flex;align-items:center;font-size:12px;" title="${tRef.current('common.bookmark') || 'Bookmark'}">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </button>
            <a href="${detailUrl}" style="flex:1;display:inline-flex;align-items:center;justify-content:center;padding:6px 12px;background:#4f46e5;color:white;border-radius:6px;font-size:12px;font-weight:500;text-decoration:none;">${tRef.current('common.view_detail') || '상세보기'}</a>
          </div>
        </div>
      </div>
    `;
  }, []);

  // === MAPBOX INITIALIZATION ===
  useEffect(() => {
    if (!settingsLoaded || mapEngine !== 'mapbox' || !mapboxToken || !mapContainerRef.current || gpsStatus === 'pending') return;

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

      map.on('moveend', () => {
        if (mapRef.current) filterByViewportRef.current();
      });

      map.on('load', () => {
        map.addSource('places', {
          type: 'geojson',
          data: { type: 'FeatureCollection', features: [] },
        });

        map.addLayer({
          id: 'places-shadow',
          type: 'circle',
          source: 'places',
          paint: {
            'circle-radius': ['case', ['get', 'selected'], 14, 10],
            'circle-color': 'rgba(0,0,0,0.15)',
            'circle-translate': [0, 2],
            'circle-blur': 0.4,
          },
        });

        map.addLayer({
          id: 'places-circle',
          type: 'circle',
          source: 'places',
          paint: {
            'circle-radius': ['case', ['get', 'selected'], 12, 8],
            'circle-color': ['case', ['get', 'selected'], '#dc2626', '#4f46e5'],
            'circle-stroke-color': '#ffffff',
            'circle-stroke-width': 2.5,
          },
        });

        map.addLayer({
          id: 'places-icon',
          type: 'circle',
          source: 'places',
          paint: {
            'circle-radius': ['case', ['get', 'selected'], 3.5, 2.5],
            'circle-color': '#ffffff',
          },
        });

        map.on('click', 'places-circle', (e: any) => {
          if (!e.features || e.features.length === 0) return;
          const feature = e.features[0];
          const itemId = feature.properties.itemId;
          const item = itemsRef.current.find(i => i.id === itemId);
          if (item) handleSelectItemMapbox(item, mapboxgl, map);
        });

        map.on('mouseenter', 'places-circle', () => {
          map.getCanvas().style.cursor = 'pointer';
        });
        map.on('mouseleave', 'places-circle', () => {
          map.getCanvas().style.cursor = '';
        });

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
  }, [settingsLoaded, mapEngine, mapboxToken, gpsStatus, mapCenter.lat, mapCenter.lng]);

  // === GOOGLE MAPS INITIALIZATION ===
  useEffect(() => {
    if (!settingsLoaded || mapEngine !== 'google' || !googleApiKey || !mapContainerRef.current || gpsStatus === 'pending') return;

    let map: any;
    const initGoogleMap = async () => {
      try {
        await loadGoogleMapsScript(googleApiKey);
        const google = (window as any).google;

        map = new google.maps.Map(mapContainerRef.current!, {
          center: { lat: mapCenter.lat, lng: mapCenter.lng },
          zoom: DEFAULT_ZOOM,
          mapId: 'exporoute-map',
        });

        // Viewport filtering on idle (equivalent to Mapbox moveend)
        map.addListener('idle', () => {
          if (mapRef.current) filterByViewportRef.current();
        });

        // Create shared InfoWindow
        googleInfoWindowRef.current = new google.maps.InfoWindow();
        googleInfoWindowRef.current.addListener('closeclick', () => {
          setSelectedItem(null);
          selectedIdRef.current = null;
          updateGoogleMarkerStyles(null);
        });

        mapRef.current = map;
        setMapReady(true);
      } catch (err) {
        console.error('Failed to initialize Google Maps:', err);
      }
    };

    initGoogleMap();
    return () => {
      // Clean up Google markers
      googleMarkersRef.current.forEach(m => m.setMap(null));
      googleMarkersRef.current = [];
      if (googleInfoWindowRef.current) googleInfoWindowRef.current.close();
      map = null;
      mapRef.current = null;
      setMapReady(false);
    };
  }, [settingsLoaded, mapEngine, googleApiKey, gpsStatus, mapCenter.lat, mapCenter.lng]);

  // Update Google marker icon styles based on selection
  const updateGoogleMarkerStyles = useCallback((selectedId: number | null) => {
    const google = (window as any).google;
    if (!google) return;
    googleMarkersRef.current.forEach((gMarker) => {
      const itemId = gMarker._itemId;
      const isSelected = itemId === selectedId;
      gMarker.setIcon({
        path: google.maps.SymbolPath.CIRCLE,
        scale: isSelected ? 12 : 8,
        fillColor: isSelected ? '#dc2626' : '#4f46e5',
        fillOpacity: 1,
        strokeColor: '#ffffff',
        strokeWeight: 2.5,
      });
      gMarker.setZIndex(isSelected ? 1000 : 1);
    });
  }, []);

  // Update Google markers when items change
  useEffect(() => {
    if (!mapReady || mapEngine !== 'google' || !mapRef.current) return;
    const google = (window as any).google;
    if (!google) return;

    // Remove old markers
    googleMarkersRef.current.forEach(m => m.setMap(null));
    googleMarkersRef.current = [];

    // Close info window
    if (googleInfoWindowRef.current) googleInfoWindowRef.current.close();
    selectedIdRef.current = null;
    setSelectedItem(null);

    // Add new markers
    items.forEach((item) => {
      const coords = getCoords(item);
      if (!coords) return;

      const marker = new google.maps.Marker({
        position: { lat: coords.lat, lng: coords.lng },
        map: mapRef.current,
        icon: {
          path: google.maps.SymbolPath.CIRCLE,
          scale: 8,
          fillColor: '#4f46e5',
          fillOpacity: 1,
          strokeColor: '#ffffff',
          strokeWeight: 2.5,
        },
        zIndex: 1,
      });

      (marker as any)._itemId = item.id;

      marker.addListener('click', () => {
        handleSelectItemGoogle(item, marker);
      });

      googleMarkersRef.current.push(marker);
    });

    filterByViewportRef.current();
  }, [items, mapReady, mapEngine]);

  // Handle item selection on Google Maps
  const handleSelectItemGoogle = useCallback((item: PlaceItem, marker?: any) => {
    const coords = getCoords(item);
    if (!coords || !mapRef.current) return;
    const google = (window as any).google;
    if (!google) return;

    setSelectedItem(item);
    selectedIdRef.current = item.id;
    updateGoogleMarkerStyles(item.id);

    const popupHtml = buildPopupHtml(item);

    if (googleInfoWindowRef.current) {
      googleInfoWindowRef.current.setContent(popupHtml);
      if (marker) {
        googleInfoWindowRef.current.open(mapRef.current, marker);
      } else {
        // Find the marker for this item
        const targetMarker = googleMarkersRef.current.find((m: any) => m._itemId === item.id);
        if (targetMarker) {
          googleInfoWindowRef.current.open(mapRef.current, targetMarker);
        } else {
          googleInfoWindowRef.current.setPosition({ lat: coords.lat, lng: coords.lng });
          googleInfoWindowRef.current.open(mapRef.current);
        }
      }
    }

    mapRef.current.panTo({ lat: coords.lat, lng: coords.lng });

    // Scroll selected item into view in the list
    setTimeout(() => {
      const cardEl = document.querySelector(`[data-list-item-id="${item.id}"]`);
      if (cardEl) {
        cardEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    }, 100);
  }, [updateGoogleMarkerStyles, buildPopupHtml]);

  // Handle item selection on Mapbox
  const handleSelectItemMapbox = useCallback((item: PlaceItem, mapboxgl: any, map: any) => {
    const coords = getCoords(item);
    if (!coords) return;

    setSelectedItem(item);
    selectedIdRef.current = item.id;
    updateSource(item.id);

    // Remove old popup
    if (popupRef.current) popupRef.current.remove();

    const popupHtml = buildPopupHtml(item);

    const popup = new mapboxgl.Popup({
      offset: 15,
      closeButton: true,
      maxWidth: '300px',
    })
      .setLngLat([coords.lng, coords.lat])
      .setHTML(popupHtml)
      .addTo(map);

    popupRef.current = popup;

    popup.on('close', () => {
      setSelectedItem(null);
      selectedIdRef.current = null;
      updateSource(null);
      popupRef.current = null;
    });

    map.flyTo({ center: [coords.lng, coords.lat], zoom: map.getZoom(), duration: 500 });

    // Scroll selected item into view in the list
    setTimeout(() => {
      const cardEl = document.querySelector(`[data-list-item-id="${item.id}"]`);
      if (cardEl) {
        cardEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    }, 100);
  }, [updateSource, buildPopupHtml]);

  // Update user location marker (Mapbox)
  useEffect(() => {
    if (!mapRef.current || !mapReady || !userLocation || mapEngine !== 'mapbox') return;
    (async () => {
      const mapboxgl = (await import('mapbox-gl')).default;
      if (userMarkerRef.current) {
        userMarkerRef.current.remove();
        userMarkerRef.current = null;
      }
      const userEl = document.createElement('div');
      userEl.style.cssText = 'width:16px;height:16px;background:#3b82f6;border-radius:50%;border:3px solid white;box-shadow:0 0 0 4px rgba(59,130,246,0.25);';
      userMarkerRef.current = new mapboxgl.Marker(userEl)
        .setLngLat([userLocation.lng, userLocation.lat])
        .addTo(mapRef.current);
    })();
  }, [userLocation, mapReady, mapEngine]);

  // Update user location marker (Google Maps)
  useEffect(() => {
    if (!mapRef.current || !mapReady || !userLocation || mapEngine !== 'google') return;
    const google = (window as any).google;
    if (!google) return;

    if (userMarkerRef.current) {
      userMarkerRef.current.setMap(null);
      userMarkerRef.current = null;
    }

    userMarkerRef.current = new google.maps.Marker({
      position: { lat: userLocation.lat, lng: userLocation.lng },
      map: mapRef.current,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 8,
        fillColor: '#3b82f6',
        fillOpacity: 1,
        strokeColor: '#ffffff',
        strokeWeight: 3,
      },
      zIndex: 2000,
    });
  }, [userLocation, mapReady, mapEngine]);

  // Update Mapbox GeoJSON source when items change
  useEffect(() => {
    if (!mapRef.current || !mapReady || mapEngine !== 'mapbox') return;
    updateSource(null);
    selectedIdRef.current = null;
    setSelectedItem(null);
    if (popupRef.current) { popupRef.current.remove(); popupRef.current = null; }
    filterByViewport();
  }, [items, mapReady, mapEngine, updateSource, filterByViewport]);

  // Handle item selection from bottom list (engine-aware)
  const handleSelectItem = useCallback(async (item: PlaceItem) => {
    if (mapEngine === 'google') {
      handleSelectItemGoogle(item);
    } else {
      const mapboxgl = (await import('mapbox-gl')).default;
      const map = mapRef.current;
      if (!map) return;
      handleSelectItemMapbox(item, mapboxgl, map);
    }
  }, [mapEngine, handleSelectItemGoogle, handleSelectItemMapbox]);

  // B2: My location button handler (engine-aware)
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
        const flyToLoc = () => {
          if (mapRef.current) {
            if (mapEngine === 'google') {
              mapRef.current.panTo({ lat: loc.lat, lng: loc.lng });
            } else {
              const currentZoom = mapRef.current.getZoom();
              mapRef.current.flyTo({ center: [loc.lng, loc.lat], zoom: currentZoom, duration: 800 });
            }
          } else {
            setTimeout(flyToLoc, 500);
          }
        };
        flyToLoc();
      },
      () => {
        setGpsStatus('denied');
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

  const hasMapKey = mapboxToken || googleApiKey;

  return (
    <div className="relative" style={{ height: 'calc(100dvh - 128px)' }}>
      {/* Search & Filter Overlay */}
      <div className="fixed top-16 left-0 right-0 z-30 p-3 space-y-2 pointer-events-none">
        <div className="relative w-[80%] pointer-events-auto">
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
        <div className="pointer-events-auto">
          <FilterChips chips={categoryChips} selected={categoryFilter} onSelect={(k) => k && setCategoryFilter(k)} />
        </div>
      </div>

      {/* Map Area */}
      <div className="fixed left-0 right-0" style={{ top: '64px', bottom: '64px' }}>
        {hasMapKey ? (
          <div ref={mapContainerRef} className="w-full h-full" />
        ) : (
          <div className="w-full h-full bg-gray-100 dark:bg-[#1a1a1a] flex items-center justify-center">
            <div className="text-center text-gray-500 dark:text-gray-400">
              <MapPin className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p className="text-sm">{t('map.loading') || 'Loading map...'}</p>
            </div>
          </div>
        )}
      </div>

      {/* Bottom spot list */}
      {displayItems.length > 0 && (
        <div className="fixed bottom-16 left-0 right-0 z-20 px-3 py-2" ref={listContainerRef}>
          <div className="flex gap-3 overflow-x-auto scrollbar-hide pb-1">
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

      {/* GPS button */}
      <button
        onClick={handleMyLocation}
        className="fixed z-20 right-4 w-12 h-12 bg-white dark:bg-[#1e1e1e] rounded-full shadow-lg flex items-center justify-center text-indigo-600 dark:text-indigo-400 hover:bg-gray-50 dark:hover:bg-[#2a2a2a] transition-colors active:scale-95"
        style={{ bottom: displayItems.length > 0 ? 'calc(64px + 80px)' : 'calc(64px + 16px)' }}
        title={t('map.my_location') || 'My Location'}
      >
        <Navigation className="w-5 h-5" />
      </button>
    </div>
  );
}
