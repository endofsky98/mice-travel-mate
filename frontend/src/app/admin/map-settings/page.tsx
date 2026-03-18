'use client';

import { useEffect, useState } from 'react';
import { MapPin, Save } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import LoadingSpinner from '@/components/ui/LoadingSpinner';

interface MapSettings {
  mapbox_api_key: string;
  default_center_lat: number;
  default_center_lng: number;
  default_zoom: number;
}

export default function AdminMapSettingsPage() {
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [settings, setSettings] = useState<MapSettings>({
    mapbox_api_key: '',
    default_center_lat: 37.5665,
    default_center_lng: 126.978,
    default_zoom: 12,
  });

  useEffect(() => {
    const fetchSettings = async () => {
      setLoading(true);
      try {
        const data = await api.get<MapSettings>('/api/admin/settings/map');
        setSettings(data);
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
    } catch { alert('Failed to save settings'); }
    setSaving(false);
  };

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Map Settings</h1>
        <Button onClick={handleSave} disabled={saving}>
          <Save className="w-4 h-4" />
          {saving ? 'Saving...' : saved ? 'Saved!' : 'Save Settings'}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Settings */}
        <div className="space-y-6">
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">API Configuration</h2>
            <Input
              label="Mapbox API Key"
              type="password"
              value={settings.mapbox_api_key}
              onChange={(e) => setSettings((p) => ({ ...p, mapbox_api_key: e.target.value }))}
              placeholder="pk.eyJ1Ijoi..."
            />
            <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
              Get your API key from <a href="https://account.mapbox.com/" target="_blank" rel="noopener noreferrer" className="text-indigo-600 dark:text-indigo-400 hover:underline">mapbox.com</a>
            </p>
          </Card>

          <Card className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Default View</h2>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="Center Latitude"
                  type="number"
                  step="any"
                  value={String(settings.default_center_lat)}
                  onChange={(e) => setSettings((p) => ({ ...p, default_center_lat: parseFloat(e.target.value) || 0 }))}
                />
                <Input
                  label="Center Longitude"
                  type="number"
                  step="any"
                  value={String(settings.default_center_lng)}
                  onChange={(e) => setSettings((p) => ({ ...p, default_center_lng: parseFloat(e.target.value) || 0 }))}
                />
              </div>
              <Input
                label="Default Zoom Level"
                type="number"
                min="1"
                max="20"
                value={String(settings.default_zoom)}
                onChange={(e) => setSettings((p) => ({ ...p, default_zoom: parseInt(e.target.value) || 12 }))}
              />
              <div className="flex flex-wrap gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSettings((p) => ({ ...p, default_center_lat: 37.5665, default_center_lng: 126.978, default_zoom: 12 }))}
                >
                  Seoul
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSettings((p) => ({ ...p, default_center_lat: 35.1796, default_center_lng: 129.0756, default_zoom: 12 }))}
                >
                  Busan
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSettings((p) => ({ ...p, default_center_lat: 33.4996, default_center_lng: 126.5312, default_zoom: 11 }))}
                >
                  Jeju
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSettings((p) => ({ ...p, default_center_lat: 35.8714, default_center_lng: 128.6014, default_zoom: 12 }))}
                >
                  Daegu
                </Button>
              </div>
            </div>
          </Card>
        </div>

        {/* Map Preview */}
        <Card className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">Map Preview</h2>
          <div className="w-full h-[400px] rounded-xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-green-50 dark:from-blue-950/30 dark:to-green-950/30" />
            <div className="relative text-center">
              <MapPin className="w-12 h-12 text-indigo-500 mx-auto mb-3" />
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Map Preview</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Center: {settings.default_center_lat.toFixed(4)}, {settings.default_center_lng.toFixed(4)}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Zoom: {settings.default_zoom}
              </p>
              {!settings.mapbox_api_key && (
                <p className="text-xs text-amber-600 dark:text-amber-400 mt-3">
                  Add a Mapbox API key to see the live preview
                </p>
              )}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
