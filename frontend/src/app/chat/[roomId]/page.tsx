'use client';

import { useEffect, useState, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, Send, Image } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { useAuth } from '@/hooks/useAuth';
import api from '@/lib/api';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { ChatMessage } from '@/types';
import { cn } from '@/lib/utils';

export default function ChatRoomPage() {
  const { roomId } = useParams();
  const router = useRouter();
  const { t } = useLanguage();
  const { user } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const pollRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetchMessages();
    // Poll for new messages every 5s
    pollRef.current = setInterval(fetchMessages, 5000);
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [roomId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchMessages = async () => {
    try {
      const data = await api.get<{ items: ChatMessage[] }>(`/api/chat/rooms/${roomId}/messages`, { per_page: 100 });
      setMessages(data.items || []);
    } catch { /* */ }
    setLoading(false);
  };

  const handleSend = async () => {
    if (!newMessage.trim() || sending) return;
    setSending(true);
    try {
      await api.post(`/api/chat/rooms/${roomId}/messages`, {
        message_type: 'text',
        content: newMessage.trim(),
      });
      setNewMessage('');
      fetchMessages();
    } catch { /* */ }
    setSending(false);
  };

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div className="flex flex-col h-[calc(100vh-64px)]">
      {/* Header */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-200 dark:border-gray-500/40 bg-white dark:bg-[#141414]">
        <button onClick={() => router.back()} className="p-1">
          <ArrowLeft className="w-5 h-5 text-gray-600 dark:text-gray-300" />
        </button>
        <h1 className="font-semibold text-gray-900 dark:text-gray-100">{t('nav.chat') || 'Chat'}</h1>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50 dark:bg-[#1a1a1a]">
        {messages.map((msg) => {
          const isMe = msg.sender_type === 'user';
          return (
            <div key={msg.id} className={cn('flex', isMe ? 'justify-end' : 'justify-start')}>
              <div className={cn(
                'max-w-[75%] px-4 py-2.5 rounded-2xl text-sm',
                isMe
                  ? 'bg-indigo-600 text-white rounded-br-md'
                  : 'bg-white dark:bg-[#1e1e1e] text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-500/40 rounded-bl-md'
              )}>
                {msg.message_type === 'image' && msg.image_url ? (
                  <img src={msg.image_url} alt="" className="rounded-lg max-w-full" />
                ) : (
                  <p>{msg.content}</p>
                )}
                <div className={cn('text-[10px] mt-1', isMe ? 'text-white/60' : 'text-gray-400')}>
                  {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  {isMe && msg.is_read && <span className="ml-1">✓</span>}
                </div>
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-500/40 bg-white dark:bg-[#141414] flex items-center gap-2">
        <button className="p-2 text-gray-400 hover:text-gray-600">
          <Image className="w-5 h-5" />
        </button>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={t('chat.type_message') || 'Type a message...'}
          className="flex-1 px-4 py-2.5 rounded-full border border-gray-200 dark:border-gray-500/40 bg-gray-50 dark:bg-[#2a2a2a] text-sm outline-none focus:ring-2 focus:ring-indigo-600/20 dark:text-gray-100"
        />
        <button
          onClick={handleSend}
          disabled={!newMessage.trim() || sending}
          className="p-2.5 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
