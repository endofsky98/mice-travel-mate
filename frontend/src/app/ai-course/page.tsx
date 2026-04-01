'use client';

import { useState } from 'react';
import { Sparkles, Clock, MapPin, DollarSign, RotateCcw, Bookmark, Users } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import MapView from '@/components/map/MapView';
import { cn } from '@/lib/utils';

const DURATIONS = [
  { key: 'half_day', label: 'Half Day (4h)', icon: '🕐' },
  { key: 'full_day', label: 'Full Day (8h)', icon: '🕗' },
  { key: '2day', label: '2 Days', icon: '📅' },
];

const INTERESTS = [
  { key: 'food', label: 'Food & Dining', icon: '🍜' },
  { key: 'history', label: 'History & Culture', icon: '🏛️' },
  { key: 'shopping', label: 'Shopping', icon: '🛍️' },
  { key: 'kpop', label: 'K-Pop & Hallyu', icon: '🎤' },
  { key: 'nature', label: 'Nature', icon: '🌿' },
  { key: 'nightlife', label: 'Nightlife', icon: '🌃' },
];

const START_LOCATIONS = [
  { key: 'coex', label: 'COEX', lat: 37.5116, lng: 127.0595 },
  { key: 'gangnam', label: 'Gangnam Station', lat: 37.4979, lng: 127.0276 },
  { key: 'seoul_station', label: 'Seoul Station', lat: 37.5547, lng: 126.9707 },
  { key: 'myeongdong', label: 'Myeongdong', lat: 37.5636, lng: 126.9869 },
  { key: 'hongdae', label: 'Hongdae', lat: 37.5563, lng: 126.9234 },
  { key: 'itaewon', label: 'Itaewon', lat: 37.5345, lng: 126.9946 },
];

