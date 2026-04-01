'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { BookOpen, Bus, Utensils, ShoppingBag, CreditCard, Phone, AlertTriangle, Heart, CloudSun } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { LivingGuideCategory, LivingGuideArticle } from '@/types';

const CATEGORY_ICONS: Record<string, any> = {
  transportation: Bus,
  food_culture: Utensils,
  shopping: ShoppingBag,
  currency: CreditCard,
  telecom: Phone,
  emergency: AlertTriangle,
  etiquette: Heart,
  weather: CloudSun,
  // Fallbacks for alternative icon names from seed data
  bus: Bus,
  utensils: Utensils,
  'shopping-bag': ShoppingBag,
  'currency-exchange': CreditCard,
  wifi: Phone,
  'alert-circle': AlertTriangle,
  'hand-shake': Heart,
};

export default function LivingGuidePage() {
  const { t, lt, language } = useLanguage();
  const searchParams = useSearchParams();
  const catParam = searchParams.get('cat');
  const [categories, setCategories] = useState<LivingGuideCategory[]>([]);
  const [articles, setArticles] = useState<LivingGuideArticle[]>([]);
  const [selectedCat, setSelectedCat] = useState<string | null>(catParam);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await api.get<{ items: LivingGuideCategory[] }>('/api/living-guide/categories');
        setCategories(data.items || []);
      } catch {
        setCategories([]);
      }
      setLoading(false);
    };
    fetch();
  }, [language]);

  useEffect(() => {
    if (selectedCat) {
      fetchArticles(selectedCat);
    }
  }, [selectedCat, language]);

  const fetchArticles = async (catId: string) => {
    try {
      const data = await api.get<{ items: LivingGuideArticle[] }>(`/api/living-guide/categories/${catId}/articles`);
      setArticles(data.items || []);
    } catch {
      setArticles([]);
    }
  };

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div className="page-container max-w-4xl">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6 flex items-center gap-2">
        <BookOpen className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
        {t('home.living_guide_title') || 'Korea Living Guide'}
      </h1>

      {/* Categories */}
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-8 gap-3 mb-8">
        {categories.map((cat) => {
          const Icon = CATEGORY_ICONS[cat.icon || ''] || BookOpen;
          const isSelected = selectedCat === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCat(isSelected ? null : cat.id)}
              className={`flex flex-col items-center gap-2 p-3 rounded-xl transition-all ${
                isSelected
                  ? 'bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-600 dark:border-indigo-500'
                  : 'bg-gray-50 dark:bg-[#1e1e1e] border border-transparent hover:border-gray-200 dark:hover:border-gray-500/40'
              }`}
            >
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                isSelected ? 'bg-indigo-100 dark:bg-indigo-900/40' : 'bg-white dark:bg-[#2a2a2a]'
              }`}>
                <Icon className={`w-5 h-5 ${isSelected ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-500'}`} />
              </div>
              <span className="text-xs font-medium text-center text-gray-700 dark:text-gray-300 line-clamp-1">
                {lt(cat.name)}
              </span>
            </button>
          );
        })}
      </div>

      {/* Articles */}
      {selectedCat && (
        <div className="space-y-4">
          {articles.length === 0 ? (
            <p className="text-center text-gray-400 py-8">{t('common.no_results') || 'No articles'}</p>
          ) : (
            articles.map((article) => (
              <Card key={article.id} className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
                  {lt(article.title)}
                </h2>
                {article.image_url && (
                  <img src={article.image_url} alt="" className="w-full h-48 object-cover rounded-lg mb-4" />
                )}
                <div className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-line">
                  {lt(article.content)}
                </div>
              </Card>
            ))
          )}
        </div>
      )}

      {!selectedCat && (
        <p className="text-center text-gray-400 py-12">
          {t('living_guide.select_category') || 'Select a category to view guides'}
        </p>
      )}
    </div>
  );
}
