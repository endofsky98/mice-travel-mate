'use client';

import { useState, useEffect, useCallback } from 'react';

type BookmarkType = 'restaurant' | 'course' | 'product' | 'guide';

interface BookmarkItem {
  id: number;
  type: BookmarkType;
}

const BOOKMARKS_KEY = 'bookmarks';

function getStoredBookmarks(): BookmarkItem[] {
  if (typeof window === 'undefined') return [];
  try {
    const stored = localStorage.getItem(BOOKMARKS_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

function saveBookmarks(bookmarks: BookmarkItem[]): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem(BOOKMARKS_KEY, JSON.stringify(bookmarks));
}

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<BookmarkItem[]>([]);

  useEffect(() => {
    setBookmarks(getStoredBookmarks());
  }, []);

  const isBookmarked = useCallback(
    (id: number, type: BookmarkType): boolean => {
      return bookmarks.some((b) => b.id === id && b.type === type);
    },
    [bookmarks]
  );

  const toggleBookmark = useCallback(
    (id: number, type: BookmarkType) => {
      const exists = bookmarks.some((b) => b.id === id && b.type === type);
      let updated: BookmarkItem[];
      if (exists) {
        updated = bookmarks.filter((b) => !(b.id === id && b.type === type));
      } else {
        updated = [...bookmarks, { id, type }];
      }
      setBookmarks(updated);
      saveBookmarks(updated);
    },
    [bookmarks]
  );

  const getBookmarksByType = useCallback(
    (type: BookmarkType): number[] => {
      return bookmarks.filter((b) => b.type === type).map((b) => b.id);
    },
    [bookmarks]
  );

  return { bookmarks, isBookmarked, toggleBookmark, getBookmarksByType };
}
