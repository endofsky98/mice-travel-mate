"""
Generate additional seed data to reach 100 items for each category.
Run from backend directory: python seed/generate_extra.py
This creates seed/extra_restaurants.py, seed/extra_courses.py, seed/extra_guides.py, seed/extra_festivals.py
"""
import uuid
import json
import random

# =============================================================================
# RESTAURANTS - 70 extra to reach 100
# =============================================================================
RESTAURANT_TEMPLATES = [
    # Korean (20)
    ("Hansik House", "한식집", "korean", 2, "종로구", 37.5710, 126.9920),
    ("Bukchon Galbi", "북촌갈비", "korean", 3, "종로구 북촌로", 37.5826, 126.9836),
    ("Myeongdong Kalguksu", "명동칼국수", "korean", 1, "중구 명동길", 37.5636, 126.9869),
    ("Mapo Tofu House", "마포두부집", "korean", 2, "마포구 와우산로", 37.5551, 126.9228),
    ("Jongno Gomtang", "종로곰탕", "korean", 2, "종로구 종로3길", 37.5708, 126.9926),
    ("Gangnam Bibimbap", "강남비빔밥", "korean", 2, "강남구 역삼동", 37.4989, 127.0287),
    ("Yongsan Budae Jjigae", "용산부대찌개", "korean", 1, "용산구 이태원로", 37.5340, 126.9946),
    ("Songpa Samgyeopsal", "송파삼겹살", "korean", 2, "송파구 올림픽로", 37.5145, 127.1058),
    ("Seodaemun Dakgalbi", "서대문닭갈비", "korean", 2, "서대문구 연세로", 37.5592, 126.9368),
    ("Gwangjin Bossam", "광진보쌈", "korean", 2, "광진구 아차산로", 37.5385, 127.0826),
    ("Yeongdeungpo Sundae", "영등포순대", "korean", 1, "영등포구 당산로", 37.5348, 126.9025),
    ("Nowon Jokbal", "노원족발", "korean", 2, "노원구 동일로", 37.6543, 127.0567),
    ("Dongjak Naengmyeon", "동작냉면", "korean", 2, "동작구 사당로", 37.4835, 126.9815),
    ("Gangbuk Bulgogi", "강북불고기", "korean", 2, "강북구 도봉로", 37.6399, 127.0255),
    ("Eunpyeong Kimchi Jjigae", "은평김치찌개", "korean", 1, "은평구 진관동", 37.6283, 126.9220),
    ("Jamsil Shabu Shabu", "잠실샤브샤브", "korean", 2, "송파구 잠실동", 37.5133, 127.0998),
    ("Sinchon Chicken", "신촌치킨", "korean", 1, "서대문구 신촌역로", 37.5558, 126.9368),
    ("Apgujeong Hanwoo", "압구정한우", "korean", 4, "강남구 압구정로", 37.5273, 127.0286),
    ("Hongdae Tteokbokki", "홍대떡볶이", "korean", 1, "마포구 홍익로", 37.5563, 126.9237),
    ("Gangdong Samgyetang", "강동삼계탕", "korean", 2, "강동구 천호대로", 37.5372, 127.1236),
    # Japanese (10)
    ("Sushi Sakura", "스시 사쿠라", "japanese", 3, "강남구 도산대로", 37.5227, 127.0376),
    ("Ramen Ichiban", "라멘 이치방", "japanese", 2, "마포구 잔다리로", 37.5497, 126.9146),
    ("Donkatsu King", "돈카츠 킹", "japanese", 2, "서초구 서초대로", 37.4956, 127.0282),
    ("Yakitori Tori", "야키토리 토리", "japanese", 2, "용산구 녹사평대로", 37.5346, 126.9872),
    ("Izakaya Moon", "이자카야 문", "japanese", 2, "종로구 인사동길", 37.5729, 126.9856),
    ("Udon Paradise", "우동 파라다이스", "japanese", 1, "중구 충무로", 37.5611, 126.9940),
    ("Tempura House", "텐푸라 하우스", "japanese", 3, "강남구 신사동", 37.5165, 127.0199),
    ("Soba Noodle Bar", "소바 누들 바", "japanese", 2, "영등포구 여의도동", 37.5217, 126.9240),
    ("Matcha Cafe Tokyo", "말차 카페 도쿄", "japanese", 2, "성동구 성수이로", 37.5437, 127.0562),
    ("Okonomiyaki Lab", "오코노미야키 랩", "japanese", 2, "광진구 건대입구역", 37.5404, 127.0694),
    # Chinese (8)
    ("Beijing Garden", "베이징 가든", "chinese", 2, "중구 소공로", 37.5649, 126.9817),
    ("Sichuan Fire", "쓰촨 파이어", "chinese", 2, "마포구 양화로", 37.5547, 126.9190),
    ("Shanghai Palace", "상하이 팰리스", "chinese", 3, "강남구 학동로", 37.5152, 127.0378),
    ("Hong Kong Dim Sum", "홍콩딤섬", "chinese", 2, "영등포구 국제금융로", 37.5249, 126.9260),
    ("Chinatown Jajangmyeon", "차이나타운 짜장면", "chinese", 1, "중구 충무로3가", 37.5600, 126.9950),
    ("Lanzhou Noodle", "란저우 누들", "chinese", 1, "용산구 이태원동", 37.5346, 126.9946),
    ("Malatang House", "마라탕 하우스", "chinese", 1, "광진구 능동로", 37.5380, 127.0750),
    ("Dragon Wok", "드래곤 웍", "chinese", 2, "서초구 방배동", 37.4790, 126.9910),
    # Western (8)
    ("Le Petit Paris", "르쁘띠 파리", "western", 3, "강남구 청담동", 37.5255, 127.0485),
    ("Brooklyn Burger", "브루클린 버거", "western", 2, "마포구 연남동", 37.5623, 126.9258),
    ("Pasta Primo", "파스타 프리모", "western", 2, "용산구 한남동", 37.5346, 127.0000),
    ("Steak 42", "스테이크 42", "western", 4, "강남구 논현동", 37.5119, 127.0260),
    ("Pizzeria Napoli", "피제리아 나폴리", "western", 2, "종로구 삼청동", 37.5817, 126.9838),
    ("Brunch Club", "브런치 클럽", "western", 2, "성동구 서울숲길", 37.5468, 127.0430),
    ("Wine & Dine", "와인 앤 다인", "western", 3, "서초구 서래마을", 37.4856, 126.9970),
    ("Fish & Chips Pub", "피쉬 앤 칩스 펍", "western", 2, "중구 명동", 37.5640, 126.9850),
    # Cafe (6)
    ("Cafe Bene Bukchon", "카페 베네 북촌", "cafe", 2, "종로구 북촌로", 37.5834, 126.9843),
    ("Rooftop Coffee", "루프탑 커피", "cafe", 2, "마포구 동교동", 37.5590, 126.9233),
    ("Dessert Lab", "디저트 랩", "cafe", 2, "강남구 가로수길", 37.5194, 127.0234),
    ("Matcha Garden", "말차 가든", "cafe", 2, "서초구 반포동", 37.5045, 126.9979),
    ("Bread & Coffee", "빵과 커피", "cafe", 2, "성동구 성수동", 37.5441, 127.0570),
    ("Vintage Roasters", "빈티지 로스터즈", "cafe", 3, "영등포구 양평동", 37.5330, 126.8950),
    # Street Food (4)
    ("Gwangjang Market Stall", "광장시장 먹거리", "street_food", 1, "종로구 광장시장", 37.5700, 126.9990),
    ("Myeongdong Street Snacks", "명동 길거리 간식", "street_food", 1, "중구 명동", 37.5627, 126.9856),
    ("Hongdae Food Alley", "홍대 먹자골목", "street_food", 1, "마포구 와우산로", 37.5534, 126.9235),
    ("Dongdaemun Night Market", "동대문 야시장", "street_food", 1, "중구 장충단로", 37.5670, 127.0090),
    # Halal (2)
    ("Halal Kitchen Itaewon", "할랄 키친 이태원", "halal", 2, "용산구 이태원로", 37.5344, 126.9942),
    ("Istanbul Kebab", "이스탄불 케밥", "halal", 1, "용산구 보광동", 37.5310, 126.9910),
    # Vegan (2)
    ("Plant Seoul", "플랜트 서울", "vegan", 2, "종로구 안국동", 37.5770, 126.9860),
    ("Green Kitchen", "그린 키친", "vegan", 2, "강남구 신사동", 37.5190, 127.0220),
    # Extra to reach 70
    ("Songpa Galbi Village", "송파갈비마을", "korean", 3, "송파구 석촌동", 37.5060, 127.0986),
    ("Mapo Sutbul Gui", "마포숯불구이", "korean", 2, "마포구 상암동", 37.5776, 126.8904),
    ("Jamsil Sushi Omakase", "잠실스시오마카세", "japanese", 4, "송파구 잠실로", 37.5110, 127.0820),
    ("Sinsa Brunch", "신사브런치", "western", 2, "강남구 신사동", 37.5165, 127.0180),
    ("Yangjae Chicken", "양재치킨", "korean", 1, "서초구 양재동", 37.4856, 127.0340),
    ("Guro BBQ", "구로바베큐", "korean", 2, "구로구 구로동", 37.4954, 126.8878),
    ("Hannam Tapas", "한남타파스", "western", 3, "용산구 한남동", 37.5330, 127.0020),
    ("Seocho Thai Kitchen", "서초타이키친", "halal", 2, "서초구 서초동", 37.4919, 127.0075),
    ("Mangwon Bakery", "망원빵집", "cafe", 2, "마포구 망원동", 37.5558, 126.9065),
    ("Seoul Station Gukbap", "서울역국밥", "korean", 1, "중구 서울역", 37.5547, 126.9707),
]

