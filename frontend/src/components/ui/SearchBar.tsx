'use client';

import { useState, useRef, useEffect } from 'react';
import { Search, X, Clock, TrendingUp } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface SearchBarProps {
  t: (key: string) => string;
  language: string;
  placeholder?: string;
}

export default function SearchBar({ t, language, placeholder }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();
  const debounceRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('recent_searches');
    if (stored) {
      try {
        setRecentSearches(JSON.parse(stored).slice(0, 5));
      } catch { /* ignore */ }
    }
  }, []);

  const handleSearch = (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    const updated = [searchQuery, ...recentSearches.filter(s => s !== searchQuery)].slice(0, 5);
    setRecentSearches(updated);
    localStorage.setItem('recent_searches', JSON.stringify(updated));
    router.push(`/search?q=${encodeURIComponent(searchQuery)}&lang=${language}`);
    setIsFocused(false);
  };

  const handleInputChange = (value: string) => {
    setQuery(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (value.length >= 2) {
      debounceRef.current = setTimeout(async () => {
        try {
          const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
          const res = await fetch(`${apiUrl}/api/search/suggest?q=${encodeURIComponent(value)}&lang=${language}`);
          if (res.ok) {
            const data = await res.json();
            setSuggestions(data.suggestions || []);
          }
        } catch { /* ignore */ }
      }, 300);
    } else {
      setSuggestions([]);
    }
  };

  return (
    <div className="relative">
      <div className="bg-white dark:bg-[#1e1e1e] px-4 py-3">
        <div className="max-w-7xl mx-auto">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => handleInputChange(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch(query)}
              placeholder={placeholder || t('home.search_placeholder') || 'Search restaurants, courses, guides...'}
              className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-gray-200 dark:border-gray-500/40 bg-gray-50 dark:bg-[#2a2a2a] text-sm outline-none focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:focus:ring-indigo-400/30 dark:focus:border-indigo-400 dark:text-gray-100 placeholder:text-gray-400"
            />
            {query && (
              <button
                onClick={() => { setQuery(''); setSuggestions([]); }}
                className="absolute right-3 top-1/2 -translate-y-1/2"
              >
                <X className="w-4 h-4 text-gray-400" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Dropdown */}
      {isFocused && (query.length > 0 || recentSearches.length > 0) && (
        <div className="absolute top-full left-0 right-0 bg-white dark:bg-[#1e1e1e] border-t border-gray-100 dark:border-gray-500/40 shadow-lg z-50 max-h-80 overflow-y-auto">
          <div className="max-w-7xl mx-auto px-4 py-2">
            {suggestions.length > 0 ? (
              suggestions.map((s, i) => (
                <button
                  key={i}
                  onClick={() => handleSearch(s)}
                  className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5 rounded-lg flex items-center gap-2 text-gray-700 dark:text-gray-200"
                >
                  <Search className="w-3.5 h-3.5 text-gray-400" />
                  {s}
                </button>
              ))
            ) : recentSearches.length > 0 && !query ? (
              <>
                <p className="text-xs text-gray-400 px-3 py-1 flex items-center gap-1">
                  <Clock className="w-3 h-3" /> {t('common.recent') || 'Recent'}
                </p>
                {recentSearches.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => handleSearch(s)}
                    className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 dark:hover:bg-white/5 rounded-lg text-gray-700 dark:text-gray-200"
                  >
                    {s}
                  </button>
                ))}
              </>
            ) : null}
          </div>
        </div>
      )}

      {/* Overlay to close dropdown */}
      {isFocused && (
        <div className="fixed inset-0 z-40" onClick={() => setIsFocused(false)} />
      )}
    </div>
  );
}
