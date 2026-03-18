'use client';

import { useState, useEffect } from 'react';
import { MessageSquare, Flag, Camera, Send } from 'lucide-react';
import StarRating from './StarRating';
import api from '@/lib/api';
import { Review, ReviewStats } from '@/types';
import { cn } from '@/lib/utils';

interface ReviewSectionProps {
  targetType: string;
  targetId: string;
  t: (key: string) => string;
  isLoggedIn?: boolean;
}

export default function ReviewSection({ targetType, targetId, t, isLoggedIn }: ReviewSectionProps) {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [stats, setStats] = useState<ReviewStats | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [newRating, setNewRating] = useState(0);
  const [newContent, setNewContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchReviews();
    fetchStats();
  }, [targetType, targetId]);

  const fetchReviews = async () => {
    try {
      const data = await api.get<{ items: Review[] }>('/api/reviews', {
        target_type: targetType,
        target_id: targetId,
        per_page: 10,
      });
      setReviews(data.items || []);
    } catch { /* ignore */ }
  };

  const fetchStats = async () => {
    try {
      const data = await api.get<ReviewStats>('/api/reviews/stats', {
        target_type: targetType,
        target_id: targetId,
      });
      setStats(data);
    } catch { /* ignore */ }
  };

  const handleSubmit = async () => {
    if (newRating === 0 || newContent.length < 10) return;
    setSubmitting(true);
    try {
      await api.post('/api/reviews', {
        target_type: targetType,
        target_id: targetId,
        rating: newRating,
        content: newContent,
      });
      setNewRating(0);
      setNewContent('');
      setShowForm(false);
      fetchReviews();
      fetchStats();
    } catch { /* ignore */ }
    setSubmitting(false);
  };

  return (
    <div className="mt-8">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <MessageSquare className="w-5 h-5" />
        {t('review.avg_rating') || 'Reviews'}
      </h3>

      {/* Stats */}
      {stats && (
        <div className="flex items-center gap-6 mb-6 p-4 bg-gray-50 dark:bg-[#1e1e1e] rounded-xl">
          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900 dark:text-white">
              {stats.avg_rating > 0 ? stats.avg_rating.toFixed(1) : '-'}
            </div>
            <StarRating rating={stats.avg_rating} size="md" />
            <div className="text-xs text-gray-400 mt-1">
              {stats.total_count} {t('label.reviews') || 'reviews'}
            </div>
          </div>
          <div className="flex-1 space-y-1">
            {[5, 4, 3, 2, 1].map((star) => (
              <div key={star} className="flex items-center gap-2">
                <span className="text-xs text-gray-500 w-3">{star}</span>
                <div className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-amber-400 rounded-full"
                    style={{
                      width: stats.total_count > 0
                        ? `${((stats.distribution[star] || 0) / stats.total_count) * 100}%`
                        : '0%'
                    }}
                  />
                </div>
                <span className="text-xs text-gray-400 w-6 text-right">
                  {stats.distribution[star] || 0}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Write Review Button */}
      {isLoggedIn && !showForm && (
        <button
          onClick={() => setShowForm(true)}
          className="mb-4 px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-400 transition-colors"
        >
          {t('button.write_review') || 'Write a Review'}
        </button>
      )}

      {/* Review Form */}
      {showForm && (
        <div className="mb-6 p-4 border border-gray-200 dark:border-gray-500/40 rounded-xl">
          <div className="mb-3">
            <label className="text-sm text-gray-600 dark:text-gray-300 mb-1 block">
              {t('review.rating') || 'Rating'}
            </label>
            <StarRating rating={newRating} size="lg" interactive onChange={setNewRating} />
          </div>
          <textarea
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            placeholder={t('review.your_review') || 'Write your review (min 10 characters)...'}
            className="w-full px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-500/40 bg-transparent outline-none focus:ring-2 focus:ring-indigo-600/20 focus:border-indigo-600 dark:bg-[#2a2a2a] dark:text-gray-100 text-sm min-h-[100px] resize-none"
          />
          <div className="flex items-center justify-between mt-3">
            <span className="text-xs text-gray-400">{newContent.length}/10 min</span>
            <div className="flex gap-2">
              <button
                onClick={() => setShowForm(false)}
                className="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-white/5 rounded-lg"
              >
                {t('common.cancel') || 'Cancel'}
              </button>
              <button
                onClick={handleSubmit}
                disabled={submitting || newRating === 0 || newContent.length < 10}
                className="px-4 py-1.5 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? '...' : t('review.submit_review') || 'Submit'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Review List */}
      <div className="space-y-4">
        {reviews.map((review) => (
          <div key={review.id} className="p-4 bg-white dark:bg-[#1e1e1e] border border-gray-100 dark:border-gray-500/40 rounded-xl">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center">
                  <span className="text-xs font-medium text-indigo-600 dark:text-indigo-400">
                    {(review.user_name || 'U')[0].toUpperCase()}
                  </span>
                </div>
                <div>
                  <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {review.user_name || 'User'}
                  </div>
                  <div className="text-xs text-gray-400">
                    {new Date(review.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
              <StarRating rating={review.rating} size="sm" />
            </div>
            <p className="text-sm text-gray-700 dark:text-gray-300">{review.content}</p>
            {review.images && review.images.length > 0 && (
              <div className="flex gap-2 mt-3">
                {review.images.map((img, i) => (
                  <img key={i} src={img} alt="" className="w-16 h-16 rounded-lg object-cover" />
                ))}
              </div>
            )}
          </div>
        ))}
        {reviews.length === 0 && (
          <p className="text-sm text-gray-400 text-center py-8">
            {t('common.no_results') || 'No reviews yet'}
          </p>
        )}
      </div>
    </div>
  );
}
