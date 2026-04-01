'use client';

import { useEffect, useState } from 'react';
import { Bus, Train, Car, Footprints, CreditCard, Smartphone, MapPin, Ticket, ChevronDown, ChevronUp, Plane, BookOpen } from 'lucide-react';
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

const TRANSPORT_GUIDE_SECTIONS = [
  {
    id: 'subway',
    icon: Train,
    title: 'Seoul Subway',
    titleKo: '서울 지하철',
    color: 'from-blue-500 to-blue-600',
    content: {
      howToUse: {
        en: 'Seoul\'s subway system has 23 lines covering the entire metropolitan area. Signs and announcements are in Korean, English, Chinese, and Japanese. To ride, tap your T-money card or buy a single-trip token at the ticket machines (English available). Follow the color-coded line numbers and direction signs to find your platform.',
        ko: '서울 지하철은 23개 노선으로 수도권 전역을 연결합니다. 안내판과 안내방송은 한국어, 영어, 중국어, 일본어로 제공됩니다. T-money 카드를 태그하거나 발매기에서 1회권을 구매하세요. 색상별 노선 번호와 방향 안내를 따라 승강장을 찾으세요.',
      },
      fare: {
        en: 'Base fare: 1,250 KRW (T-money) / 1,350 KRW (cash token). Extra charges apply for distances over 10km. Operating hours: approximately 5:30 AM to midnight. Free transfers between bus and subway within 30 minutes.',
        ko: '기본 요금: 1,250원 (T-money) / 1,350원 (1회권). 10km 초과 시 추가 요금. 운행시간: 약 오전 5:30~자정. 30분 이내 버스-지하철 무료 환승.',
      },
      tips: {
        en: 'Download the "Subway Korea" or "KakaoMap" app for route planning. Avoid rush hours (8-9 AM, 6-7 PM). Priority seats are strictly reserved for elderly, disabled, and pregnant passengers. Keep your phone on silent mode.',
        ko: '"Subway Korea" 또는 "카카오맵" 앱으로 경로를 계획하세요. 출퇴근 시간(오전 8-9시, 오후 6-7시)을 피하세요. 노약자석은 반드시 양보하세요. 휴대폰은 진동 모드로 설정하세요.',
      },
      keyRoutes: {
        en: 'Line 2 (green circle): Gangnam, Hongdae, Jamsil\nLine 4 (light blue): Myeongdong, Seoul Station\nLine 9 (gold): Gimpo Airport, Express Bus Terminal\nAirport Railroad (AREX): Incheon Airport to Seoul Station',
        ko: '2호선 (녹색 순환): 강남, 홍대, 잠실\n4호선 (하늘색): 명동, 서울역\n9호선 (금색): 김포공항, 고속터미널\n공항철도 (AREX): 인천공항~서울역',
      },
    },
  },
  {
    id: 'bus',
    icon: Bus,
    title: 'City Bus',
    titleKo: '시내버스',
    color: 'from-emerald-500 to-teal-500',
    content: {
      howToUse: {
        en: 'Seoul buses are color-coded by type: Blue (trunk routes across the city), Green (neighborhood feeder routes), Red (express routes to suburbs), Yellow (circular routes in downtown). Board at the front door and tap your T-money card. Tap again when exiting at the rear door.',
        ko: '서울 버스는 유형별 색상 구분: 파란색 (간선, 시내 횡단), 초록색 (지선, 동네 연결), 빨간색 (광역, 교외 급행), 노란색 (순환, 도심 순환). 앞문으로 승차하여 T-money를 태그하고, 뒷문으로 하차 시 다시 태그하세요.',
      },
      fare: {
        en: 'Base fare: 1,200 KRW (T-money) / 1,300 KRW (cash). Red express buses: 2,300 KRW. Night buses (N-prefix): 2,150 KRW. Free transfer with subway within 30 minutes.',
        ko: '기본 요금: 1,200원 (T-money) / 1,300원 (현금). 빨간색 광역버스: 2,300원. 심야버스 (N 접두사): 2,150원. 30분 이내 지하철 무료 환승.',
      },
      tips: {
        en: 'Bus stop displays show real-time arrival info. Use KakaoMap or Naver Map to check bus routes. Many buses have USB charging ports. Night owl buses (N-prefix) run from midnight to 5 AM on major routes.',
        ko: '버스 정류장 전광판에서 실시간 도착 정보를 확인하세요. 카카오맵이나 네이버지도로 버스 노선을 확인하세요. 많은 버스에 USB 충전 포트가 있습니다. 심야버스(N 접두사)는 자정부터 오전 5시까지 주요 노선을 운행합니다.',
      },
      keyRoutes: {
        en: 'Bus 472: Gangnam to Gyeongbokgung\nBus 740: Seoul Station to COEX\nBus 6006: Incheon Airport to Gangnam\nBus N13: Night bus through Gangnam',
        ko: '472번: 강남~경복궁\n740번: 서울역~코엑스\n6006번: 인천공항~강남\nN13번: 강남 심야버스',
      },
    },
  },
  {
    id: 'taxi',
    icon: Car,
    title: 'Taxi',
    titleKo: '택시',
    color: 'from-amber-500 to-orange-500',
    content: {
      howToUse: {
        en: 'Hail a taxi on the street or use KakaoT app (recommended for foreigners). Regular taxis are orange or silver. Deluxe taxis are black and more spacious. International taxis at airports have English-speaking drivers. All taxis use meters.',
        ko: '길에서 택시를 잡거나 카카오T 앱을 사용하세요 (외국인 추천). 일반택시는 주황색 또는 은색, 모범택시는 검정색으로 더 넓습니다. 공항에는 영어 가능한 국제택시가 있습니다. 모든 택시는 미터기를 사용합니다.',
      },
      fare: {
        en: 'Regular taxi base fare: 4,800 KRW (first 1.6km). Additional: 100 KRW per 131m. Late night surcharge (20%): midnight to 4 AM. Deluxe taxi: 7,000 KRW base fare. T-money card and credit cards accepted.',
        ko: '일반택시 기본요금: 4,800원 (1.6km까지). 추가: 131m당 100원. 심야 할증(20%): 자정~오전 4시. 모범택시: 기본요금 7,000원. T-money 및 신용카드 사용 가능.',
      },
      tips: {
        en: 'Screenshot your destination in Korean to show the driver. KakaoT app shows fare estimate and provides translation. Tipping is not expected. Avoid "call taxis" from bars (overpriced). Check the taxi license plate matches the app.',
        ko: '목적지를 한국어로 캡처하여 기사님께 보여주세요. 카카오T 앱에서 예상 요금 확인 및 번역 기능을 제공합니다. 팁은 필요 없습니다. 바에서 호출하는 "콜택시"는 비쌀 수 있으니 주의하세요.',
      },
      keyRoutes: {
        en: 'Incheon Airport to Gangnam: ~75,000 KRW (55 min)\nGimpo Airport to COEX: ~35,000 KRW (35 min)\nGangnam to Hongdae: ~18,000 KRW (25 min)\nMyeongdong to Itaewon: ~8,000 KRW (10 min)',
        ko: '인천공항~강남: ~75,000원 (55분)\n김포공항~코엑스: ~35,000원 (35분)\n강남~홍대: ~18,000원 (25분)\n명동~이태원: ~8,000원 (10분)',
      },
    },
  },
  {
    id: 'ktx',
    icon: Train,
    title: 'KTX (High-Speed Rail)',
    titleKo: 'KTX (고속열차)',
    color: 'from-red-500 to-rose-600',
    content: {
      howToUse: {
        en: 'KTX is Korea\'s high-speed rail connecting major cities. Book tickets online at letskorail.com or at station ticket counters. Reserve seats in advance for weekends and holidays. Departs from Seoul Station or Yongsan Station.',
        ko: 'KTX는 주요 도시를 연결하는 한국의 고속열차입니다. letskorail.com에서 온라인 예매하거나 역 매표소에서 구매하세요. 주말과 공휴일에는 미리 좌석을 예약하세요. 서울역 또는 용산역에서 출발합니다.',
      },
      fare: {
        en: 'Seoul to Busan: ~59,800 KRW (2h 15min)\nSeoul to Daejeon: ~23,700 KRW (50min)\nSeoul to Gwangju: ~46,800 KRW (1h 50min)\nForeign tourist discount: Korea Rail Pass available',
        ko: '서울~부산: ~59,800원 (2시간 15분)\n서울~대전: ~23,700원 (50분)\n서울~광주: ~46,800원 (1시간 50분)\n외국인 할인: 코레일패스 이용 가능',
      },
      tips: {
        en: 'Buy a KORAIL Pass (foreigners only) for unlimited KTX rides: 1-day 67,600 KRW, 3-day 106,900 KRW. Free WiFi on board. Food cart service available. Luggage racks above seats and at car ends.',
        ko: '코레일패스(외국인 전용)로 KTX 무제한 탑승: 1일권 67,600원, 3일권 106,900원. 차내 무료 WiFi. 이동식 식당차 서비스. 좌석 위와 차량 끝에 짐 보관대가 있습니다.',
      },
      keyRoutes: {
        en: 'Seoul - Busan: 2h 15min (most popular)\nSeoul - Daejeon: 50min\nSeoul - Gwangju: 1h 50min\nSeoul - Gangneung: 1h 30min (via KTX-Eum)',
        ko: '서울~부산: 2시간 15분 (가장 인기)\n서울~대전: 50분\n서울~광주: 1시간 50분\n서울~강릉: 1시간 30분 (KTX-이음)',
      },
    },
  },
  {
    id: 'airport',
    icon: Plane,
    title: 'Airport Railroad (AREX)',
    titleKo: '공항철도 (AREX)',
    color: 'from-purple-500 to-violet-500',
    content: {
      howToUse: {
        en: 'AREX connects Incheon International Airport to Seoul Station. Two types: Express (non-stop, 43 min) and All-Stop (66 min, connects to other subway lines). Express train departs every 30-40 minutes. Buy tickets at airport basement level 1.',
        ko: 'AREX는 인천국제공항과 서울역을 연결합니다. 두 종류: 직통열차 (43분, 논스톱)와 일반열차 (66분, 다른 지하철 환승 가능). 직통열차는 30~40분 간격 운행. 공항 지하 1층에서 승차권을 구매하세요.',
      },
      fare: {
        en: 'Express train: 9,500 KRW (adult one-way)\nAll-Stop train: 1,250 KRW~4,750 KRW (varies by station, T-money)\nGimpo Airport to Seoul Station: 1,350 KRW (All-Stop)',
        ko: '직통열차: 9,500원 (성인 편도)\n일반열차: 1,250원~4,750원 (역별 상이, T-money)\n김포공항~서울역: 1,350원 (일반열차)',
      },
      tips: {
        en: 'Express train offers in-city check-in at Seoul Station for select airlines (check in luggage 3 hours before flight). The All-Stop train connects to Line 5, 9, and other subway lines at transfer stations. Last Express train from airport: ~10:40 PM.',
        ko: '직통열차는 서울역에서 일부 항공사 도심공항터미널 서비스 제공 (출발 3시간 전 수하물 체크인). 일반열차는 환승역에서 5호선, 9호선 등으로 환승 가능. 공항발 마지막 직통열차: ~오후 10:40.',
      },
      keyRoutes: {
        en: 'Incheon T1 - Seoul Station: 43min (Express) / 66min (All-Stop)\nIncheon T2 - Seoul Station: 51min (Express)\nIncheon Airport - Hongdae: 52min (All-Stop)\nGimpo Airport - Seoul Station: 20min (All-Stop)',
        ko: '인천 T1~서울역: 43분 (직통) / 66분 (일반)\n인천 T2~서울역: 51분 (직통)\n인천공항~홍대입구: 52분 (일반)\n김포공항~서울역: 20분 (일반)',
      },
    },
  },
];

