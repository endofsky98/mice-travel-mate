import uuid

def _id():
    return str(uuid.uuid4())

def get_guides():
    guides = []

    def guide(name_en, name_ko, bio_en, bio_ko, langs, specialties, regions, h_rate, hd_rate, fd_rate, services_en, services_ko, rating, reviews, names_extra=None, bios_extra=None, services_extra=None):
        guides.append({
            "id": _id(), "user_id": None,
            "name_en": name_en, "name_ko": name_ko,
            "name_zh_cn": (names_extra or {}).get("zh_cn", name_en),
            "name_zh_tw": (names_extra or {}).get("zh_tw", name_en),
            "name_ja": (names_extra or {}).get("ja", name_en),
            "name_es": (names_extra or {}).get("es", name_en),
            "name_th": (names_extra or {}).get("th", name_en),
            "name_vi": (names_extra or {}).get("vi", name_en),
            "name_fr": (names_extra or {}).get("fr", name_en),
            "bio_en": bio_en, "bio_ko": bio_ko,
            "bio_zh_cn": (bios_extra or {}).get("zh_cn", bio_en),
            "bio_zh_tw": (bios_extra or {}).get("zh_tw", bio_en),
            "bio_ja": (bios_extra or {}).get("ja", bio_en),
            "bio_es": (bios_extra or {}).get("es", bio_en),
            "bio_th": (bios_extra or {}).get("th", bio_en),
            "bio_vi": (bios_extra or {}).get("vi", bio_en),
            "bio_fr": (bios_extra or {}).get("fr", bio_en),
            "profile_image_url": (['https://images.unsplash.com/photo-1580489944761-15a19d654956?w=600', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600', 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=600', 'https://images.unsplash.com/photo-1542190891-2093d38760f2?w=600', 'https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?w=600'])[len(guides) % 5],
            "languages": langs,
            "specialties": specialties,
            "regions": regions,
            "price_per_hour_usd": h_rate,
            "price_half_day_usd": hd_rate,
            "price_full_day_usd": fd_rate,
            "services_en": services_en, "services_ko": services_ko,
            "services_zh_cn": (services_extra or {}).get("zh_cn", services_en),
            "services_zh_tw": (services_extra or {}).get("zh_tw", services_en),
            "services_ja": (services_extra or {}).get("ja", services_en),
            "services_es": (services_extra or {}).get("es", services_en),
            "services_th": (services_extra or {}).get("th", services_en),
            "services_vi": (services_extra or {}).get("vi", services_en),
            "services_fr": (services_extra or {}).get("fr", services_en),
            "avg_rating": rating, "review_count": reviews, "status": "active",
        })

    # Korean guides (8)
    guide("Kim Jihoon", "김지훈",
        "Certified tour guide with 10+ years experience specializing in Korean history and culture. Former history professor.",
        "10년 이상 경력의 공인 관광 가이드. 한국 역사와 문화 전문. 전 역사학 교수.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ja", "level": "conversational"}],
        ["history_culture", "food"], ["gangnam", "seocho", "jongno"],
        30, 100, 180, "Walking tours, palace tours, food tours, cultural experiences",
        "워킹 투어, 궁궐 투어, 맛집 투어, 문화 체험", 4.9, 145)

    guide("Park Soyeon", "박소연",
        "Young and energetic guide passionate about K-Pop and Korean pop culture. Speaks 3 languages fluently.",
        "K-POP과 한국 대중문화에 열정적인 젊고 에너지 넘치는 가이드. 3개 국어 유창.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "zh", "level": "conversational"}],
        ["kpop_hallyu", "shopping"], ["gangnam", "hongdae"],
        25, 80, 150, "K-Pop tours, shopping guides, nightlife, photo tours",
        "K-POP 투어, 쇼핑 가이드, 나이트라이프, 포토 투어", 4.8, 120)

    guide("Lee Minho", "이민호",
        "Adventure and nature specialist. Certified mountain guide with extensive knowledge of Seoul's trails and hidden spots.",
        "모험과 자연 전문가. 서울 등산로와 숨겨진 명소에 해박한 공인 산악 가이드.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["nature", "food"], ["gangnam", "seocho"],
        20, 70, 130, "Hiking tours, nature walks, cycling tours, outdoor activities",
        "등산 투어, 자연 산책, 자전거 투어, 아웃도어 활동", 4.7, 88)

    guide("Choi Yuna", "최유나",
        "Professional food critic and culinary guide. Expert in Korean cuisine and restaurant recommendations.",
        "전문 음식 평론가 겸 미식 가이드. 한국 요리와 맛집 추천 전문.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "fr", "level": "conversational"}],
        ["food", "shopping"], ["gangnam", "seocho", "itaewon"],
        35, 120, 220, "Food tours, cooking classes, market tours, wine pairing",
        "맛집 투어, 쿠킹 클래스, 시장 투어, 와인 페어링", 4.9, 132)

    guide("Jung Taehyun", "정태현",
        "Business and MICE specialist. Helps corporate travelers maximize their Seoul experience.",
        "비즈니스 및 MICE 전문가. 기업 출장자의 서울 경험 극대화를 돕습니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ja", "level": "fluent"}],
        ["business", "food"], ["gangnam", "seocho"],
        45, 150, 280, "Business tours, networking events, MICE support, interpretation",
        "비즈니스 투어, 네트워킹 이벤트, MICE 지원, 통역", 4.6, 54)

    guide("Yoon Jiyeon", "윤지연",
        "Art and culture enthusiast with deep knowledge of Seoul's gallery scene and traditional crafts.",
        "서울 갤러리와 전통 공예에 해박한 예술·문화 애호가.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "es", "level": "conversational"}],
        ["history_culture", "shopping"], ["gangnam", "seocho", "jongno"],
        25, 85, 160, "Art gallery tours, craft workshops, museum tours, cultural experiences",
        "미술관 투어, 공예 워크숍, 박물관 투어, 문화 체험", 4.7, 67)

    guide("Han Sungwoo", "한성우",
        "Night photography and nightlife specialist. Knows every rooftop bar and hidden gem.",
        "야간 사진·나이트라이프 전문가. 모든 루프탑 바와 숨은 명소를 압니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["nightlife", "kpop_hallyu"], ["gangnam", "itaewon", "hongdae"],
        30, 100, 180, "Night tours, photography walks, bar crawls, nightlife guide",
        "야경 투어, 사진 산책, 바 크롤, 나이트라이프 가이드", 4.5, 76)

    guide("Song Minji", "송민지",
        "Wellness and K-Beauty expert. Helps visitors discover Korean beauty and wellness culture.",
        "웰니스와 K-뷰티 전문가. 한국의 뷰티·웰니스 문화를 알려드립니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "zh", "level": "basic"}],
        ["shopping", "nature"], ["gangnam", "seocho", "myeongdong"],
        25, 80, 150, "K-Beauty tours, spa experiences, wellness retreats, shopping",
        "K-뷰티 투어, 스파 체험, 웰니스 리트릿, 쇼핑", 4.8, 91)

    # Chinese guides (5)
    guide("Wang Lei", "왕레이",
        "Chinese-Korean bilingual guide born in Seoul. Expert in Korean shopping and food scenes.",
        "서울 출생 중한 이중언어 가이드. 한국 쇼핑·먹거리 전문.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["shopping", "food"], ["gangnam", "myeongdong"],
        20, 70, 130, "Shopping tours, food tours, translation services, duty-free guidance",
        "쇼핑 투어, 맛집 투어, 통역 서비스, 면세점 안내",
        4.6, 98, {"zh_cn": "王磊", "zh_tw": "王磊"})

    guide("Li Xiaomei", "리샤오메이",
        "Passionate about Korean culture with 5 years guide experience. Specializes in K-Drama filming locations.",
        "5년 경력의 한국 문화 열정 가이드. 한국 드라마 촬영지 전문.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["kpop_hallyu", "history_culture"], ["gangnam", "jongno"],
        18, 65, 120, "Drama location tours, K-Pop tours, palace tours",
        "드라마 촬영지 투어, K-POP 투어, 궁궐 투어",
        4.7, 82, {"zh_cn": "李小美", "zh_tw": "李小美"})

    guide("Zhang Wei", "장웨이",
        "Business interpreter and tour guide. Helps Chinese business travelers in Seoul's MICE district.",
        "비즈니스 통역 겸 관광 가이드. 서울 MICE 지구의 중국 비즈니스 여행객 지원.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "fluent"}],
        ["business", "food"], ["gangnam", "seocho"],
        40, 130, 240, "Business interpretation, MICE support, VIP tours, restaurant reservations",
        "비즈니스 통역, MICE 지원, VIP 투어, 식당 예약",
        4.5, 44, {"zh_cn": "张伟", "zh_tw": "張偉"})

    guide("Chen Yuki", "천유키",
        "Trilingual guide specializing in temple stays and spiritual experiences in Korea.",
        "한국의 템플스테이와 영적 체험 전문 3개 국어 가이드.",
        [{"code": "zh", "level": "native"}, {"code": "ja", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["history_culture", "nature"], ["gangnam", "seocho"],
        22, 75, 140, "Temple stays, meditation tours, cultural immersion, nature walks",
        "템플스테이, 명상 투어, 문화 체험, 자연 산책",
        4.8, 56, {"zh_cn": "陈由纪", "zh_tw": "陳由紀"})

    guide("Liu Mei", "류메이",
        "Fashion and beauty blogger turned guide. Knows every hidden shop and beauty salon in Gangnam.",
        "패션·뷰티 블로거 출신 가이드. 강남의 모든 숨은 가게와 뷰티 살롱을 압니다.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["shopping", "kpop_hallyu"], ["gangnam", "seocho", "myeongdong"],
        22, 75, 140, "Shopping tours, K-Beauty experiences, fashion districts, social media tours",
        "쇼핑 투어, K-뷰티 체험, 패션 지구, SNS 투어",
        4.6, 71, {"zh_cn": "刘美", "zh_tw": "劉美"})

    # Japanese guides (4)
    guide("Tanaka Yuki", "다나카 유키",
        "Japanese guide living in Seoul for 8 years. Expert in comparing Korean and Japanese cultures.",
        "서울 거주 8년차 일본인 가이드. 한일 문화 비교 전문.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["food", "history_culture"], ["gangnam", "seocho", "itaewon"],
        25, 85, 160, "Food tours, culture tours, translation, restaurant guidance",
        "맛집 투어, 문화 투어, 통역, 식당 안내",
        4.7, 93, {"ja": "田中ゆき"})

    guide("Suzuki Haruto", "스즈키 하루토",
        "Active outdoors guide offering hiking and cycling tours around Seoul.",
        "서울 주변 하이킹·사이클링 투어를 제공하는 활동적인 아웃도어 가이드.",
        [{"code": "ja", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["nature", "food"], ["gangnam", "seocho"],
        20, 70, 130, "Hiking tours, cycling, outdoor adventures, nature photography",
        "하이킹 투어, 사이클링, 아웃도어 모험, 자연 사진",
        4.5, 45, {"ja": "鈴木はると"})

    guide("Sato Mika", "사토 미카",
        "K-Pop fan and Hallyu culture specialist. Guides Japanese fans to K-Pop hotspots.",
        "K-POP 팬이자 한류 문화 전문가. 일본 팬들을 K-POP 핫스팟으로 안내.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["kpop_hallyu", "shopping"], ["gangnam", "hongdae"],
        22, 75, 140, "K-Pop tours, fan meetup assistance, concert logistics, merchandise shopping",
        "K-POP 투어, 팬미팅 지원, 콘서트 물류, 굿즈 쇼핑",
        4.8, 110, {"ja": "佐藤みか"})

    guide("Nakamura Ken", "나카무라 켄",
        "Business and MICE guide for Japanese corporate visitors in the COEX area.",
        "코엑스 지역 일본 기업 방문객을 위한 비즈니스·MICE 가이드.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "fluent"}],
        ["business", "food"], ["gangnam", "seocho"],
        40, 130, 240, "Business interpretation, MICE support, corporate dinners, business culture guidance",
        "비즈니스 통역, MICE 지원, 기업 회식, 비즈니스 문화 안내",
        4.6, 38, {"ja": "中村健"})

    # American/British (3)
    guide("James Wilson", "제임스 윌슨",
        "American expat in Seoul for 12 years. Deep local knowledge with a fun personality.",
        "서울 거주 12년차 미국인. 깊은 현지 지식과 재미있는 성격의 소유자.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "fluent"}],
        ["food", "nightlife", "local_experience"], ["gangnam", "itaewon", "hongdae"],
        30, 100, 180, "Food tours, bar crawls, local experience tours, photo walks",
        "맛집 투어, 바 크롤, 로컬 체험 투어, 포토 워크", 4.7, 108)

    guide("Sarah Thompson", "사라 톰슨",
        "British wellness expert and yoga instructor. Combines travel with mindfulness.",
        "영국인 웰니스 전문가 겸 요가 강사. 여행과 마음챙김을 결합합니다.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "conversational"}],
        ["nature", "history_culture"], ["gangnam", "seocho"],
        25, 85, 160, "Wellness tours, yoga sessions, meditation, temple visits, nature walks",
        "웰니스 투어, 요가 세션, 명상, 사찰 방문, 자연 산책", 4.8, 62)

    guide("Michael Brown", "마이클 브라운",
        "Professional photographer and guide. Helps visitors capture stunning Seoul photos.",
        "전문 사진작가 겸 가이드. 멋진 서울 사진을 찍을 수 있도록 도와드립니다.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "conversational"}, {"code": "es", "level": "basic"}],
        ["nightlife", "nature"], ["gangnam", "jongno"],
        35, 120, 220, "Photography tours, night photography, portrait sessions, Instagram tours",
        "사진 투어, 야경 촬영, 인물 촬영, 인스타 투어", 4.6, 55)

    # Spanish (2)
    guide("Carlos Rodriguez", "카를로스 로드리게스",
        "Spanish guide living in Korea. Passionate about Korean history and food culture.",
        "한국 거주 스페인인 가이드. 한국 역사와 음식 문화에 열정적.",
        [{"code": "es", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["history_culture", "food"], ["gangnam", "jongno"],
        22, 75, 140, "Historical tours, food tours, cultural experiences, language exchange",
        "역사 투어, 맛집 투어, 문화 체험, 언어 교환", 4.5, 34)

    guide("Maria Garcia", "마리아 가르시아",
        "Latin dance instructor and K-Pop enthusiast. Energetic tours with a unique perspective.",
        "라틴 댄스 강사 겸 K-POP 팬. 독특한 시각의 에너지 넘치는 투어.",
        [{"code": "es", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["kpop_hallyu", "nightlife"], ["gangnam", "hongdae"],
        20, 70, 130, "K-Pop dance tours, nightlife tours, entertainment district guides",
        "K-POP 댄스 투어, 나이트라이프 투어, 유흥가 가이드", 4.4, 28)

    # French (2)
    guide("Pierre Dubois", "피에르 뒤부아",
        "French chef turned guide. Compares French and Korean culinary traditions.",
        "프랑스 셰프 출신 가이드. 프랑스·한국 요리 전통을 비교합니다.",
        [{"code": "fr", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "shopping"], ["gangnam", "seocho", "itaewon"],
        35, 120, 220, "Gourmet food tours, cooking classes, wine & Korean food pairing, market tours",
        "미식 투어, 쿠킹 클래스, 와인 & 한식 페어링, 시장 투어", 4.8, 47)

    guide("Sophie Laurent", "소피 로랑",
        "Fashion designer and style consultant. Guides fashion-focused tours in Gangnam.",
        "패션 디자이너 겸 스타일 컨설턴트. 강남 패션 중심 투어 진행.",
        [{"code": "fr", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["shopping", "kpop_hallyu"], ["gangnam", "seocho"],
        30, 100, 180, "Fashion tours, K-Beauty shopping, designer boutique visits, style consulting",
        "패션 투어, K-뷰티 쇼핑, 디자이너 부티크, 스타일 컨설팅", 4.5, 33)

    # Thai (2)
    guide("Somchai Patel", "솜차이 파텔",
        "Thai guide helping Southeast Asian visitors navigate Seoul. Fluent in Thai and English.",
        "동남아 방문객의 서울 여행을 돕는 태국인 가이드. 태국어와 영어 유창.",
        [{"code": "th", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "shopping"], ["gangnam", "myeongdong"],
        18, 60, 110, "Food tours (halal-friendly options), shopping tours, temple visits",
        "맛집 투어 (할랄 옵션), 쇼핑 투어, 사찰 방문", 4.5, 45)

    guide("Ploy Siriwan", "플로이 시리완",
        "Thai-Korean bilingual guide specializing in K-Pop tours for Thai fans.",
        "태국 K-POP 팬을 위한 태한 이중언어 K-POP 투어 전문 가이드.",
        [{"code": "th", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["kpop_hallyu", "shopping"], ["gangnam", "hongdae"],
        20, 70, 130, "K-Pop tours, fan events, shopping, entertainment district guides",
        "K-POP 투어, 팬 이벤트, 쇼핑, 엔터가 가이드", 4.7, 67)

    # Vietnamese (2)
    guide("Nguyen Van Thanh", "응우옌 반 탄",
        "Vietnamese guide in Seoul specializing in budget-friendly tours and local food experiences.",
        "저렴한 투어와 현지 음식 체험 전문 서울 거주 베트남인 가이드.",
        [{"code": "vi", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["food", "local_experience"], ["gangnam", "seocho"],
        15, 50, 95, "Budget tours, street food tours, local market visits, translation",
        "저렴 투어, 길거리 음식 투어, 재래시장 방문, 통역", 4.4, 38)

    guide("Tran Thi Mai", "쩐 티 마이",
        "Vietnamese beauty blogger and shopping guide. Knows the best deals in Gangnam.",
        "베트남 뷰티 블로거 겸 쇼핑 가이드. 강남 최저가를 압니다.",
        [{"code": "vi", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["shopping", "kpop_hallyu"], ["gangnam", "myeongdong"],
        18, 60, 110, "Shopping tours, duty-free guidance, K-Beauty tours, Instagram spots",
        "쇼핑 투어, 면세점 안내, K-뷰티 투어, 인스타 명소", 4.6, 52)

    # Other (2)
    guide("Ahmed Hassan", "아메드 하산",
        "Arabic-speaking guide specializing in halal food and Muslim-friendly tours in Seoul.",
        "서울의 할랄 음식 및 무슬림 친화 투어 전문 아랍어 가이드.",
        [{"code": "ar", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "history_culture"], ["gangnam", "itaewon"],
        25, 85, 160, "Halal food tours, Muslim-friendly tours, mosque visits, cultural bridge tours",
        "할랄 맛집 투어, 무슬림 친화 투어, 모스크 방문, 문화 교류 투어", 4.7, 41)

    guide("Anna Petrova", "안나 페트로바",
        "Russian guide with background in Korean studies. Passionate about Korean traditional culture.",
        "한국학 전공 러시아인 가이드. 한국 전통 문화에 열정적.",
        [{"code": "ru", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "fluent"}],
        ["history_culture", "nature"], ["gangnam", "seocho", "jongno"],
        22, 75, 140, "Cultural tours, temple visits, traditional craft workshops, nature walks",
        "문화 투어, 사찰 방문, 전통 공예 워크숍, 자연 산책", 4.5, 29)

    # ═══════════════════════════════════════════════
    # ADDITIONAL 70 GUIDES (31-100)
    # ═══════════════════════════════════════════════

    # ── Korean guides (10 more) ──
    guide("Baek Seunghyun", "백승현",
        "Former chef turned food guide. Specializes in hidden gem restaurants and Korean street food tours.",
        "전직 셰프 출신 음식 가이드. 숨은 맛집과 길거리 음식 투어 전문.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["food", "local_experience"], ["jongno", "mapo", "yeongdeungpo"],
        28, 95, 170, "Street food tours, hidden restaurant tours, cooking workshops, market explorations",
        "길거리 음식 투어, 숨은 맛집 투어, 쿠킹 워크숍, 시장 탐방", 4.7, 112)

    guide("Shin Eunji", "신은지",
        "Licensed interpreter and cultural guide. Expert in Korean modern history and DMZ tours.",
        "공인 통역사 겸 문화 가이드. 한국 근현대사와 DMZ 투어 전문.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "zh", "level": "conversational"}],
        ["history_culture", "nature"], ["jongno", "seocho"],
        32, 110, 200, "DMZ tours, historical walking tours, museum tours, war memorial visits",
        "DMZ 투어, 역사 워킹 투어, 박물관 투어, 전쟁기념관 방문", 4.8, 98)

    guide("Oh Jaehyun", "오재현",
        "Professional photographer guide specializing in Seoul sunrise and sunset photo spots.",
        "서울 일출·일몰 포토 스팟 전문 프로 사진작가 가이드.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ja", "level": "basic"}],
        ["nature", "nightlife"], ["gangnam", "jongno", "mapo"],
        35, 120, 220, "Photography tours, sunrise/sunset spots, portrait sessions, hidden Seoul spots",
        "사진 투어, 일출/일몰 스팟, 인물 촬영, 서울 숨은 명소", 4.6, 76)

    guide("Kang Mirae", "강미래",
        "Yoga instructor and wellness guide. Combines traditional Korean wellness with modern mindfulness.",
        "요가 강사 겸 웰니스 가이드. 한국 전통 웰니스와 현대 마음챙김을 결합.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["nature", "local_experience"], ["gangnam", "seocho"],
        25, 85, 160, "Wellness tours, yoga sessions, jjimjilbang experiences, meditation retreats",
        "웰니스 투어, 요가 세션, 찜질방 체험, 명상 리트릿", 4.7, 64)

    guide("Noh Dongwon", "노동원",
        "Retired university professor specializing in Korean palace architecture and Joseon dynasty history.",
        "은퇴한 대학 교수. 한국 궁궐 건축과 조선왕조 역사 전문.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ja", "level": "conversational"}],
        ["history_culture"], ["jongno", "seocho"],
        35, 120, 220, "Palace architecture tours, Joseon history walks, scholarly lectures, heritage tours",
        "궁궐 건축 투어, 조선 역사 산책, 학술 강의, 유산 투어", 4.9, 52)

    guide("Im Chaeyoung", "임채영",
        "K-Drama and K-Pop filming location specialist. Runs immersive fan experience tours.",
        "K-드라마·K-POP 촬영지 전문가. 몰입형 팬 체험 투어 진행.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "zh", "level": "basic"}],
        ["kpop_hallyu", "shopping"], ["gangnam", "hongdae", "jongno"],
        22, 75, 140, "Drama filming tours, K-Pop dance class, fan meetup support, photo tours",
        "드라마 촬영지 투어, K-POP 댄스 수업, 팬미팅 지원, 포토 투어", 4.6, 134)

    guide("Seo Jungmin", "서정민",
        "Night market and street food expert. Knows every late-night food alley in Seoul.",
        "야시장과 길거리 음식 전문가. 서울의 모든 심야 먹자골목을 꿰고 있습니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["food", "nightlife"], ["mapo", "jongno", "yeongdeungpo"],
        20, 70, 130, "Night market tours, pojangmacha crawls, late-night food tours, soju culture",
        "야시장 투어, 포장마차 크롤, 심야 맛집 투어, 소주 문화", 4.4, 88)

    guide("Hwang Serin", "황세린",
        "Fashion stylist and Gangnam shopping guide. Helps visitors build their Korean fashion wardrobe.",
        "패션 스타일리스트 겸 강남 쇼핑 가이드. 한국 패션 워드로브 구성을 도와드립니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "fr", "level": "basic"}],
        ["shopping", "kpop_hallyu"], ["gangnam", "seocho", "myeongdong"],
        30, 100, 180, "Fashion shopping tours, styling consultations, K-Beauty guides, outlet tours",
        "패션 쇼핑 투어, 스타일링 컨설팅, K-뷰티 가이드, 아울렛 투어", 4.5, 71)

    guide("Ryu Taeyang", "류태양",
        "Mountain and cycling guide. Certified Korea hiking guide with extensive trail knowledge.",
        "산악·자전거 가이드. 공인 한국 등산 가이드로 산길 지식이 풍부합니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "conversational"}],
        ["nature"], ["gangnam", "seocho"],
        18, 65, 120, "Mountain hiking tours, cycling tours, nature photography, fitness tours",
        "등산 투어, 자전거 투어, 자연 사진, 피트니스 투어", 4.6, 47)

    guide("Yang Jihye", "양지혜",
        "Tea ceremony and traditional craft specialist. Teaches Korean calligraphy and pottery making.",
        "다도 및 전통 공예 전문가. 한국 서예와 도자기 만들기를 가르칩니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ja", "level": "conversational"}],
        ["history_culture", "local_experience"], ["jongno", "seocho"],
        25, 85, 160, "Tea ceremony experiences, pottery workshops, calligraphy classes, hanbok experiences",
        "다도 체험, 도자기 워크숍, 서예 수업, 한복 체험", 4.8, 55)

    # ── Chinese guides (8 more) ──
    guide("Sun Xiaoli", "쑨샤오리",
        "Chinese food blogger and Seoul restaurant guide specializing in authentic Chinese food in Seoul.",
        "중국 음식 블로거 겸 서울 레스토랑 가이드. 서울의 정통 중식 전문.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["food", "shopping"], ["gangnam", "myeongdong", "jongno"],
        20, 70, 130, "Chinese food tours, Korean restaurant guidance, translation, duty-free shopping",
        "중식 맛집 투어, 한식당 안내, 통역, 면세점 쇼핑",
        4.5, 87, {"zh_cn": "孙小丽", "zh_tw": "孫小麗"})

    guide("Huang Jie", "황제",
        "Tech industry guide for Chinese business travelers. Expert in Seoul's startup ecosystem.",
        "중국 비즈니스 여행객을 위한 테크 산업 가이드. 서울 스타트업 생태계 전문.",
        [{"code": "zh", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "fluent"}],
        ["business", "local_experience"], ["gangnam", "seocho"],
        45, 150, 280, "Tech company visits, startup tours, business interpretation, networking events",
        "테크 기업 방문, 스타트업 투어, 비즈니스 통역, 네트워킹 이벤트",
        4.6, 42, {"zh_cn": "黄杰", "zh_tw": "黃傑"})

    guide("Zhou Mingyu", "저우밍위",
        "History enthusiast specializing in Korea-China historical connections and ancient trade routes.",
        "한·중 역사적 연결과 고대 교역로 전문 역사 애호가.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["history_culture"], ["jongno", "seocho"],
        22, 75, 140, "Historical tours, museum visits, palace tours, cultural comparison talks",
        "역사 투어, 박물관 방문, 궁궐 투어, 문화 비교 강연",
        4.4, 38, {"zh_cn": "周明宇", "zh_tw": "周明宇"})

    guide("Zhao Yilin", "자오이린",
        "K-Beauty and skincare expert. Guides Chinese visitors to the best Korean cosmetics shops.",
        "K-뷰티·스킨케어 전문가. 중국 방문객을 최고의 한국 화장품 매장으로 안내.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["shopping", "kpop_hallyu"], ["gangnam", "myeongdong"],
        22, 75, 140, "K-Beauty tours, skincare consultations, cosmetics shopping, dermatology clinic tours",
        "K-뷰티 투어, 스킨케어 상담, 화장품 쇼핑, 피부과 클리닉 투어",
        4.7, 96, {"zh_cn": "赵艺琳", "zh_tw": "趙藝琳"})

    guide("Ma Donghai", "마둥하이",
        "Professional photographer from Beijing. Leads photo tours capturing Seoul's best angles.",
        "베이징 출신 프로 사진작가. 서울의 최고 앵글을 담는 포토 투어 진행.",
        [{"code": "zh", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["nature", "nightlife"], ["gangnam", "jongno", "mapo"],
        30, 100, 180, "Photography tours, night photography, Instagram spot tours, portrait sessions",
        "사진 투어, 야경 촬영, 인스타 스팟 투어, 인물 촬영",
        4.5, 55, {"zh_cn": "马东海", "zh_tw": "馬東海"})

    guide("Wu Qian", "우치엔",
        "Family travel specialist for Chinese families. Creates kid-friendly itineraries in Seoul.",
        "중국 가족 여행 전문가. 어린이 친화 서울 여행 코스를 기획합니다.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["local_experience", "food"], ["gangnam", "songpa"],
        18, 60, 110, "Family tours, kid-friendly itineraries, theme park visits, educational tours",
        "가족 투어, 어린이 친화 일정, 테마파크 방문, 교육 투어",
        4.6, 73, {"zh_cn": "吴倩", "zh_tw": "吳倩"})

    guide("Deng Zihao", "덩쯔하오",
        "Outdoor adventure guide. Expert in Han River activities and Seoul's nature spots.",
        "아웃도어 어드벤처 가이드. 한강 액티비티와 서울 자연 명소 전문.",
        [{"code": "zh", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["nature", "food"], ["gangnam", "mapo"],
        20, 70, 130, "Han River activities, cycling tours, hiking, kayaking, outdoor photography",
        "한강 액티비티, 자전거 투어, 등산, 카약, 야외 사진",
        4.4, 48, {"zh_cn": "邓子浩", "zh_tw": "鄧子浩"})

    guide("Liang Wenxin", "량원신",
        "Luxury shopping and gastronomy guide for high-end Chinese travelers visiting Seoul.",
        "서울을 방문하는 고급 중국 여행객을 위한 럭셔리 쇼핑·미식 가이드.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "fluent"}],
        ["shopping", "food"], ["gangnam", "seocho"],
        50, 170, 320, "Luxury shopping, fine dining reservations, VIP experiences, personal styling",
        "럭셔리 쇼핑, 파인다이닝 예약, VIP 체험, 퍼스널 스타일링",
        4.8, 35, {"zh_cn": "梁文欣", "zh_tw": "梁文欣"})

    # ── Japanese guides (6 more) ──
    guide("Yamamoto Rina", "야마모토 리나",
        "Japanese-Korean bilingual guide specializing in Seoul cafe culture and Instagrammable spots.",
        "서울 카페 문화와 인스타 명소 전문 일한 이중언어 가이드.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["food", "shopping"], ["gangnam", "seocho", "hongdae"],
        22, 75, 140, "Cafe tours, Instagram spot tours, dessert tours, shopping guides",
        "카페 투어, 인스타 스팟 투어, 디저트 투어, 쇼핑 가이드",
        4.6, 88, {"ja": "山本りな"})

    guide("Takahashi Kenji", "다카하시 켄지",
        "Korean history expert from Tokyo. Specializes in Korea-Japan historical sites and cultural exchanges.",
        "도쿄 출신 한국 역사 전문가. 한일 역사 유적지와 문화 교류 전문.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["history_culture", "nature"], ["jongno", "seocho"],
        28, 95, 170, "Historical site tours, museum tours, cultural exchange programs, educational walks",
        "역사 유적 투어, 박물관 투어, 문화 교류 프로그램, 교육 산책",
        4.7, 52, {"ja": "高橋健二"})

    guide("Watanabe Akiko", "와타나베 아키코",
        "Food writer and gourmet guide from Osaka. Expert in comparing Korean and Japanese cuisine.",
        "오사카 출신 음식 작가 겸 미식 가이드. 한일 요리 비교 전문.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["food", "local_experience"], ["gangnam", "mapo", "jongno"],
        30, 100, 180, "Gourmet food tours, restaurant reservations, food market tours, sake & soju tasting",
        "미식 투어, 레스토랑 예약, 시장 투어, 사케 & 소주 시음",
        4.8, 75, {"ja": "渡辺明子"})

    guide("Ito Yusuke", "이토 유스케",
        "Young and energetic guide specializing in Hongdae nightlife and indie music scene for Japanese visitors.",
        "홍대 나이트라이프와 인디 음악씬 전문. 일본 방문객을 위한 활기찬 가이드.",
        [{"code": "ja", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["nightlife", "kpop_hallyu"], ["hongdae", "itaewon"],
        20, 70, 130, "Hongdae nightlife tours, indie music tours, bar hopping, live music venues",
        "홍대 나이트라이프 투어, 인디 음악 투어, 바 호핑, 라이브 공연장",
        4.4, 63, {"ja": "伊藤裕介"})

    guide("Kimura Mao", "기무라 마오",
        "K-Beauty specialist guide helping Japanese visitors discover Korean skincare and beauty trends.",
        "일본 방문객의 한국 스킨케어·뷰티 트렌드 발견을 돕는 K-뷰티 전문 가이드.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["shopping", "kpop_hallyu"], ["gangnam", "myeongdong"],
        22, 75, 140, "K-Beauty tours, skincare clinic visits, cosmetics shopping, beauty class",
        "K-뷰티 투어, 피부과 방문, 화장품 쇼핑, 뷰티 클래스",
        4.7, 91, {"ja": "木村まお"})

    guide("Hayashi Taro", "하야시 타로",
        "Architect and design guide from Tokyo. Leads tours of Seoul's modern architecture and design districts.",
        "도쿄 출신 건축가 겸 디자인 가이드. 서울 현대 건축·디자인 지구 투어 진행.",
        [{"code": "ja", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["history_culture", "shopping"], ["gangnam", "seocho", "jongno"],
        35, 120, 220, "Architecture tours, design district tours, gallery visits, urban photography",
        "건축 투어, 디자인 지구 투어, 갤러리 방문, 도시 사진",
        4.5, 34, {"ja": "林太郎"})

    # ── English guides (8 more) ──
    guide("David Kim", "데이비드 김",
        "Korean-American guide born in LA, living in Seoul for 8 years. Bridges Korean and American cultures.",
        "LA 출신 한국계 미국인. 서울 거주 8년차로 한미 문화를 연결합니다.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "fluent"}],
        ["food", "local_experience", "nightlife"], ["gangnam", "itaewon", "hongdae"],
        28, 95, 170, "Local food tours, nightlife guides, craft beer tours, cultural immersion",
        "로컬 맛집 투어, 나이트라이프 가이드, 크래프트 맥주 투어, 문화 체험", 4.6, 134)

    guide("Emily Watson", "에밀리 왓슨",
        "British history teacher turned Seoul guide. Expert in comparing European and Korean historical periods.",
        "영국 역사 교사 출신 서울 가이드. 유럽·한국 역사 비교 전문.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "conversational"}],
        ["history_culture"], ["jongno", "seocho"],
        25, 85, 160, "Palace tours, museum tours, historical walking tours, educational tours",
        "궁궐 투어, 박물관 투어, 역사 워킹 투어, 교육 투어", 4.7, 78)

    guide("Ryan O'Brien", "라이언 오브라이언",
        "Irish pub enthusiast and nightlife guide. Knows every craft beer bar and rooftop in Seoul.",
        "아일랜드인 펍 애호가 겸 나이트라이프 가이드. 서울 모든 크래프트 맥주 바와 루프탑을 알고 있습니다.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "basic"}],
        ["nightlife", "food"], ["itaewon", "hongdae", "gangnam"],
        22, 75, 140, "Pub crawls, craft beer tours, rooftop bar tours, nightlife experiences",
        "펍 크롤, 크래프트 맥주 투어, 루프탑 바 투어, 나이트라이프 체험", 4.3, 67)

    guide("Jennifer Park", "제니퍼 박",
        "Korean-Canadian wellness coach and guide. Combines hiking with meditation and healthy eating.",
        "한국계 캐나다인 웰니스 코치 겸 가이드. 등산, 명상, 건강식을 결합합니다.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "fluent"}],
        ["nature", "food"], ["gangnam", "seocho"],
        25, 85, 160, "Wellness hiking, meditation tours, healthy food tours, temple stays",
        "웰니스 등산, 명상 투어, 건강식 투어, 템플스테이", 4.8, 54)

    guide("Tom Andersen", "톰 앤더슨",
        "Danish architect living in Seoul. Leads tours of Seoul's innovative and traditional architecture.",
        "서울 거주 덴마크 건축가. 서울의 혁신적·전통적 건축 투어 진행.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "conversational"}, {"code": "de", "level": "fluent"}],
        ["history_culture", "nature"], ["gangnam", "jongno"],
        30, 100, 180, "Architecture tours, DDP & modern buildings, hanok village, urban design walks",
        "건축 투어, DDP·현대 건축, 한옥마을, 도시 디자인 산책", 4.5, 42)

    guide("Olivia Chen", "올리비아 첸",
        "Chinese-American guide fluent in three languages. Specializes in MICE support and corporate tours.",
        "3개 국어 유창한 중국계 미국인 가이드. MICE 지원과 기업 투어 전문.",
        [{"code": "en", "level": "native"}, {"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}],
        ["business", "shopping"], ["gangnam", "seocho"],
        45, 150, 280, "MICE support, corporate tours, translation services, VIP shopping tours",
        "MICE 지원, 기업 투어, 통역 서비스, VIP 쇼핑 투어", 4.7, 38)

    guide("Alex Turner", "알렉스 터너",
        "Australian surfing instructor and outdoor guide. Leads day trips to beaches and nature around Seoul.",
        "호주 서핑 강사 겸 아웃도어 가이드. 서울 근교 해변·자연 일일 여행 진행.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "basic"}],
        ["nature", "local_experience"], ["gangnam"],
        20, 70, 130, "Beach day trips, outdoor adventures, cycling tours, water sports",
        "해변 일일 여행, 아웃도어 모험, 자전거 투어, 수상 스포츠", 4.4, 45)

    guide("Sophia Martinez-Kim", "소피아 마르티네스-김",
        "Korean-American art curator. Leads gallery and art district tours across Seoul.",
        "한국계 미국인 아트 큐레이터. 서울 갤러리·아트 디스트릭트 투어 진행.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "es", "level": "fluent"}],
        ["history_culture", "shopping"], ["gangnam", "jongno"],
        35, 120, 220, "Art gallery tours, contemporary art tours, artist studio visits, art market tours",
        "아트 갤러리 투어, 현대미술 투어, 작가 스튜디오 방문, 아트 마켓 투어", 4.6, 31)

    # ── Spanish guides (4 more) ──
    guide("Diego Hernández", "디에고 에르난데스",
        "Colombian guide in Seoul specializing in Korean food tours for Latin American visitors.",
        "서울 거주 콜롬비아인 가이드. 라틴 아메리카 방문객을 위한 한식 투어 전문.",
        [{"code": "es", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "nightlife"], ["gangnam", "itaewon", "hongdae"],
        20, 70, 130, "Korean food tours, nightlife tours, cultural comparisons, salsa dance tours",
        "한식 투어, 나이트라이프 투어, 문화 비교, 살사 댄스 투어", 4.3, 45)

    guide("Isabella Moreno", "이사벨라 모레노",
        "Spanish art historian and guide. Expert in Seoul's museum scene and contemporary art.",
        "스페인 미술사학자 겸 가이드. 서울 박물관·현대미술 전문.",
        [{"code": "es", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["history_culture"], ["gangnam", "jongno"],
        25, 85, 160, "Museum tours, art gallery walks, cultural heritage tours, photography tours",
        "박물관 투어, 아트 갤러리 산책, 문화유산 투어, 사진 투어", 4.5, 28)

    guide("Javier López", "하비에르 로페스",
        "Mexican chef and food enthusiast living in Seoul. Leads Korean-Mexican fusion food tours.",
        "서울 거주 멕시코 셰프 겸 미식가. 한국-멕시코 퓨전 음식 투어 진행.",
        [{"code": "es", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "local_experience"], ["itaewon", "mapo"],
        25, 85, 160, "Fusion food tours, cooking classes, market tours, restaurant hopping",
        "퓨전 맛집 투어, 쿠킹 클래스, 시장 투어, 레스토랑 호핑", 4.6, 38)

    guide("Ana Ruiz", "아나 루이스",
        "Spanish yoga instructor and wellness guide. Combines Korean temple stays with wellness programs.",
        "스페인 요가 강사 겸 웰니스 가이드. 한국 템플스테이와 웰니스 프로그램을 결합.",
        [{"code": "es", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["nature", "history_culture"], ["seocho", "jongno"],
        22, 75, 140, "Temple stays, yoga sessions, meditation, nature wellness tours",
        "템플스테이, 요가 세션, 명상, 자연 웰니스 투어", 4.4, 32)

    # ── French guides (4 more) ──
    guide("Antoine Leroy", "앙투안 르루아",
        "French sommelier and gastronomy guide. Expert in Korean natural wines and traditional alcohol.",
        "프랑스 소믈리에 겸 미식 가이드. 한국 자연 와인과 전통주 전문.",
        [{"code": "fr", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "local_experience"], ["gangnam", "itaewon", "jongno"],
        35, 120, 220, "Wine tours, traditional alcohol tasting, fine dining tours, market gastronomy",
        "와인 투어, 전통주 시음, 파인다이닝 투어, 시장 미식", 4.7, 42)

    guide("Camille Dupont", "카밀 뒤퐁",
        "French-Korean translator and cultural bridge guide. Helps Francophone visitors navigate Seoul.",
        "한불 통역사 겸 문화 가교 가이드. 프랑스어권 방문객의 서울 여행을 돕습니다.",
        [{"code": "fr", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "fluent"}],
        ["history_culture", "shopping"], ["gangnam", "jongno"],
        25, 85, 160, "Cultural tours, translation services, shopping guides, business interpretation",
        "문화 투어, 통역 서비스, 쇼핑 가이드, 비즈니스 통역", 4.6, 35)

    guide("Nicolas Blanc", "니콜라 블랑",
        "French photographer and K-Drama fan. Leads cinematic photo tours of Seoul filming locations.",
        "프랑스 사진작가 겸 K-드라마 팬. 서울 촬영지 시네마틱 포토 투어 진행.",
        [{"code": "fr", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["kpop_hallyu", "nightlife"], ["gangnam", "hongdae", "jongno"],
        30, 100, 180, "Photography tours, K-Drama location tours, night photography, portrait sessions",
        "사진 투어, K-드라마 촬영지 투어, 야경 촬영, 인물 촬영", 4.5, 29)

    guide("Marie Fontaine", "마리 퐁텐",
        "French pastry chef turned guide. Compares Korean and French baking traditions through café tours.",
        "프랑스 파티시에 출신 가이드. 카페 투어를 통해 한불 베이킹 전통을 비교합니다.",
        [{"code": "fr", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "shopping"], ["gangnam", "seocho"],
        28, 95, 170, "Bakery & café tours, pastry workshops, dessert tastings, baking comparisons",
        "베이커리·카페 투어, 페이스트리 워크숍, 디저트 시음, 베이킹 비교", 4.7, 44)

    # ── Thai guides (4 more) ──
    guide("Kittipong Chaiyo", "키티퐁 차이요",
        "Thai guide specializing in Korean BBQ and food tours for Southeast Asian visitors.",
        "동남아 방문객을 위한 한국 바비큐·맛집 투어 전문 태국인 가이드.",
        [{"code": "th", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "local_experience"], ["gangnam", "mapo"],
        18, 60, 110, "Korean BBQ tours, street food tours, market tours, cooking experiences",
        "한국 BBQ 투어, 길거리 음식 투어, 시장 투어, 쿠킹 체험", 4.4, 55)

    guide("Natthaya Suwanrat", "나타야 수완랏",
        "Thai-Korean bilingual guide. Expert in K-Pop and Thai-Korean celebrity culture connections.",
        "태한 이중언어 가이드. K-POP과 태한 셀럽 문화 연결 전문.",
        [{"code": "th", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["kpop_hallyu", "shopping"], ["gangnam", "hongdae", "myeongdong"],
        20, 70, 130, "K-Pop tours, celebrity culture tours, fan event support, K-Beauty shopping",
        "K-POP 투어, 셀럽 문화 투어, 팬 이벤트 지원, K-뷰티 쇼핑", 4.6, 78)

    guide("Worawit Panyakit", "워라윗 판야킷",
        "Thai photography guide. Captures the best of Seoul for Thai social media influencers.",
        "태국 사진 가이드. 태국 SNS 인플루언서를 위해 서울의 베스트 앵글을 포착합니다.",
        [{"code": "th", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["nature", "kpop_hallyu"], ["gangnam", "jongno"],
        22, 75, 140, "Photo tours, influencer tours, scenic spot tours, video content support",
        "포토 투어, 인플루언서 투어, 경치 스팟 투어, 영상 콘텐츠 지원", 4.5, 42)

    guide("Apinya Chaowalit", "아피냐 차오왈릿",
        "Thai Buddhist guide specializing in Korean temple visits and meditation experiences.",
        "한국 사찰 방문과 명상 체험 전문 태국 불교 가이드.",
        [{"code": "th", "level": "native"}, {"code": "ko", "level": "conversational"}, {"code": "en", "level": "fluent"}],
        ["history_culture", "nature"], ["jongno", "seocho"],
        18, 60, 110, "Temple visits, meditation tours, Buddhist culture tours, nature walks",
        "사찰 방문, 명상 투어, 불교 문화 투어, 자연 산책", 4.7, 36)

    # ── Vietnamese guides (4 more) ──
    guide("Pham Duc Anh", "팜 득 안",
        "Vietnamese IT professional and part-time Seoul guide. Helps Vietnamese tech workers explore the city.",
        "베트남 IT 전문가 겸 파트타임 서울 가이드. 베트남 IT 근무자의 서울 탐험을 돕습니다.",
        [{"code": "vi", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["local_experience", "food"], ["gangnam", "seocho"],
        15, 50, 95, "Local tours, tech district tours, affordable food tours, nightlife",
        "로컬 투어, 테크 지구 투어, 저렴 맛집 투어, 나이트라이프", 4.3, 42)

    guide("Le Thi Hong", "레 티 홍",
        "Vietnamese K-Drama fanatic and filming location guide. Leads drama pilgrimage tours in Seoul.",
        "베트남 K-드라마 팬이자 촬영지 가이드. 서울 드라마 성지순례 투어 진행.",
        [{"code": "vi", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["kpop_hallyu", "history_culture"], ["gangnam", "jongno"],
        18, 60, 110, "K-Drama location tours, palace tours, photo tours, fan experience",
        "K-드라마 촬영지 투어, 궁궐 투어, 포토 투어, 팬 체험", 4.5, 67)

    guide("Vo Minh Tuan", "보 민 투안",
        "Vietnamese food vlogger and Seoul street food guide. Expert in affordable Korean dining.",
        "베트남 먹방 브이로거 겸 서울 길거리 음식 가이드. 저렴한 한식 전문.",
        [{"code": "vi", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "local_experience"], ["mapo", "jongno"],
        15, 50, 95, "Street food tours, budget dining, market tours, food vlog support",
        "길거리 음식 투어, 저예산 맛집, 시장 투어, 먹방 브이로그 지원", 4.4, 55)

    guide("Nguyen Thi Lan", "응우옌 티 란",
        "Vietnamese fashion student and shopping guide. Expert in affordable Korean fashion districts.",
        "베트남 패션 학생 겸 쇼핑 가이드. 저렴한 한국 패션 지구 전문.",
        [{"code": "vi", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["shopping", "kpop_hallyu"], ["myeongdong", "hongdae", "gangnam"],
        18, 60, 110, "Fashion shopping tours, K-Beauty tours, underground mall tours, vintage shopping",
        "패션 쇼핑 투어, K-뷰티 투어, 지하상가 투어, 빈티지 쇼핑", 4.5, 48)

    # ── Other language guides (6 more) ──
    guide("Mohammed Al-Rashid", "모하메드 알라시드",
        "Saudi Arabian guide specializing in halal dining and Muslim-friendly experiences in Seoul.",
        "서울의 할랄 다이닝·무슬림 친화 체험 전문 사우디아라비아인 가이드.",
        [{"code": "ar", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["food", "shopping"], ["gangnam", "itaewon"],
        25, 85, 160, "Halal food tours, Muslim-friendly tours, prayer room guidance, halal shopping",
        "할랄 맛집 투어, 무슬림 친화 투어, 기도실 안내, 할랄 쇼핑", 4.6, 52)

    guide("Fatima Hassan", "파티마 하산",
        "Egyptian guide focusing on halal Korean food experiences and Islamic cultural connections.",
        "할랄 한식 체험과 이슬람 문화 연결에 초점을 맞춘 이집트인 가이드.",
        [{"code": "ar", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["food", "history_culture"], ["itaewon", "jongno"],
        22, 75, 140, "Halal food tours, cultural tours, mosque visits, interfaith experiences",
        "할랄 맛집 투어, 문화 투어, 모스크 방문, 종교간 교류 체험", 4.5, 34)

    guide("Dmitri Volkov", "드미트리 볼코프",
        "Russian tech entrepreneur and Seoul guide. Helps Russian-speaking visitors explore Seoul's tech scene.",
        "러시아 테크 기업가 겸 서울 가이드. 러시아어권 방문객의 서울 테크씬 탐방을 돕습니다.",
        [{"code": "ru", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["business", "local_experience"], ["gangnam", "seocho"],
        30, 100, 180, "Tech tours, startup visits, business networking, gaming district tours",
        "테크 투어, 스타트업 방문, 비즈니스 네트워킹, 게임 지구 투어", 4.4, 28)

    guide("Priya Sharma", "프리야 샤르마",
        "Indian Bollywood dancer and cultural guide. Creates vibrant Seoul experiences for Indian visitors.",
        "인도 볼리우드 댄서 겸 문화 가이드. 인도 방문객을 위한 활기찬 서울 체험을 기획합니다.",
        [{"code": "hi", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "basic"}],
        ["food", "kpop_hallyu"], ["gangnam", "itaewon"],
        20, 70, 130, "K-Pop dance tours, Indian food tours in Seoul, cultural exchange, shopping",
        "K-POP 댄스 투어, 서울 인도 맛집 투어, 문화 교류, 쇼핑", 4.5, 39)

    guide("Hans Mueller", "한스 뮐러",
        "German engineer and history buff. Leads technical and historical tours of Seoul's infrastructure.",
        "독일 엔지니어 겸 역사 애호가. 서울 인프라의 기술·역사 투어 진행.",
        [{"code": "de", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ko", "level": "conversational"}],
        ["history_culture", "nature"], ["gangnam", "jongno"],
        28, 95, 170, "Infrastructure tours, historical tours, engineering marvels, urban development walks",
        "인프라 투어, 역사 투어, 공학 경이, 도시 개발 산책", 4.4, 22)

    guide("Yuki Taniguchi", "유키 타니구치",
        "Japanese-Brazilian guide fluent in Portuguese, Japanese, and Korean. Popular with Brazilian K-Pop fans.",
        "포르투갈어·일본어·한국어 유창한 일본계 브라질인 가이드. 브라질 K-POP 팬에게 인기.",
        [{"code": "pt", "level": "native"}, {"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "fluent"}],
        ["kpop_hallyu", "food"], ["gangnam", "hongdae"],
        22, 75, 140, "K-Pop tours, cultural fusion tours, food tours, fan experience support",
        "K-POP 투어, 문화 퓨전 투어, 맛집 투어, 팬 체험 지원", 4.6, 47)

    # ── Additional Korean guides (6 more) ──
    guide("Jeon Woojin", "전우진",
        "Former K-Pop trainee and current entertainment industry guide. Insider knowledge of idol life.",
        "전 K-POP 연습생 출신 엔터테인먼트 업계 가이드. 아이돌 생활 내부 지식 보유.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "zh", "level": "basic"}],
        ["kpop_hallyu", "nightlife"], ["gangnam", "hongdae"],
        28, 95, 170, "K-Pop insider tours, trainee experience talks, entertainment district tours, dance classes",
        "K-POP 인사이더 투어, 연습생 경험 이야기, 엔터가 투어, 댄스 수업", 4.8, 156)

    guide("Moon Yejin", "문예진",
        "Korean traditional music (gugak) performer and cultural guide. Teaches visitors about Korean music heritage.",
        "한국 전통 음악(국악) 연주자 겸 문화 가이드. 한국 음악 유산을 알려드립니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["history_culture", "local_experience"], ["jongno", "seocho"],
        25, 85, 160, "Traditional music experiences, gugak performances, cultural workshops, palace tours",
        "전통 음악 체험, 국악 공연, 문화 워크숍, 궁궐 투어", 4.7, 48)

    guide("Ahn Dongha", "안동하",
        "Seoul night market and craft cocktail expert. Leads unique evening food and drink tours.",
        "서울 야시장·크래프트 칵테일 전문가. 독특한 저녁 음식·음료 투어 진행.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["food", "nightlife"], ["gangnam", "itaewon", "hongdae"],
        25, 85, 160, "Cocktail tours, night market tours, pojangmacha tours, food & drink pairing",
        "칵테일 투어, 야시장 투어, 포장마차 투어, 음식·음료 페어링", 4.5, 82)

    guide("Cho Hyunwoo", "조현우",
        "Professional esports commentator and gaming district guide. Leads tours of PC bang culture.",
        "프로 이스포츠 해설가 겸 게이밍 가이드. PC방 문화 투어 진행.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}, {"code": "ja", "level": "basic"}],
        ["local_experience", "nightlife"], ["gangnam", "hongdae"],
        20, 70, 130, "Gaming district tours, esports arena visits, PC bang experiences, tech culture",
        "게이밍 지구 투어, 이스포츠 경기장 방문, PC방 체험, 테크 문화", 4.3, 67)

    guide("Yoo Seoyeon", "유서연",
        "Korean calligraphy artist and hanbok designer. Offers immersive traditional Korean art experiences.",
        "한국 서예 작가 겸 한복 디자이너. 몰입형 한국 전통 예술 체험을 제공합니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "conversational"}],
        ["history_culture", "local_experience"], ["jongno"],
        30, 100, 180, "Calligraphy workshops, hanbok experiences, traditional art tours, craft making",
        "서예 워크숍, 한복 체험, 전통 예술 투어, 공예 만들기", 4.8, 43)

    guide("Park Junghwan", "박정환",
        "Former taekwondo national team athlete. Offers martial arts and fitness-focused Korean tours.",
        "전 태권도 국가대표 선수. 무술·피트니스 중심 한국 투어를 제공합니다.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["nature", "local_experience"], ["gangnam", "seocho"],
        25, 85, 160, "Taekwondo experiences, fitness tours, martial arts workshops, active tours",
        "태권도 체험, 피트니스 투어, 무술 워크숍, 액티브 투어", 4.6, 57)

    # ── Additional English guides (4 more) ──
    guide("Rachel Kim-Stevens", "레이첼 김스티븐스",
        "Korean-American food writer specializing in Seoul's emerging restaurant scene and hidden gems.",
        "서울 신생 레스토랑과 숨은 맛집 전문 한국계 미국인 음식 작가.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "fluent"}],
        ["food", "local_experience"], ["gangnam", "mapo", "jongno"],
        30, 100, 180, "Hidden gem food tours, restaurant scene tours, food writing workshops, market tours",
        "숨은 맛집 투어, 레스토랑 씬 투어, 음식 글쓰기 워크숍, 시장 투어", 4.7, 92)

    guide("Peter Johansson", "피터 요한슨",
        "Swedish sustainability consultant and eco-tour guide. Leads green and sustainable tours of Seoul.",
        "스웨덴 지속가능성 컨설턴트 겸 에코투어 가이드. 서울의 친환경 투어 진행.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "conversational"}, {"code": "sv", "level": "native"}],
        ["nature", "local_experience"], ["gangnam", "mapo"],
        25, 85, 160, "Eco tours, sustainable food tours, urban farming visits, recycling center tours",
        "에코 투어, 지속가능 맛집 투어, 도시 농장 방문, 재활용 센터 투어", 4.5, 28)

    guide("Lisa Chang", "리사 장",
        "Singaporean-Korean guide specializing in luxury shopping and fine dining experiences in Seoul.",
        "서울 럭셔리 쇼핑과 파인다이닝 체험 전문 싱가포르계 한국인 가이드.",
        [{"code": "en", "level": "native"}, {"code": "zh", "level": "fluent"}, {"code": "ko", "level": "fluent"}],
        ["shopping", "food"], ["gangnam", "seocho"],
        45, 150, 280, "Luxury shopping tours, fine dining reservations, personal shopping, VIP experiences",
        "럭셔리 쇼핑 투어, 파인다이닝 예약, 퍼스널 쇼핑, VIP 체험", 4.8, 65)

    guide("Mark Williams", "마크 윌리엄스",
        "American craft beer enthusiast and brewery guide. Leads tours of Seoul's growing craft beer scene.",
        "미국인 크래프트 맥주 매니아 겸 브루어리 가이드. 서울 크래프트 맥주 씬 투어 진행.",
        [{"code": "en", "level": "native"}, {"code": "ko", "level": "conversational"}],
        ["food", "nightlife"], ["itaewon", "gangnam", "hongdae"],
        22, 75, 140, "Craft beer tours, brewery visits, beer & food pairing, pub crawls",
        "크래프트 맥주 투어, 브루어리 방문, 맥주·음식 페어링, 펍 크롤", 4.4, 56)

    # ── Additional Chinese guides (2 more) ──
    guide("Tang Xiaoyu", "탕샤오위",
        "Chinese medical tourism guide. Helps Chinese visitors with Korean dermatology and beauty clinics.",
        "중국 의료 관광 가이드. 중국 방문객의 한국 피부과·뷰티 클리닉 방문을 돕습니다.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["shopping", "local_experience"], ["gangnam", "seocho"],
        35, 120, 220, "Medical tourism support, dermatology clinic tours, K-Beauty shopping, wellness experiences",
        "의료 관광 지원, 피부과 클리닉 투어, K-뷰티 쇼핑, 웰니스 체험",
        4.7, 88, {"zh_cn": "唐小雨", "zh_tw": "唐小雨"})

    guide("Lin Haoran", "린하오란",
        "Chinese university student studying in Seoul. Offers budget-friendly tours for Chinese student travelers.",
        "서울 유학 중인 중국 대학생. 중국 학생 여행자를 위한 저예산 투어 제공.",
        [{"code": "zh", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["food", "kpop_hallyu"], ["hongdae", "gangnam", "jongno"],
        12, 40, 75, "Budget tours, student-friendly tours, K-Pop tours, night market tours",
        "저예산 투어, 학생 친화 투어, K-POP 투어, 야시장 투어",
        4.3, 62, {"zh_cn": "林浩然", "zh_tw": "林浩然"})

    # ── Additional Japanese guides (2 more) ──
    guide("Ogawa Sakura", "오가와 사쿠라",
        "Japanese wellness and onsen culture guide. Compares Korean jjimjilbang with Japanese onsen traditions.",
        "일본 웰니스·온천 문화 가이드. 한국 찜질방과 일본 온천 전통을 비교합니다.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "conversational"}],
        ["nature", "local_experience"], ["gangnam", "seocho"],
        22, 75, 140, "Jjimjilbang tours, wellness experiences, spa guide, Korean sauna culture",
        "찜질방 투어, 웰니스 체험, 스파 가이드, 한국 사우나 문화",
        4.6, 58, {"ja": "小川さくら"})

    guide("Matsuda Ren", "마쓰다 렌",
        "Japanese ramen chef living in Seoul. Leads Japanese-Korean fusion food tours and cooking classes.",
        "서울 거주 일본 라멘 셰프. 일한 퓨전 맛집 투어와 쿠킹 클래스 진행.",
        [{"code": "ja", "level": "native"}, {"code": "ko", "level": "fluent"}, {"code": "en", "level": "basic"}],
        ["food", "local_experience"], ["mapo", "gangnam"],
        25, 85, 160, "Ramen tours, fusion food tours, cooking classes, food market tours",
        "라멘 투어, 퓨전 맛집 투어, 쿠킹 클래스, 시장 투어",
        4.7, 44, {"ja": "松田蓮"})

    # ── Additional diverse guides (2 more) ──
    guide("Yoon Daesung", "윤대성",
        "Korean baseball fan and sports guide. Leads tours to KBO games and Seoul's sports attractions.",
        "한국 야구 팬 겸 스포츠 가이드. KBO 경기와 서울 스포츠 관광 투어 진행.",
        [{"code": "ko", "level": "native"}, {"code": "en", "level": "fluent"}],
        ["local_experience", "nightlife"], ["gangnam", "songpa"],
        20, 70, 130, "Baseball game tours, sports attraction tours, Olympic Park visits, fan culture",
        "야구 경기 투어, 스포츠 관광 투어, 올림픽공원 방문, 팬 문화", 4.4, 78)

    guide("Emma Lindqvist", "엠마 린드크비스트",
        "Finnish sauna culture researcher comparing Korean jjimjilbang with Nordic sauna traditions.",
        "한국 찜질방과 북유럽 사우나 전통을 비교하는 핀란드 사우나 문화 연구자.",
        [{"code": "en", "level": "native"}, {"code": "fi", "level": "native"}, {"code": "ko", "level": "basic"}],
        ["local_experience", "nature"], ["gangnam", "seocho"],
        22, 75, 140, "Jjimjilbang tours, sauna culture comparison, wellness experiences, nature walks",
        "찜질방 투어, 사우나 문화 비교, 웰니스 체험, 자연 산책", 4.5, 25)

    return guides