export default function AICoursePage() {
  const { t, lt, language } = useLanguage();
  const [step, setStep] = useState<'input' | 'loading' | 'result'>('input');
  const [duration, setDuration] = useState('half_day');
  const [interests, setInterests] = useState<string[]>([]);
  const [budget, setBudget] = useState(100);
  const [people, setPeople] = useState(2);
  const [startLocation, setStartLocation] = useState('coex');
  const [result, setResult] = useState<any>(null);

  const toggleInterest = (key: string) => {
    setInterests((prev) =>
      prev.includes(key) ? prev.filter((i) => i !== key) : [...prev, key]
    );
  };

  const selectedStart = START_LOCATIONS.find(l => l.key === startLocation) || START_LOCATIONS[0];

  const handleGenerate = async () => {
    setStep('loading');
    try {
      const data = await api.post('/api/ai-courses/generate', {
        duration,
        interests,
        budget,
        people,
        start_lat: selectedStart.lat,
        start_lng: selectedStart.lng,
      });
      setResult(data);
      setStep('result');
    } catch {
      // Fallback demo data
      const demoSpots = getDemoSpots(interests, duration);
      setResult({
        spots: demoSpots,
        total_duration_minutes: duration === 'half_day' ? 240 : duration === 'full_day' ? 480 : 960,
        total_distance_km: 5.2 + demoSpots.length * 1.3,
        estimated_cost: budget * 0.7,
        summary: `A curated ${duration.replace('_', ' ')} tour for ${people} people.`,
      });
      setStep('result');
    }
  };

  const handleRegenerate = () => {
    setStep('input');
    setResult(null);
  };

  const getResultMarkers = () => {
    if (!result?.spots) return [];
    return result.spots
      .filter((s: any) => s.lat && s.lng)
      .map((s: any, i: number) => ({
        id: i,
        lat: s.lat,
        lng: s.lng,
        title: lt(s.name) || s.name,
        description: lt(s.description) || s.description,
      }));
  };

  const getPolyline = () => {
    if (!result?.spots) return undefined;
    return result.spots
      .filter((s: any) => s.lat && s.lng)
      .map((s: any) => ({ lat: s.lat, lng: s.lng }));
  };

  if (step === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <Sparkles className="w-12 h-12 text-indigo-600 dark:text-indigo-400 animate-pulse" />
        <p className="text-lg font-medium text-gray-900 dark:text-gray-100">
          {t('ai_course.generating') || 'Generating your perfect course...'}
        </p>
        <LoadingSpinner />
      </div>
    );
  }

  if (step === 'result' && result) {
    const markers = getResultMarkers();
    const polylineData = getPolyline();

    return (
      <div className="page-container max-w-3xl">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            {t('ai_course.title') || 'Your AI Course'}
          </h1>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleRegenerate}>
              <RotateCcw className="w-4 h-4" /> {t('button.retry') || 'Regenerate'}
            </Button>
            <Button>
              <Bookmark className="w-4 h-4" /> {t('common.save') || 'Save'}
            </Button>
          </div>
        </div>

        {/* Summary */}
        <Card className="p-4 mb-6">
          <p className="text-gray-600 dark:text-gray-300 mb-3">{result.summary}</p>
          <div className="flex flex-wrap gap-4 text-sm">
            <span className="flex items-center gap-1 text-gray-500">
              <Clock className="w-4 h-4" /> {Math.round((result.total_duration_minutes || 240) / 60)}h
            </span>
            <span className="flex items-center gap-1 text-gray-500">
              <MapPin className="w-4 h-4" /> {(result.total_distance_km || 0).toFixed(1)}km
            </span>
            <span className="flex items-center gap-1 text-gray-500">
              <DollarSign className="w-4 h-4" /> ~${result.estimated_cost || 0}
            </span>
            <span className="flex items-center gap-1 text-gray-500">
              <Users className="w-4 h-4" /> {people} people
            </span>
          </div>
        </Card>

        {/* Map */}
        {markers.length > 0 && (
          <div className="mb-6 h-64 md:h-80">
            <MapView
              markers={markers}
              polyline={polylineData}
              className="h-full"
              t={t}
            />
          </div>
        )}

        {/* Timeline */}
        <div className="space-y-0">
          {(result.spots || []).map((spot: any, i: number) => (
            <div key={i} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="w-8 h-8 rounded-full bg-indigo-600 text-white text-sm flex items-center justify-center font-bold">
                  {i + 1}
                </div>
                {i < (result.spots || []).length - 1 && (
                  <div className="w-0.5 h-16 bg-indigo-200 dark:bg-indigo-800 my-1" />
                )}
              </div>
              <Card className="flex-1 p-4 mb-3">
                <h3 className="font-semibold text-gray-900 dark:text-gray-100">{lt(spot.name) || spot.name}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{lt(spot.description) || spot.description}</p>
                <div className="flex gap-3 mt-2">
                  {spot.stay_duration_minutes && (
                    <span className="text-xs text-indigo-600 dark:text-indigo-400 flex items-center gap-1">
                      <Clock className="w-3 h-3" /> {spot.stay_duration_minutes} min
                    </span>
                  )}
                  {spot.estimated_cost && (
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <DollarSign className="w-3 h-3" /> ~${spot.estimated_cost}
                    </span>
                  )}
                </div>
              </Card>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Input form
  return (
    <div className="page-container max-w-2xl">
      <div className="text-center mb-8">
        <Sparkles className="w-10 h-10 text-indigo-600 dark:text-indigo-400 mx-auto mb-3" />
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
          {t('ai_course.title') || 'AI Course Generator'}
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mt-2">
          {t('ai_course.subtitle') || 'Tell us your preferences and we\'ll create a perfect travel course.'}
        </p>
      </div>

      {/* Duration */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
          {t('ai_course.select_duration') || 'Duration'}
        </h2>
        <div className="grid grid-cols-3 gap-3">
          {DURATIONS.map((d) => (
            <button
              key={d.key}
              onClick={() => setDuration(d.key)}
              className={cn(
                'p-4 rounded-xl border text-center transition-all',
                duration === d.key
                  ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20 dark:border-indigo-500'
                  : 'border-gray-200 dark:border-gray-500/40 hover:border-gray-300'
              )}
            >
              <span className="text-2xl block mb-1">{d.icon}</span>
              <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{d.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Interests */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
          {t('ai_course.select_interests') || 'Interests'} <span className="text-sm font-normal text-gray-400">(select multiple)</span>
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {INTERESTS.map((item) => (
            <button
              key={item.key}
              onClick={() => toggleInterest(item.key)}
              className={cn(
                'p-3 rounded-xl border text-left transition-all flex items-center gap-2',
                interests.includes(item.key)
                  ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20 dark:border-indigo-500'
                  : 'border-gray-200 dark:border-gray-500/40 hover:border-gray-300'
              )}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{item.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* People & Start Location */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3 flex items-center gap-2">
            <Users className="w-5 h-5" /> {t('ai_course.people') || 'People'}
          </h2>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setPeople(Math.max(1, people - 1))}
              className="w-10 h-10 rounded-lg border border-gray-200 dark:border-gray-500/40 flex items-center justify-center text-lg font-bold hover:bg-gray-50 dark:hover:bg-white/5"
            >
              -
            </button>
            <span className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 w-8 text-center">{people}</span>
            <button
              onClick={() => setPeople(Math.min(10, people + 1))}
              className="w-10 h-10 rounded-lg border border-gray-200 dark:border-gray-500/40 flex items-center justify-center text-lg font-bold hover:bg-gray-50 dark:hover:bg-white/5"
            >
              +
            </button>
          </div>
        </div>
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3 flex items-center gap-2">
            <MapPin className="w-5 h-5" /> {t('ai_course.start_location') || 'Start'}
          </h2>
          <select
            value={startLocation}
            onChange={(e) => setStartLocation(e.target.value)}
            className="w-full px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-500/40 bg-transparent dark:bg-[#2a2a2a] text-gray-900 dark:text-gray-100 outline-none focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600"
          >
            {START_LOCATIONS.map((loc) => (
              <option key={loc.key} value={loc.key}>{loc.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Budget */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
          {t('ai_course.enter_budget') || 'Budget'} <span className="text-sm font-normal text-gray-400">(per person, USD)</span>
        </h2>
        <div className="flex items-center gap-4">
          <input
            type="range"
            min={0}
            max={500}
            step={10}
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
            className="flex-1 accent-indigo-600"
          />
          <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400 w-16 text-right">
            ${budget}
          </span>
        </div>
      </div>

      {/* Generate Button */}
      <Button
        onClick={handleGenerate}
        className="w-full py-4 text-lg"
        disabled={interests.length === 0}
      >
        <Sparkles className="w-5 h-5 mr-2" />
        {t('button.generate_course') || 'Generate Course'}
      </Button>
    </div>
  );
}

function getDemoSpots(interests: string[], duration: string) {
  const allSpots = [
    { name: 'Gyeongbokgung Palace', description: 'Grand 14th-century royal palace with changing of the guard ceremony', stay_duration_minutes: 90, estimated_cost: 3, lat: 37.5796, lng: 126.9770, tags: ['history'] },
    { name: 'Bukchon Hanok Village', description: 'Charming neighborhood with hundreds of traditional Korean houses', stay_duration_minutes: 60, estimated_cost: 0, lat: 37.5826, lng: 126.9831, tags: ['history'] },
    { name: 'Insadong Street', description: 'Vibrant art street with galleries, tea houses, and traditional crafts', stay_duration_minutes: 45, estimated_cost: 10, lat: 37.5735, lng: 126.9851, tags: ['shopping', 'history'] },
    { name: 'Gwangjang Market', description: 'Korea\'s first permanent market, famous for street food and vintage clothing', stay_duration_minutes: 60, estimated_cost: 15, lat: 37.5700, lng: 126.9993, tags: ['food'] },
    { name: 'Myeongdong Shopping District', description: 'Seoul\'s premier shopping area with Korean cosmetics and fashion', stay_duration_minutes: 90, estimated_cost: 30, lat: 37.5636, lng: 126.9869, tags: ['shopping'] },
    { name: 'N Seoul Tower', description: 'Iconic observation tower on Namsan Mountain with panoramic city views', stay_duration_minutes: 60, estimated_cost: 16, lat: 37.5512, lng: 126.9882, tags: ['nature'] },
    { name: 'HYBE Insight', description: 'Museum dedicated to K-Pop history and BTS memorabilia', stay_duration_minutes: 90, estimated_cost: 22, lat: 37.5266, lng: 127.0405, tags: ['kpop'] },
    { name: 'Gangnam K-Star Road', description: 'Walk of fame featuring K-Pop idol bear statues', stay_duration_minutes: 30, estimated_cost: 0, lat: 37.5109, lng: 127.0213, tags: ['kpop'] },
    { name: 'Cheonggyecheon Stream', description: 'Beautiful urban stream park perfect for a relaxing walk', stay_duration_minutes: 40, estimated_cost: 0, lat: 37.5696, lng: 126.9784, tags: ['nature'] },
    { name: 'Itaewon & Yongsan', description: 'Multicultural district with diverse restaurants and trendy bars', stay_duration_minutes: 90, estimated_cost: 25, lat: 37.5345, lng: 126.9946, tags: ['food', 'nightlife'] },
    { name: 'Hongdae Club Street', description: 'Youthful district famous for nightlife, street performances, and indie music', stay_duration_minutes: 120, estimated_cost: 20, lat: 37.5563, lng: 126.9234, tags: ['nightlife'] },
    { name: 'Noryangjin Fish Market', description: 'Massive seafood market where you pick your fish and have it prepared fresh', stay_duration_minutes: 60, estimated_cost: 20, lat: 37.5131, lng: 126.9404, tags: ['food'] },
  ];

  let filtered = allSpots.filter(s => interests.some(i => s.tags.includes(i)));
  if (filtered.length < 3) filtered = allSpots.slice(0, 5);

  const count = duration === 'half_day' ? 4 : duration === 'full_day' ? 6 : 10;
  return filtered.slice(0, count);
}