def generate_restaurants():
    restaurants = []
    for idx, (name_en, name_ko, cat, price, addr, lat, lng) in enumerate(RESTAURANT_TEMPLATES):
        r = {
            "id": str(uuid.uuid4()),
            "name_en": name_en,
            "name_ko": name_ko,
            "description_en": f"A popular {cat} restaurant in the heart of Seoul's {addr} area. Known for authentic flavors and warm atmosphere.",
            "description_ko": f"서울 {addr} 지역의 인기 {name_ko} 맛집입니다. 정통 맛과 따뜻한 분위기로 유명합니다.",
            "category": cat,
            "price_range": price,
            "address": f"서울특별시 {addr}",
            "latitude": lat + random.uniform(-0.002, 0.002),
            "longitude": lng + random.uniform(-0.002, 0.002),
            "phone": f"02-{random.randint(200,999)}-{random.randint(1000,9999)}",
            "opening_hours": {
                "mon": "11:00-22:00", "tue": "11:00-22:00", "wed": "11:00-22:00",
                "thu": "11:00-22:00", "fri": "11:00-23:00", "sat": "11:00-23:00", "sun": "11:00-21:00"
            },
            "menu_highlights": [
                {"name_en": f"Signature {name_en}", "name_ko": f"시그니처 {name_ko}", "price": price * 15000 + random.randint(0, 10000)},
                {"name_en": f"Special Set", "name_ko": f"스페셜 세트", "price": price * 20000 + random.randint(0, 10000)},
            ],
            "images": [f"/images/placeholder/restaurant_{31 + idx}.jpg"],
            "avg_rating": round(random.uniform(3.5, 4.9), 1),
            "review_count": random.randint(10, 300),
            "is_active": True,
        }
        restaurants.append(r)
    return restaurants


