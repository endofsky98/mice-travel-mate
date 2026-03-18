'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { UserCheck, Mail, Lock } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import { login } from '@/lib/auth';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

export default function GuideLoginPage() {
  const { t } = useLanguage();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    setLoading(true);
    setError('');
    try {
      await login(email, password);
      router.push('/guide-dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-50 to-indigo-50 dark:from-[#141414] dark:to-[#1a1a1a]">
      <Card className="w-full max-w-md p-8">
        <div className="flex items-center gap-2 justify-center mb-8">
          <UserCheck className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
          <span className="text-xl font-bold text-gray-900 dark:text-white">Guide Portal</span>
        </div>

        <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-1 text-center">
          {t('guide.login_title') || 'Guide Login'}
        </h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 text-center">
          {t('guide.login_subtitle') || 'Sign in to manage your bookings and schedule'}
        </p>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-300 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
            <Input
              type="email"
              placeholder={t('auth.email') || 'Email'}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10"
              required
            />
          </div>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
            <Input
              type="password"
              placeholder={t('auth.password') || 'Password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10"
              required
            />
          </div>
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? (t('common.loading') || 'Loading...') : (t('auth.login') || 'Sign In')}
          </Button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
          {t('guide.login_help') || 'Contact the admin if you need a guide account'}
        </p>
      </Card>
    </div>
  );
}
