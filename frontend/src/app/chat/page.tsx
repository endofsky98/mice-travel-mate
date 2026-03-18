'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { MessageCircle } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useAuth } from '@/hooks/useAuth';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import EmptyState from '@/components/ui/EmptyState';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { ChatRoom } from '@/types';
import Link from 'next/link';

export default function ChatPage() {
  const { t, language } = useLanguage();
  const { isLoggedIn, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const [rooms, setRooms] = useState<ChatRoom[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isLoggedIn) {
      router.push('/auth/login');
      return;
    }
    if (isLoggedIn) {
      fetchRooms();
    }
  }, [authLoading, isLoggedIn]);

  const fetchRooms = async () => {
    try {
      const data = await api.get<{ items: ChatRoom[] }>('/api/chat/rooms');
      setRooms(data.items || []);
    } catch {
      setRooms([]);
    }
    setLoading(false);
  };

  if (authLoading || loading) return <LoadingSpinner fullPage />;

  return (
    <div className="page-container max-w-2xl">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
        {t('nav.chat') || 'Chat'}
      </h1>

      {rooms.length === 0 ? (
        <EmptyState
          icon={MessageCircle}
          title={t('chat.no_messages') || 'No conversations yet'}
          description={t('chat.start_chat') || 'Start a chat from a guide\'s detail page'}
        />
      ) : (
        <div className="space-y-2">
          {rooms.map((room) => (
            <Link key={room.id} href={`/chat/${room.id}`}>
              <Card hoverable className="p-4 flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center flex-shrink-0">
                  {room.guide_image ? (
                    <img src={room.guide_image} alt="" className="w-12 h-12 rounded-full object-cover" />
                  ) : (
                    <MessageCircle className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium text-gray-900 dark:text-gray-100">{room.guide_name || 'Guide'}</h3>
                    {room.last_message_at && (
                      <span className="text-xs text-gray-400">
                        {new Date(room.last_message_at).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400 truncate">{room.last_message || '...'}</p>
                </div>
                {room.unread_count > 0 && (
                  <div className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs flex items-center justify-center flex-shrink-0">
                    {room.unread_count}
                  </div>
                )}
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
