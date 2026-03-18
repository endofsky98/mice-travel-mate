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
            "profile_image_url": f"/images/placeholder/guide_{len(guides)+1}.jpg",
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

    return guides
