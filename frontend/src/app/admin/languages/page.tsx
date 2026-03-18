'use client';

import { useEffect, useState, useCallback } from 'react';
import { Globe, Plus, Save, AlertTriangle } from 'lucide-react';
import api from '@/lib/api';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Badge from '@/components/ui/Badge';
import Tabs from '@/components/ui/Tabs';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { SUPPORTED_LANGUAGES } from '@/types';

interface LanguageSetting {
  code: string;
  name: string;
  is_active: boolean;
}

interface TranslationEntry {
  key: string;
  values: Record<string, string>;
}

export default function AdminLanguagesPage() {
  const [loading, setLoading] = useState(true);
  const [languages, setLanguages] = useState<LanguageSetting[]>([]);
  const [activeTab, setActiveTab] = useState('languages');
  const [translations, setTranslations] = useState<TranslationEntry[]>([]);
  const [selectedLang, setSelectedLang] = useState('en');
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => { fetchLanguages(); }, []);

  const fetchTranslations = useCallback(async () => {
    try {
      const data = await api.get<{ items: TranslationEntry[] }>('/api/admin/translations', { lang: selectedLang });
      setTranslations(data.items || []);
    } catch { setTranslations([]); }
  }, [selectedLang]);

  useEffect(() => { if (activeTab === 'translations') fetchTranslations(); }, [activeTab, selectedLang, fetchTranslations]);

  const fetchLanguages = async () => {
    setLoading(true);
    try {
      const data = await api.get<{ items: LanguageSetting[] }>('/api/admin/languages');
      setLanguages(data.items || SUPPORTED_LANGUAGES.map((l) => ({ code: l.code, name: l.name, is_active: true })));
    } catch {
      setLanguages(SUPPORTED_LANGUAGES.map((l) => ({ code: l.code, name: l.name, is_active: true })));
    }
    setLoading(false);
  };

  const toggleLanguage = async (code: string, isActive: boolean) => {
    try {
      await api.patch(`/api/admin/languages/${code}`, { is_active: !isActive });
      setLanguages((prev) => prev.map((l) => l.code === code ? { ...l, is_active: !isActive } : l));
    } catch { alert('업데이트에 실패했습니다'); }
  };

  const handleAddTranslation = async () => {
    if (!newKey || !newValue) return;
    setSaving(true);
    try {
      await api.post('/api/admin/translations', { key: newKey, value: newValue, lang: selectedLang });
      setNewKey(''); setNewValue('');
      fetchTranslations();
    } catch { alert('저장에 실패했습니다'); }
    setSaving(false);
  };

  const handleUpdateTranslation = async (key: string, value: string) => {
    try {
      await api.put('/api/admin/translations', { key, value, lang: selectedLang });
    } catch { alert('업데이트에 실패했습니다'); }
  };

  const tabs = [
    { id: 'languages', label: '언어 설정' },
    { id: 'translations', label: '번역 관리' },
  ];

  const langTabs = SUPPORTED_LANGUAGES.map((l) => ({ id: l.code, label: l.name }));

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">언어 관리</h1>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

      {activeTab === 'languages' && (
        <div className="space-y-3">
          {languages.map((lang) => (
            <Card key={lang.code} className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Globe className="w-5 h-5 text-gray-400" />
                <div>
                  <p className="font-medium text-gray-900 dark:text-gray-100">{lang.name}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{lang.code}</p>
                </div>
              </div>
              <button
                onClick={() => toggleLanguage(lang.code, lang.is_active)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  lang.is_active ? 'bg-indigo-600' : 'bg-gray-300 dark:bg-gray-600'
                }`}
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  lang.is_active ? 'translate-x-6' : 'translate-x-1'
                }`} />
              </button>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'translations' && (
        <div>
          <Tabs tabs={langTabs} activeTab={selectedLang} onChange={setSelectedLang} className="mb-6" />

          {/* Add new translation */}
          <Card className="p-4 mb-6">
            <div className="flex flex-col sm:flex-row gap-3">
              <Input
                placeholder="번역 키"
                value={newKey}
                onChange={(e) => setNewKey(e.target.value)}
                className="flex-1"
              />
              <Input
                placeholder="번역 값"
                value={newValue}
                onChange={(e) => setNewValue(e.target.value)}
                className="flex-1"
              />
              <Button onClick={handleAddTranslation} disabled={saving}>
                <Plus className="w-4 h-4" />
                추가
              </Button>
            </div>
          </Card>

          {/* Translation list */}
          <Card className="overflow-hidden">
            <div className="overflow-x-auto"><table className="w-full">
              <thead className="bg-gray-50 dark:bg-dark-input"><tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">키</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">값</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase w-20">상태</th>
              </tr></thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-500/40">
                {translations.length === 0 ? (
                  <tr><td colSpan={3} className="px-6 py-8 text-center text-sm text-gray-500">결과가 없습니다</td></tr>
                ) : translations.map((entry) => (
                  <tr key={`${entry.key}-${selectedLang}`} className="hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <td className="px-6 py-3 text-sm font-mono text-gray-500 dark:text-gray-400">{entry.key}</td>
                    <td className="px-6 py-3">
                      <input
                        type="text"
                        key={`${entry.key}-${selectedLang}`}
                        defaultValue={entry.values[selectedLang] || ''}
                        onBlur={(e) => handleUpdateTranslation(entry.key, e.target.value)}
                        className="w-full text-sm px-2 py-1 rounded border border-transparent hover:border-gray-200 focus:border-indigo-600 focus:ring-1 focus:ring-indigo-600/20 outline-none bg-transparent dark:text-gray-100"
                      />
                    </td>
                    <td className="px-6 py-3">
                      {!entry.values[selectedLang] && (
                        <Badge variant="warning"><AlertTriangle className="w-3 h-3 mr-1" />미번역</Badge>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table></div>
          </Card>
        </div>
      )}
    </div>
  );
}