# =============================================================================
# GUIDES - 70 extra
# =============================================================================
GUIDE_FIRST_NAMES_EN = ["Minho", "Soyeon", "Jiwon", "Hyunwoo", "Yuna", "Taejin", "Haeun", "Dongwook", "Minji", "Junghoon",
                        "Subin", "Chanwoo", "Eunji", "Seokjin", "Hayoung", "Woojin", "Nayeon", "Kyungho", "Dahyun", "Jaemin",
                        "Serin", "Jihun", "Somin", "Taeyoung", "Bora", "Hyunsoo", "Yeji", "Sangwoo", "Arin", "Donghyun",
                        "Chaeyoung", "Minseo", "Yoonho", "Jisoo", "Kangmin", "Hyerin", "Sunwoo", "Gaeun", "Doyoung", "Yerin",
                        "Seungmin", "Narae", "Junwoo", "Sieun", "Taeho", "Mirae", "Joonhyuk", "Inyoung", "Woosung", "Hyemin",
                        "Junho", "Sooyoung", "Minkyu", "Chaewon", "Sungjae", "Yujin", "Insoo", "Hana", "Taekwon", "Jiho",
                        "Seoyeon", "Minwoo", "Yoojung", "Chanho", "Suji", "Dongjin", "Yeonwoo", "Sangho", "Eunbi", "Jaewon"]

GUIDE_FIRST_NAMES_KO = ["민호", "소연", "지원", "현우", "유나", "태진", "하은", "동욱", "민지", "정훈",
                        "수빈", "찬우", "은지", "석진", "하영", "우진", "나연", "경호", "다현", "재민",
                        "세린", "지훈", "소민", "태영", "보라", "현수", "예지", "상우", "아린", "동현",
                        "채영", "민서", "윤호", "지수", "강민", "혜린", "선우", "가은", "도영", "예린",
                        "승민", "나래", "준우", "시은", "태호", "미래", "준혁", "인영", "우성", "혜민",
                        "준호", "수영", "민규", "채원", "성재", "유진", "인수", "하나", "택원", "지호",
                        "서연", "민우", "유정", "찬호", "수지", "동진", "연우", "상호", "은비", "재원"]

LANGUAGES = [
    [{"language": "English", "proficiency": "native"}, {"language": "Korean", "proficiency": "fluent"}],
    [{"language": "Chinese", "proficiency": "native"}, {"language": "Korean", "proficiency": "fluent"}, {"language": "English", "proficiency": "intermediate"}],
    [{"language": "Japanese", "proficiency": "native"}, {"language": "Korean", "proficiency": "fluent"}],
    [{"language": "English", "proficiency": "fluent"}, {"language": "Korean", "proficiency": "native"}, {"language": "Spanish", "proficiency": "intermediate"}],
    [{"language": "English", "proficiency": "fluent"}, {"language": "Korean", "proficiency": "native"}, {"language": "French", "proficiency": "intermediate"}],
    [{"language": "English", "proficiency": "fluent"}, {"language": "Korean", "proficiency": "native"}],
    [{"language": "Vietnamese", "proficiency": "native"}, {"language": "Korean", "proficiency": "fluent"}, {"language": "English", "proficiency": "basic"}],
    [{"language": "Thai", "proficiency": "native"}, {"language": "Korean", "proficiency": "fluent"}, {"language": "English", "proficiency": "intermediate"}],
]

SPECIALTIES = ["history", "food", "kpop", "shopping", "nature", "nightlife", "tradition", "art"]
REGIONS = ["Gangnam", "Jongno", "Hongdae", "Itaewon", "Myeongdong", "Insadong", "Bukchon", "Yeouido", "Dongdaemun"]

def generate_guides():
    guides = []
    for i in range(70):
        langs = random.choice(LANGUAGES)
        specs = random.sample(SPECIALTIES, random.randint(2, 4))
        regions = random.sample(REGIONS, random.randint(2, 4))
        hourly = random.randint(20, 60)
        g = {
            "id": str(uuid.uuid4()),
            "name_en": GUIDE_FIRST_NAMES_EN[i],
            "name_ko": GUIDE_FIRST_NAMES_KO[i],
            "bio_en": f"Experienced travel guide specializing in {', '.join(specs[:2])} tours around Seoul. I love sharing Korean culture with visitors from around the world.",
            "bio_ko": f"서울 {', '.join(specs[:2])} 투어 전문 가이드입니다. 전 세계 방문객들에게 한국 문화를 알리는 것을 좋아합니다.",
            "languages": langs,
            "specialties": specs,
            "regions": regions,
            "price_per_hour_usd": hourly,
            "price_half_day_usd": hourly * 4,
            "price_full_day_usd": hourly * 7,
            "currency": "USD",
            "avg_rating": round(random.uniform(3.8, 5.0), 1),
            "review_count": random.randint(5, 150),
            "is_active": True,
        }
        guides.append(g)
    return guides


