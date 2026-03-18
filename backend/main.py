import uuid
import logging
from datetime import datetime, date
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text

from config import settings
from database import engine, Base, async_session
from models import (
    User, Bookmark,
    Event, EventRestaurant, EventCourse, EventProduct, EventGuide,
    Restaurant,
    Course, CourseSpot, CourseSpotTransition,
    TransportRoute, TransportTip,
    Product, ProductInventory,
    Guide, GuideAvailability,
    Booking,
    Language, UITranslation,
)
from routers import auth, events, restaurants, courses, transport, products, guides, bookings, languages
from routers import bookmarks, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_migrations(conn):
    """Run ALTER TABLE migrations with try/except for idempotency."""
    migrations = [
        "ALTER TABLE users ADD COLUMN reset_token VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN reset_token_expires DATETIME",
    ]
    for migration in migrations:
        try:
            await conn.execute(text(migration))
            logger.info("Migration applied: %s", migration[:60])
        except Exception:
            pass  # Column already exists


async def seed_languages(session):
    """Seed default languages."""
    result = await session.execute(select(Language))
    if result.scalars().first():
        return  # Already seeded

    default_languages = [
        Language(code="en", name_en="English", name_native="English", is_active=True, display_order=1),
        Language(code="ko", name_en="Korean", name_native="한국어", is_active=True, display_order=2),
        Language(code="zh-CN", name_en="Chinese (Simplified)", name_native="中文(简体)", is_active=True, display_order=3),
        Language(code="zh-TW", name_en="Chinese (Traditional)", name_native="中文(繁體)", is_active=True, display_order=4),
        Language(code="ja", name_en="Japanese", name_native="日本語", is_active=True, display_order=5),
        Language(code="es", name_en="Spanish", name_native="Español", is_active=True, display_order=6),
    ]
    for lang in default_languages:
        session.add(lang)
    await session.flush()
    logger.info("Seeded %d languages", len(default_languages))


