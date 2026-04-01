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
    RollingBanner,
    Review,
    Coupon, CouponUsage,
    ChatRoom, ChatMessage,
    Festival,
    Theme, ThemeSpot,
    LivingGuideCategory, LivingGuideArticle,
    SearchLog, VisitorLog, ContentView,
    B2BPartner,
    MapSetting,
)
from routers import auth, events, restaurants, courses, transport, products, guides, bookings, languages
from routers import bookmarks, admin
from routers import banners, reviews, coupons, chat, festivals, themes, living_guide, search, analytics, ai_courses, b2b

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_migrations(conn):
    """Run ALTER TABLE migrations with try/except for idempotency."""
    migrations = [
        # ── Users ──
        "ALTER TABLE users ADD COLUMN reset_token VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN reset_token_expires DATETIME",

        # ── Events: new language columns ──
        "ALTER TABLE events ADD COLUMN name_th VARCHAR(500)",
        "ALTER TABLE events ADD COLUMN name_vi VARCHAR(500)",
        "ALTER TABLE events ADD COLUMN name_fr VARCHAR(500)",
        "ALTER TABLE events ADD COLUMN description_th TEXT",
        "ALTER TABLE events ADD COLUMN description_vi TEXT",
        "ALTER TABLE events ADD COLUMN description_fr TEXT",

        # ── Restaurants: new language columns + avg_rating / review_count ──
        "ALTER TABLE restaurants ADD COLUMN name_th VARCHAR(500)",
        "ALTER TABLE restaurants ADD COLUMN name_vi VARCHAR(500)",
        "ALTER TABLE restaurants ADD COLUMN name_fr VARCHAR(500)",
        "ALTER TABLE restaurants ADD COLUMN description_th TEXT",
        "ALTER TABLE restaurants ADD COLUMN description_vi TEXT",
        "ALTER TABLE restaurants ADD COLUMN description_fr TEXT",
        "ALTER TABLE restaurants ADD COLUMN avg_rating FLOAT",
        "ALTER TABLE restaurants ADD COLUMN review_count INTEGER DEFAULT 0",

        # ── Courses: new language columns + avg_rating / review_count ──
        "ALTER TABLE courses ADD COLUMN name_th VARCHAR(500)",
        "ALTER TABLE courses ADD COLUMN name_vi VARCHAR(500)",
        "ALTER TABLE courses ADD COLUMN name_fr VARCHAR(500)",
        "ALTER TABLE courses ADD COLUMN description_th TEXT",
        "ALTER TABLE courses ADD COLUMN description_vi TEXT",
        "ALTER TABLE courses ADD COLUMN description_fr TEXT",
        "ALTER TABLE courses ADD COLUMN avg_rating FLOAT",
        "ALTER TABLE courses ADD COLUMN review_count INTEGER DEFAULT 0",

        # ── Course Spots: new language columns ──
        "ALTER TABLE course_spots ADD COLUMN name_th VARCHAR(500)",
        "ALTER TABLE course_spots ADD COLUMN name_vi VARCHAR(500)",
        "ALTER TABLE course_spots ADD COLUMN name_fr VARCHAR(500)",
        "ALTER TABLE course_spots ADD COLUMN description_th TEXT",
        "ALTER TABLE course_spots ADD COLUMN description_vi TEXT",
        "ALTER TABLE course_spots ADD COLUMN description_fr TEXT",

        # ── Products: new language columns + avg_rating / review_count ──
        "ALTER TABLE products ADD COLUMN name_th VARCHAR(500)",
        "ALTER TABLE products ADD COLUMN name_vi VARCHAR(500)",
        "ALTER TABLE products ADD COLUMN name_fr VARCHAR(500)",
        "ALTER TABLE products ADD COLUMN description_th TEXT",
        "ALTER TABLE products ADD COLUMN description_vi TEXT",
        "ALTER TABLE products ADD COLUMN description_fr TEXT",
        "ALTER TABLE products ADD COLUMN includes_th JSON",
        "ALTER TABLE products ADD COLUMN includes_vi JSON",
        "ALTER TABLE products ADD COLUMN includes_fr JSON",
        "ALTER TABLE products ADD COLUMN excludes_th JSON",
        "ALTER TABLE products ADD COLUMN excludes_vi JSON",
        "ALTER TABLE products ADD COLUMN excludes_fr JSON",
        "ALTER TABLE products ADD COLUMN cancellation_policy_th TEXT",
        "ALTER TABLE products ADD COLUMN cancellation_policy_vi TEXT",
        "ALTER TABLE products ADD COLUMN cancellation_policy_fr TEXT",
        "ALTER TABLE products ADD COLUMN avg_rating FLOAT",
        "ALTER TABLE products ADD COLUMN review_count INTEGER DEFAULT 0",

        # ── Guides: new language columns + user_id + avg_rating / review_count ──
        "ALTER TABLE guides ADD COLUMN name_th VARCHAR(500)",
        "ALTER TABLE guides ADD COLUMN name_vi VARCHAR(500)",
        "ALTER TABLE guides ADD COLUMN name_fr VARCHAR(500)",
        "ALTER TABLE guides ADD COLUMN bio_th TEXT",
        "ALTER TABLE guides ADD COLUMN bio_vi TEXT",
        "ALTER TABLE guides ADD COLUMN bio_fr TEXT",
        "ALTER TABLE guides ADD COLUMN services_th TEXT",
        "ALTER TABLE guides ADD COLUMN services_vi TEXT",
        "ALTER TABLE guides ADD COLUMN services_fr TEXT",
        "ALTER TABLE guides ADD COLUMN user_id VARCHAR(36)",
        "ALTER TABLE guides ADD COLUMN avg_rating FLOAT",
        "ALTER TABLE guides ADD COLUMN review_count INTEGER DEFAULT 0",

        # ── Transport Routes: new language columns ──
        "ALTER TABLE transport_routes ADD COLUMN from_name_th VARCHAR(500)",
        "ALTER TABLE transport_routes ADD COLUMN from_name_vi VARCHAR(500)",
        "ALTER TABLE transport_routes ADD COLUMN from_name_fr VARCHAR(500)",
        "ALTER TABLE transport_routes ADD COLUMN to_name_th VARCHAR(500)",
        "ALTER TABLE transport_routes ADD COLUMN to_name_vi VARCHAR(500)",
        "ALTER TABLE transport_routes ADD COLUMN to_name_fr VARCHAR(500)",

        # ── Transport Tips: new language columns ──
        "ALTER TABLE transport_tips ADD COLUMN title_th VARCHAR(500)",
        "ALTER TABLE transport_tips ADD COLUMN title_vi VARCHAR(500)",
        "ALTER TABLE transport_tips ADD COLUMN title_fr VARCHAR(500)",
        "ALTER TABLE transport_tips ADD COLUMN content_th TEXT",
        "ALTER TABLE transport_tips ADD COLUMN content_vi TEXT",
        "ALTER TABLE transport_tips ADD COLUMN content_fr TEXT",

        # ── Banners: transition_type ──
        "ALTER TABLE rolling_banners ADD COLUMN transition_type VARCHAR(20) DEFAULT 'slide'",

        # ── Map Settings: engine selection + google maps ──
        "ALTER TABLE map_settings ADD COLUMN map_engine VARCHAR(20) DEFAULT 'mapbox'",
        "ALTER TABLE map_settings ADD COLUMN google_maps_api_key VARCHAR(500)",
        # ── Map Settings: Google OAuth keys stored in map_settings ──
        "ALTER TABLE map_settings ADD COLUMN google_oauth_client_id VARCHAR(500)",
        "ALTER TABLE map_settings ADD COLUMN google_oauth_client_secret VARCHAR(500)",
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
        Language(code="th", name_en="Thai", name_native="ไทย", is_active=True, display_order=7),
        Language(code="vi", name_en="Vietnamese", name_native="Tiếng Việt", is_active=True, display_order=8),
        Language(code="fr", name_en="French", name_native="Français", is_active=True, display_order=9),
    ]
    for lang in default_languages:
        session.add(lang)
    await session.flush()
    logger.info("Seeded %d languages", len(default_languages))


