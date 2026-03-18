'use client';

import { useEffect, useState } from 'react';
import { Bus, Train, Car, Footprints, CreditCard, Smartphone, MapPin, Ticket } from 'lucide-react';
import { useLanguage } from '@/hooks/useLanguage';
import api from '@/lib/api';
import Tabs from '@/components/ui/Tabs';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { TransportRoute, TransportTip } from '@/types';

const modeIcons: Record<string, typeof Bus> = {
  subway: Train,
  bus: Bus,
  taxi: Car,
  walk: Footprints,
};

const tipIcons: Record<string, typeof Bus> = {
  tmoney: CreditCard,
  taxi: Car,
  apps: Smartphone,
  pass: Ticket,
};

export default function TransportPage() {
  const { t, lt, language } = useLanguage();
  const [activeTab, setActiveTab] = useState('routes');
  const [loading, setLoading] = useState(true);
  const [routes, setRoutes] = useState<TransportRoute[]>([]);
  const [tips, setTips] = useState<TransportTip[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [routeData, tipData] = await Promise.all([
          api.get<{ items: TransportRoute[] }>('/api/transport/routes').catch(() => ({ items: [] })),
          api.get<{ items: TransportTip[] }>('/api/transport/tips').catch(() => ({ items: [] })),
        ]);
        setRoutes(routeData.items || []);
        setTips(tipData.items || []);
      } catch {
        setRoutes([]);
        setTips([]);
      }
      setLoading(false);
    };
    fetchData();
  }, [language]);

  const tabs = [
    { id: 'routes', label: t('transport.routes') },
    { id: 'tips', label: t('transport.tips') },
  ];

  const defaultTips = [
    {
      icon: CreditCard,
      title: t('transport.tmoney'),
      description: t('transport.tmoney_desc'),
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: Car,
      title: t('transport.taxi_tip'),
      description: t('transport.taxi_tip_desc'),
      color: 'from-amber-500 to-orange-500',
    },
    {
      icon: Smartphone,
      title: t('transport.useful_apps'),
      description: t('transport.useful_apps_desc'),
      color: 'from-emerald-500 to-teal-500',
    },
    {
      icon: Ticket,
      title: t('transport.tourist_pass'),
      description: t('transport.tourist_pass_desc'),
      color: 'from-purple-500 to-violet-500',
    },
  ];

  if (loading) return <LoadingSpinner fullPage />;

  return (
    <div className="page-container">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">{t('transport.title')}</h1>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="mb-6" />

      {activeTab === 'routes' && (
        <div className="space-y-4">
          {routes.length > 0 ? (
            routes.map((route) => (
              <Card key={route.id} className="p-4">
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex items-center gap-2 flex-1">
                    <div className="flex items-center gap-1 px-3 py-1.5 bg-indigo-50 dark:bg-indigo-900/30 rounded-lg">
                      <MapPin className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                      <span className="text-sm font-medium text-indigo-700 dark:text-indigo-300">{lt(route.from)}</span>
                    </div>
                    <div className="flex-1 border-t-2 border-dashed border-gray-300 dark:border-gray-600" />
                    <div className="flex items-center gap-1 px-3 py-1.5 bg-emerald-50 dark:bg-emerald-900/30 rounded-lg">
                      <MapPin className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      <span className="text-sm font-medium text-emerald-700 dark:text-emerald-300">{lt(route.to)}</span>
                    </div>
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {route.modes.map((mode, idx) => {
                    const Icon = modeIcons[mode.mode] || Bus;
                    return (
                      <div key={idx} className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-dark-input">
                        <Icon className="w-5 h-5 text-gray-500 dark:text-gray-400 flex-shrink-0" />
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-gray-900 dark:text-gray-100 capitalize">{mode.mode}</span>
                            <Badge variant="info">{mode.duration}</Badge>
                          </div>
                          {mode.cost && (
                            <span className="text-xs text-gray-500 dark:text-gray-400">{mode.cost}</span>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Card>
            ))
          ) : (
            <div className="text-center py-12">
              <Bus className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-3" />
              <p className="text-gray-500 dark:text-gray-400">{t('common.no_results')}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'tips' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {(tips.length > 0 ? tips : []).map((tip, idx) => {
            const Icon = tipIcons[tip.category] || tipIcons[Object.keys(tipIcons)[idx]] || Bus;
            return (
              <Card key={tip.id || idx} className="p-6">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">{lt(tip.title)}</h3>
                    <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{lt(tip.description)}</p>
                  </div>
                </div>
              </Card>
            );
          })}

          {tips.length === 0 && defaultTips.map((tip, idx) => (
            <Card key={idx} className="p-6">
              <div className="flex items-start gap-4">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${tip.color} flex items-center justify-center flex-shrink-0`}>
                  <tip.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">{tip.title}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{tip.description}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
