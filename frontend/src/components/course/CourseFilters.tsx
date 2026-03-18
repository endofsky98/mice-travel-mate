'use client';

import Select from '@/components/ui/Select';

interface CourseFiltersProps {
  t: (key: string) => string;
  duration: string;
  theme: string;
  difficulty: string;
  onDurationChange: (value: string) => void;
  onThemeChange: (value: string) => void;
  onDifficultyChange: (value: string) => void;
}

export default function CourseFilters({
  t,
  duration,
  theme,
  difficulty,
  onDurationChange,
  onThemeChange,
  onDifficultyChange,
}: CourseFiltersProps) {
  const durationOptions = [
    { value: '', label: t('common.all') },
    { value: 'half_day', label: t('course.half_day') },
    { value: 'full_day', label: t('course.full_day') },
    { value: 'two_days', label: t('course.two_days') },
  ];

  const themeOptions = [
    { value: '', label: t('common.all') },
    { value: 'culture', label: t('course.culture') },
    { value: 'food', label: t('course.food') },
    { value: 'shopping', label: t('course.shopping') },
    { value: 'nature', label: t('course.nature') },
    { value: 'history', label: t('course.history') },
    { value: 'nightlife', label: t('course.nightlife') },
  ];

  const difficultyOptions = [
    { value: '', label: t('common.all') },
    { value: 'easy', label: t('course.easy') },
    { value: 'moderate', label: t('course.moderate') },
    { value: 'challenging', label: t('course.challenging') },
  ];

  return (
    <div className="flex flex-col sm:flex-row gap-3">
      <div className="flex-1">
        <Select
          options={durationOptions}
          value={duration}
          onChange={(e) => onDurationChange(e.target.value)}
        />
      </div>
      <div className="flex-1">
        <Select
          options={themeOptions}
          value={theme}
          onChange={(e) => onThemeChange(e.target.value)}
        />
      </div>
      <div className="flex-1">
        <Select
          options={difficultyOptions}
          value={difficulty}
          onChange={(e) => onDifficultyChange(e.target.value)}
        />
      </div>
    </div>
  );
}
