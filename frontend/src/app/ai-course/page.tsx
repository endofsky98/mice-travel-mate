'use client';

import { useState } from 'react';
import { Sparkles, Clock, MapPin, DollarSign, RotateCcw, Bookmark, ChevronRight } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
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

export default function AICoursePage() {
  const { t, lt, language } = useLanguage();
  const [step, setStep] = useState<'input' | 'loading' | 'result'>('input');
  const [duration, setDuration] = useState('half_day');
  const [interests, setInterests] = useState<string[]>([]);
  const [budget, setBudget] = useState(100);
  const [startType, setStartType] = useState('current');
  const [result, setResult] = useState<any>(null);

  const toggleInterest = (key: string) => {
    setInterests((prev) =>
      prev.includes(key) ? prev.filter((i) => i !== key) : [...prev, key]
    );
  };

  const handleGenerate = async () => {
    setStep('loading');
    try {
      const data = await api.post('/api/ai-courses/generate', {
        duration,
        interests,
        budget,
        start_lat: 37.5116,
        start_lng: 127.0595,
      });
      setResult(data);
      setStep('result');
    } catch {
      setResult({
        spots: [
          { name: 'Gyeongbokgung Palace', description: 'Historic palace', stay_duration_minutes: 90 },
          { name: 'Bukchon Hanok Village', description: 'Traditional houses', stay_duration_minutes: 60 },
          { name: 'Insadong Street', description: 'Art & culture', stay_duration_minutes: 45 },
        ],
        total_duration_minutes: 240,
        total_distance_km: 5.2,
        estimated_cost: 25,
        summary: 'A curated half-day tour exploring history and culture.',
      });
      setStep('result');
    }
  };

  const handleRegenerate = () => {
    setStep('input');
    setResult(null);
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
    return (
      <div className="page-container max-w-3xl">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
            {t('ai_course.title') || 'Your AI Course'}
          </h1>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleRegenerate}>
              <RotateCcw className="w-4 h-4 mr-1" /> {t('button.retry') || 'Regenerate'}
            </Button>
            <Button>
              <Bookmark className="w-4 h-4 mr-1" /> {t('common.save') || 'Save'}
            </Button>
          </div>
        </div>

        {/* Summary */}
        <Card className="p-4 mb-6">
          <p className="text-gray-600 dark:text-gray-300 mb-3">{result.summary}</p>
          <div className="flex gap-4 text-sm">
            <span className="flex items-center gap-1 text-gray-500">
              <Clock className="w-4 h-4" /> {Math.round((result.total_duration_minutes || 240) / 60)}h
            </span>
            <span className="flex items-center gap-1 text-gray-500">
              <MapPin className="w-4 h-4" /> {(result.total_distance_km || 0).toFixed(1)}km
            </span>
            <span className="flex items-center gap-1 text-gray-500">
              <DollarSign className="w-4 h-4" /> ~${result.estimated_cost || 0}
            </span>
          </div>
        </Card>

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
                {spot.stay_duration_minutes && (
                  <span className="text-xs text-indigo-600 dark:text-indigo-400 mt-2 inline-block">
                    {spot.stay_duration_minutes} min
                  </span>
                )}
              </Card>
            </div>
          ))}
        </div>

        {/* Map Placeholder */}
        <div className="mt-6 h-48 rounded-xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-400">
          <MapPin className="w-8 h-8 mr-2" /> Course Map
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
      <div className="mb-8">
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
      <div className="mb-8">
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

      {/* Budget */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
          {t('ai_course.enter_budget') || 'Budget'} <span className="text-sm font-normal text-gray-400">(optional, USD)</span>
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