# =============================================================================
# FESTIVALS - 88 extra to reach 100
# =============================================================================
FESTIVAL_DATA = [
    # Seoul festivals
    ("Seoul Lantern Festival", "서울 빛초롱 축제", "festival", "서울 청계천", 37.5694, 126.9822, "2025-11-01", "2025-11-17"),
    ("Seoul Food Festival", "서울 음식 축제", "food_festival", "서울 광화문광장", 37.5721, 126.9768, "2025-10-10", "2025-10-13"),
    ("Hongdae Free Market", "홍대 프리마켓", "market", "서울 홍대입구", 37.5563, 126.9237, "2025-03-01", "2025-12-31"),
    ("Seoul International Fireworks Festival", "서울세계불꽃축제", "festival", "여의도 한강공원", 37.5171, 126.9314, "2025-10-04", "2025-10-04"),
    ("Seoul Drum Festival", "서울 드럼 페스티벌", "concert", "서울 남산 일대", 37.5511, 126.9882, "2025-10-09", "2025-10-12"),
    ("Jamsil Comic World", "잠실 코믹월드", "exhibition", "잠실 COEX", 37.5116, 127.0593, "2025-08-15", "2025-08-17"),
    ("Seoul Jazz Festival", "서울재즈페스티벌", "concert", "올림픽공원", 37.5207, 127.1212, "2025-05-23", "2025-05-25"),
    ("Bukchon Traditional Culture", "북촌 전통문화 축제", "festival", "서울 북촌한옥마을", 37.5826, 126.9836, "2025-09-20", "2025-09-21"),
    ("Seoul Comic Con", "서울 코믹콘", "exhibition", "COEX", 37.5116, 127.0593, "2025-08-08", "2025-08-10"),
    ("Han River Night Market", "한강 야시장", "market", "여의도 한강공원", 37.5253, 126.9328, "2025-04-01", "2025-10-31"),
    ("Seoul Design Festival", "서울디자인페스티벌", "exhibition", "COEX", 37.5116, 127.0593, "2025-12-05", "2025-12-08"),
    ("Itaewon Global Village Festival", "이태원지구촌축제", "festival", "이태원 거리", 37.5344, 126.9942, "2025-10-18", "2025-10-19"),
    ("Seoul Bamdokkaebi Night Market", "서울밤도깨비야시장", "market", "DDP 앞", 37.5671, 127.0090, "2025-04-04", "2025-10-26"),
    ("K-pop Concert in Seoul", "K-pop 콘서트", "concert", "잠실종합운동장", 37.5153, 127.0729, "2025-07-12", "2025-07-13"),
    ("Seoul International Book Fair", "서울국제도서전", "exhibition", "COEX", 37.5116, 127.0593, "2025-06-18", "2025-06-22"),
    ("Seoul Fashion Week", "서울패션위크", "exhibition", "DDP", 37.5671, 127.0090, "2025-10-13", "2025-10-18"),
    ("Seoul Coffee Festival", "서울 커피 페스티벌", "food_festival", "COEX", 37.5116, 127.0593, "2025-11-06", "2025-11-09"),
    ("Seoul Street Art Festival", "서울 거리예술축제", "festival", "서울 광화문", 37.5721, 126.9768, "2025-09-26", "2025-09-28"),
    ("Hongdae Busking Festival", "홍대 버스킹 페스티벌", "concert", "홍대 거리", 37.5563, 126.9237, "2025-05-10", "2025-05-11"),
    ("Seoul VR/AR Expo", "서울 VR/AR 엑스포", "exhibition", "COEX", 37.5116, 127.0593, "2025-04-17", "2025-04-19"),
    # Nationwide major festivals
    ("Busan International Film Festival", "부산국제영화제", "festival", "부산 해운대", 35.1587, 129.1604, "2025-10-01", "2025-10-10"),
    ("Jeju Fire Festival", "제주들불축제", "festival", "제주 새별오름", 33.3530, 126.3690, "2025-03-06", "2025-03-08"),
    ("Jeonju Bibimbap Festival", "전주비빔밥축제", "food_festival", "전주 한옥마을", 35.8151, 127.1528, "2025-10-23", "2025-10-26"),
    ("Boryeong Mud Festival", "보령머드축제", "festival", "보령 대천해수욕장", 36.3150, 126.5133, "2025-07-18", "2025-07-27"),
    ("Andong Mask Dance Festival", "안동탈춤페스티벌", "festival", "안동 하회마을", 36.5394, 128.5186, "2025-09-26", "2025-10-05"),
    ("Gimje Horizon Festival", "김제 지평선 축제", "festival", "김제 벽골제", 35.7950, 126.8750, "2025-10-01", "2025-10-05"),
    ("Jinju Lantern Festival", "진주남강유등축제", "festival", "진주 남강", 35.1917, 128.0847, "2025-10-01", "2025-10-12"),
    ("Busan Fireworks Festival", "부산불꽃축제", "festival", "부산 광안리", 35.1533, 129.1184, "2025-11-01", "2025-11-01"),
    ("Tongyeong International Music Festival", "통영국제음악제", "concert", "통영 시민문화회관", 34.8544, 128.4331, "2025-03-28", "2025-04-03"),
    ("Hadong Wild Tea Festival", "하동야생차문화축제", "food_festival", "하동 화개면", 35.1461, 127.7081, "2025-05-17", "2025-05-25"),
    ("Incheon Pentaport Rock Festival", "인천펜타포트록페스티벌", "concert", "인천 송도달빛축제공원", 37.3800, 126.6600, "2025-08-01", "2025-08-03"),
    ("Gwangju Biennale", "광주비엔날레", "exhibition", "광주 비엔날레전시관", 35.1796, 126.8885, "2025-09-05", "2025-12-01"),
    ("Gyeongju Cherry Blossom Festival", "경주벚꽃축제", "festival", "경주 보문단지", 35.8444, 129.2908, "2025-04-01", "2025-04-10"),
    ("Daegu Chimac Festival", "대구치맥페스티벌", "food_festival", "대구 두류공원", 35.8536, 128.5642, "2025-07-16", "2025-07-20"),
    ("Sokcho Squid Festival", "속초오징어축제", "food_festival", "속초 중앙시장", 38.2043, 128.5940, "2025-09-12", "2025-09-14"),
    ("Yeoju Pottery Festival", "여주도자기축제", "festival", "여주 신륵사", 37.2827, 127.6361, "2025-05-02", "2025-05-11"),
    ("Ganghwa Dolmen Festival", "강화고인돌축제", "festival", "인천 강화도", 37.7470, 126.4880, "2025-10-17", "2025-10-19"),
    ("Chuncheon Makguksu Festival", "춘천막국수축제", "food_festival", "춘천시 효자동", 37.8813, 127.7298, "2025-06-06", "2025-06-08"),
    ("Damyang Bamboo Festival", "담양대나무축제", "festival", "담양 죽녹원", 35.3192, 126.9881, "2025-05-01", "2025-05-05"),
    ("Suncheon Bay Garden Festival", "순천만정원박람회", "exhibition", "순천만국가정원", 34.9275, 127.4950, "2025-04-01", "2025-10-31"),
    ("Pohang International Light Festival", "포항빛축제", "festival", "포항 형산강", 36.0190, 129.3434, "2025-12-24", "2026-01-01"),
    ("Ulsan Whale Festival", "울산고래축제", "festival", "울산 장생포", 35.4924, 129.3803, "2025-05-23", "2025-05-26"),
    ("Gapyeong Strawberry Festival", "가평딸기축제", "food_festival", "경기 가평", 37.8313, 127.5097, "2025-03-15", "2025-04-15"),
    ("Paju Book City Festival", "파주출판도시축제", "exhibition", "파주출판도시", 37.7480, 126.7440, "2025-09-19", "2025-09-21"),
    ("Chungju Martial Arts Festival", "충주세계무술축제", "festival", "충주 탄금대", 36.9740, 127.9510, "2025-10-03", "2025-10-08"),
    ("Seogwipo Tangerine Festival", "서귀포감귤축제", "food_festival", "제주 서귀포", 33.2532, 126.5601, "2025-11-07", "2025-11-09"),
    # 2026 events
    ("Seoul Spring Flower Festival", "서울 봄꽃 축제", "festival", "서울 여의도", 37.5253, 126.9328, "2026-04-05", "2026-04-13"),
    ("Seoul International Art Fair", "서울 아트 페어", "exhibition", "COEX", 37.5116, 127.0593, "2026-03-12", "2026-03-16"),
    ("K-Culture Festival", "K-컬처 페스티벌", "festival", "서울 광화문", 37.5721, 126.9768, "2026-05-01", "2026-05-05"),
    ("Seoul Beer Festival", "서울 맥주 축제", "food_festival", "한강공원", 37.5171, 126.9314, "2026-06-20", "2026-06-22"),
    ("Seoul Film Festival", "서울영화제", "festival", "서울 CGV 용산", 37.5283, 126.9657, "2026-04-18", "2026-04-27"),
    ("Lotus Lantern Festival", "연등회", "festival", "서울 종로 일대", 37.5710, 126.9920, "2026-05-10", "2026-05-17"),
    ("Seoul Summer Music Festival", "서울 여름 음악 축제", "concert", "올림픽공원", 37.5207, 127.1212, "2026-07-10", "2026-07-13"),
    ("Seoul Robot & AI Expo", "서울 로봇/AI 엑스포", "exhibition", "COEX", 37.5116, 127.0593, "2026-02-18", "2026-02-21"),
    ("Seoul Marathon 2026", "서울마라톤 2026", "sports", "광화문~잠실", 37.5710, 126.9920, "2026-03-15", "2026-03-15"),
    ("Jinhae Cherry Blossom Festival", "진해군항제", "festival", "진해 여좌천", 35.1350, 128.6640, "2026-04-01", "2026-04-10"),
    ("Busan One Asia Festival", "부산원아시아페스티벌", "concert", "부산 아시아드주경기장", 35.1909, 129.0568, "2026-10-18", "2026-10-25"),
    ("Gwangju World Kimchi Festival", "광주세계김치축제", "food_festival", "광주 김치타운", 35.1526, 126.8482, "2025-10-16", "2025-10-19"),
    ("Seoul Kimchi Festival", "서울김장문화제", "food_festival", "서울광장", 37.5662, 126.9781, "2025-11-07", "2025-11-09"),
    ("Andong Mask Dance & Culture", "안동문화축제", "festival", "안동시", 36.5694, 128.7286, "2026-05-20", "2026-05-25"),
    ("Jeju Canola Flower Festival", "제주유채꽃축제", "festival", "제주 서귀포", 33.3061, 126.2517, "2026-04-01", "2026-04-15"),
    ("Seoul Pet Show", "서울펫쇼", "exhibition", "COEX", 37.5116, 127.0593, "2025-09-05", "2025-09-07"),
    ("Seoul Motor Show", "서울모터쇼", "exhibition", "KINTEX", 37.6700, 126.7450, "2026-03-27", "2026-04-06"),
    ("Seoul Illustration Fair", "서울일러스트레이션페어", "exhibition", "COEX", 37.5116, 127.0593, "2025-12-19", "2025-12-21"),
    ("Winter Sonata Festival", "겨울연가축제", "festival", "춘천 남이섬", 37.7901, 127.5254, "2025-12-20", "2026-02-28"),
    ("Seoul Startup Festival", "서울창업축제", "exhibition", "DDP", 37.5671, 127.0090, "2026-05-14", "2026-05-16"),
    ("Gangneung Coffee Festival", "강릉커피축제", "food_festival", "강릉 안목해변", 37.7713, 128.9470, "2025-10-03", "2025-10-06"),
    # Extra to reach 88
    ("Seoul International Dance Festival", "서울국제무용제", "concert", "예술의전당", 37.4784, 127.0076, "2025-10-08", "2025-10-19"),
    ("Suwon Hwaseong Cultural Festival", "수원화성문화제", "festival", "수원 화성", 37.2866, 127.0015, "2025-10-07", "2025-10-09"),
    ("Sejong Street Performance Festival", "세종거리공연축제", "concert", "서울 세종문화회관", 37.5724, 126.9758, "2025-06-13", "2025-06-15"),
    ("Wonju Dynamic Dancing Carnival", "원주다이내믹댄싱카니발", "festival", "원주시", 37.3415, 127.9209, "2025-10-03", "2025-10-05"),
    ("Changwon K-Pop World Festival", "창원K-pop월드페스티벌", "concert", "창원 종합운동장", 35.2340, 128.6810, "2025-09-26", "2025-09-28"),
    ("Yeosu Night Sea Festival", "여수밤바다축제", "festival", "여수 해양공원", 34.7476, 127.7386, "2025-08-01", "2025-08-10"),
    ("Seoul International Writers Festival", "서울국제작가축제", "exhibition", "남산 한옥마을", 37.5590, 126.9940, "2025-10-10", "2025-10-13"),
    ("Goyang International Flower Festival", "고양국제꽃박람회", "exhibition", "고양 일산", 37.6590, 126.7680, "2025-04-25", "2025-05-12"),
    ("Buyeo Baekje Cultural Festival", "부여백제문화제", "festival", "부여 백제문화단지", 36.2838, 126.9060, "2025-10-01", "2025-10-07"),
    ("Seogwipo Jeju Art Festival", "서귀포예술축제", "art", "서귀포", 33.2479, 126.5628, "2026-02-14", "2026-02-16"),
    ("Seoul Craft Beer Week", "서울크래프트비어위크", "food_festival", "서울 성수동", 37.5441, 127.0570, "2026-05-20", "2026-05-25"),
    ("Gyeonggi International Ceramic Biennale", "경기세계도자비엔날레", "exhibition", "이천", 37.2718, 127.4349, "2025-04-26", "2025-06-01"),
    ("Jeonju International Film Festival", "전주국제영화제", "festival", "전주 한옥마을", 35.8151, 127.1528, "2025-05-01", "2025-05-10"),
    ("Seoul Illustration Fair Winter", "서울일러스트레이션페어 겨울", "exhibition", "COEX", 37.5116, 127.0593, "2026-01-09", "2026-01-11"),
    ("Pyeongchang Trout Festival", "평창송어축제", "festival", "평창", 37.3708, 128.3904, "2026-01-15", "2026-02-15"),
    ("Seoul Night Walking Festival", "서울야간산책축제", "festival", "서울 도심", 37.5662, 126.9781, "2025-09-05", "2025-09-07"),
    ("Sacheon Aerospace Expo", "사천항공우주엑스포", "exhibition", "사천 항공우주박물관", 35.0738, 128.0710, "2025-10-25", "2025-10-29"),
    ("Seoul Vegan Festival", "서울비건페스티벌", "food_festival", "DDP", 37.5671, 127.0090, "2025-11-14", "2025-11-16"),
    ("Namhae German Village Beer Festival", "남해독일마을맥주축제", "food_festival", "남해 독일마을", 34.8061, 127.9390, "2025-10-17", "2025-10-19"),
    ("Gwangju Food Festival", "광주음식문화축제", "food_festival", "광주 518기념공원", 35.1526, 126.8482, "2025-10-24", "2025-10-26"),
    ("Seoul LED Rose Festival", "서울장미축제", "festival", "서울 중랑천", 37.5780, 127.0490, "2025-05-15", "2025-05-31"),
]

