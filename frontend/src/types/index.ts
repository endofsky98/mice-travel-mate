export interface MultilingualText {
  en?: string;
  ko?: string;
  ja?: string;
  'zh-CN'?: string;
  'zh-TW'?: string;
  es?: string;
  th?: string;
  vi?: string;
  fr?: string;
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
  latitude?: number;
  longitude?: number;
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
  latitude?: number;
  longitude?: number;
  distance_from_venue?: number;
  event_id?: number;
  avg_rating?: number;
  review_count?: number;
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
  duration_type?: string;
  difficulty: string;
  theme: string;
  region?: string;
  transport_cost?: string;
  total_duration_minutes?: number;
  total_distance_km?: number;
  estimated_transport_cost?: number;
  images?: string[];
  image_url?: string;
  spots?: CourseSpot[];
  event_id?: number;
  avg_rating?: number;
  review_count?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CourseSpot {
  id: number;
  order: number;
  spot_order?: number;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  image?: string;
  image_url?: string;
  duration?: string;
  stay_duration_minutes?: number;
  lat?: number;
  lng?: number;
  latitude?: number;
  longitude?: number;
  transition?: SpotTransition;
}

export interface SpotTransition {
  mode: string;
  transport_mode?: string;
  duration: string;
  duration_minutes?: number;
  distance?: string;
  distance_km?: number;
  description?: string | MultilingualText;
}

export interface Product {
  id: number;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  category: string;
  price: number;
  price_usd?: number;
  currency: string;
  duration?: string;
  duration_hours?: number;
  region?: string;
  images?: string[];
  includes?: (string | MultilingualText)[];
  excludes?: (string | MultilingualText)[];
  itinerary?: ItineraryItem[];
  meeting_point?: string | MultilingualText;
  dismissal_point?: string | MultilingualText;
  meeting_point_lat?: number;
  meeting_point_lng?: number;
  min_participants?: number;
  max_participants?: number;
  cancellation_policy?: string | MultilingualText;
  lat?: number;
  lng?: number;
  event_id?: number;
  avg_rating?: number;
  review_count?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ItineraryItem {
  time: string;
  title: string | MultilingualText;
  activity?: string;
  description?: string | MultilingualText;
}

export interface Guide {
  id: number;
  name: string | MultilingualText;
  bio?: string | MultilingualText;
  profile_image?: string;
  profile_image_url?: string;
  languages?: GuideLanguage[];
  specialties?: string[];
  regions?: string[];
  services?: string | MultilingualText;
  hourly_rate?: number;
  half_day_rate?: number;
  full_day_rate?: number;
  price_per_hour_usd?: number;
  price_half_day_usd?: number;
  price_full_day_usd?: number;
  currency: string;
  availability?: string[];
  event_id?: number;
  avg_rating?: number;
  review_count?: number;
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
  duration_minutes?: number;
  cost?: string;
  cost_krw?: number;
  cost_usd?: number;
  description?: string | MultilingualText;
  instructions_en?: string;
  steps?: string[];
}

export interface TransportTip {
  id: number;
  title: string | MultilingualText;
  description: string | MultilingualText;
  content?: string | MultilingualText;
  icon?: string;
  category: string;
  event_id?: number;
  is_active: boolean;
}

export interface Booking {
  id: number;
  booking_number: string;
  type: 'product' | 'guide';
  booking_type?: string;
  item_id: number;
  item_name?: string;
  date: string;
  booking_date?: string;
  time?: string;
  participants: number;
  num_participants?: number;
  total_price: number;
  total_amount_usd?: number;
  currency: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  booker_name: string;
  booker_email: string;
  booker_phone?: string;
  booker_nationality?: string;
  special_requests?: string;
  options?: BookingOption[];
  coupon_code?: string;
  discount_amount?: number;
  created_at: string;
  updated_at: string;
}

export interface BookingOption {
  name: string;
  value: string;
  price?: number;
}

export interface User {
  id: number | string;
  name: string;
  email: string;
  nationality?: string;
  preferred_language?: string;
  role?: string;
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
  category?: string;
  image?: string;
  rating?: number;
}

export interface Translations {
  [key: string]: string | Translations;
}

export type Language = 'en' | 'ko' | 'ja' | 'zh-CN' | 'zh-TW' | 'es' | 'th' | 'vi' | 'fr';

export const SUPPORTED_LANGUAGES: { code: Language; name: string; flag: string }[] = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'ko', name: '한국어', flag: '🇰🇷' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
  { code: 'zh-CN', name: '简体中文', flag: '🇨🇳' },
  { code: 'zh-TW', name: '繁體中文', flag: '🇹🇼' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'th', name: 'ไทย', flag: '🇹🇭' },
  { code: 'vi', name: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
];

// --- New types for v4 features ---

export interface RollingBanner {
  id: string;
  title: string | MultilingualText;
  subtitle: string | MultilingualText;
  image_url: string;
  link_url?: string;
  display_order: number;
  is_active: boolean;
  rolling_interval?: number;
}

export interface Review {
  id: string;
  user_id: string;
  user_name?: string;
  target_type: 'restaurant' | 'course' | 'product' | 'guide';
  target_id: string;
  rating: number;
  content: string;
  images?: string[];
  status: 'pending' | 'approved' | 'deleted';
  is_reported: boolean;
  created_at: string;
}

export interface ReviewStats {
  avg_rating: number;
  total_count: number;
  distribution: { [key: number]: number }; // { 5: 10, 4: 5, 3: 2, 2: 1, 1: 0 }
}

export interface Coupon {
  id: string;
  code: string;
  name: string;
  discount_type: 'fixed' | 'percentage' | 'upgrade';
  discount_value: number;
  max_discount_usd?: number;
  min_order_usd?: number;
  is_valid: boolean;
  error_message?: string;
}

export interface ChatRoom {
  id: string;
  guide_id: string;
  guide_name?: string;
  guide_image?: string;
  last_message?: string;
  last_message_at?: string;
  unread_count: number;
}

export interface ChatMessage {
  id: string;
  room_id: string;
  sender_type: 'user' | 'guide';
  sender_id: string;
  message_type: 'text' | 'image';
  content?: string;
  image_url?: string;
  is_read: boolean;
  created_at: string;
}

export interface Festival {
  id: string;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  category: string;
  image_url?: string;
  images?: string[];
  venue_name?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  start_date: string;
  end_date: string;
  website_url?: string;
  is_active: boolean;
}

export interface ThemeData {
  id: string;
  name: string | MultilingualText;
  description?: string | MultilingualText;
  icon?: string;
  color?: string;
  spots?: ThemeSpot[];
}

export interface ThemeSpot {
  id: string;
  theme_id: string;
  target_type: string;
  target_id: string;
  name?: string;
  lat?: number;
  lng?: number;
}

export interface LivingGuideCategory {
  id: string;
  name: string | MultilingualText;
  icon?: string;
  articles?: LivingGuideArticle[];
}

export interface LivingGuideArticle {
  id: string;
  category_id: string;
  title: string | MultilingualText;
  content?: string | MultilingualText;
  image_url?: string;
}

export interface AIGeneratedCourse {
  spots: CourseSpot[];
  total_duration_minutes: number;
  total_distance_km: number;
  estimated_cost: number;
  summary: string;
}

export interface CompareItem {
  id: string;
  type: 'restaurant' | 'course' | 'product' | 'guide';
  data: Restaurant | Course | Product | Guide;
}
