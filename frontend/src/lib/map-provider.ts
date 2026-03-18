import { MapMarker } from '@/types';

export function generateGoogleMapsUrl(lat: number, lng: number, label?: string): string {
  const query = label ? encodeURIComponent(label) : `${lat},${lng}`;
  return `https://www.google.com/maps/search/?api=1&query=${query}&center=${lat},${lng}`;
}

export function generateGoogleMapsDirectionsUrl(
  fromLat: number,
  fromLng: number,
  toLat: number,
  toLng: number
): string {
  return `https://www.google.com/maps/dir/?api=1&origin=${fromLat},${fromLng}&destination=${toLat},${toLng}`;
}

export function generateNaverMapUrl(lat: number, lng: number, label?: string): string {
  const name = label ? encodeURIComponent(label) : '';
  return `https://map.naver.com/v5/search/${name}?c=${lng},${lat},15,0,0,0,dh`;
}

export function getMarkerBounds(markers: MapMarker[]): {
  center: { lat: number; lng: number };
  zoom: number;
} {
  if (markers.length === 0) {
    return { center: { lat: 37.5665, lng: 126.978 }, zoom: 12 };
  }

  if (markers.length === 1) {
    return { center: { lat: markers[0].lat, lng: markers[0].lng }, zoom: 15 };
  }

  const lats = markers.map((m) => m.lat);
  const lngs = markers.map((m) => m.lng);
  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);
  const minLng = Math.min(...lngs);
  const maxLng = Math.max(...lngs);

  const centerLat = (minLat + maxLat) / 2;
  const centerLng = (minLng + maxLng) / 2;

  const latDiff = maxLat - minLat;
  const lngDiff = maxLng - minLng;
  const maxDiff = Math.max(latDiff, lngDiff);

  let zoom = 15;
  if (maxDiff > 1) zoom = 8;
  else if (maxDiff > 0.5) zoom = 10;
  else if (maxDiff > 0.1) zoom = 12;
  else if (maxDiff > 0.01) zoom = 14;

  return { center: { lat: centerLat, lng: centerLng }, zoom };
}
