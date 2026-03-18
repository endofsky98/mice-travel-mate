import uuid

def _id():
    return str(uuid.uuid4())

def _ml(en, ko, zh_cn=None, zh_tw=None, ja=None, es=None, th=None, vi=None, fr=None):
    return {
        "en": en, "ko": ko,
        "zh_cn": zh_cn or en, "zh_tw": zh_tw or en,
        "ja": ja or en, "es": es or en,
        "th": th or en, "vi": vi or en, "fr": fr or en,
    }

def get_products():
    products = []

    def product(name, desc, cat, price, dur, min_p, max_p, includes, excludes, itinerary, meeting, mlat, mlng, cancel, rating, reviews):
        products.append({
            "id": _id(),
            "name_en": name["en"], "name_ko": name["ko"],
            "name_zh_cn": name["zh_cn"], "name_zh_tw": name["zh_tw"],
            "name_ja": name["ja"], "name_es": name["es"],
            "name_th": name["th"], "name_vi": name["vi"], "name_fr": name["fr"],
            "description_en": desc["en"], "description_ko": desc["ko"],
            "description_zh_cn": desc["zh_cn"], "description_zh_tw": desc["zh_tw"],
            "description_ja": desc["ja"], "description_es": desc["es"],
            "description_th": desc["th"], "description_vi": desc["vi"], "description_fr": desc["fr"],
            "category": cat,
            "price_usd": price,
            "duration_hours": dur,
            "region": "seoul",
            "min_participants": min_p,
            "max_participants": max_p,
            "includes_en": includes["en"], "includes_ko": includes["ko"],
            "includes_zh_cn": includes.get("zh_cn", includes["en"]),
            "includes_zh_tw": includes.get("zh_tw", includes["en"]),
            "includes_ja": includes.get("ja", includes["en"]),
            "includes_es": includes.get("es", includes["en"]),
            "includes_th": includes.get("th", includes["en"]),
            "includes_vi": includes.get("vi", includes["en"]),
            "includes_fr": includes.get("fr", includes["en"]),
            "excludes_en": excludes["en"], "excludes_ko": excludes["ko"],
            "excludes_zh_cn": excludes.get("zh_cn", excludes["en"]),
            "excludes_zh_tw": excludes.get("zh_tw", excludes["en"]),
            "excludes_ja": excludes.get("ja", excludes["en"]),
            "excludes_es": excludes.get("es", excludes["en"]),
            "excludes_th": excludes.get("th", excludes["en"]),
            "excludes_vi": excludes.get("vi", excludes["en"]),
            "excludes_fr": excludes.get("fr", excludes["en"]),
            "itinerary": itinerary,
            "meeting_point": meeting,
            "meeting_point_lat": mlat,
            "meeting_point_lng": mlng,
            "dismissal_point": meeting,
            "cancellation_policy_en": cancel, "cancellation_policy_ko": "48시간 전 무료 취소, 24시간 전 50% 환불, 이후 환불 불가",
            "cancellation_policy_zh_cn": cancel, "cancellation_policy_zh_tw": cancel,
            "cancellation_policy_ja": cancel, "cancellation_policy_es": cancel,
            "cancellation_policy_th": cancel, "cancellation_policy_vi": cancel,
            "cancellation_policy_fr": cancel,
            "images": [f"/images/placeholder/product_{len(products)+1}_{j}.jpg" for j in range(3)],
            "avg_rating": rating,
            "review_count": reviews,
            "status": "active",
        })

    cancel = "Free cancellation 48h before. 50% refund 24h before. No refund after."

    # 1-8: Tour
    product(
        _ml("Gangnam K-Pop & Culture Walking Tour", "강남 K-POP & 문화 워킹 투어"),
        _ml("Explore K-Pop landmarks, entertainment company buildings, and Hallyu culture in Gangnam.", "강남의 K-POP 랜드마크, 엔터사 사옥, 한류 문화를 탐험합니다."),
        "tour", 45, 3, 1, 15,
        {"en": ["Professional English-speaking guide", "K-Star Road photo stops", "Bottled water"], "ko": ["전문 영어 가이드", "K스타 거리 포토스팟", "생수"]},
        {"en": ["Personal expenses", "Transportation"], "ko": ["개인 경비", "교통비"]},
        [{"time": "14:00", "activity_en": "Meet at Gangnam Station", "activity_ko": "강남역 집합"}, {"time": "14:30", "activity_en": "K-Star Road tour", "activity_ko": "K스타의 거리 투어"}, {"time": "16:00", "activity_en": "SM/JYP Entertainment area", "activity_ko": "SM/JYP 엔터 일대"}, {"time": "17:00", "activity_en": "Free time at COEX", "activity_ko": "코엑스 자유시간"}],
        "Gangnam Station Exit 10", 37.4979, 127.0276, cancel, 4.7, 89)

    product(
        _ml("Seoul Historical Palace Tour from Gangnam", "강남 출발 서울 고궁 투어"),
        _ml("Visit Seoul's magnificent palaces with expert guide starting from Gangnam.", "강남에서 출발하여 전문 가이드와 서울 궁궐을 방문합니다."),
        "tour", 65, 5, 1, 12,
        {"en": ["Palace entrance fees", "Professional guide", "Lunch", "Transportation"], "ko": ["궁궐 입장료", "전문 가이드", "점심", "교통비"]},
        {"en": ["Personal expenses", "Travel insurance"], "ko": ["개인 경비", "여행자 보험"]},
        [{"time": "09:00", "activity_en": "Depart from Gangnam", "activity_ko": "강남 출발"}, {"time": "10:00", "activity_en": "Gyeongbokgung Palace tour", "activity_ko": "경복궁 투어"}, {"time": "12:00", "activity_en": "Korean lunch", "activity_ko": "한식 점심"}, {"time": "13:30", "activity_en": "Changdeokgung Palace", "activity_ko": "창덕궁"}, {"time": "15:00", "activity_en": "Bukchon Hanok Village", "activity_ko": "북촌한옥마을"}],
        "COEX Mall Gate 1", 37.5126, 127.0590, cancel, 4.8, 120)

    product(
        _ml("DMZ & JSA Tour from Gangnam", "강남 출발 DMZ & JSA 투어"),
        _ml("Full-day tour to the Korean Demilitarized Zone and Joint Security Area.", "한국 비무장지대와 공동경비구역 전일 투어."),
        "tour", 120, 8, 1, 20,
        {"en": ["All entrance fees", "Professional guide", "Lunch", "Round-trip transportation", "DMZ pass"], "ko": ["입장료 전체", "전문 가이드", "점심", "왕복 교통", "DMZ 출입증"]},
        {"en": ["Personal expenses", "Travel insurance", "Passport required"], "ko": ["개인 경비", "여행자 보험", "여권 필수"]},
        [{"time": "07:00", "activity_en": "Depart from Gangnam", "activity_ko": "강남 출발"}, {"time": "09:30", "activity_en": "Imjingak Park", "activity_ko": "임진각 공원"}, {"time": "11:00", "activity_en": "JSA / Panmunjom", "activity_ko": "판문점"}, {"time": "13:00", "activity_en": "Lunch", "activity_ko": "점심"}, {"time": "14:00", "activity_en": "3rd Tunnel of Aggression", "activity_ko": "제3땅굴"}, {"time": "16:00", "activity_en": "Return to Gangnam", "activity_ko": "강남 복귀"}],
        "Gangnam Station Exit 10", 37.4979, 127.0276, cancel, 4.9, 95)

    product(
        _ml("Night Tour: Seoul Skyline & Nightlife", "야경 투어: 서울 스카이라인 & 나이트라이프"),
        _ml("Experience Seoul's stunning nightscape from the best viewpoints.", "최고의 전망 포인트에서 서울의 멋진 야경을 경험하세요."),
        "tour", 55, 4, 1, 15,
        {"en": ["Professional guide", "Observatory entrance fee", "Traditional cocktail"], "ko": ["전문 가이드", "전망대 입장료", "전통 칵테일"]},
        {"en": ["Personal expenses", "Dinner"], "ko": ["개인 경비", "저녁 식사"]},
        [{"time": "18:00", "activity_en": "Meet at Gangnam Station", "activity_ko": "강남역 집합"}, {"time": "18:30", "activity_en": "Namsan Tower night view", "activity_ko": "남산타워 야경"}, {"time": "20:00", "activity_en": "Banpo Bridge Rainbow Fountain", "activity_ko": "반포대교 무지개 분수"}, {"time": "21:30", "activity_en": "Gangnam rooftop bar", "activity_ko": "강남 루프탑 바"}],
        "Gangnam Station Exit 5", 37.4979, 127.0276, cancel, 4.6, 77)

    product(
        _ml("Jeju Island Day Trip from Seoul", "서울 출발 제주도 당일 투어"),
        _ml("Quick day trip to Jeju Island's top attractions by air from Seoul.", "서울에서 비행기로 제주도 주요 명소 당일 투어."),
        "tour", 280, 12, 1, 10,
        {"en": ["Round-trip flight", "All entrance fees", "Lunch", "Transportation on Jeju", "Guide"], "ko": ["왕복 항공권", "입장료 전체", "점심", "제주 내 교통", "가이드"]},
        {"en": ["Personal expenses", "Travel insurance"], "ko": ["개인 경비", "여행자 보험"]},
        [{"time": "06:00", "activity_en": "Depart to Gimpo Airport", "activity_ko": "김포공항 출발"}, {"time": "08:00", "activity_en": "Arrive Jeju", "activity_ko": "제주 도착"}, {"time": "09:00", "activity_en": "Seongsan Ilchulbong", "activity_ko": "성산일출봉"}, {"time": "12:00", "activity_en": "Seafood lunch", "activity_ko": "해산물 점심"}, {"time": "14:00", "activity_en": "Hallasan National Park", "activity_ko": "한라산국립공원"}, {"time": "17:00", "activity_en": "Return flight", "activity_ko": "귀환 항공편"}],
        "Gangnam Station Exit 10", 37.4979, 127.0276, cancel, 4.8, 42)

    product(
        _ml("Bukchon Hanok Village Walking Tour", "북촌한옥마을 워킹투어"),
        _ml("Stroll through traditional Korean houses in historic Bukchon.", "역사적인 북촌의 전통 한옥을 거닐어 보세요."),
        "tour", 35, 2.5, 1, 12,
        {"en": ["Professional guide", "Traditional snack", "Photo service"], "ko": ["전문 가이드", "전통 간식", "사진 서비스"]},
        {"en": ["Personal expenses", "Transportation to meeting point"], "ko": ["개인 경비", "집합 장소까지 교통"]},
        [{"time": "10:00", "activity_en": "Meet at Anguk Station", "activity_ko": "안국역 집합"}, {"time": "10:15", "activity_en": "Bukchon Hanok Village walk", "activity_ko": "북촌한옥마을 산책"}, {"time": "11:30", "activity_en": "Traditional tea break", "activity_ko": "전통 다도 휴식"}, {"time": "12:30", "activity_en": "Tour ends", "activity_ko": "투어 종료"}],
        "Anguk Station Exit 2", 37.5760, 126.9850, cancel, 4.5, 68)

    product(
        _ml("Gangnam Food & Market Tour", "강남 음식 & 시장 투어"),
        _ml("Taste authentic Korean street food and local market delicacies.", "진정한 한국 길거리 음식과 시장 별미를 맛보세요."),
        "tour", 50, 3.5, 2, 10,
        {"en": ["Food tastings (8+ items)", "Local guide", "Bottled water"], "ko": ["음식 시식 (8가지 이상)", "현지 가이드", "생수"]},
        {"en": ["Additional food purchases", "Alcoholic beverages"], "ko": ["추가 음식 구매", "주류"]},
        [{"time": "11:00", "activity_en": "Meet at Express Bus Terminal", "activity_ko": "고속터미널 집합"}, {"time": "11:30", "activity_en": "Underground market food tour", "activity_ko": "지하 시장 먹거리 투어"}, {"time": "13:00", "activity_en": "Korean BBQ experience", "activity_ko": "한국 BBQ 체험"}, {"time": "14:30", "activity_en": "Dessert cafe in Garosu-gil", "activity_ko": "가로수길 디저트 카페"}],
        "Express Bus Terminal Station Exit 5", 37.5048, 126.9822, cancel, 4.7, 93)

    product(
        _ml("Hangang River Cruise Dinner Tour", "한강 유람선 디너 투어"),
        _ml("Enjoy a scenic dinner cruise along the Han River.", "한강을 따라 경치 좋은 디너 크루즈를 즐기세요."),
        "tour", 85, 2.5, 2, 20,
        {"en": ["Dinner buffet", "Cruise ticket", "Welcome drink", "Live music"], "ko": ["디너 뷔페", "크루즈 티켓", "웰컴 드링크", "라이브 음악"]},
        {"en": ["Personal expenses", "Additional drinks"], "ko": ["개인 경비", "추가 음료"]},
        [{"time": "18:30", "activity_en": "Board at Banpo dock", "activity_ko": "반포 선착장 탑승"}, {"time": "19:00", "activity_en": "Dinner cruise departs", "activity_ko": "디너 크루즈 출발"}, {"time": "20:00", "activity_en": "Banpo Bridge rainbow fountain view", "activity_ko": "반포대교 무지개분수 관람"}, {"time": "21:00", "activity_en": "Return to dock", "activity_ko": "선착장 복귀"}],
        "Banpo Hangang Park Dock", 37.5080, 126.9950, cancel, 4.6, 58)

    # 9-13: Experience
    product(
        _ml("Hanbok Traditional Costume Experience", "한복 전통의상 체험"),
        _ml("Wear a beautiful hanbok and have a professional photo shoot.", "아름다운 한복을 입고 전문 포토 촬영을 받으세요."),
        "experience", 40, 2, 1, 6,
        {"en": ["Hanbok rental", "Professional photographer", "10 edited photos", "Hair styling"], "ko": ["한복 대여", "전문 사진작가", "보정 사진 10장", "헤어 스타일링"]},
        {"en": ["Additional photo prints", "Transportation"], "ko": ["추가 사진 인화", "교통비"]},
        [{"time": "10:00", "activity_en": "Arrive & select hanbok", "activity_ko": "도착 & 한복 선택"}, {"time": "10:30", "activity_en": "Hair styling & dressing", "activity_ko": "헤어 스타일링 & 착용"}, {"time": "11:00", "activity_en": "Photo shoot at scenic spots", "activity_ko": "경치 좋은 곳에서 촬영"}, {"time": "12:00", "activity_en": "Return hanbok", "activity_ko": "한복 반납"}],
        "Gangnam Hanbok Studio", 37.5014, 127.0262, cancel, 4.8, 145)

    product(
        _ml("Traditional Pottery Making Workshop", "전통 도자기 만들기 워크숍"),
        _ml("Create your own Korean pottery with master artisan guidance.", "장인의 지도 아래 나만의 한국 도자기를 만들어 보세요."),
        "experience", 55, 2.5, 1, 8,
        {"en": ["All materials", "Expert instruction", "Kiln firing", "Shipping to your country"], "ko": ["재료 전체", "전문 강사", "가마 소성", "해외 배송"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "14:00", "activity_en": "Introduction to Korean pottery", "activity_ko": "한국 도자기 소개"}, {"time": "14:30", "activity_en": "Hands-on pottery making", "activity_ko": "도자기 만들기 실습"}, {"time": "16:00", "activity_en": "Glazing & decoration", "activity_ko": "유약 & 장식"}, {"time": "16:30", "activity_en": "Wrap up", "activity_ko": "마무리"}],
        "Seocho Ceramic Studio", 37.4922, 127.0098, cancel, 4.6, 37)

    product(
        _ml("K-Beauty Masterclass", "K-뷰티 마스터클래스"),
        _ml("Learn Korean skincare and makeup techniques from professionals.", "전문가에게 한국 스킨케어와 메이크업 기법을 배우세요."),
        "experience", 60, 2, 1, 8,
        {"en": ["All skincare products", "K-Beauty gift set", "Professional instruction", "Certificate"], "ko": ["스킨케어 제품 전체", "K-뷰티 선물세트", "전문 강습", "수료증"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "14:00", "activity_en": "K-Beauty skincare routine", "activity_ko": "K-뷰티 스킨케어 루틴"}, {"time": "15:00", "activity_en": "Korean makeup tutorial", "activity_ko": "한국식 메이크업 튜토리얼"}, {"time": "16:00", "activity_en": "Q&A and gift set", "activity_ko": "Q&A 및 선물세트"}],
        "Gangnam Beauty Studio", 37.4979, 127.0276, cancel, 4.7, 82)

    product(
        _ml("Traditional Korean Tea Ceremony", "전통 한국 다도 체험"),
        _ml("Experience the art of Korean tea in a traditional setting.", "전통 공간에서 한국 다도의 예술을 경험하세요."),
        "experience", 35, 1.5, 1, 6,
        {"en": ["Tea ceremony experience", "Traditional sweets", "Tea set souvenir"], "ko": ["다도 체험", "전통 과자", "다기 기념품"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "15:00", "activity_en": "Introduction to Korean tea culture", "activity_ko": "한국 차 문화 소개"}, {"time": "15:20", "activity_en": "Tea brewing & tasting", "activity_ko": "차 우리기 & 시음"}, {"time": "16:00", "activity_en": "Mindful meditation with tea", "activity_ko": "차와 함께하는 명상"}, {"time": "16:30", "activity_en": "End", "activity_ko": "종료"}],
        "Seocho Traditional Tea House", 37.4867, 127.0045, cancel, 4.5, 41)

    product(
        _ml("Temple Stay Experience", "템플스테이 체험"),
        _ml("Overnight temple stay with meditation and traditional meals.", "명상과 사찰음식이 포함된 1박 템플스테이."),
        "experience", 95, 24, 1, 10,
        {"en": ["Overnight accommodation", "3 temple meals", "Meditation sessions", "Morning prayer", "Tea ceremony"], "ko": ["1박 숙박", "사찰 음식 3회", "명상 세션", "새벽 예불", "다도"]},
        {"en": ["Personal expenses", "Transportation to temple"], "ko": ["개인 경비", "사찰까지 교통"]},
        [{"time": "15:00", "activity_en": "Check-in & orientation", "activity_ko": "체크인 & 오리엔테이션"}, {"time": "16:00", "activity_en": "Temple tour", "activity_ko": "사찰 투어"}, {"time": "18:00", "activity_en": "Temple dinner", "activity_ko": "사찰 저녁"}, {"time": "19:30", "activity_en": "Evening meditation", "activity_ko": "저녁 명상"}, {"time": "04:30", "activity_en": "Morning prayer", "activity_ko": "새벽 예불"}, {"time": "07:00", "activity_en": "Breakfast & checkout", "activity_ko": "아침 & 체크아웃"}],
        "Bongeunsa Temple", 37.5153, 127.0575, cancel, 4.9, 65)

    # 14-17: Performance
    product(_ml("K-Pop Live Concert Experience", "K-POP 라이브 콘서트 체험"), _ml("Attend a live K-Pop performance with backstage access.", "백스테이지 접근이 포함된 K-POP 라이브 공연 관람."), "performance", 95, 3, 1, 30,
        {"en": ["Concert ticket", "Backstage tour", "Official merchandise", "Light stick"], "ko": ["콘서트 티켓", "백스테이지 투어", "공식 굿즈", "응원봉"]},
        {"en": ["Personal expenses", "Transportation"], "ko": ["개인 경비", "교통비"]},
        [{"time": "18:00", "activity_en": "Arrive & check-in", "activity_ko": "도착 & 체크인"}, {"time": "18:30", "activity_en": "Backstage tour", "activity_ko": "백스테이지 투어"}, {"time": "19:00", "activity_en": "Concert begins", "activity_ko": "콘서트 시작"}, {"time": "21:00", "activity_en": "Concert ends", "activity_ko": "콘서트 종료"}],
        "COEX Convention Center", 37.5126, 127.0590, cancel, 4.8, 110)

    product(_ml("Nanta Show VIP Experience", "난타 쇼 VIP 체험"), _ml("Watch Korea's famous non-verbal comedy show with VIP seating.", "VIP석에서 한국의 유명 비언어 코미디 공연 관람."), "performance", 65, 2, 1, 20,
        {"en": ["VIP seat ticket", "Welcome drink", "Photo with cast"], "ko": ["VIP석 티켓", "웰컴 드링크", "출연진과 사진"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "19:00", "activity_en": "Arrive at theater", "activity_ko": "극장 도착"}, {"time": "19:30", "activity_en": "Welcome drink", "activity_ko": "웰컴 드링크"}, {"time": "20:00", "activity_en": "Nanta Show", "activity_ko": "난타 쇼"}, {"time": "21:30", "activity_en": "Photo time", "activity_ko": "포토 타임"}],
        "Gangnam Nanta Theater", 37.4979, 127.0276, cancel, 4.5, 73)

    product(_ml("Traditional Korean Music Performance", "전통 한국 음악 공연"), _ml("Experience traditional Korean music (gugak) at Seoul Arts Center.", "예술의전당에서 전통 한국 음악(국악)을 경험하세요."), "performance", 45, 2, 1, 30,
        {"en": ["Performance ticket", "Program guide", "Traditional tea"], "ko": ["공연 티켓", "프로그램 안내", "전통 차"]},
        {"en": ["Personal expenses", "Transportation"], "ko": ["개인 경비", "교통비"]},
        [{"time": "19:00", "activity_en": "Arrive at venue", "activity_ko": "공연장 도착"}, {"time": "19:30", "activity_en": "Performance begins", "activity_ko": "공연 시작"}, {"time": "21:00", "activity_en": "Performance ends", "activity_ko": "공연 종료"}],
        "Seoul Arts Center", 37.4784, 127.0117, cancel, 4.6, 38)

    product(_ml("Seoul Jazz Night", "서울 재즈 나이트"), _ml("Enjoy live jazz performances at Gangnam's finest jazz clubs.", "강남 최고의 재즈 클럽에서 라이브 재즈 공연을 즐기세요."), "performance", 50, 3, 1, 15,
        {"en": ["Club entrance", "2 drinks", "Live jazz performance"], "ko": ["클럽 입장", "음료 2잔", "라이브 재즈 공연"]},
        {"en": ["Additional drinks", "Food"], "ko": ["추가 음료", "음식"]},
        [{"time": "20:00", "activity_en": "Arrive at jazz club", "activity_ko": "재즈 클럽 도착"}, {"time": "20:30", "activity_en": "Live jazz begins", "activity_ko": "라이브 재즈 시작"}, {"time": "23:00", "activity_en": "End", "activity_ko": "종료"}],
        "Gangnam Jazz Club", 37.5014, 127.0262, cancel, 4.4, 29)

    # 18-22: Activity
    product(_ml("K-POP Dance Class", "K-POP 댄스 클래스"), _ml("Learn choreography from popular K-Pop songs with professional dancers.", "프로 댄서에게 인기 K-POP 안무를 배우세요."), "activity", 40, 2, 1, 15,
        {"en": ["Professional dance instructor", "Practice room", "Bottled water", "Video recording"], "ko": ["전문 댄스 강사", "연습실", "생수", "영상 촬영"]},
        {"en": ["Personal expenses", "Dance shoes (provided if needed)"], "ko": ["개인 경비", "댄스화 (필요시 제공)"]},
        [{"time": "14:00", "activity_en": "Warm up & stretching", "activity_ko": "워밍업 & 스트레칭"}, {"time": "14:30", "activity_en": "Learn choreography", "activity_ko": "안무 배우기"}, {"time": "15:30", "activity_en": "Practice & recording", "activity_ko": "연습 & 촬영"}, {"time": "16:00", "activity_en": "End", "activity_ko": "종료"}],
        "Gangnam Dance Studio", 37.4979, 127.0276, cancel, 4.8, 156)

    product(_ml("Taekwondo Trial Experience", "태권도 체험"), _ml("Try Korea's national martial art with certified instructors.", "공인 사범과 함께 한국의 국기 태권도를 체험하세요."), "activity", 35, 1.5, 1, 12,
        {"en": ["Taekwondo uniform rental", "Certified instructor", "Certificate", "Photo"], "ko": ["태권도복 대여", "공인 사범", "수료증", "사진"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "10:00", "activity_en": "Introduction & uniform", "activity_ko": "소개 & 도복 착용"}, {"time": "10:15", "activity_en": "Basic techniques", "activity_ko": "기본 기술"}, {"time": "11:00", "activity_en": "Board breaking demo", "activity_ko": "격파 시범"}, {"time": "11:30", "activity_en": "Certificate ceremony", "activity_ko": "수료식"}],
        "Gangnam Taekwondo Center", 37.5050, 127.0286, cancel, 4.6, 47)

    product(_ml("Hangang River Kayaking", "한강 카약 체험"), _ml("Paddle along the scenic Han River with stunning city views.", "멋진 도시 전경과 함께 한강을 카약으로 즐기세요."), "activity", 45, 2, 2, 8,
        {"en": ["Kayak & equipment", "Safety gear", "Instructor", "Changing room"], "ko": ["카약 & 장비", "안전장비", "강사", "탈의실"]},
        {"en": ["Personal expenses", "Towel"], "ko": ["개인 경비", "수건"]},
        [{"time": "09:00", "activity_en": "Safety briefing", "activity_ko": "안전 교육"}, {"time": "09:30", "activity_en": "Kayaking on Han River", "activity_ko": "한강 카약"}, {"time": "10:30", "activity_en": "Break & photo time", "activity_ko": "휴식 & 사진"}, {"time": "11:00", "activity_en": "End", "activity_ko": "종료"}],
        "Banpo Hangang Park", 37.5080, 126.9950, cancel, 4.5, 33)

    product(_ml("Seoul E-Bike City Tour", "서울 전기자전거 시티 투어"), _ml("Explore Seoul on an e-bike covering more ground with less effort.", "전기자전거로 더 넓은 서울을 더 편하게 탐험하세요."), "activity", 55, 3, 1, 10,
        {"en": ["E-bike rental", "Helmet", "Guide", "Bottled water"], "ko": ["전기자전거 대여", "헬멧", "가이드", "생수"]},
        {"en": ["Personal expenses", "Travel insurance"], "ko": ["개인 경비", "여행자 보험"]},
        [{"time": "09:00", "activity_en": "Bike fitting & safety", "activity_ko": "자전거 맞춤 & 안전교육"}, {"time": "09:30", "activity_en": "Ride along Han River", "activity_ko": "한강 따라 라이딩"}, {"time": "11:00", "activity_en": "Park break", "activity_ko": "공원 휴식"}, {"time": "12:00", "activity_en": "Return", "activity_ko": "귀환"}],
        "Banpo Hangang Park E-Bike Station", 37.5080, 126.9950, cancel, 4.6, 61)

    product(_ml("Seoul Photography Walking Tour", "서울 포토그래피 워킹 투어"), _ml("Capture Seoul's beauty with photography tips from a professional.", "전문가의 사진 팁으로 서울의 아름다움을 담으세요."), "activity", 50, 3, 1, 8,
        {"en": ["Professional photographer guide", "Photo editing tips", "5 edited photos"], "ko": ["전문 사진작가 가이드", "보정 팁", "보정 사진 5장"]},
        {"en": ["Camera (bring your own)", "Personal expenses"], "ko": ["카메라 (개인 지참)", "개인 경비"]},
        [{"time": "16:00", "activity_en": "Meet & intro", "activity_ko": "만남 & 소개"}, {"time": "16:30", "activity_en": "Golden hour shooting", "activity_ko": "골든아워 촬영"}, {"time": "18:00", "activity_en": "Sunset & blue hour", "activity_ko": "일몰 & 블루아워"}, {"time": "19:00", "activity_en": "End", "activity_ko": "종료"}],
        "Gangnam Station Exit 10", 37.4979, 127.0276, cancel, 4.5, 44)

    # 23-26: Cooking
    product(_ml("Korean BBQ Cooking Class", "한국 BBQ 쿠킹 클래스"), _ml("Learn to grill Korean BBQ like a pro. Includes Galbi, Bulgogi, and Samgyeopsal.", "프로처럼 한국 BBQ를 굽는 법을 배우세요. 갈비, 불고기, 삼겹살 포함."), "cooking", 65, 3, 2, 10,
        {"en": ["All ingredients", "Recipe booklet", "Apron", "Full meal"], "ko": ["모든 재료", "레시피 책자", "앞치마", "풀 식사"]},
        {"en": ["Personal expenses", "Alcoholic beverages"], "ko": ["개인 경비", "주류"]},
        [{"time": "11:00", "activity_en": "Introduction to Korean BBQ", "activity_ko": "한국 BBQ 소개"}, {"time": "11:30", "activity_en": "Prep & marinate", "activity_ko": "손질 & 양념"}, {"time": "12:30", "activity_en": "Grilling & cooking", "activity_ko": "굽기 & 조리"}, {"time": "13:30", "activity_en": "Eat together", "activity_ko": "함께 식사"}, {"time": "14:00", "activity_en": "End", "activity_ko": "종료"}],
        "Gangnam Cooking Studio", 37.5010, 127.0276, cancel, 4.8, 98)

    product(_ml("Kimchi Making Workshop", "김치 만들기 워크숍"), _ml("Make your own kimchi with traditional Korean methods.", "전통 방식으로 나만의 김치를 만들어 보세요."), "cooking", 45, 2, 2, 12,
        {"en": ["All ingredients", "Take-home kimchi jar", "Recipe card", "Apron"], "ko": ["모든 재료", "김치 포장", "레시피 카드", "앞치마"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "14:00", "activity_en": "History of kimchi", "activity_ko": "김치의 역사"}, {"time": "14:30", "activity_en": "Prepare ingredients", "activity_ko": "재료 준비"}, {"time": "15:00", "activity_en": "Make kimchi", "activity_ko": "김치 만들기"}, {"time": "16:00", "activity_en": "Tasting & packaging", "activity_ko": "시식 & 포장"}],
        "Seocho Cooking Academy", 37.4922, 127.0098, cancel, 4.7, 76)

    product(_ml("Korean Dessert Baking Class", "한국 디저트 베이킹 클래스"), _ml("Learn to make traditional Korean sweets like tteok and hoddeok.", "떡, 호떡 등 전통 한국 디저트를 만들어 보세요."), "cooking", 50, 2.5, 1, 8,
        {"en": ["All ingredients", "Recipe booklet", "Take-home treats", "Tea pairing"], "ko": ["모든 재료", "레시피 책자", "디저트 포장", "차 페어링"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "14:00", "activity_en": "Intro to Korean desserts", "activity_ko": "한국 디저트 소개"}, {"time": "14:30", "activity_en": "Make tteok", "activity_ko": "떡 만들기"}, {"time": "15:30", "activity_en": "Make hoddeok", "activity_ko": "호떡 만들기"}, {"time": "16:30", "activity_en": "Tea time & tasting", "activity_ko": "다과 시간"}],
        "Gangnam Baking Studio", 37.5050, 127.0286, cancel, 4.6, 52)

    product(_ml("Korean Royal Cuisine Experience", "한국 궁중음식 체험"), _ml("Cook and taste exquisite Korean royal court cuisine.", "정교한 한국 궁중음식을 요리하고 맛보세요."), "cooking", 85, 3, 2, 8,
        {"en": ["Premium ingredients", "Expert chef instruction", "Full course meal", "Traditional tableware experience", "Recipe book"], "ko": ["프리미엄 재료", "전문 셰프 지도", "풀코스 식사", "전통 식기 체험", "레시피 북"]},
        {"en": ["Personal expenses"], "ko": ["개인 경비"]},
        [{"time": "11:00", "activity_en": "Royal cuisine history", "activity_ko": "궁중음식 역사"}, {"time": "11:30", "activity_en": "Ingredient preparation", "activity_ko": "재료 준비"}, {"time": "12:30", "activity_en": "Cooking royal dishes", "activity_ko": "궁중음식 조리"}, {"time": "13:30", "activity_en": "Plating & dining", "activity_ko": "플레이팅 & 식사"}, {"time": "14:00", "activity_en": "End", "activity_ko": "종료"}],
        "Seocho Royal Cuisine Center", 37.4867, 127.0045, cancel, 4.9, 35)

    # 27-30: Wellness
    product(_ml("Korean Jjimjilbang Spa Experience", "한국 찜질방 스파 체험"), _ml("Full Korean spa experience with sauna, hot rooms, and cold plunge.", "사우나, 찜질방, 냉탕이 포함된 한국식 스파 체험."), "wellness", 35, 3, 1, 10,
        {"en": ["Jjimjilbang entrance", "Robe & towel", "Guide assistance", "Snack (eggs & sikhye)"], "ko": ["찜질방 입장", "가운 & 수건", "가이드 도움", "간식 (계란·식혜)"]},
        {"en": ["Personal expenses", "Additional treatments"], "ko": ["개인 경비", "추가 시술"]},
        [{"time": "10:00", "activity_en": "Arrive & check-in", "activity_ko": "도착 & 체크인"}, {"time": "10:30", "activity_en": "Hot rooms & sauna", "activity_ko": "찜질방 & 사우나"}, {"time": "12:00", "activity_en": "Snack time", "activity_ko": "간식 시간"}, {"time": "13:00", "activity_en": "End", "activity_ko": "종료"}],
        "Gangnam Jjimjilbang", 37.4995, 127.0278, cancel, 4.5, 88)

    product(_ml("Traditional Korean Massage & Acupressure", "전통 한국 마사지 & 지압"), _ml("Relax with traditional Korean body massage and acupressure therapy.", "전통 한국식 전신 마사지와 지압 치료로 휴식하세요."), "wellness", 75, 2, 1, 4,
        {"en": ["90-min massage", "Herbal tea", "Relaxation room access", "Foot bath"], "ko": ["90분 마사지", "한방 차", "휴게실 이용", "족욕"]},
        {"en": ["Personal expenses", "Tips (not expected)"], "ko": ["개인 경비", "팁 (불필요)"]},
        [{"time": "14:00", "activity_en": "Consultation", "activity_ko": "상담"}, {"time": "14:15", "activity_en": "Foot bath", "activity_ko": "족욕"}, {"time": "14:30", "activity_en": "Full body massage", "activity_ko": "전신 마사지"}, {"time": "16:00", "activity_en": "Herbal tea & relaxation", "activity_ko": "한방차 & 휴식"}],
        "Seocho Wellness Center", 37.4922, 127.0098, cancel, 4.7, 54)

    product(_ml("Yoga & Meditation Retreat", "요가 & 명상 리트릿"), _ml("Half-day yoga and meditation retreat in a peaceful Seocho setting.", "평화로운 서초에서 반나절 요가·명상 리트릿."), "wellness", 50, 3, 1, 12,
        {"en": ["Yoga mat & props", "Meditation session", "Herbal tea", "Healthy snack"], "ko": ["요가 매트 & 소품", "명상 세션", "한방 차", "건강 간식"]},
        {"en": ["Personal expenses", "Change of clothes"], "ko": ["개인 경비", "갈아입을 옷"]},
        [{"time": "09:00", "activity_en": "Morning yoga", "activity_ko": "모닝 요가"}, {"time": "10:00", "activity_en": "Guided meditation", "activity_ko": "가이드 명상"}, {"time": "10:45", "activity_en": "Tea break", "activity_ko": "다과 시간"}, {"time": "11:15", "activity_en": "Mindfulness walk", "activity_ko": "마음챙김 산책"}, {"time": "12:00", "activity_en": "End", "activity_ko": "종료"}],
        "Yangjae Forest Yoga Center", 37.4708, 127.0378, cancel, 4.6, 29)

    product(_ml("Korean Herbal Medicine Experience", "한방 체험"), _ml("Experience traditional Korean herbal medicine with a licensed practitioner.", "한의사와 함께 전통 한방 체험을 하세요."), "wellness", 65, 2, 1, 6,
        {"en": ["Pulse diagnosis", "Body constitution analysis", "Herbal tea blending", "Take-home tea pack"], "ko": ["맥진", "체질 분석", "한방 차 블렌딩", "차 가져가기"]},
        {"en": ["Personal expenses", "Additional herbal products"], "ko": ["개인 경비", "추가 한방 제품"]},
        [{"time": "14:00", "activity_en": "Welcome & introduction", "activity_ko": "환영 & 소개"}, {"time": "14:15", "activity_en": "Pulse diagnosis & consultation", "activity_ko": "맥진 & 상담"}, {"time": "15:00", "activity_en": "Herbal tea blending", "activity_ko": "한방 차 블렌딩"}, {"time": "15:45", "activity_en": "Tasting & Q&A", "activity_ko": "시음 & Q&A"}, {"time": "16:00", "activity_en": "End", "activity_ko": "종료"}],
        "Gangnam Oriental Medicine Clinic", 37.5014, 127.0262, cancel, 4.5, 22)

    return products
