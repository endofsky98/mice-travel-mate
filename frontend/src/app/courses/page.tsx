'use client';

import { useEffect, useState } from 'react';
import { Search, Map } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import CourseCard from '@/components/course/CourseCard';
import CourseFilters from '@/components/course/CourseFilters';
import Pagination from '@/components/ui/Pagination';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Input from '@/components/ui/Input';
import { Course } from '@/types';

export default function CoursesPage() {
  const { t, lt, language } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState<Course[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [duration, setDuration] = useState('');
  const [theme, setTheme] = useState('');
  const [difficulty, setDifficulty] = useState('');

  useEffect(() => {
    const fetchCourses = async () => {
      setLoading(true);
      try {
        const data = await api.get<{ items: Course[]; pages: number }>('/api/v1/courses', {
          page: currentPage,
          per_page: 12,
          search: search || undefined,
          duration: duration || undefined,
          theme: theme || undefined,
          difficulty: difficulty || undefined,
        });
        setCourses(data.items || []);
        setTotalPages(data.pages || 1);
      } catch {
        setCourses([]);
      }
      setLoading(false);
    };
    fetchCourses();
  }, [currentPage, search, duration, theme, difficulty, language]);

  return (
    <div className="page-container">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('nav.courses')}</h1>

      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <Input
            placeholder={t('common.search')}
            value={search}
            onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }}
            className="pl-10"
          />
        </div>
      </div>

      <div className="mb-6">
        <CourseFilters
          t={t}
          duration={duration}
          theme={theme}
          difficulty={difficulty}
          onDurationChange={(v) => { setDuration(v); setCurrentPage(1); }}
          onThemeChange={(v) => { setTheme(v); setCurrentPage(1); }}
          onDifficultyChange={(v) => { setDifficulty(v); setCurrentPage(1); }}
        />
      </div>

      {loading ? (
        <LoadingSpinner fullPage />
      ) : courses.length === 0 ? (
        <EmptyState icon={Map} title={t('common.no_results')} />
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {courses.map((c) => (
              <CourseCard key={c.id} course={c} lt={lt} />
            ))}
          </div>
          <div className="mt-8">
            <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={setCurrentPage} />
          </div>
        </>
      )}
    </div>
  );
}