async def seed_admin_user(session):
    """Seed default admin user or ensure existing user has superadmin role and correct password."""
    import bcrypt

    admin_email = settings.DEFAULT_ADMIN_EMAIL
    admin_password = settings.DEFAULT_ADMIN_PASSWORD

    result = await session.execute(select(User).where(User.email == admin_email))
    existing = result.scalar_one_or_none()
    if existing:
        changed = False
        if existing.role != "superadmin":
            existing.role = "superadmin"
            changed = True
        # Always reset password to ensure it matches config
        hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        existing.password_hash = hashed
        existing.is_active = True
        changed = True
        if changed:
            await session.flush()
        logger.info("Admin user verified: %s (role=superadmin, password reset)", admin_email)
        return

    hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    admin_user = User(
        id=str(uuid.uuid4()),
        email=admin_email,
        password_hash=hashed,
        name=settings.DEFAULT_ADMIN_NAME,
        role="superadmin",
        provider="local",
        is_active=True,
    )
    session.add(admin_user)
    await session.flush()
    logger.info("Created admin user: %s", admin_email)


async def seed_test_user(session):
    """Seed test user or reset password if already exists."""
    import bcrypt

    test_email = "test@runhatch.com"
    test_password = "test1234"

    result = await session.execute(select(User).where(User.email == test_email))
    existing = result.scalar_one_or_none()
    if existing:
        hashed = bcrypt.hashpw(test_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        existing.password_hash = hashed
        existing.role = "user"
        existing.is_active = True
        await session.flush()
        logger.info("Test user verified: %s (role=user, password reset)", test_email)
        return

    hashed = bcrypt.hashpw(test_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    test_user = User(
        id=str(uuid.uuid4()),
        email=test_email,
        password_hash=hashed,
        name="Test User",
        role="user",
        provider="local",
        is_active=True,
    )
    session.add(test_user)
    await session.flush()
    logger.info("Created test user: %s", test_email)


async def seed_rolling_banners(session):
    """Seed rolling banners with 9-language translations."""
    result = await session.execute(select(RollingBanner))
    if result.scalars().first():
        return

    banners_data = [
        RollingBanner(
            id=str(uuid.uuid4()),
            title_en="Seoul After Dark",
            title_ko="서울의 밤",
            title_zh_cn="首尔夜色",
            title_zh_tw="首爾夜色",
            title_ja="ソウルの夜",
            title_es="Seúl de Noche",
            title_th="โซลยามค่ำคืน",
            title_vi="Seoul Về Đêm",
            title_fr="Séoul la Nuit",
            subtitle_en="Neon lights, rooftop bars & skyline views await you",
            subtitle_ko="네온 불빛, 루프탑 바, 스카이라인이 당신을 기다립니다",
            subtitle_zh_cn="霓虹灯、天台酒吧和天际线美景等着你",
            subtitle_zh_tw="霓虹燈、天台酒吧和天際線美景等著你",
            subtitle_ja="ネオンの光、ルーフトップバー、スカイラインがあなたを待っています",
            subtitle_es="Luces de neón, bares en azoteas y vistas del horizonte te esperan",
            subtitle_th="แสงนีออน บาร์ดาดฟ้า และวิวเส้นขอบฟ้ารอคุณอยู่",
            subtitle_vi="Ánh đèn neon, quán bar sân thượng và tầm nhìn đường chân trời đang chờ bạn",
            subtitle_fr="Néons, bars sur les toits et vues sur la skyline vous attendent",
            image_url="https://images.unsplash.com/photo-1546874177-9e664107314e?w=1200",
            display_order=1,
            is_active=True,
        ),
        RollingBanner(
            id=str(uuid.uuid4()),
            title_en="Taste the Real Korea",
            title_ko="진짜 한국의 맛",
            title_zh_cn="品味真正的韩国",
            title_zh_tw="品味真正的韓國",
            title_ja="本物の韓国を味わう",
            title_es="Saborea la Verdadera Corea",
            title_th="ลิ้มรสเกาหลีแท้ๆ",
            title_vi="Nếm Vị Hàn Quốc Thật Sự",
            title_fr="Goûtez la Vraie Corée",
            subtitle_en="From sizzling BBQ to hidden street food gems",
            subtitle_ko="불고기 BBQ에서 숨겨진 길거리 음식까지",
            subtitle_zh_cn="从滋滋作响的烤肉到隐藏的街头美食",
            subtitle_zh_tw="從滋滋作響的烤肉到隱藏的街頭美食",
            subtitle_ja="ジュージューのBBQから隠れたストリートフードまで",
            subtitle_es="Desde BBQ chisporroteante hasta joyas ocultas de comida callejera",
            subtitle_th="จากบาร์บีคิวร้อนฉ่าสู่อาหารริมทางที่ซ่อนอยู่",
            subtitle_vi="Từ BBQ xèo xèo đến những viên ngọc ẩm thực đường phố",
            subtitle_fr="Du BBQ grésillant aux trésors cachés de la street food",
            image_url="https://images.unsplash.com/photo-1590301157890-4810ed352733?w=1200",
            display_order=2,
            is_active=True,
        ),
        RollingBanner(
            id=str(uuid.uuid4()),
            title_en="Temples & Traditions",
            title_ko="사찰과 전통",
            title_zh_cn="寺庙与传统",
            title_zh_tw="寺廟與傳統",
            title_ja="寺院と伝統",
            title_es="Templos y Tradiciones",
            title_th="วัดวาและประเพณี",
            title_vi="Đền Chùa & Truyền Thống",
            title_fr="Temples et Traditions",
            subtitle_en="Ancient beauty meets modern wonder",
            subtitle_ko="고대의 아름다움이 현대의 경이로움을 만나다",
            subtitle_zh_cn="古老之美遇见现代奇迹",
            subtitle_zh_tw="古老之美遇見現代奇蹟",
            subtitle_ja="古代の美しさが現代の驚異と出会う",
            subtitle_es="La belleza antigua se encuentra con la maravilla moderna",
            subtitle_th="ความงามโบราณพบกับความมหัศจรรย์สมัยใหม่",
            subtitle_vi="Vẻ đẹp cổ xưa gặp gỡ kỳ quan hiện đại",
            subtitle_fr="La beauté ancienne rencontre la merveille moderne",
            image_url="https://images.unsplash.com/photo-1553621042-f6e147245754?w=1200",
            display_order=3,
            is_active=True,
        ),
        RollingBanner(
            id=str(uuid.uuid4()),
            title_en="K-Culture is Calling",
            title_ko="K-컬처가 부른다",
            title_zh_cn="韩流在召唤",
            title_zh_tw="韓流在召喚",
            title_ja="K-カルチャーが呼んでいる",
            title_es="La K-Culture te Llama",
            title_th="K-Culture กำลังเรียกคุณ",
            title_vi="K-Culture Đang Gọi",
            title_fr="La K-Culture vous Appelle",
            subtitle_en="K-Pop, K-Beauty, K-Food — experience it all",
            subtitle_ko="K-Pop, K-뷰티, K-푸드 — 모든 것을 경험하세요",
            subtitle_zh_cn="K-Pop、K-Beauty、K-Food——全部体验",
            subtitle_zh_tw="K-Pop、K-Beauty、K-Food——全部體驗",
            subtitle_ja="K-Pop、K-Beauty、K-Food——すべてを体験",
            subtitle_es="K-Pop, K-Beauty, K-Food — experiméntalo todo",
            subtitle_th="K-Pop, K-Beauty, K-Food — สัมผัสทุกอย่าง",
            subtitle_vi="K-Pop, K-Beauty, K-Food — trải nghiệm tất cả",
            subtitle_fr="K-Pop, K-Beauty, K-Food — vivez tout cela",
            image_url="https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=1200",
            display_order=4,
            is_active=True,
        ),
        RollingBanner(
            id=str(uuid.uuid4()),
            title_en="Nature Escapes Near the City",
            title_ko="도심 속 자연",
            title_zh_cn="城市近郊自然之旅",
            title_zh_tw="城市近郊自然之旅",
            title_ja="都心近くの自然",
            title_es="Escapes Naturales Cerca de la Ciudad",
            title_th="หนีเข้าธรรมชาติใกล้เมือง",
            title_vi="Thiên Nhiên Gần Thành Phố",
            title_fr="Évasions Nature Près de la Ville",
            subtitle_en="Mountains, rivers & coastal trails just minutes away",
            subtitle_ko="몇 분 거리의 산, 강, 해안 트레일",
            subtitle_zh_cn="几分钟即可到达的山川与海岸步道",
            subtitle_zh_tw="幾分鐘即可到達的山川與海岸步道",
            subtitle_ja="数分で到着する山、川、海岸トレイル",
            subtitle_es="Montañas, ríos y senderos costeros a minutos de distancia",
            subtitle_th="ภูเขา แม่น้ำ และเส้นทางชายฝั่งเพียงไม่กี่นาที",
            subtitle_vi="Núi, sông và đường mòn ven biển chỉ cách vài phút",
            subtitle_fr="Montagnes, rivières et sentiers côtiers à quelques minutes",
            image_url="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200",
            display_order=5,
            is_active=True,
        ),
    ]
    for b in banners_data:
        session.add(b)
    await session.flush()
    logger.info("Seeded %d rolling banners", len(banners_data))


async def seed_festivals(session):
    """Seed sample festivals with 9-language translations."""
    result = await session.execute(select(Festival))
    if result.scalars().first():
        return

    festivals_data = [
        Festival(
            id=str(uuid.uuid4()),
            name_en="Seoul Cherry Blossom Festival 2026",
            name_ko="서울 벚꽃축제 2026",
            name_zh_cn="2026首尔樱花节",
            name_zh_tw="2026首爾櫻花節",
            name_ja="2026ソウル桜祭り",
            name_es="Festival de los Cerezos en Flor de Seúl 2026",
            name_th="เทศกาลซากุระโซล 2026",
            name_vi="Lễ Hội Hoa Anh Đào Seoul 2026",
            name_fr="Festival des Cerisiers en Fleurs de Séoul 2026",
            description_en="Enjoy the breathtaking cherry blossoms along Yeouido and Seokchon Lake. Featuring live performances, food stalls, and night illuminations.",
            description_ko="여의도와 석촌호수를 따라 펼쳐지는 벚꽃을 즐기세요. 공연, 먹거리, 야간 조명이 함께합니다.",
            description_zh_cn="在汝矣岛和石村湖欣赏令人惊叹的樱花。现场表演、美食摊位和夜间灯光秀。",
            description_zh_tw="在汝矣島和石村湖欣賞令人驚嘆的櫻花。現場表演、美食攤位和夜間燈光秀。",
            description_ja="汝矣島と石村湖の息を呑む桜をお楽しみください。ライブパフォーマンス、屋台、夜間イルミネーション。",
            description_es="Disfruta de los impresionantes cerezos en flor en Yeouido y el lago Seokchon. Actuaciones en vivo, puestos de comida e iluminación nocturna.",
            description_th="เพลิดเพลินกับดอกซากุระที่สวยงามตามเกาะยออีโดและทะเลสาบซอกชน การแสดงสด ร้านอาหาร และไฟประดับยามค่ำคืน",
            description_vi="Thưởng thức hoa anh đào tuyệt đẹp dọc Yeouido và Hồ Seokchon. Biểu diễn trực tiếp, gian hàng ẩm thực và đèn chiếu sáng ban đêm.",
            description_fr="Profitez des magnifiques cerisiers en fleurs le long de Yeouido et du lac Seokchon. Spectacles, stands de nourriture et illuminations nocturnes.",
            category="festival",
            image_url="https://images.unsplash.com/photo-1522383225653-ed111181a951?w=800",
            venue_name="Yeouido Hangang Park & Seokchon Lake",
            address="Yeouido-dong, Yeongdeungpo-gu, Seoul",
            latitude=37.5283,
            longitude=126.9346,
            start_date=date(2026, 4, 1),
            end_date=date(2026, 4, 15),
            website_url="https://www.seoul.go.kr",
            is_active=True,
        ),
        Festival(
            id=str(uuid.uuid4()),
            name_en="Busan International Film Festival 2026",
            name_ko="부산국제영화제 2026",
            name_zh_cn="2026釜山国际电影节",
            name_zh_tw="2026釜山國際電影節",
            name_ja="2026釜山国際映画祭",
            name_es="Festival Internacional de Cine de Busan 2026",
            name_th="เทศกาลภาพยนตร์นานาชาติปูซาน 2026",
            name_vi="Liên Hoan Phim Quốc Tế Busan 2026",
            name_fr="Festival International du Film de Busan 2026",
            description_en="Asia's largest film festival featuring over 300 films from 70 countries. Red carpet events, outdoor screenings, and meet-the-directors sessions.",
            description_ko="70개국 300편 이상의 영화가 상영되는 아시아 최대 영화제. 레드카펫, 야외 상영, 감독과의 대화.",
            description_zh_cn="亚洲最大的电影节，放映来自70个国家的300多部电影。红毯活动、露天放映和导演见面会。",
            description_zh_tw="亞洲最大的電影節，放映來自70個國家的300多部電影。紅毯活動、露天放映和導演見面會。",
            description_ja="70か国から300本以上の映画が上映されるアジア最大の映画祭。レッドカーペット、野外上映、監督との対話。",
            description_es="El festival de cine más grande de Asia con más de 300 películas de 70 países. Alfombra roja, proyecciones al aire libre y sesiones con directores.",
            description_th="เทศกาลภาพยนตร์ที่ใหญ่ที่สุดในเอเชียนำเสนอภาพยนตร์กว่า 300 เรื่องจาก 70 ประเทศ พรมแดง ฉายกลางแจ้ง และพบผู้กำกับ",
            description_vi="Liên hoan phim lớn nhất châu Á chiếu hơn 300 phim từ 70 quốc gia. Thảm đỏ, chiếu ngoài trời và giao lưu đạo diễn.",
            description_fr="Le plus grand festival de cinéma d'Asie avec plus de 300 films de 70 pays. Tapis rouge, projections en plein air et rencontres avec les réalisateurs.",
            category="festival",
            image_url="https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800",
            venue_name="Busan Cinema Center",
            address="120 Suyeonggangbyeon-daero, Haeundae-gu, Busan",
            latitude=35.1714,
            longitude=129.1300,
            start_date=date(2026, 10, 7),
            end_date=date(2026, 10, 16),
            website_url="https://www.biff.kr",
            is_active=True,
        ),
        Festival(
            id=str(uuid.uuid4()),
            name_en="Seoul Lantern Festival 2026",
            name_ko="서울빛초롱축제 2026",
            name_zh_cn="2026首尔灯笼节",
            name_zh_tw="2026首爾燈籠節",
            name_ja="2026ソウルランタンフェスティバル",
            name_es="Festival de Linternas de Seúl 2026",
            name_th="เทศกาลโคมไฟโซล 2026",
            name_vi="Lễ Hội Đèn Lồng Seoul 2026",
            name_fr="Festival des Lanternes de Séoul 2026",
            description_en="Beautiful lantern displays along the Cheonggyecheon Stream. Traditional and modern lantern art, cultural performances, and walking tours.",
            description_ko="청계천을 따라 펼쳐지는 아름다운 등불 전시. 전통과 현대의 등예술, 문화 공연, 도보 투어.",
            description_zh_cn="清溪川沿岸的美丽灯笼展。传统与现代灯笼艺术、文化表演和步行游览。",
            description_zh_tw="清溪川沿岸的美麗燈籠展。傳統與現代燈籠藝術、文化表演和步行遊覽。",
            description_ja="清渓川沿いの美しいランタン展示。伝統と現代のランタンアート、文化パフォーマンス、ウォーキングツアー。",
            description_es="Hermosas exhibiciones de linternas a lo largo del arroyo Cheonggyecheon. Arte de linternas tradicional y moderno, actuaciones culturales y recorridos a pie.",
            description_th="การจัดแสดงโคมไฟสวยงามตามลำธารชองเกชอน ศิลปะโคมไฟแบบดั้งเดิมและสมัยใหม่ การแสดงทางวัฒนธรรม และทัวร์เดิน",
            description_vi="Trưng bày đèn lồng tuyệt đẹp dọc suối Cheonggyecheon. Nghệ thuật đèn lồng truyền thống và hiện đại, biểu diễn văn hóa và tour đi bộ.",
            description_fr="Magnifiques expositions de lanternes le long du ruisseau Cheonggyecheon. Art des lanternes traditionnel et moderne, spectacles culturels et visites à pied.",
            category="festival",
            image_url="https://images.unsplash.com/photo-1513622470522-26c3c8a854bc?w=800",
            venue_name="Cheonggyecheon Stream",
            address="Cheonggyecheon-ro, Jongno-gu, Seoul",
            latitude=37.5701,
            longitude=126.9779,
            start_date=date(2026, 11, 6),
            end_date=date(2026, 11, 22),
            website_url="https://www.seoullantern.com",
            is_active=True,
        ),
    ]
    for f in festivals_data:
        session.add(f)
    await session.flush()
    logger.info("Seeded %d festivals", len(festivals_data))


async def seed_living_guide(session):
    """Seed living guide categories and articles with rich content."""
    result = await session.execute(select(LivingGuideCategory))
    if result.scalars().first():
        return

    categories = [
        {
            "name_en": "Transportation", "name_ko": "교통",
            "name_zh_cn": "交通", "name_zh_tw": "交通", "name_ja": "交通",
            "name_es": "Transporte", "name_th": "การขนส่ง", "name_vi": "Giao thong", "name_fr": "Transport",
            "icon": "transportation", "display_order": 1,
        },
        {
            "name_en": "Food & Dining", "name_ko": "음식 문화",
            "name_zh_cn": "饮食文化", "name_zh_tw": "飲食文化", "name_ja": "食文化",
            "name_es": "Gastronomia", "name_th": "อาหาร", "name_vi": "Am thuc", "name_fr": "Gastronomie",
            "icon": "food_culture", "display_order": 2,
        },
        {
            "name_en": "Shopping", "name_ko": "쇼핑",
            "name_zh_cn": "购物", "name_zh_tw": "購物", "name_ja": "ショッピング",
            "name_es": "Compras", "name_th": "ช้อปปิ้ง", "name_vi": "Mua sam", "name_fr": "Shopping",
            "icon": "shopping", "display_order": 3,
        },
        {
            "name_en": "Emergency", "name_ko": "긴급 상황",
            "name_zh_cn": "紧急情况", "name_zh_tw": "緊急情況", "name_ja": "緊急",
            "name_es": "Emergencia", "name_th": "ฉุกเฉิน", "name_vi": "Khan cap", "name_fr": "Urgence",
            "icon": "emergency", "display_order": 4,
        },
        {
            "name_en": "Communication", "name_ko": "통신",
            "name_zh_cn": "通信", "name_zh_tw": "通訊", "name_ja": "通信",
            "name_es": "Comunicacion", "name_th": "การสื่อสาร", "name_vi": "Lien lac", "name_fr": "Communication",
            "icon": "telecom", "display_order": 5,
        },
        {
            "name_en": "Money & Currency", "name_ko": "환전",
            "name_zh_cn": "换钱", "name_zh_tw": "換錢", "name_ja": "両替",
            "name_es": "Cambio", "name_th": "แลกเงิน", "name_vi": "Doi tien", "name_fr": "Change",
            "icon": "currency", "display_order": 6,
        },
        {
            "name_en": "Culture & Etiquette", "name_ko": "문화 & 에티켓",
            "name_zh_cn": "文化礼仪", "name_zh_tw": "文化禮儀", "name_ja": "文化とマナー",
            "name_es": "Cultura", "name_th": "วัฒนธรรม", "name_vi": "Van hoa", "name_fr": "Culture",
            "icon": "etiquette", "display_order": 7,
        },
        {
            "name_en": "Weather & Clothing", "name_ko": "날씨 & 옷차림",
            "name_zh_cn": "天气穿衣", "name_zh_tw": "天氣穿搭", "name_ja": "天気と服装",
            "name_es": "Clima", "name_th": "สภาพอากาศ", "name_vi": "Thoi tiet", "name_fr": "Meteo",
            "icon": "weather", "display_order": 8,
        },
    ]

    cat_ids = []
    for cat_data in categories:
        cat_id = str(uuid.uuid4())
        cat_ids.append(cat_id)
        session.add(LivingGuideCategory(id=cat_id, **cat_data, is_active=True))
    await session.flush()

    # Articles organized by category index
    articles_by_cat = {
        0: [  # Transportation
            {
                "title_en": "T-money Card",
                "title_ko": "T-money 카드",
                "title_ja": "T-moneyカード",
                "title_zh_cn": "T-money卡",
                "content_en": "T-money is a rechargeable smart card used for public transportation in Korea. You can buy one at any convenience store (CU, GS25, 7-Eleven) for 2,500 KRW. It works on subway, bus, and even some taxis. Recharge at convenience stores or subway station machines. Each ride saves you 100 KRW compared to cash payment. When transferring between bus and subway within 30 minutes, you get a free transfer discount.",
                "content_ko": "T-money는 한국 대중교통에서 사용하는 충전식 스마트카드입니다. 편의점(CU, GS25, 세븐일레븐)에서 2,500원에 구입 가능합니다. 지하철, 버스, 일부 택시에서 사용 가능하며, 편의점이나 지하철역 기계에서 충전할 수 있습니다. 현금 대비 100원 할인되며, 30분 이내 버스-지하철 환승 시 무료 환승 할인을 받을 수 있습니다.",
                "display_order": 1,
            },
            {
                "title_en": "Seoul Subway Guide",
                "title_ko": "서울 지하철 가이드",
                "title_ja": "ソウル地下鉄ガイド",
                "title_zh_cn": "首尔地铁指南",
                "content_en": "Seoul's subway system has 23 lines covering the entire metropolitan area. Most signs and announcements are in Korean, English, Chinese, and Japanese. Operating hours are roughly 5:30 AM to midnight. Base fare is 1,250 KRW with T-money (1,350 KRW cash). Download the 'Subway Korea' app for route planning. Key lines: Line 2 (green circle) for Gangnam/Hongdae, Line 4 for Myeongdong, Airport Railroad (AREX) for Incheon Airport.",
                "content_ko": "서울 지하철은 23개 노선으로 수도권 전역을 커버합니다. 대부분의 안내판과 안내방송은 한국어, 영어, 중국어, 일본어로 제공됩니다. 운행 시간은 대략 새벽 5:30부터 자정까지입니다. T-money 기본요금 1,250원 (현금 1,350원). 주요 노선: 2호선(강남/홍대), 4호선(명동), 공항철도(인천공항).",
                "display_order": 2,
            },
            {
                "title_en": "Taxi Tips for Foreigners",
                "title_ko": "외국인을 위한 택시 팁",
                "title_ja": "外国人のためのタクシーガイド",
                "title_zh_cn": "外国人打车指南",
                "content_en": "Korean taxis are safe and relatively affordable. Regular (orange/silver) base fare is 4,800 KRW. Use Kakao T app for easy booking - it shows the fare estimate and driver speaks through translation. International taxis (black) have English-speaking drivers but cost more. Tip: Screenshot your destination in Korean to show the driver. Late night surcharge (20%) applies from midnight to 4 AM.",
                "content_ko": "한국 택시는 안전하고 비교적 저렴합니다. 일반택시(주황/은색) 기본요금은 4,800원입니다. 카카오 T 앱을 사용하면 편리하게 호출할 수 있으며, 예상 요금을 확인할 수 있습니다. 목적지를 한국어로 캡처하여 기사님께 보여주세요. 심야 할증(20%)은 자정~오전 4시에 적용됩니다.",
                "display_order": 3,
            },
        ],
        1: [  # Food & Dining
            {
                "title_en": "How to Order Food in Korea",
                "title_ko": "한국에서 음식 주문하는 법",
                "content_en": "Many Korean restaurants use kiosk ordering systems. Look for the machine near the entrance. Some have English options - press the flag icon. In traditional restaurants, press the call button on your table to call a server. Side dishes (banchan) are free and can be refilled. Water is usually self-serve from a water dispenser. Tipping is NOT customary in Korea.",
                "content_ko": "많은 한국 식당은 무인 주문기(키오스크)를 사용합니다. 입구 근처의 기계를 찾으세요. 일부는 영어 옵션이 있으며, 국기 아이콘을 누르세요. 전통 식당에서는 테이블 위 호출 벨을 누르세요. 반찬은 무료이며 리필 가능합니다. 물은 보통 셀프서비스입니다. 한국에서는 팁 문화가 없습니다.",
                "display_order": 1,
            },
            {
                "title_en": "Korean Food Etiquette",
                "title_ko": "한국 음식 에티켓",
                "content_en": "Wait for the eldest person to start eating first. Use both hands when receiving or giving dishes. Don't stick chopsticks upright in rice (funeral ritual). Slurping noodles is acceptable. Sharing dishes is the norm - most Korean meals are communal. Drinking etiquette: turn away from elders when drinking alcohol, pour for others before yourself.",
                "content_ko": "어른이 먼저 식사를 시작할 때까지 기다리세요. 음식을 주고받을 때는 양손을 사용하세요. 밥에 젓가락을 꽂지 마세요(장례식 풍습). 면을 소리 내며 먹는 것은 괜찮습니다. 한국 식사는 대부분 함께 나눠 먹습니다. 음주 예절: 어른 앞에서는 고개를 돌려 마시세요.",
                "display_order": 2,
            },
            {
                "title_en": "Allergy & Dietary Info",
                "title_ko": "알레르기 & 식이 정보",
                "content_en": "Korean cuisine uses many common allergens: sesame, soy, shellfish, wheat, and peanuts. Vegetarian/vegan options are limited in traditional restaurants but growing in Seoul. Useful phrases: '알레르기 있어요' (I have allergies), '고기 빼주세요' (No meat please), '채식주의자예요' (I'm vegetarian). Temple food restaurants are always vegetarian.",
                "content_ko": "한국 음식에는 참깨, 간장, 조개류, 밀, 땅콩 등 알레르기 유발 식품이 많이 사용됩니다. 채식 옵션은 전통 식당에서는 제한적이지만 서울에서는 증가하고 있습니다. 사찰음식 식당은 항상 채식입니다.",
                "display_order": 3,
            },
        ],
        2: [  # Shopping
            {
                "title_en": "Tax Refund Guide",
                "title_ko": "세금 환급 가이드",
                "content_en": "Foreign tourists can get a VAT refund (10%) on purchases over 30,000 KRW at tax-free stores. Look for 'Tax Free' signs. Methods: 1) Immediate refund at checkout (show passport), 2) Refund at airport kiosks before departure. Keep receipts! Major refund operators: Global Tax Free, Korea Tax Refund. At Incheon Airport, use the automated kiosks near customs.",
                "content_ko": "외국인 관광객은 면세점에서 30,000원 이상 구매 시 부가세(10%) 환급을 받을 수 있습니다. 'Tax Free' 표시를 찾으세요. 방법: 1) 계산 시 즉시 환급(여권 제시), 2) 출국 전 공항 키오스크에서 환급. 영수증을 보관하세요!",
                "display_order": 1,
            },
            {
                "title_en": "Popular Shopping Areas",
                "title_ko": "인기 쇼핑 지역",
                "content_en": "Myeongdong: K-beauty cosmetics, fashion. Gangnam/Apgujeong: Luxury brands, trendy boutiques. Hongdae: Indie fashion, vintage shops. Dongdaemun: Wholesale fashion market (open late night). Insadong: Traditional crafts, souvenirs. Itaewon: International brands, custom tailoring. COEX Mall: Underground shopping mall with aquarium. Goto Mall (Gangnam): 620+ fashion shops underground.",
                "content_ko": "명동: K-뷰티 화장품, 패션. 강남/압구정: 명품, 트렌디 부티크. 홍대: 인디 패션, 빈티지. 동대문: 도매 패션(심야 운영). 인사동: 전통 공예품. 이태원: 해외 브랜드. 코엑스몰: 지하 쇼핑몰. 고투몰(강남): 620개+ 패션 매장.",
                "display_order": 2,
            },
        ],
        3: [  # Emergency
            {
                "title_en": "Emergency Numbers",
                "title_ko": "긴급 전화번호",
                "content_en": "Police: 112 (English available)\nFire/Ambulance: 119\nTourist Helpline: 1330 (24/7, multilingual)\nMedical Emergency for Foreigners: +82-2-790-7561\nEmbassy assistance: Contact your embassy\n\nThe 1330 Korea Travel Hotline is incredibly useful - they provide translation, tourist info, and emergency assistance in English, Chinese, Japanese, and more. Available 24 hours.",
                "content_ko": "경찰: 112\n소방/구급: 119\n관광 안내: 1330 (24시간, 다국어)\n외국인 의료 긴급: +82-2-790-7561\n대사관: 해당 대사관 연락\n\n1330 관광안내전화는 번역, 관광 정보, 긴급 지원을 영어, 중국어, 일본어 등으로 24시간 제공합니다.",
                "display_order": 1,
            },
            {
                "title_en": "Medical Care",
                "title_ko": "의료 서비스",
                "content_en": "International clinics in Seoul: Severance Hospital International Health Care Center, Samsung Medical Center International Clinic, Seoul National University Hospital. Most major hospitals have international patient services with interpreters. Pharmacies are everywhere - pharmacists can recommend medicine for common ailments. Over-the-counter medicine like Tylenol is available without prescription.",
                "content_ko": "서울의 국제 클리닉: 세브란스 국제진료센터, 삼성서울병원 국제진료센터, 서울대학교병원. 대부분의 대형 병원에 통역 서비스가 있습니다. 약국은 어디에나 있으며, 약사가 일반 질환에 대한 약을 추천해줄 수 있습니다.",
                "display_order": 2,
            },
        ],
        4: [  # Communication
            {
                "title_en": "SIM Cards & WiFi",
                "title_ko": "SIM 카드 & WiFi",
                "content_en": "Options: 1) Tourist SIM cards at Incheon Airport (KT, SKT, LG U+) - data only from 20,000 KRW/5 days. 2) Portable WiFi router rental at airport - 5,000-8,000 KRW/day, unlimited data, connect 5+ devices. 3) Free WiFi is widely available in subway stations, cafes, and convenience stores. Network name: 'KT_Free_WiFi' or 'Public WiFi Free'. 4) eSIM options via Airalo or Klook - activate before arrival.",
                "content_ko": "옵션: 1) 인천공항에서 관광 SIM 카드 (KT, SKT, LG U+) - 데이터 전용 20,000원/5일. 2) 공항에서 포터블 WiFi 라우터 대여 - 5,000~8,000원/일, 무제한 데이터. 3) 지하철역, 카페, 편의점에서 무료 WiFi 이용 가능. 4) Airalo, Klook 등 eSIM 옵션 - 도착 전 활성화.",
                "display_order": 1,
            },
        ],
        5: [  # Money & Currency
            {
                "title_en": "Currency Exchange Tips",
                "title_ko": "환전 팁",
                "content_en": "Korean Won (KRW) comes in notes: 1,000, 5,000, 10,000, 50,000. Best exchange rates: Myeongdong money changers, Itaewon, or banks. Avoid airport exchange (worst rates). Most places accept credit cards (Visa/Mastercard widely accepted). Mobile payment: Many shops accept Samsung Pay and Apple Pay. Cash needed: Traditional markets, small street food vendors. ATMs: Look for 'Global ATM' signs at convenience stores (7-Eleven, CU).",
                "content_ko": "한국 원(KRW) 지폐: 1,000, 5,000, 10,000, 50,000원. 최적 환율: 명동 환전소, 이태원, 은행. 공항 환전은 피하세요. 대부분 신용카드(비자/마스터카드) 사용 가능. 삼성페이, 애플페이도 많은 매장에서 사용됩니다. 현금 필요: 전통시장, 소규모 노점.",
                "display_order": 1,
            },
        ],
        6: [  # Culture & Etiquette
            {
                "title_en": "Korean Etiquette Basics",
                "title_ko": "한국 에티켓 기본",
                "content_en": "Bowing: A slight bow (15 degrees) is a common greeting. Deeper bows show more respect. Shoes: Remove shoes when entering homes, some restaurants (look for raised floors), and temples. Age & Hierarchy: Korea is hierarchical - use both hands when giving/receiving items from elders. Quiet zones: Keep phones silent on public transport. Priority seats on subway are for elderly/disabled/pregnant. Trash: Separate recycling (general/plastic/paper/food waste). Smoking: Only in designated areas.",
                "content_ko": "인사: 약간의 고개 숙임(15도)이 일반적인 인사입니다. 신발: 가정, 일부 식당(마루가 높은 곳), 사찰에 들어갈 때 신발을 벗으세요. 나이 & 위계: 어른에게 물건을 줄 때 양손을 사용하세요. 대중교통에서 휴대폰은 진동 모드로. 노약자석은 반드시 양보. 분리수거(일반/플라스틱/종이/음식물). 흡연은 지정 구역에서만.",
                "display_order": 1,
            },
        ],
        7: [  # Weather & Clothing
            {
                "title_en": "Seasonal Guide",
                "title_ko": "계절별 가이드",
                "content_en": "Spring (Mar-May): 5-20 C, cherry blossoms in April. Light layers, jacket needed.\nSummer (Jun-Aug): 25-35 C, humid with monsoon rain (July). Light clothes, umbrella essential, sunscreen.\nAutumn (Sep-Nov): 10-25 C, stunning foliage in October-November. Perfect weather, light to medium layers.\nWinter (Dec-Feb): -10 to 5 C, cold and dry. Heavy coat, thermal wear, gloves essential. Indoor heating is strong.\n\nTip: Korean buildings are well-heated in winter and air-conditioned in summer, so layering is key!",
                "content_ko": "봄 (3-5월): 5-20 C, 4월 벚꽃. 가벼운 겹옷, 재킷 필요.\n여름 (6-8월): 25-35 C, 습하고 7월 장마. 가벼운 옷, 우산 필수, 자외선차단제.\n가을 (9-11월): 10-25 C, 10-11월 단풍. 가벼운~중간 겹옷.\n겨울 (12-2월): -10~5 C, 춥고 건조. 두꺼운 코트, 발열내의, 장갑 필수.\n\n팁: 한국 건물은 겨울에 난방이, 여름에 에어컨이 잘 되어 있으니 레이어링이 핵심!",
                "display_order": 1,
            },
        ],
    }

    sample_articles = []
    for cat_idx, arts in articles_by_cat.items():
        cat_id = cat_ids[cat_idx]
        for art_data in arts:
            sample_articles.append(LivingGuideArticle(
                id=str(uuid.uuid4()),
                category_id=cat_id,
                title_en=art_data.get("title_en", ""),
                title_ko=art_data.get("title_ko", ""),
                title_ja=art_data.get("title_ja", ""),
                title_zh_cn=art_data.get("title_zh_cn", ""),
                content_en=art_data.get("content_en", ""),
                content_ko=art_data.get("content_ko", ""),
                display_order=art_data.get("display_order", 1),
                is_active=True,
            ))

    for article in sample_articles:
        session.add(article)
    await session.flush()
    logger.info("Seeded %d living guide categories and %d articles", len(categories), len(sample_articles))


async def seed_map_settings(session):
    """Seed default map settings with Seoul center coordinates."""
    result = await session.execute(select(MapSetting))
    if result.scalars().first():
        return

    map_setting = MapSetting(
        id=str(uuid.uuid4()),
        default_latitude=37.5665,
        default_longitude=126.9780,
        default_zoom=12,
    )
    session.add(map_setting)
    await session.flush()
    logger.info("Seeded default map settings (Seoul center)")


async def seed_sample_data(session):
    """Seed sample events, restaurants, courses, products, guides, transport."""
    # Check if data already exists (restaurants 기준으로 체크 — events만 있고 restaurants 없는 경우 방지)
    result = await session.execute(select(Restaurant))
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

    # ── Sample UI Translations (all 9 languages) ──
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
        "nav.map": "Map",
        "nav.ai_course": "AI Course",
        "nav.chat": "Chat",
        "nav.festivals": "Festivals",
        "nav.living_guide": "Living Guide",
        "nav.search": "Search",
        "button.book_now": "Book Now",
        "button.view_details": "View Details",
        "button.add_bookmark": "Add Bookmark",
        "button.remove_bookmark": "Remove Bookmark",
        "button.login": "Login",
        "button.register": "Register",
        "button.logout": "Logout",
        "button.send_message": "Send Message",
        "button.write_review": "Write Review",
        "button.apply_coupon": "Apply Coupon",
        "button.generate_course": "Generate Course",
        "label.price": "Price",
        "label.duration": "Duration",
        "label.difficulty": "Difficulty",
        "label.category": "Category",
        "label.region": "Region",
        "label.rating": "Rating",
        "label.reviews": "Reviews",
        "label.coupon_code": "Coupon Code",
        "label.festival_period": "Festival Period",
        "label.living_guide": "Living Guide",
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
        "nav.map": "지도",
        "nav.ai_course": "AI 코스",
        "nav.chat": "채팅",
        "nav.festivals": "축제",
        "nav.living_guide": "생활정보",
        "nav.search": "검색",
        "button.book_now": "예약하기",
        "button.view_details": "상세보기",
        "button.add_bookmark": "즐겨찾기 추가",
        "button.remove_bookmark": "즐겨찾기 삭제",
        "button.login": "로그인",
        "button.register": "회원가입",
        "button.logout": "로그아웃",
        "button.send_message": "메시지 보내기",
        "button.write_review": "리뷰 작성",
        "button.apply_coupon": "쿠폰 적용",
        "button.generate_course": "코스 생성",
        "label.price": "가격",
        "label.duration": "소요시간",
        "label.difficulty": "난이도",
        "label.category": "카테고리",
        "label.region": "지역",
        "label.rating": "평점",
        "label.reviews": "리뷰",
        "label.coupon_code": "쿠폰 코드",
        "label.festival_period": "축제 기간",
        "label.living_guide": "생활정보",
    }
    for key, value in ko_translations.items():
        session.add(UITranslation(language_code="ko", key=key, value=value))

    zh_cn_translations = {
        "nav.home": "首页",
        "nav.events": "展会",
        "nav.restaurants": "美食",
        "nav.courses": "旅游路线",
        "nav.transport": "交通指南",
        "nav.products": "旅游与活动",
        "nav.guides": "导游",
        "nav.bookmarks": "收藏",
        "nav.mypage": "我的",
        "nav.map": "地图",
        "nav.ai_course": "AI路线",
        "nav.chat": "聊天",
        "nav.festivals": "节日",
        "nav.living_guide": "生活指南",
        "nav.search": "搜索",
        "button.book_now": "立即预订",
        "button.view_details": "查看详情",
        "button.add_bookmark": "添加收藏",
        "button.remove_bookmark": "取消收藏",
        "button.login": "登录",
        "button.register": "注册",
        "button.logout": "退出",
        "button.send_message": "发送消息",
        "button.write_review": "撰写评论",
        "button.apply_coupon": "使用优惠券",
        "button.generate_course": "生成路线",
        "label.price": "价格",
        "label.duration": "时长",
        "label.difficulty": "难度",
        "label.category": "类别",
        "label.region": "地区",
        "label.rating": "评分",
        "label.reviews": "评论",
        "label.coupon_code": "优惠券代码",
        "label.festival_period": "节日期间",
        "label.living_guide": "生活指南",
    }
    for key, value in zh_cn_translations.items():
        session.add(UITranslation(language_code="zh-CN", key=key, value=value))

    zh_tw_translations = {
        "nav.home": "首頁",
        "nav.events": "展會",
        "nav.restaurants": "美食",
        "nav.courses": "旅遊路線",
        "nav.transport": "交通指南",
        "nav.products": "旅遊與活動",
        "nav.guides": "導遊",
        "nav.bookmarks": "收藏",
        "nav.mypage": "我的",
        "nav.map": "地圖",
        "nav.ai_course": "AI路線",
        "nav.chat": "聊天",
        "nav.festivals": "節日",
        "nav.living_guide": "生活指南",
        "nav.search": "搜尋",
        "button.book_now": "立即預訂",
        "button.view_details": "查看詳情",
        "button.add_bookmark": "添加收藏",
        "button.remove_bookmark": "取消收藏",
        "button.login": "登入",
        "button.register": "註冊",
        "button.logout": "登出",
        "button.send_message": "發送訊息",
        "button.write_review": "撰寫評論",
        "button.apply_coupon": "使用優惠券",
        "button.generate_course": "生成路線",
        "label.price": "價格",
        "label.duration": "時長",
        "label.difficulty": "難度",
        "label.category": "類別",
        "label.region": "地區",
        "label.rating": "評分",
        "label.reviews": "評論",
        "label.coupon_code": "優惠券代碼",
        "label.festival_period": "節日期間",
        "label.living_guide": "生活指南",
    }
    for key, value in zh_tw_translations.items():
        session.add(UITranslation(language_code="zh-TW", key=key, value=value))

    ja_translations = {
        "nav.home": "ホーム",
        "nav.events": "展示会",
        "nav.restaurants": "グルメ",
        "nav.courses": "旅行コース",
        "nav.transport": "交通情報",
        "nav.products": "ツアー & アクティビティ",
        "nav.guides": "ガイド",
        "nav.bookmarks": "ブックマーク",
        "nav.mypage": "マイページ",
        "nav.map": "マップ",
        "nav.ai_course": "AIコース",
        "nav.chat": "チャット",
        "nav.festivals": "フェスティバル",
        "nav.living_guide": "生活ガイド",
        "nav.search": "検索",
        "button.book_now": "今すぐ予約",
        "button.view_details": "詳細を見る",
        "button.add_bookmark": "ブックマーク追加",
        "button.remove_bookmark": "ブックマーク削除",
        "button.login": "ログイン",
        "button.register": "新規登録",
        "button.logout": "ログアウト",
        "button.send_message": "メッセージ送信",
        "button.write_review": "レビューを書く",
        "button.apply_coupon": "クーポン適用",
        "button.generate_course": "コース生成",
        "label.price": "価格",
        "label.duration": "所要時間",
        "label.difficulty": "難易度",
        "label.category": "カテゴリ",
        "label.region": "地域",
        "label.rating": "評価",
        "label.reviews": "レビュー",
        "label.coupon_code": "クーポンコード",
        "label.festival_period": "フェスティバル期間",
        "label.living_guide": "生活ガイド",
    }
    for key, value in ja_translations.items():
        session.add(UITranslation(language_code="ja", key=key, value=value))

    es_translations = {
        "nav.home": "Inicio",
        "nav.events": "Eventos",
        "nav.restaurants": "Restaurantes",
        "nav.courses": "Rutas de Viaje",
        "nav.transport": "Transporte",
        "nav.products": "Tours y Actividades",
        "nav.guides": "Guías",
        "nav.bookmarks": "Favoritos",
        "nav.mypage": "Mi Página",
        "nav.map": "Mapa",
        "nav.ai_course": "Ruta IA",
        "nav.chat": "Chat",
        "nav.festivals": "Festivales",
        "nav.living_guide": "Guía de Vida",
        "nav.search": "Buscar",
        "button.book_now": "Reservar Ahora",
        "button.view_details": "Ver Detalles",
        "button.add_bookmark": "Agregar Favorito",
        "button.remove_bookmark": "Eliminar Favorito",
        "button.login": "Iniciar Sesión",
        "button.register": "Registrarse",
        "button.logout": "Cerrar Sesión",
        "button.send_message": "Enviar Mensaje",
        "button.write_review": "Escribir Reseña",
        "button.apply_coupon": "Aplicar Cupón",
        "button.generate_course": "Generar Ruta",
        "label.price": "Precio",
        "label.duration": "Duración",
        "label.difficulty": "Dificultad",
        "label.category": "Categoría",
        "label.region": "Región",
        "label.rating": "Calificación",
        "label.reviews": "Reseñas",
        "label.coupon_code": "Código de Cupón",
        "label.festival_period": "Período del Festival",
        "label.living_guide": "Guía de Vida",
    }
    for key, value in es_translations.items():
        session.add(UITranslation(language_code="es", key=key, value=value))

    th_translations = {
        "nav.home": "หน้าแรก",
        "nav.events": "อีเวนต์",
        "nav.restaurants": "ร้านอาหาร",
        "nav.courses": "เส้นทางท่องเที่ยว",
        "nav.transport": "การเดินทาง",
        "nav.products": "ทัวร์และกิจกรรม",
        "nav.guides": "ไกด์",
        "nav.bookmarks": "บุ๊กมาร์ก",
        "nav.mypage": "ของฉัน",
        "nav.map": "แผนที่",
        "nav.ai_course": "เส้นทาง AI",
        "nav.chat": "แชท",
        "nav.festivals": "เทศกาล",
        "nav.living_guide": "คู่มือการใช้ชีวิต",
        "nav.search": "ค้นหา",
        "button.book_now": "จองเลย",
        "button.view_details": "ดูรายละเอียด",
        "button.add_bookmark": "เพิ่มบุ๊กมาร์ก",
        "button.remove_bookmark": "ลบบุ๊กมาร์ก",
        "button.login": "เข้าสู่ระบบ",
        "button.register": "สมัครสมาชิก",
        "button.logout": "ออกจากระบบ",
        "button.send_message": "ส่งข้อความ",
        "button.write_review": "เขียนรีวิว",
        "button.apply_coupon": "ใช้คูปอง",
        "button.generate_course": "สร้างเส้นทาง",
        "label.price": "ราคา",
        "label.duration": "ระยะเวลา",
        "label.difficulty": "ความยาก",
        "label.category": "หมวดหมู่",
        "label.region": "ภูมิภาค",
        "label.rating": "คะแนน",
        "label.reviews": "รีวิว",
        "label.coupon_code": "รหัสคูปอง",
        "label.festival_period": "ช่วงเทศกาล",
        "label.living_guide": "คู่มือการใช้ชีวิต",
    }
    for key, value in th_translations.items():
        session.add(UITranslation(language_code="th", key=key, value=value))

    vi_translations = {
        "nav.home": "Trang chủ",
        "nav.events": "Sự kiện",
        "nav.restaurants": "Nhà hàng",
        "nav.courses": "Lộ trình Du lịch",
        "nav.transport": "Di chuyển",
        "nav.products": "Tour & Hoạt động",
        "nav.guides": "Hướng dẫn viên",
        "nav.bookmarks": "Đánh dấu",
        "nav.mypage": "Của tôi",
        "nav.map": "Bản đồ",
        "nav.ai_course": "Lộ trình AI",
        "nav.chat": "Trò chuyện",
        "nav.festivals": "Lễ hội",
        "nav.living_guide": "Cẩm nang Sinh hoạt",
        "nav.search": "Tìm kiếm",
        "button.book_now": "Đặt ngay",
        "button.view_details": "Xem chi tiết",
        "button.add_bookmark": "Thêm đánh dấu",
        "button.remove_bookmark": "Xóa đánh dấu",
        "button.login": "Đăng nhập",
        "button.register": "Đăng ký",
        "button.logout": "Đăng xuất",
        "button.send_message": "Gửi tin nhắn",
        "button.write_review": "Viết đánh giá",
        "button.apply_coupon": "Áp dụng mã giảm giá",
        "button.generate_course": "Tạo lộ trình",
        "label.price": "Giá",
        "label.duration": "Thời lượng",
        "label.difficulty": "Độ khó",
        "label.category": "Danh mục",
        "label.region": "Khu vực",
        "label.rating": "Đánh giá",
        "label.reviews": "Nhận xét",
        "label.coupon_code": "Mã giảm giá",
        "label.festival_period": "Thời gian lễ hội",
        "label.living_guide": "Cẩm nang Sinh hoạt",
    }
    for key, value in vi_translations.items():
        session.add(UITranslation(language_code="vi", key=key, value=value))

    fr_translations = {
        "nav.home": "Accueil",
        "nav.events": "Événements",
        "nav.restaurants": "Restaurants",
        "nav.courses": "Itinéraires",
        "nav.transport": "Se Déplacer",
        "nav.products": "Tours & Activités",
        "nav.guides": "Guides",
        "nav.bookmarks": "Favoris",
        "nav.mypage": "Mon Espace",
        "nav.map": "Carte",
        "nav.ai_course": "Itinéraire IA",
        "nav.chat": "Discussion",
        "nav.festivals": "Festivals",
        "nav.living_guide": "Guide Pratique",
        "nav.search": "Rechercher",
        "button.book_now": "Réserver",
        "button.view_details": "Voir les Détails",
        "button.add_bookmark": "Ajouter aux Favoris",
        "button.remove_bookmark": "Retirer des Favoris",
        "button.login": "Connexion",
        "button.register": "Inscription",
        "button.logout": "Déconnexion",
        "button.send_message": "Envoyer un Message",
        "button.write_review": "Écrire un Avis",
        "button.apply_coupon": "Appliquer le Coupon",
        "button.generate_course": "Générer un Itinéraire",
        "label.price": "Prix",
        "label.duration": "Durée",
        "label.difficulty": "Difficulté",
        "label.category": "Catégorie",
        "label.region": "Région",
        "label.rating": "Note",
        "label.reviews": "Avis",
        "label.coupon_code": "Code Promo",
        "label.festival_period": "Période du Festival",
        "label.living_guide": "Guide Pratique",
    }
    for key, value in fr_translations.items():
        session.add(UITranslation(language_code="fr", key=key, value=value))

    await session.flush()
    logger.info("Seeded sample data: events, restaurants, courses, products, guides, transport, translations (9 languages)")


async def check_data_counts(session) -> dict:
    """Check record counts for key tables. Returns dict of table->count."""
    counts = {}
    tables = [
        ("restaurants", Restaurant),
        ("courses", Course),
        ("guides", Guide),
        ("festivals", Festival),
        ("events", Event),
    ]
    for name, model in tables:
        try:
            result = await session.execute(select(model))
            items = result.scalars().all()
            counts[name] = len(items)
        except Exception:
            counts[name] = 0
    return counts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown."""
    print("[STARTUP] Starting MICE Travel Mate Backend...", flush=True)
    logger.info("Starting MICE Travel Mate Backend...")

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("[STARTUP] Database tables created", flush=True)
        logger.info("Database tables created")

    # Run migrations
    async with engine.begin() as conn:
        await run_migrations(conn)

    # Seed users (independent transaction to prevent rollback)
    async with async_session() as session:
        try:
            await seed_admin_user(session)
            await seed_test_user(session)
            await session.commit()
            print("[STARTUP] User seed completed", flush=True)
            logger.info("User seed completed")
        except Exception as e:
            print(f"[STARTUP] User seed error: {e}", flush=True)
            logger.error("User seed error: %s", str(e))
            await session.rollback()

    # Seed basic data (languages, banners, living guide, map, inline samples)
    async with async_session() as session:
        try:
            await seed_languages(session)
            await seed_rolling_banners(session)
            await seed_festivals(session)
            await seed_living_guide(session)
            await seed_map_settings(session)
            await seed_sample_data(session)
            await session.commit()
            print("[STARTUP] Basic seed data completed", flush=True)
        except Exception as e:
            print(f"[STARTUP] Seed error: {e}", flush=True)
            logger.error("Seed error: %s", str(e))
            await session.rollback()

    # Check if comprehensive seed is needed (any key table has < 10 items)
    needs_comprehensive_seed = False
    async with async_session() as session:
        counts = await check_data_counts(session)
        print(f"[STARTUP] Current data counts: {counts}", flush=True)
        for table_name, count in counts.items():
            if count < 10:
                print(f"[STARTUP] {table_name} has only {count} items (< 10), comprehensive seed needed", flush=True)
                needs_comprehensive_seed = True
                break

    # Seed comprehensive data from seed/ directory (duplicate-safe, fills up to 100 each)
    if needs_comprehensive_seed:
        try:
            from seed_data import (
                seed_restaurants as seed_restaurants_full,
                seed_courses as seed_courses_full,
                seed_guides as seed_guides_full,
                seed_festivals as seed_festivals_full,
                seed_banners as seed_banners_full,
                seed_events as seed_events_full,
                seed_transport as seed_transport_full,
                seed_themes as seed_themes_full,
                seed_living_guide as seed_living_guide_full,
            )
            async with async_session() as session:
                await seed_restaurants_full(session)
                await seed_courses_full(session)
                await seed_guides_full(session)
                await seed_festivals_full(session)
                await seed_banners_full(session)
                await seed_events_full(session)
                await seed_transport_full(session)
                await seed_themes_full(session)
                await seed_living_guide_full(session)
                print("[STARTUP] Comprehensive seed data completed", flush=True)
                logger.info("Comprehensive seed data completed")
        except Exception as e:
            print(f"[STARTUP] Comprehensive seed error: {e}", flush=True)
            logger.error("Comprehensive seed error: %s", str(e))
    else:
        print("[STARTUP] All key tables have >= 10 items, skipping comprehensive seed", flush=True)

    # Final count verification
    async with async_session() as session:
        final_counts = await check_data_counts(session)
        print(f"[STARTUP] Final data counts: {final_counts}", flush=True)

    print("[STARTUP] MICE Travel Mate Backend started on port 8007", flush=True)
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
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
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
app.include_router(banners.router)
app.include_router(reviews.router)
app.include_router(coupons.router)
app.include_router(chat.router)
app.include_router(festivals.router)
app.include_router(themes.router)
app.include_router(living_guide.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(ai_courses.router)
app.include_router(b2b.router)


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


@app.get("/api/map-settings")
async def public_map_settings():
    """Public endpoint to get map settings (no auth required)."""
    from models.map_setting import MapSetting

    async with async_session() as session:
        result = await session.execute(select(MapSetting).limit(1))
        setting = result.scalar_one_or_none()

    if not setting:
        return {
            "map_engine": "mapbox",
            "mapbox_api_key": "",
            "google_maps_api_key": "",
            "default_center_lat": 37.5665,
            "default_center_lng": 126.978,
            "default_zoom": 12,
        }

    return {
        "map_engine": setting.map_engine or "mapbox",
        "mapbox_api_key": setting.mapbox_api_key or "",
        "google_maps_api_key": setting.google_maps_api_key or "",
        "default_center_lat": setting.default_latitude or 37.5665,
        "default_center_lng": setting.default_longitude or 126.978,
        "default_zoom": setting.default_zoom or 12,
    }


@app.get("/api/settings/google-login-enabled")
async def google_login_enabled():
    """Public endpoint to check if Google login is configured."""
    from models.map_setting import MapSetting

    async with async_session() as session:
        result = await session.execute(select(MapSetting).limit(1))
        setting = result.scalar_one_or_none()

    enabled = False
    client_id = ""
    if setting and setting.google_oauth_client_id:
        enabled = True
        client_id = setting.google_oauth_client_id
    elif settings.GOOGLE_CLIENT_ID:
        enabled = True
        client_id = settings.GOOGLE_CLIENT_ID
    return {"enabled": enabled, "client_id": client_id}


@app.post("/api/seed")
async def seed_database():
    """Trigger database seeding via API."""
    try:
        from seed_data import run_seed
        await run_seed()
        return {"status": "ok", "message": "Database seeded successfully"}
    except Exception as e:
        logger.error(f"Seed error: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True)