function GuideSection({ section, language }: { section: typeof TRANSPORT_GUIDE_SECTIONS[0]; language: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const Icon = section.icon;
  const isKo = language === 'ko';

  return (
    <Card className="overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center gap-4 p-5 text-left hover:bg-gray-50 dark:hover:bg-white/[0.02] transition-colors"
      >
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${section.color} flex items-center justify-center flex-shrink-0`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">
            {isKo ? section.titleKo : section.title}
          </h3>
        </div>
        {isOpen ? (
          <ChevronUp className="w-5 h-5 text-gray-400 flex-shrink-0" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-400 flex-shrink-0" />
        )}
      </button>

      {isOpen && (
        <div className="px-5 pb-5 space-y-4 border-t border-gray-100 dark:border-gray-500/20 pt-4">
          <div>
            <h4 className="text-sm font-semibold text-indigo-600 dark:text-indigo-400 mb-2">
              {isKo ? '이용 방법' : 'How to Use'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
              {isKo ? section.content.howToUse.ko : section.content.howToUse.en}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-emerald-600 dark:text-emerald-400 mb-2">
              {isKo ? '요금 정보' : 'Fare Information'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed whitespace-pre-line">
              {isKo ? section.content.fare.ko : section.content.fare.en}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-amber-600 dark:text-amber-400 mb-2">
              {isKo ? '외국인 팁' : 'Tips for Foreigners'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
              {isKo ? section.content.tips.ko : section.content.tips.en}
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-purple-600 dark:text-purple-400 mb-2">
              {isKo ? '주요 노선' : 'Key Routes'}
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed whitespace-pre-line">
              {isKo ? section.content.keyRoutes.ko : section.content.keyRoutes.en}
            </p>
          </div>
        </div>
      )}
    </Card>
  );
}

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
    { id: 'routes', label: t('transport.routes') || 'Routes' },
    { id: 'tips', label: t('transport.tips') || 'Tips' },
    { id: 'guide', label: t('transport.guide') || 'Guide' },
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
                      <span className="text-sm font-medium text-indigo-700 dark:text-indigo-300">{route.from_name || lt(route.from)}</span>
                    </div>
                    <div className="flex-1 border-t-2 border-dashed border-gray-300 dark:border-gray-600" />
                    <div className="flex items-center gap-1 px-3 py-1.5 bg-emerald-50 dark:bg-emerald-900/30 rounded-lg">
                      <MapPin className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      <span className="text-sm font-medium text-emerald-700 dark:text-emerald-300">{route.to_name || lt(route.to)}</span>
                    </div>
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {(route.transport_modes || route.modes || []).map((mode, idx) => {
                    const Icon = modeIcons[mode.mode] || Bus;
                    const duration = mode.duration_minutes ? `${mode.duration_minutes}분` : mode.duration || '';
                    const cost = mode.cost_krw ? `₩${mode.cost_krw.toLocaleString()}` : mode.cost || '';
                    return (
                      <div key={idx} className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-dark-input">
                        <Icon className="w-5 h-5 text-gray-500 dark:text-gray-400 flex-shrink-0" />
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-medium text-gray-900 dark:text-gray-100 capitalize">{mode.mode}</span>
                            {duration && <Badge variant="info">{duration}</Badge>}
                          </div>
                          {cost && (
                            <span className="text-xs text-gray-500 dark:text-gray-400">{cost}</span>
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
                    <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{lt(tip.content || tip.description)}</p>
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

      {activeTab === 'guide' && (
        <div className="space-y-3">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {language === 'ko'
                ? '각 교통수단을 클릭하면 상세 가이드를 확인할 수 있습니다.'
                : 'Click on each transport mode to see detailed guides.'}
            </p>
          </div>
          {TRANSPORT_GUIDE_SECTIONS.map((section) => (
            <GuideSection key={section.id} section={section} language={language} />
          ))}
        </div>
      )}
    </div>
  );
}
