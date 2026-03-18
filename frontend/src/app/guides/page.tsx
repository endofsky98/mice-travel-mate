'use client';

import { useEffect, useState } from 'react';
import { Search, Users } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import GuideCard from '@/components/guide/GuideCard';
import GuideFilters from '@/components/guide/GuideFilters';
import Pagination from '@/components/ui/Pagination';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Input from '@/components/ui/Input';
import { Guide } from '@/types';

export default function GuidesPage() {
  const { t, lt, language } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [guides, setGuides] = useState<Guide[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [filterLanguage, setFilterLanguage] = useState('');
  const [specialty, setSpecialty] = useState('');
  const [sortBy, setSortBy] = useState('recommended');

  useEffect(() => {
    const fetchGuides = async () => {
      setLoading(true);
      try {
        const data = await api.get<{ items: Guide[]; pages: number }>('/api/guides', {
          page: currentPage,
          per_page: 12,
          search: search || undefined,
          language: filterLanguage || undefined,
          specialty: specialty || undefined,
          sort: sortBy || undefined,
        });
        setGuides(data.items || []);
        setTotalPages(data.pages || 1);
      } catch {
        setGuides([]);
      }
      setLoading(false);
    };
    fetchGuides();
  }, [currentPage, search, filterLanguage, specialty, sortBy, language]);

  return (
    <div className="page-container">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('nav.guides')}</h1>

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
        <GuideFilters
          t={t}
          language={filterLanguage}
          specialty={specialty}
          sortBy={sortBy}
          onLanguageChange={(v) => { setFilterLanguage(v); setCurrentPage(1); }}
          onSpecialtyChange={(v) => { setSpecialty(v); setCurrentPage(1); }}
          onSortChange={setSortBy}
        />
      </div>

      {loading ? (
        <LoadingSpinner fullPage />
      ) : guides.length === 0 ? (
        <EmptyState icon={Users} title={t('common.no_results')} />
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {guides.map((g) => (
              <GuideCard key={g.id} guide={g} lt={lt} />
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