def generate_festivals():
    festivals = []
    for idx, (name_en, name_ko, cat, venue, lat, lng, start, end) in enumerate(FESTIVAL_DATA):
        f = {
            "id": str(uuid.uuid4()),
            "name_en": name_en,
            "name_ko": name_ko,
            "description_en": f"Annual {cat} event held at {venue}. A must-visit for travelers exploring Korean culture.",
            "description_ko": f"{venue}에서 열리는 {name_ko}. 한국 문화를 체험하는 여행자에게 추천하는 행사입니다.",
            "category": cat,
            "venue_name": venue,
            "address": venue,
            "latitude": lat,
            "longitude": lng,
            "start_date": start,
            "end_date": end,
            "is_active": True,
        }
        festivals.append(f)
    return festivals


# =============================================================================
# COURSES - 70 extra
# =============================================================================
COURSE_TEMPLATES = [
    ("Gangnam Food Tour", "강남 맛집 투어", "food", "half_day", "easy", "Gangnam", [(37.4979,127.0276,"Gangnam Station","강남역"),(37.5194,127.0234,"Garosu-gil","가로수길"),(37.5247,127.0397,"Apgujeong Rodeo","압구정 로데오")]),
    ("Bukchon Heritage Walk", "북촌 한옥마을 산책", "history", "half_day", "easy", "Jongno", [(37.5826,126.9836,"Bukchon Hanok Village","북촌한옥마을"),(37.5793,126.9855,"Changdeokgung","창덕궁"),(37.5817,126.9838,"Samcheong-dong","삼청동")]),
    ("K-Pop Hotspots Tour", "K-Pop 성지순례", "kpop", "full_day", "easy", "Various", [(37.5563,126.9237,"Hongdae","홍대"),(37.5116,127.0593,"COEX SM Town","코엑스 SM타운"),(37.5088,127.0631,"Samsung Station","삼성역")]),
    ("Night Views of Seoul", "서울 야경 투어", "nightview", "half_day", "easy", "Various", [(37.5511,126.9882,"N Seoul Tower","남산타워"),(37.5253,126.9328,"Yeouido Han River","여의도한강"),(37.5207,127.1212,"Olympic Park","올림픽공원")]),
    ("Traditional Market Tour", "전통시장 투어", "shopping", "half_day", "easy", "Various", [(37.5700,126.9990,"Gwangjang Market","광장시장"),(37.5670,127.0090,"Dongdaemun Market","동대문시장"),(37.5636,126.9869,"Myeongdong","명동")]),
    ("Nature & Temple Walk", "자연과 사찰 탐방", "nature", "full_day", "moderate", "Northern Seoul", [(37.6596,126.9787,"Bukhansan Trail","북한산 트레일"),(37.5826,126.9836,"Bukchon","북촌"),(37.5793,126.9855,"Changdeokgung Secret Garden","창덕궁 후원")]),
    ("Art & Design Seoul", "서울 아트 투어", "art", "half_day", "easy", "Various", [(37.5671,127.0090,"DDP","동대문디자인플라자"),(37.5441,127.0570,"Seongsu Art Street","성수동 예술거리"),(37.5190,127.0220,"Garosu-gil Galleries","가로수길 갤러리")]),
    ("Han River Cycling", "한강 자전거 투어", "nature", "half_day", "moderate", "Han River", [(37.5253,126.9328,"Yeouido","여의도"),(37.5171,126.9314,"Mapo Bridge","마포대교"),(37.5088,126.9657,"Yongsan","용산")]),
    ("Itaewon Global Food Walk", "이태원 글로벌 맛집", "food", "half_day", "easy", "Itaewon", [(37.5344,126.9942,"Itaewon Main St","이태원 메인거리"),(37.5346,126.9872,"Noksapyeong","녹사평"),(37.5346,127.0000,"Hannam-dong","한남동")]),
    ("Royal Palace Trail", "궁궐 트레일", "history", "full_day", "easy", "Central Seoul", [(37.5796,126.9770,"Gyeongbokgung","경복궁"),(37.5793,126.9855,"Changdeokgung","창덕궁"),(37.5714,126.9952,"Changgyeonggung","창경궁"),(37.5680,126.9966,"Jongmyo","종묘")]),
    ("Seoul Cafe Hopping", "서울 카페 투어", "food", "half_day", "easy", "Various", [(37.5437,127.0562,"Seongsu Cafes","성수동 카페"),(37.5623,126.9258,"Yeonnam Cafes","연남동 카페"),(37.5834,126.9843,"Bukchon Cafes","북촌 카페")]),
    ("Myeongdong Shopping", "명동 쇼핑 투어", "shopping", "half_day", "easy", "Myeongdong", [(37.5636,126.9869,"Myeongdong Main","명동 메인거리"),(37.5649,126.9817,"Lotte","롯데백화점"),(37.5617,126.9923,"Namsan entrance","남산입구")]),
    ("Jamsil Adventure", "잠실 어드벤처", "nature", "full_day", "easy", "Songpa", [(37.5116,127.0593,"COEX","코엑스"),(37.5133,127.0998,"Lotte World","롯데월드"),(37.5207,127.1212,"Olympic Park","올림픽공원")]),
    ("Hongdae Culture Walk", "홍대 문화 산책", "art", "half_day", "easy", "Hongdae", [(37.5563,126.9237,"Hongdae Main","홍대 거리"),(37.5590,126.9233,"Yeonnam-dong","연남동"),(37.5497,126.9146,"Mangwon Market","망원시장")]),
]

