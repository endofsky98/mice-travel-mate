'use client';

import { useEffect, useState } from 'react';
import { MapPin, Save, Key } from 'lucide-react';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

interface MapSettings {
  map_engine: string;
  mapbox_api_key: string;
  google_maps_api_key: string;
  google_oauth_client_id: string;
  google_oauth_client_secret: string;
  default_center_lat: number;
  default_center_lng: number;
  default_zoom: number;
}

export default function AdminMapSettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [settings, setSettings] = useState<MapSettings>({
    map_engine: 'mapbox',
    mapbox_api_key: '',
    google_maps_api_key: '',
    google_oauth_client_id: '',
    google_oauth_client_secret: '',
    default_center_lat: 37.5665,
    default_center_lng: 126.978,
    default_zoom: 12,
  });

  useEffect(() => {
    const fetchSettings = async () => {
      setLoading(true);
      try {
        const data = await api.get<MapSettings>('/api/admin/settings/map');
        setSettings(prev => ({ ...prev, ...data }));
      } catch {
        // Use defaults
      }
      setLoading(false);
    };
    fetchSettings();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    try {
      await api.put('/api/admin/settings/map', settings);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch { alert('설정 저장에 실패했습니다'); }
    setSaving(false);
  };

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">지도 및 API 설정</h1>
        <Button onClick={handleSave} disabled={saving}>
          <Save className="w-4 h-4" />
          {saving ? '저장 중...' : saved ? '저장 완료!' : '설정 저장'}
        </Button>
      </div>

      <div className="space-y-6">
        {/* Map Engine Selection */}
        <Card className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">지도 엔진 선택</h2>
          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => setSettings(p => ({ ...p, map_engine: 'mapbox' }))}
              className={`p-4 rounded-xl border-2 text-left transition-all ${
                settings.map_engine === 'mapbox'
                  ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20 dark:border-indigo-500'
                  : 'border-gray-200 dark:border-gray-500/40 hover:border-gray-300'
              }`}
            >
              <div className="font-semibold text-gray-900 dark:text-gray-100 mb-1">Mapbox</div>
              <p className="text-xs text-gray-500 dark:text-gray-400">고품질 벡터 지도, 커스텀 스타일</p>
            </button>
            <button
              onClick={() => setSettings(p => ({ ...p, map_engine: 'google' }))}
              className={`p-4 rounded-xl border-2 text-left transition-all ${
                settings.map_engine === 'google'
                  ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20 dark:border-indigo-500'
                  : 'border-gray-200 dark:border-gray-500/40 hover:border-gray-300'
              }`}
            >
              <div className="font-semibold text-gray-900 dark:text-gray-100 mb-1">Google Maps</div>
              <p className="text-xs text-gray-500 dark:text-gray-400">Google Maps JavaScript API</p>
            </button>
          </div>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Map API Keys */}
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">지도 API 키</h2>
            <div className="space-y-4">
              <div>
                <Input
                  label="Mapbox API 키"
                  type="password"
                  value={settings.mapbox_api_key}
                  onChange={(e) => setSettings(p => ({ ...p, mapbox_api_key: e.target.value }))}
                  placeholder="pk.eyJ1Ijoi..."
                />
                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  <a href="https://account.mapbox.com/" target="_blank" rel="noopener noreferrer" className="text-indigo-600 dark:text-indigo-400 hover:underline">mapbox.com</a>에서 발급
                </p>
              </div>
              <div>
                <Input
                  label="Google Maps API 키"
                  type="password"
                  value={settings.google_maps_api_key}
                  onChange={(e) => setSettings(p => ({ ...p, google_maps_api_key: e.target.value }))}
                  placeholder="AIzaSy..."
                />
                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  <a href="https://console.cloud.google.com/apis/credentials" target="_blank" rel="noopener noreferrer" className="text-indigo-600 dark:text-indigo-400 hover:underline">Google Cloud Console</a>에서 발급
                </p>
              </div>
            </div>
          </Card>

          {/* Google OAuth */}
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1 flex items-center gap-2">
              <Key className="w-5 h-5" />
              Google 로그인 설정
            </h2>
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-4">Google OAuth를 위한 Client ID/Secret을 입력하세요</p>
            <div className="space-y-4">
              <Input
                label="Google OAuth Client ID"
                type="password"
                value={settings.google_oauth_client_id}
                onChange={(e) => setSettings(p => ({ ...p, google_oauth_client_id: e.target.value }))}
                placeholder="xxxxx.apps.googleusercontent.com"
              />
              <Input
                label="Google OAuth Client Secret"
                type="password"
                value={settings.google_oauth_client_secret}
                onChange={(e) => setSettings(p => ({ ...p, google_oauth_client_secret: e.target.value }))}
                placeholder="GOCSPX-..."
              />
              <p className="text-xs text-gray-500 dark:text-gray-400">
                <a href="https://console.cloud.google.com/apis/credentials" target="_blank" rel="noopener noreferrer" className="text-indigo-600 dark:text-indigo-400 hover:underline">Google Cloud Console</a> → OAuth 2.0 클라이언트 ID에서 발급
              </p>
            </div>
          </Card>
        </div>

        {/* Default Map Display */}
        <Card className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">기본 표시 설정</h2>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="중심 위도"
                type="number"
                step="any"
                value={String(settings.default_center_lat)}
                onChange={(e) => setSettings(p => ({ ...p, default_center_lat: parseFloat(e.target.value) || 0 }))}
              />
              <Input
                label="중심 경도"
                type="number"
                step="any"
                value={String(settings.default_center_lng)}
                onChange={(e) => setSettings(p => ({ ...p, default_center_lng: parseFloat(e.target.value) || 0 }))}
              />
            </div>
            <Input
              label="기본 줌 레벨"
              type="number"
              min="1"
              max="20"
              value={String(settings.default_zoom)}
              onChange={(e) => setSettings(p => ({ ...p, default_zoom: parseInt(e.target.value) || 12 }))}
            />
            <div className="flex flex-wrap gap-2">
              <Button variant="outline" size="sm" onClick={() => setSettings(p => ({ ...p, default_center_lat: 37.5665, default_center_lng: 126.978, default_zoom: 12 }))}>서울</Button>
              <Button variant="outline" size="sm" onClick={() => setSettings(p => ({ ...p, default_center_lat: 35.1796, default_center_lng: 129.0756, default_zoom: 12 }))}>부산</Button>
              <Button variant="outline" size="sm" onClick={() => setSettings(p => ({ ...p, default_center_lat: 33.4996, default_center_lng: 126.5312, default_zoom: 11 }))}>제주</Button>
              <Button variant="outline" size="sm" onClick={() => setSettings(p => ({ ...p, default_center_lat: 35.8714, default_center_lng: 128.6014, default_zoom: 12 }))}>대구</Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
