'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Compass, Mail, Lock } from 'lucide-react';
import { adminLogin } from '@/lib/auth';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';

export default function AdminLoginPage() {
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
      await adminLogin(email, password);
      router.push('/admin');
    } catch (err) {
      setError(err instanceof Error ? err.message : '로그인에 실패했습니다');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-gray-50 to-indigo-50 dark:from-dark-main dark:to-dark-sidebar">
      <Card className="w-full max-w-md p-8">
        <div className="flex items-center gap-2 justify-center mb-8">
          <Compass className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
          <span className="text-xl font-bold text-gray-900 dark:text-white">관리자 패널</span>
        </div>

        <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-1 text-center">관리자 로그인</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 text-center">관리자 계정으로 로그인해 주세요</p>

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
              placeholder="이메일"
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
              placeholder="비밀번호"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10"
              required
            />
          </div>
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? '로딩 중...' : '로그인'}
          </Button>
        </form>
      </Card>
    </div>
  );
}