def generate_courses():
    courses = []
    spots_all = []
    transitions_all = []

    for idx, (name_en, name_ko, theme, dur, diff, region, spot_list) in enumerate(COURSE_TEMPLATES):
        course_id = str(uuid.uuid4())
        duration_minutes = 240 if dur == "half_day" else 480
        total_distance = round(random.uniform(5, 25), 1)

        c = {
            "id": course_id,
            "name_en": name_en,
            "name_ko": name_ko,
            "description_en": f"Explore the best of {region} with this curated {dur.replace('_', ' ')} course focusing on {theme}.",
            "description_ko": f"{region} 지역의 {theme} 테마 {dur.replace('_', ' ')} 코스입니다.",
            "duration": dur.replace("_", " ").title(),
            "duration_type": dur,
            "theme": theme,
            "region": region,
            "difficulty": diff,
            "total_duration_minutes": duration_minutes,
            "total_distance_km": total_distance,
            "estimated_transport_cost": random.randint(3000, 15000),
            "avg_rating": round(random.uniform(3.8, 4.9), 1),
            "review_count": random.randint(5, 120),
            "is_active": True,
        }
        courses.append(c)

        for si, (lat, lng, spot_en, spot_ko) in enumerate(spot_list):
            spot_id = str(uuid.uuid4())
            stay = random.randint(30, 90)
            s = {
                "id": spot_id,
                "course_id": course_id,
                "spot_order": si + 1,
                "name_en": spot_en,
                "name_ko": spot_ko,
                "description_en": f"Visit {spot_en} - a popular spot in {region}.",
                "description_ko": f"{spot_ko} - {region} 지역의 인기 장소입니다.",
                "latitude": lat,
                "longitude": lng,
                "stay_duration_minutes": stay,
            }
            spots_all.append(s)

            if si < len(spot_list) - 1:
                mode = random.choice(["walk", "bus", "subway", "taxi"])
                t = {
                    "id": str(uuid.uuid4()),
                    "from_spot_id": spot_id,
                    "transport_mode": mode,
                    "duration_minutes": random.randint(5, 30),
                    "distance_km": round(random.uniform(0.5, 5.0), 1),
                }
                transitions_all.append(t)

    # Generate more courses by cycling through templates with variations
    themes_extra = ["food", "history", "kpop", "nightview", "shopping", "nature", "art", "tradition"]
    durations = ["half_day", "full_day", "two_day"]
    diffs = ["easy", "moderate", "challenging"]

    for i in range(56):  # 14 + 56 = 70 total extra courses
        theme = themes_extra[i % len(themes_extra)]
        dur = durations[i % len(durations)]
        diff = diffs[i % len(diffs)]
        region = REGIONS[i % len(REGIONS)]

        course_id = str(uuid.uuid4())
        duration_minutes = 240 if dur == "half_day" else 480 if dur == "full_day" else 960

        name_en = f"{region} {theme.title()} {'Discovery' if i%3==0 else 'Adventure' if i%3==1 else 'Experience'}"
        name_ko = f"{region} {theme} {'탐방' if i%3==0 else '모험' if i%3==1 else '체험'}"

        c = {
            "id": course_id,
            "name_en": name_en,
            "name_ko": name_ko,
            "description_en": f"A curated {dur.replace('_', ' ')} {theme} course in the {region} area of Seoul.",
            "description_ko": f"서울 {region} 지역의 {theme} 테마 코스입니다.",
            "duration": dur.replace("_", " ").title(),
            "duration_type": dur,
            "theme": theme,
            "region": region,
            "difficulty": diff,
            "total_duration_minutes": duration_minutes,
            "total_distance_km": round(random.uniform(3, 30), 1),
            "estimated_transport_cost": random.randint(2000, 20000),
            "avg_rating": round(random.uniform(3.5, 4.9), 1),
            "review_count": random.randint(3, 80),
            "is_active": True,
        }
        courses.append(c)

        # Generate 3-4 spots per course
        num_spots = random.randint(3, 4)
        base_lat = 37.50 + random.uniform(0, 0.1)
        base_lng = 126.90 + random.uniform(0, 0.15)

        prev_spot_id = None
        for si in range(num_spots):
            spot_id = str(uuid.uuid4())
            s = {
                "id": spot_id,
                "course_id": course_id,
                "spot_order": si + 1,
                "name_en": f"Spot {si+1}",
                "name_ko": f"스팟 {si+1}",
                "latitude": base_lat + random.uniform(-0.02, 0.02),
                "longitude": base_lng + random.uniform(-0.02, 0.02),
                "stay_duration_minutes": random.randint(20, 90),
            }
            spots_all.append(s)

            if prev_spot_id:
                t = {
                    "id": str(uuid.uuid4()),
                    "from_spot_id": prev_spot_id,
                    "transport_mode": random.choice(["walk", "bus", "subway", "taxi"]),
                    "duration_minutes": random.randint(5, 25),
                    "distance_km": round(random.uniform(0.3, 4.0), 1),
                }
                transitions_all.append(t)
            prev_spot_id = spot_id

    return courses, spots_all, transitions_all


if __name__ == "__main__":
    print(f"Extra Restaurants: {len(generate_restaurants())}")
    guides = generate_guides()
    print(f"Extra Guides: {len(guides)}")
    festivals = generate_festivals()
    print(f"Extra Festivals: {len(festivals)}")
    courses, spots, trans = generate_courses()
    print(f"Extra Courses: {len(courses)}, Spots: {len(spots)}, Transitions: {len(trans)}")
