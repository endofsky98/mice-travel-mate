export interface MultilingualText {
  en?: string;
  ko?: string;
  ja?: string;
  'zh-CN'?: string;
  'zh-TW'?: string;
  es?: string;
  [key: string]: string | undefined;
}

export interface Event {
  id: number;
  slug: string;
  name: string | MultilingualText;
  description: string | MultilingualText;
  banner_image?: string;
  start_date: string;
  end_date: string;
  venue_name?: string | MultilingualText;
  venue_address?: string | MultilingualText;
  venue_lat?: number;
  venue_lng?: number;
  region?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Restaurant {
  id: number;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  category: string;
  price_range: number;
  address?: string | MultilingualText;
  phone?: string;
  hours?: string | MultilingualText;
  images?: string[];
  menu_highlights?: MenuHighlight[];
  lat?: number;
  lng?: number;
  distance_from_venue?: number;
  event_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface MenuHighlight {
  name: string | MultilingualText;
  description?: string | MultilingualText;
  price?: string;
  image?: string;
}

export interface Course {
  id: number;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  duration: string;
  difficulty: string;
  theme: string;
  region?: string;
  transport_cost?: string;
  images?: string[];
  spots?: CourseSpot[];
  event_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CourseSpot {
  id: number;
  order: number;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  image?: string;
  duration?: string;
  lat?: number;
  lng?: number;
  transition?: SpotTransition;
}

export interface SpotTransition {
  mode: string;
  duration: string;
  distance?: string;
  description?: string | MultilingualText;
}

export interface Product {
  id: number;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  category: string;
  price: number;
  currency: string;
  duration?: string;
  region?: string;
  images?: string[];
  includes?: (string | MultilingualText)[];
  excludes?: (string | MultilingualText)[];
  itinerary?: ItineraryItem[];
  meeting_point?: string | MultilingualText;
  dismissal_point?: string | MultilingualText;
  min_participants?: number;
  max_participants?: number;
  cancellation_policy?: string | MultilingualText;
  lat?: number;
  lng?: number;
  event_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ItineraryItem {
  time: string;
  title: string | MultilingualText;
  description?: string | MultilingualText;
}

export interface Guide {
  id: number;
  name: string | MultilingualText;
  bio?: string | MultilingualText;
  profile_image?: string;
  languages?: GuideLanguage[];
  specialties?: string[];
  regions?: string[];
  services?: string | MultilingualText;
  hourly_rate?: number;
  half_day_rate?: number;
  full_day_rate?: number;
  currency: string;
  availability?: string[];
  event_id?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface GuideLanguage {
  language: string;
  proficiency: string;
}

export interface TransportRoute {
  id: number;
  from: string | MultilingualText;
  to: string | MultilingualText;
  modes: TransportMode[];
  event_id?: number;
  is_active: boolean;
}

export interface TransportMode {
  mode: string;
  duration: string;
  cost?: string;
  description?: string | MultilingualText;
  steps?: string[];
}

export interface TransportTip {
  id: number;
  title: string | MultilingualText;
  description: string | MultilingualText;
  icon?: string;
  category: string;
  event_id?: number;
  is_active: boolean;
}

export interface Booking {
  id: number;
  booking_number: string;
  type: 'product' | 'guide';
  item_id: number;
  item_name?: string;
  date: string;
  time?: string;
  participants: number;
  total_price: number;
  currency: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  booker_name: string;
  booker_email: string;
  booker_phone?: string;
  booker_nationality?: string;
  special_requests?: string;
  options?: BookingOption[];
  created_at: string;
  updated_at: string;
}

export interface BookingOption {
  name: string;
  value: string;
  price?: number;
}

export interface User {
  id: number;
  name: string;
  email: string;
  nationality?: string;
  preferred_language?: string;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  total?: number;
  page?: number;
  per_page?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface MapMarker {
  id: string | number;
  lat: number;
  lng: number;
  title?: string;
  description?: string;
  type?: string;
}

export interface Translations {
  [key: string]: string | Translations;
}

export type Language = 'en' | 'ko' | 'ja' | 'zh-CN' | 'zh-TW' | 'es';

export const SUPPORTED_LANGUAGES: { code: Language; name: string; flag: string }[] = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'ko', name: '한국어', flag: '🇰🇷' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
  { code: 'zh-CN', name: '简体中文', flag: '🇨🇳' },
  { code: 'zh-TW', name: '繁體中文', flag: '🇹🇼' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
];