async def seed_admin_user(session):
    """Seed default admin user."""
    import bcrypt

    result = await session.execute(select(User).where(User.email == settings.DEFAULT_ADMIN_EMAIL))
    if result.scalar_one_or_none():
        return  # Already exists

    hashed = bcrypt.hashpw(settings.DEFAULT_ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    admin_user = User(
        id=str(uuid.uuid4()),
        email=settings.DEFAULT_ADMIN_EMAIL,
        password_hash=hashed,
        name=settings.DEFAULT_ADMIN_NAME,
        role="superadmin",
        provider="local",
        is_active=True,
    )
    session.add(admin_user)
    await session.flush()
    logger.info("Seeded admin user: %s", settings.DEFAULT_ADMIN_EMAIL)


async def seed_sample_data(session):
    """Seed sample events, restaurants, courses, products, guides, transport."""
    # Check if data already exists
    result = await session.execute(select(Event))
    if result.scalars().first():
        return

    # ── Events ──
    event1_id = str(uuid.uuid4())
    event2_id = str(uuid.uuid4())
    event3_id = str(uuid.uuid4())

    events = [
        Event(
            id=event1_id,
            slug="coex-food-expo-2026",
            name_en="COEX Food & Hotel Expo 2026",
            name_ko="코엑스 식품호텔 엑스포 2026",
            name_ja="COEX フード&ホテルエキスポ 2026",
            name_zh_cn="COEX 食品酒店博览会 2026",
            description_en="Asia's premier food and hospitality exhibition at COEX, Seoul. Featuring over 500 exhibitors from 30 countries.",
            description_ko="서울 코엑스에서 열리는 아시아 최대의 식품 및 호텔 전시회. 30개국 500여 업체 참가.",
            venue_name="COEX Convention & Exhibition Center",
            venue_address="513 Yeongdong-daero, Gangnam-gu, Seoul",
            latitude=37.5116,
            longitude=127.0595,
            start_date=date(2026, 5, 12),
            end_date=date(2026, 5, 15),
            banner_image_url="https://images.unsplash.com/photo-1540575467063-178a50c6da87?w=1200",
            is_active=True,
        ),
        Event(
            id=event2_id,
            slug="kintex-auto-show-2026",
            name_en="KINTEX International Auto Show 2026",
            name_ko="킨텍스 국제 오토쇼 2026",
            name_ja="KINTEX 国際オートショー 2026",
            name_zh_cn="KINTEX 国际车展 2026",
            description_en="Korea's largest automotive exhibition showcasing next-gen EVs, autonomous driving, and mobility solutions.",
            description_ko="차세대 EV, 자율주행, 모빌리티 솔루션을 선보이는 한국 최대 자동차 전시회.",
            venue_name="KINTEX (Korea International Exhibition Center)",
            venue_address="217-60 Kintex-ro, Ilsanseo-gu, Goyang-si, Gyeonggi-do",
            latitude=37.6716,
            longitude=126.7467,
            start_date=date(2026, 6, 20),
            end_date=date(2026, 6, 28),
            banner_image_url="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1200",
            is_active=True,
        ),
        Event(
            id=event3_id,
            slug="bexco-it-week-2026",
            name_en="BEXCO IT Week 2026",
            name_ko="벡스코 IT 위크 2026",
            name_ja="BEXCO ITウィーク 2026",
            name_zh_cn="BEXCO IT周 2026",
            description_en="Busan's flagship IT and tech conference with exhibitions on AI, cloud, and cybersecurity.",
            description_ko="AI, 클라우드, 사이버보안 등 부산 대표 IT 기술 컨퍼런스 및 전시회.",
            venue_name="BEXCO (Busan Exhibition & Convention Center)",
            venue_address="55 APEC-ro, Haeundae-gu, Busan",
            latitude=35.1695,
            longitude=129.1362,
            start_date=date(2026, 9, 1),
            end_date=date(2026, 9, 4),
            banner_image_url="https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200",
            is_active=True,
        ),
    ]
    for e in events:
        session.add(e)

    # ── Restaurants ──
    rest1_id = str(uuid.uuid4())
    rest2_id = str(uuid.uuid4())
    rest3_id = str(uuid.uuid4())

    restaurants = [
        Restaurant(
            id=rest1_id,
            name_en="Gogung Bibimbap",
            name_ko="고궁 비빔밥",
            name_ja="コグン ビビンバ",
            description_en="Famous for traditional Jeonju-style bibimbap served in a hot stone bowl. A must-try Korean classic near COEX.",
            description_ko="전주식 돌솥비빔밥으로 유명한 코엑스 인근 한식 맛집.",
            category="korean",
            price_range=2,
            address="159 Samseong-dong, Gangnam-gu, Seoul",
            latitude=37.5089,
            longitude=127.0609,
            phone="02-6002-3456",
            opening_hours={"mon-fri": "11:00-21:30", "sat-sun": "11:00-21:00"},
            menu_highlights={
                "en": ["Jeonju Bibimbap", "Bulgogi Set", "Haemul Pajeon"],
                "ko": ["전주비빔밥", "불고기 세트", "해물파전"],
            },
            images=[
                "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=600",
                "https://images.unsplash.com/photo-1617196035154-1e7e6e28b0db?w=600",
            ],
            is_active=True,
        ),
        Restaurant(
            id=rest2_id,
            name_en="Myeongdong Kyoja",
            name_ko="명동교자",
            name_ja="明洞餃子",
            description_en="Legendary noodle and dumpling house in the heart of Myeongdong. Handmade kalguksu and mandu since 1966.",
            description_ko="1966년부터 이어온 명동의 전설적인 칼국수·만두 전문점.",
            category="korean",
            price_range=1,
            address="29 Myeongdong 10-gil, Jung-gu, Seoul",
            latitude=37.5636,
            longitude=126.9863,
            phone="02-776-5348",
            opening_hours={"mon-sun": "10:30-21:00"},
            menu_highlights={
                "en": ["Kalguksu (Knife-cut Noodles)", "Mandu (Dumplings)", "Bibim Guksu"],
                "ko": ["칼국수", "만두", "비빔국수"],
            },
            images=[
                "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600",
            ],
            is_active=True,
        ),
        Restaurant(
            id=rest3_id,
            name_en="Haeundae Sashimi Alley",
            name_ko="해운대 횟집 골목",
            name_ja="海雲台 刺身横丁",
            description_en="Fresh sashimi and seafood restaurants along Haeundae Beach in Busan. Perfect after visiting BEXCO.",
            description_ko="부산 해운대 해변을 따라 늘어선 신선한 회·해산물 맛집 거리.",
            category="japanese",
            price_range=3,
            address="264 Haeundaehaebyeon-ro, Haeundae-gu, Busan",
            latitude=35.1587,
            longitude=129.1605,
            phone="051-747-0001",
            opening_hours={"mon-sun": "10:00-22:00"},
            menu_highlights={
                "en": ["Sashimi Platter", "Grilled Eel", "Sea Urchin Rice"],
                "ko": ["모듬회", "장어구이", "성게비빔밥"],
            },
            images=[
                "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=600",
            ],
            is_active=True,
        ),
    ]
    for r in restaurants:
        session.add(r)

    # ── Courses ──
    course1_id = str(uuid.uuid4())
    course2_id = str(uuid.uuid4())
    course3_id = str(uuid.uuid4())

    courses_data = [
        Course(
            id=course1_id,
            name_en="Gangnam & Gyeongbokgung Half-Day Tour",
            name_ko="강남 & 경복궁 반나절 투어",
            name_ja="江南&景福宮 半日ツアー",
            description_en="A curated half-day tour from COEX area through Gangnam, Bukchon Hanok Village, and Gyeongbokgung Palace.",
            description_ko="코엑스에서 출발하여 강남, 북촌한옥마을, 경복궁을 둘러보는 반나절 코스.",
            duration_type="half_day",
            theme="history",
            region="seoul",
            difficulty="easy",
            total_duration_minutes=240,
            total_distance_km=18.5,
            estimated_transport_cost=5000,
            image_url="https://images.unsplash.com/photo-1553621042-f6e147245754?w=800",
            is_active=True,
        ),
        Course(
            id=course2_id,
            name_en="Seoul Night View & K-Pop Tour",
            name_ko="서울 야경 & K-Pop 투어",
            name_ja="ソウル夜景&K-Popツアー",
            description_en="Experience Seoul at night: N Seoul Tower, Dongdaemun Design Plaza, and Hongdae K-Pop street performances.",
            description_ko="서울의 밤을 경험하세요: 남산타워, DDP, 홍대 K-Pop 버스킹.",
            duration_type="half_day",
            theme="nightview",
            region="seoul",
            difficulty="easy",
            total_duration_minutes=210,
            total_distance_km=15.0,
            estimated_transport_cost=8000,
            image_url="https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?w=800",
            is_active=True,
        ),
        Course(
            id=course3_id,
            name_en="Busan Coastal Full-Day Tour",
            name_ko="부산 해안 풀데이 투어",
            name_ja="釜山海岸フルデイツアー",
            description_en="Explore Busan's stunning coastline: Haedong Yonggungsa Temple, Gamcheon Culture Village, Haeundae Beach, and Jagalchi Market.",
            description_ko="부산의 멋진 해안을 탐험하세요: 해동용궁사, 감천문화마을, 해운대해수욕장, 자갈치시장.",
            duration_type="full_day",
            theme="nature",
            region="busan",
            difficulty="moderate",
            total_duration_minutes=480,
            total_distance_km=45.0,
            estimated_transport_cost=15000,
            image_url="https://images.unsplash.com/photo-1583266784186-f3c65b57cfca?w=800",
            is_active=True,
        ),
    ]
    for c in courses_data:
        session.add(c)

    # ── Course Spots for course 1 ──
    spot1_id = str(uuid.uuid4())
    spot2_id = str(uuid.uuid4())
    spot3_id = str(uuid.uuid4())

    spots = [
        CourseSpot(
            id=spot1_id,
            course_id=course1_id,
            spot_order=1,
            name_en="COEX Mall & Starfield Library",
            name_ko="코엑스몰 & 별마당 도서관",
            description_en="Start your journey at the iconic Starfield Library inside COEX Mall.",
            latitude=37.5116,
            longitude=127.0595,
            stay_duration_minutes=30,
        ),
        CourseSpot(
            id=spot2_id,
            course_id=course1_id,
            spot_order=2,
            name_en="Bukchon Hanok Village",
            name_ko="북촌한옥마을",
            description_en="Walk through traditional Korean houses (hanok) nestled between palaces.",
            latitude=37.5826,
            longitude=126.9831,
            stay_duration_minutes=60,
        ),
        CourseSpot(
            id=spot3_id,
            course_id=course1_id,
            spot_order=3,
            name_en="Gyeongbokgung Palace",
            name_ko="경복궁",
            description_en="Explore Korea's grandest Joseon Dynasty palace. Consider renting a hanbok for free entry!",
            latitude=37.5796,
            longitude=126.9770,
            stay_duration_minutes=90,
        ),
    ]
    for s in spots:
        session.add(s)

    # ── Spot Transitions ──
    transitions = [
        CourseSpotTransition(
            id=str(uuid.uuid4()),
            course_id=course1_id,
            from_spot_id=spot1_id,
            to_spot_id=spot2_id,
            transport_mode="subway",
            duration_minutes=35,
            distance_km=10.2,
        ),
        CourseSpotTransition(
            id=str(uuid.uuid4()),
            course_id=course1_id,
            from_spot_id=spot2_id,
            to_spot_id=spot3_id,
            transport_mode="walk",
            duration_minutes=10,
            distance_km=0.8,
        ),
    ]
    for t in transitions:
        session.add(t)

    # ── Products ──
    prod1_id = str(uuid.uuid4())
    prod2_id = str(uuid.uuid4())

    products = [
        Product(
            id=prod1_id,
            name_en="Seoul Palace & Temple Private Tour",
            name_ko="서울 궁궐 & 사찰 프라이빗 투어",
            name_ja="ソウル宮殿&寺院プライベートツアー",
            description_en="Full-day private tour covering Gyeongbokgung, Changdeokgung, and Jogyesa Temple with an expert English-speaking guide.",
            description_ko="전문 영어 가이드와 함께하는 경복궁, 창덕궁, 조계사 풀데이 프라이빗 투어.",
            category="tour",
            price_usd=89.00,
            duration_hours=8,
            region="seoul",
            min_participants=1,
            max_participants=8,
            includes_en=["Hotel pickup & drop-off", "Expert guide", "Palace admission tickets", "Traditional tea experience"],
            includes_ko=["호텔 픽업 & 드롭", "전문 가이드", "궁궐 입장권", "전통 차 체험"],
            excludes_en=["Lunch", "Personal expenses"],
            excludes_ko=["점심", "개인 경비"],
            itinerary={
                "en": [
                    {"time": "09:00", "activity": "Hotel pickup"},
                    {"time": "09:30", "activity": "Gyeongbokgung Palace & Guard Changing Ceremony"},
                    {"time": "11:30", "activity": "Bukchon Hanok Village walk"},
                    {"time": "12:30", "activity": "Lunch break (self-pay)"},
                    {"time": "14:00", "activity": "Changdeokgung Palace & Secret Garden"},
                    {"time": "16:00", "activity": "Jogyesa Temple"},
                    {"time": "17:00", "activity": "Traditional tea at Insadong"},
                    {"time": "17:30", "activity": "Return to hotel"},
                ],
            },
            meeting_point="Hotel lobby",
            cancellation_policy_en="Free cancellation up to 24 hours before. 50% charge within 24 hours.",
            cancellation_policy_ko="24시간 전 무료 취소. 24시간 이내 50% 수수료.",
            images=[
                "https://images.unsplash.com/photo-1553621042-f6e147245754?w=600",
                "https://images.unsplash.com/photo-1583266784186-f3c65b57cfca?w=600",
            ],
            status="active",
        ),
        Product(
            id=prod2_id,
            name_en="Korean BBQ Cooking Class",
            name_ko="한국 BBQ 쿠킹 클래스",
            name_ja="韓国BBQ料理教室",
            description_en="Learn to cook authentic Korean BBQ! Includes market tour at Gwangjang Market and hands-on cooking session.",
            description_ko="정통 한국 BBQ 요리를 배워보세요! 광장시장 투어와 실습 포함.",
            category="experience",
            price_usd=65.00,
            duration_hours=4,
            region="seoul",
            min_participants=2,
            max_participants=12,
            includes_en=["All ingredients", "Recipe booklet", "Apron to take home", "Market tour"],
            includes_ko=["모든 식재료", "레시피북", "앞치마 선물", "시장 투어"],
            excludes_en=["Transportation to venue"],
            excludes_ko=["장소까지의 교통편"],
            itinerary={
                "en": [
                    {"time": "10:00", "activity": "Meet at Gwangjang Market entrance"},
                    {"time": "10:00", "activity": "Market tour & ingredient shopping"},
                    {"time": "11:30", "activity": "Cooking class begins"},
                    {"time": "13:00", "activity": "Enjoy your meal together"},
                    {"time": "14:00", "activity": "End"},
                ],
            },
            meeting_point="Gwangjang Market Gate 2",
            meeting_point_lat=37.5700,
            meeting_point_lng=126.9990,
            cancellation_policy_en="Free cancellation up to 48 hours before. No refund within 48 hours.",
            images=[
                "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=600",
            ],
            status="active",
        ),
    ]
    for p in products:
        session.add(p)

    # ── Product Inventory ──
    for d in range(12, 31):
        try:
            inv_date = date(2026, 5, d)
            session.add(ProductInventory(
                product_id=prod1_id, date=inv_date, total_slots=8, booked_slots=0,
            ))
            session.add(ProductInventory(
                product_id=prod2_id, date=inv_date, total_slots=12, booked_slots=0,
            ))
        except ValueError:
            pass

    # ── Guides ──
    guide1_id = str(uuid.uuid4())
    guide2_id = str(uuid.uuid4())

    guides = [
        Guide(
            id=guide1_id,
            name_en="Kim Minjun",
            name_ko="김민준",
            bio_en="Professional tour guide with 10 years of experience. Specializes in Korean history and K-Pop culture. Certified by the Korea Tourism Organization.",
            bio_ko="10년 경력의 전문 관광 가이드. 한국 역사와 K-Pop 문화 전문. 한국관광공사 인증 가이드.",
            profile_image_url="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400",
            languages=[
                {"language": "Korean", "proficiency": "native"},
                {"language": "English", "proficiency": "fluent"},
                {"language": "Japanese", "proficiency": "intermediate"},
            ],
            specialties=["history", "kpop", "food"],
            regions=["seoul", "incheon"],
            price_per_hour_usd=35.00,
            price_half_day_usd=120.00,
            price_full_day_usd=200.00,
            services_en="City tours, K-Pop location tours, Historical palace tours, Food tours, Airport pickup assistance",
            services_ko="시티 투어, K-Pop 성지순례, 궁궐 역사 투어, 맛집 투어, 공항 픽업 도우미",
            status="active",
        ),
        Guide(
            id=guide2_id,
            name_en="Park Soyeon",
            name_ko="박소연",
            bio_en="Busan native and food enthusiast. Former hotel concierge. Expert in Busan seafood, local markets, and coastal sightseeing.",
            bio_ko="부산 토박이 미식가. 전 호텔 컨시어지. 부산 해산물, 재래시장, 해안 관광 전문.",
            profile_image_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400",
            languages=[
                {"language": "Korean", "proficiency": "native"},
                {"language": "English", "proficiency": "fluent"},
                {"language": "Chinese", "proficiency": "intermediate"},
            ],
            specialties=["food", "nature", "shopping"],
            regions=["busan", "gyeongju"],
            price_per_hour_usd=30.00,
            price_half_day_usd=100.00,
            price_full_day_usd=180.00,
            services_en="Seafood market tours, Coastal temple tours, Beach area guides, Shopping assistance",
            services_ko="해산물 시장 투어, 해안 사찰 투어, 해변 지역 가이드, 쇼핑 도우미",
            status="active",
        ),
    ]
    for g in guides:
        session.add(g)

    # ── Guide Availability ──
    for d in range(12, 31):
        try:
            avail_date = date(2026, 5, d)
            session.add(GuideAvailability(guide_id=guide1_id, date=avail_date, is_available=True))
            session.add(GuideAvailability(guide_id=guide2_id, date=avail_date, is_available=True))
        except ValueError:
            pass

    # ── Transport Routes ──
    routes = [
        TransportRoute(
            from_name_en="Incheon International Airport",
            from_name_ko="인천국제공항",
            to_name_en="COEX Convention Center",
            to_name_ko="코엑스 컨벤션센터",
            from_latitude=37.4602,
            from_longitude=126.4407,
            to_latitude=37.5116,
            to_longitude=127.0595,
            transport_modes=[
                {"mode": "airport_limousine", "duration_minutes": 70, "cost_krw": 16000, "cost_usd": 12, "instructions_en": "Take Airport Limousine Bus 6006 from Gate 5B. Direct to COEX."},
                {"mode": "subway", "duration_minutes": 100, "cost_krw": 4850, "cost_usd": 3.5, "instructions_en": "Take Airport Railroad (AREX) to Seoul Station, transfer to Line 2 (green) to Samseong Station."},
                {"mode": "taxi", "duration_minutes": 60, "cost_krw": 80000, "cost_usd": 60, "instructions_en": "Regular taxi from Airport Taxi Stand. Toll road fees included."},
            ],
            is_active=True,
        ),
        TransportRoute(
            from_name_en="Gimhae International Airport",
            from_name_ko="김해국제공항",
            to_name_en="BEXCO Convention Center",
            to_name_ko="벡스코 컨벤션센터",
            from_latitude=35.1796,
            from_longitude=128.9382,
            to_latitude=35.1695,
            to_longitude=129.1362,
            transport_modes=[
                {"mode": "subway", "duration_minutes": 50, "cost_krw": 1600, "cost_usd": 1.2, "instructions_en": "Take Busan-Gimhae Light Rail to Sasang Station, transfer to Line 2 (green) to Centum City Station."},
                {"mode": "taxi", "duration_minutes": 30, "cost_krw": 25000, "cost_usd": 19, "instructions_en": "Taxi from airport to BEXCO. About 20km."},
            ],
            is_active=True,
        ),
    ]
    for r in routes:
        session.add(r)

    # ── Transport Tips ──
    tips = [
        TransportTip(
            title_en="Get a T-money Card",
            title_ko="T-money 카드 구매하기",
            title_ja="T-moneyカードを入手する",
            content_en="Buy a T-money card at any convenience store (CU, GS25, 7-Eleven) for 2,500 KRW. Recharge at subway stations or convenience stores. Works on buses, subways, and taxis across Korea.",
            content_ko="편의점(CU, GS25, 세븐일레븐)에서 2,500원에 T-money 카드를 구매하세요. 지하철역이나 편의점에서 충전 가능. 전국 버스, 지하철, 택시에서 사용 가능합니다.",
            category="tmoney",
            icon="credit-card",
            display_order=1,
            is_active=True,
        ),
        TransportTip(
            title_en="Using Kakao Taxi App",
            title_ko="카카오 택시 앱 사용하기",
            title_ja="カカオタクシーアプリの使い方",
            content_en="Download Kakao T app for easy taxi booking. Supports English interface. Payment via card or cash. You can see the estimated fare before booking.",
            content_ko="간편한 택시 호출을 위해 카카오T 앱을 다운로드하세요. 영어 인터페이스 지원. 카드 또는 현금 결제 가능.",
            category="app",
            icon="smartphone",
            display_order=2,
            is_active=True,
        ),
        TransportTip(
            title_en="Subway Tips for Visitors",
            title_ko="외국인을 위한 지하철 팁",
            title_ja="訪問者向け地下鉄のヒント",
            content_en="Seoul Metro runs from 5:30 AM to midnight. All stations have signs in English, Korean, Chinese, and Japanese. Use the 'Subway Korea' app for route planning.",
            content_ko="서울 지하철은 오전 5:30부터 자정까지 운행됩니다. 모든 역에 영어, 한국어, 중국어, 일본어 표기가 있습니다.",
            category="general",
            icon="train",
            display_order=3,
            is_active=True,
        ),
    ]
    for t in tips:
        session.add(t)

    # ── Event Linkages ──
    # Link restaurants, courses, products, guides to events
    event_links = [
        EventRestaurant(event_id=event1_id, restaurant_id=rest1_id, display_order=1),
        EventRestaurant(event_id=event1_id, restaurant_id=rest2_id, display_order=2),
        EventRestaurant(event_id=event3_id, restaurant_id=rest3_id, display_order=1),
        EventCourse(event_id=event1_id, course_id=course1_id, display_order=1),
        EventCourse(event_id=event1_id, course_id=course2_id, display_order=2),
        EventCourse(event_id=event3_id, course_id=course3_id, display_order=1),
        EventProduct(event_id=event1_id, product_id=prod1_id, display_order=1),
        EventProduct(event_id=event1_id, product_id=prod2_id, display_order=2),
        EventGuide(event_id=event1_id, guide_id=guide1_id, display_order=1),
        EventGuide(event_id=event3_id, guide_id=guide2_id, display_order=1),
    ]
    for link in event_links:
        session.add(link)

    # ── Sample UI Translations ──
    en_translations = {
        "nav.home": "Home",
        "nav.events": "Events",
        "nav.restaurants": "Restaurants",
        "nav.courses": "Travel Courses",
        "nav.transport": "Getting Around",
        "nav.products": "Tours & Activities",
        "nav.guides": "Guides",
        "nav.bookmarks": "Bookmarks",
        "nav.mypage": "My Page",
        "button.book_now": "Book Now",
        "button.view_details": "View Details",
        "button.add_bookmark": "Add Bookmark",
        "button.remove_bookmark": "Remove Bookmark",
        "button.login": "Login",
        "button.register": "Register",
        "button.logout": "Logout",
        "label.price": "Price",
        "label.duration": "Duration",
        "label.difficulty": "Difficulty",
        "label.category": "Category",
        "label.region": "Region",
    }
    for key, value in en_translations.items():
        session.add(UITranslation(language_code="en", key=key, value=value))

    ko_translations = {
        "nav.home": "홈",
        "nav.events": "전시회",
        "nav.restaurants": "맛집",
        "nav.courses": "여행코스",
        "nav.transport": "교통정보",
        "nav.products": "투어 & 액티비티",
        "nav.guides": "가이드",
        "nav.bookmarks": "즐겨찾기",
        "nav.mypage": "마이페이지",
        "button.book_now": "예약하기",
        "button.view_details": "상세보기",
        "button.add_bookmark": "즐겨찾기 추가",
        "button.remove_bookmark": "즐겨찾기 삭제",
        "button.login": "로그인",
        "button.register": "회원가입",
        "button.logout": "로그아웃",
        "label.price": "가격",
        "label.duration": "소요시간",
        "label.difficulty": "난이도",
        "label.category": "카테고리",
        "label.region": "지역",
    }
    for key, value in ko_translations.items():
        session.add(UITranslation(language_code="ko", key=key, value=value))

    await session.flush()
    logger.info("Seeded sample data: events, restaurants, courses, products, guides, transport, translations")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown."""
    logger.info("Starting MICE Travel Mate Backend...")

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")

    # Run migrations
    async with engine.begin() as conn:
        await run_migrations(conn)

    # Seed data
    async with async_session() as session:
        try:
            await seed_languages(session)
            await seed_admin_user(session)
            await seed_sample_data(session)
            await session.commit()
        except Exception as e:
            logger.error("Seed error: %s", str(e))
            await session.rollback()

    logger.info("MICE Travel Mate Backend started on port 8007")
    yield

    # Shutdown
    await engine.dispose()
    logger.info("MICE Travel Mate Backend shut down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A curated travel platform for foreign MICE exhibition visitors",
    lifespan=lifespan,
)

# CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(restaurants.router)
app.include_router(courses.router)
app.include_router(transport.router)
app.include_router(products.router)
app.include_router(guides.router)
app.include_router(bookings.router)
app.include_router(bookmarks.router)
app.include_router(languages.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True)
