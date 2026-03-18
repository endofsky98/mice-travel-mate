'use client';

import { useEffect, useState } from 'react';
import { Search, ShoppingBag } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import ProductCard from '@/components/product/ProductCard';
import ProductFilters from '@/components/product/ProductFilters';
import Pagination from '@/components/ui/Pagination';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import EmptyState from '@/components/ui/EmptyState';
import Input from '@/components/ui/Input';
import { Product } from '@/types';

export default function ProductsPage() {
  const { t, lt, language } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState<Product[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [sortBy, setSortBy] = useState('recommended');

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const data = await api.get<{ items: Product[]; pages: number }>('/api/v1/products', {
          page: currentPage,
          per_page: 12,
          search: search || undefined,
          category: category || undefined,
          sort: sortBy || undefined,
        });
        setProducts(data.items || []);
        setTotalPages(data.pages || 1);
      } catch {
        setProducts([]);
      }
      setLoading(false);
    };
    fetchProducts();
  }, [currentPage, search, category, sortBy, language]);

  return (
    <div className="page-container">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('nav.products')}</h1>

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
        <ProductFilters
          t={t}
          category={category}
          sortBy={sortBy}
          onCategoryChange={(v) => { setCategory(v); setCurrentPage(1); }}
          onSortChange={setSortBy}
        />
      </div>

      {loading ? (
        <LoadingSpinner fullPage />
      ) : products.length === 0 ? (
        <EmptyState icon={ShoppingBag} title={t('common.no_results')} />
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {products.map((p) => (
              <ProductCard key={p.id} product={p} lt={lt} />
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
