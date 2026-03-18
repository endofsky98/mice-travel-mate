import uuid

def _id():
    return str(uuid.uuid4())

def get_courses():
    courses = []
    spots = []
    transitions = []

    # Helper to create spot dicts
    def spot(cid, order, name_en, name_ko, desc_en, desc_ko, lat, lng, stay, names_extra=None, descs_extra=None):
        sid = _id()
        s = {
            "id": sid, "course_id": cid, "spot_order": order,
            "name_en": name_en, "name_ko": name_ko,
            "name_zh_cn": (names_extra or {}).get("zh_cn", name_en),
            "name_zh_tw": (names_extra or {}).get("zh_tw", name_en),
            "name_ja": (names_extra or {}).get("ja", name_en),
            "name_es": (names_extra or {}).get("es", name_en),
            "name_th": (names_extra or {}).get("th", name_en),
            "name_vi": (names_extra or {}).get("vi", name_en),
            "name_fr": (names_extra or {}).get("fr", name_en),
            "description_en": desc_en, "description_ko": desc_ko,
            "description_zh_cn": (descs_extra or {}).get("zh_cn", desc_en),
            "description_zh_tw": (descs_extra or {}).get("zh_tw", desc_en),
            "description_ja": (descs_extra or {}).get("ja", desc_en),
            "description_es": (descs_extra or {}).get("es", desc_en),
            "description_th": (descs_extra or {}).get("th", desc_en),
            "description_vi": (descs_extra or {}).get("vi", desc_en),
            "description_fr": (descs_extra or {}).get("fr", desc_en),
            "latitude": lat, "longitude": lng,
            "stay_duration_minutes": stay,
            "image_url": f"/images/placeholder/spot_{order}.jpg",
            "restaurant_id": None,
        }
        spots.append(s)
        return sid

    def trans(cid, from_sid, to_sid, mode, dur, dist):
        transitions.append({
            "id": _id(), "course_id": cid,
            "from_spot_id": from_sid, "to_spot_id": to_sid,
            "transport_mode": mode, "duration_minutes": dur,
            "distance_km": dist, "route_polyline": None,
        })

    def course(name_en, name_ko, desc_en, desc_ko, dur_type, theme, diff, total_min, total_km, cost, rating, reviews, names_extra=None, descs_extra=None):
        cid = _id()
        courses.append({
            "id": cid,
            "name_en": name_en, "name_ko": name_ko,
            "name_zh_cn": (names_extra or {}).get("zh_cn", name_en),
            "name_zh_tw": (names_extra or {}).get("zh_tw", name_en),
            "name_ja": (names_extra or {}).get("ja", name_en),
            "name_es": (names_extra or {}).get("es", name_en),
            "name_th": (names_extra or {}).get("th", name_en),
            "name_vi": (names_extra or {}).get("vi", name_en),
            "name_fr": (names_extra or {}).get("fr", name_en),
            "description_en": desc_en, "description_ko": desc_ko,
            "description_zh_cn": (descs_extra or {}).get("zh_cn", desc_en),
            "description_zh_tw": (descs_extra or {}).get("zh_tw", desc_en),
            "description_ja": (descs_extra or {}).get("ja", desc_en),
            "description_es": (descs_extra or {}).get("es", desc_en),
            "description_th": (descs_extra or {}).get("th", desc_en),
            "description_vi": (descs_extra or {}).get("vi", desc_en),
            "description_fr": (descs_extra or {}).get("fr", desc_en),
            "duration_type": dur_type, "theme": theme, "region": "seoul",
            "difficulty": diff, "total_duration_minutes": total_min,
            "total_distance_km": total_km, "estimated_transport_cost": cost,
            "avg_rating": rating, "review_count": reviews,
            "image_url": f"/images/placeholder/course_{len(courses)+1}.jpg",
            "is_active": True,
        })
        return cid

    # ── Course 1: Gangnam K-Culture Walk ──
    c = course("Gangnam K-Culture Walk", "강남 K-컬처 워크", "Explore the heart of K-Pop and modern Korean culture in Gangnam.", "강남의 K-POP과 현대 한국 문화를 탐험하세요.",
        "half_day", "kpop_hallyu", "easy", 210, 5.2, 5000, 4.7, 89,
        {"zh_cn": "江南K文化漫步", "zh_tw": "江南K文化漫步", "ja": "江南Kカルチャーウォーク", "es": "Paseo K-Cultura Gangnam", "th": "เดินชม K-Culture ย่านกังนัม", "vi": "Dạo bộ Văn hóa K Gangnam", "fr": "Promenade K-Culture Gangnam"})
    s1 = spot(c, 0, "Gangnam Station", "강남역", "Start at the iconic Gangnam Station.", "상징적인 강남역에서 출발합니다.", 37.4979, 127.0276, 20)
    s2 = spot(c, 1, "COEX Mall", "코엑스몰", "Korea's largest underground shopping mall with K-Star Road.", "한국 최대 지하쇼핑몰 코엑스와 K스타의 거리.", 37.5126, 127.0590, 60)
    s3 = spot(c, 2, "SM Entertainment Building", "SM엔터테인먼트 사옥", "Visit the headquarters of one of Korea's biggest entertainment companies.", "한국 최대 엔터 기업 사옥을 방문합니다.", 37.5134, 127.0585, 30)
    s4 = spot(c, 3, "Apgujeong Rodeo Street", "압구정 로데오거리", "Trendy fashion and beauty district.", "트렌디한 패션·뷰티 거리.", 37.5270, 127.0399, 60)
    trans(c, s1, s2, "subway", 15, 2.1)
    trans(c, s2, s3, "walk", 5, 0.3)
    trans(c, s3, s4, "subway", 10, 2.5)

    # ── Course 2: Seocho Art & Nature ──
    c = course("Seocho Art & Nature", "서초 예술과 자연", "Enjoy world-class arts and beautiful nature trails.", "세계적 수준의 예술과 아름다운 자연 산책로.",
        "half_day", "nature_healing", "easy", 240, 4.5, 3000, 4.5, 67,
        {"zh_cn": "瑞草艺术与自然", "zh_tw": "瑞草藝術與自然", "ja": "瑞草アート＆ネイチャー", "es": "Arte y Naturaleza Seocho", "th": "ศิลปะและธรรมชาติ ซอโช", "vi": "Nghệ thuật & Thiên nhiên Seocho", "fr": "Art et Nature Seocho"})
    s1 = spot(c, 0, "Seoul Arts Center", "예술의전당", "Korea's premier performing arts complex.", "한국 최고의 공연예술 복합시설.", 37.4784, 127.0117, 60)
    s2 = spot(c, 1, "Yangjae Citizens' Forest", "양재시민의숲", "Beautiful urban forest with walking trails.", "아름다운 도시 숲 산책로.", 37.4708, 127.0378, 45)
    s3 = spot(c, 2, "Montmartre Park", "몽마르뜨 공원", "Scenic park with great city views.", "도시 전망이 아름다운 공원.", 37.4838, 127.0141, 30)
    trans(c, s1, s2, "bus", 15, 2.8)
    trans(c, s2, s3, "walk", 20, 1.5)

    # ── Course 3: Gangnam Food Tour ──
    c = course("Gangnam Food Tour", "강남 맛집 투어", "Taste the best Korean cuisine in Gangnam district.", "강남에서 최고의 한국 요리를 맛보세요.",
        "half_day", "food_tour", "easy", 180, 3.0, 4000, 4.8, 120,
        {"zh_cn": "江南美食之旅", "zh_tw": "江南美食之旅", "ja": "江南フードツアー", "es": "Tour Gastronómico Gangnam", "th": "ทัวร์อาหารกังนัม", "vi": "Tour Ẩm thực Gangnam", "fr": "Tour Gastronomique Gangnam"})
    s1 = spot(c, 0, "Garosu-gil", "가로수길", "Start at the famous tree-lined street of Garosu-gil.", "유명한 가로수길에서 시작합니다.", 37.5199, 127.0231, 40)
    s2 = spot(c, 1, "Gangnam Station Food Alley", "강남역 먹자골목", "Hidden food alley near Gangnam Station.", "강남역 근처 숨은 먹자골목.", 37.4981, 127.0289, 50)
    s3 = spot(c, 2, "Nonhyeon BBQ Street", "논현동 고깃집 거리", "Famous Korean BBQ restaurant street.", "유명한 한국 바비큐 식당 거리.", 37.5107, 127.0261, 60)
    trans(c, s1, s2, "walk", 15, 1.2)
    trans(c, s2, s3, "walk", 10, 0.8)

    # ── Course 4: COEX & Bongeunsa Temple ──
    c = course("COEX & Bongeunsa Temple", "코엑스 & 봉은사", "Modern shopping meets ancient temple.", "현대 쇼핑과 고대 사찰의 만남.",
        "half_day", "history_culture", "easy", 210, 2.5, 2000, 4.6, 95,
        {"zh_cn": "COEX和奉恩寺", "zh_tw": "COEX和奉恩寺", "ja": "COEX＆奉恩寺", "es": "COEX y Templo Bongeunsa", "th": "COEX และวัดบงอึนซา", "vi": "COEX & Chùa Bongeunsa", "fr": "COEX & Temple Bongeunsa"})
    s1 = spot(c, 0, "Bongeunsa Temple", "봉은사", "Ancient Buddhist temple in the heart of Gangnam.", "강남 한복판의 고대 불교 사찰.", 37.5153, 127.0575, 60)
    s2 = spot(c, 1, "Starfield COEX Mall", "스타필드 코엑스몰", "Largest underground mall with Starfield Library.", "별마당 도서관이 있는 최대 지하 쇼핑몰.", 37.5126, 127.0590, 60)
    s3 = spot(c, 2, "K-Star Road", "K스타의 거리", "K-Pop idol statues and fan culture.", "K-POP 아이돌 조형물과 팬문화.", 37.5111, 127.0596, 30)
    trans(c, s1, s2, "walk", 5, 0.3)
    trans(c, s2, s3, "walk", 5, 0.2)

    # ── Course 5: Gangnam Night Tour ──
    c = course("Gangnam Nightlife Tour", "강남 나이트 투어", "Experience the vibrant nightlife of Gangnam.", "강남의 활기찬 야간 문화를 경험하세요.",
        "half_day", "nightlife", "easy", 210, 4.0, 8000, 4.4, 55,
        {"zh_cn": "江南夜生活之旅", "zh_tw": "江南夜生活之旅", "ja": "江南ナイトライフツアー", "es": "Tour Nocturno Gangnam", "th": "ทัวร์ไนท์ไลฟ์กังนัม", "vi": "Tour Cuộc sống về đêm Gangnam", "fr": "Tour Nocturne Gangnam"})
    s1 = spot(c, 0, "Gangnam Station Area", "강남역 일대", "Start your night at Gangnam's busiest intersection.", "강남 가장 번화한 교차로에서 시작.", 37.4979, 127.0276, 30)
    s2 = spot(c, 1, "Cheongdam-dong", "청담동", "Upscale bars and restaurants.", "고급 바와 레스토랑.", 37.5243, 127.0525, 60)
    s3 = spot(c, 2, "Seolleung Park Night Walk", "선릉공원 야간 산책", "Peaceful night walk by royal tombs.", "왕릉 옆 평화로운 야간 산책.", 37.5084, 127.0469, 30)
    s4 = spot(c, 3, "Yeoksam Pojangmacha Alley", "역삼 포장마차 골목", "Traditional Korean street food tents.", "전통 한국 포장마차.", 37.5009, 127.0376, 40)
    trans(c, s1, s2, "taxi", 10, 3.2)
    trans(c, s2, s3, "walk", 10, 0.7)
    trans(c, s3, s4, "walk", 8, 0.5)

    # ── Course 6: Shopping Paradise ──
    c = course("Gangnam Shopping Paradise", "강남 쇼핑 파라다이스", "Premium shopping from luxury to underground bargains.", "럭셔리부터 지하 쇼핑까지 프리미엄 쇼핑.",
        "full_day", "shopping", "easy", 420, 7.0, 6000, 4.5, 72,
        {"zh_cn": "江南购物天堂", "zh_tw": "江南購物天堂", "ja": "江南ショッピングパラダイス", "es": "Paraíso de Compras Gangnam", "th": "สวรรค์ช้อปปิ้งกังนัม", "vi": "Thiên đường Mua sắm Gangnam", "fr": "Paradis du Shopping Gangnam"})
    s1 = spot(c, 0, "Express Bus Terminal Underground Mall", "고속터미널 지하상가", "Affordable fashion and accessories.", "저렴한 패션·액세서리.", 37.5048, 126.9822, 90)
    s2 = spot(c, 1, "Garosu-gil Boutiques", "가로수길 부티크", "Designer boutiques on the tree-lined street.", "가로수길 디자이너 부티크.", 37.5199, 127.0231, 60)
    s3 = spot(c, 2, "Cheongdam Luxury Avenue", "청담 명품거리", "Flagship stores of global luxury brands.", "글로벌 명품 브랜드 플래그십 매장.", 37.5243, 127.0525, 60)
    s4 = spot(c, 3, "COEX Mall", "코엑스몰", "Electronics, fashion, and entertainment.", "전자제품, 패션, 엔터테인먼트.", 37.5126, 127.0590, 90)
    trans(c, s1, s2, "bus", 15, 3.5)
    trans(c, s2, s3, "taxi", 8, 1.8)
    trans(c, s3, s4, "subway", 10, 1.5)

    # ── Course 7: Historical Seoul from Gangnam ──
    c = course("Historical Seoul from Gangnam", "강남에서 떠나는 역사 여행", "Day trip to Seoul's historical districts from Gangnam.", "강남에서 출발하는 서울 역사 지구 일일 여행.",
        "full_day", "history_culture", "moderate", 480, 15.0, 8000, 4.7, 88,
        {"zh_cn": "从江南出发的首尔历史之旅", "zh_tw": "從江南出發的首爾歷史之旅", "ja": "江南から行く歴史的ソウル", "es": "Seúl Histórico desde Gangnam", "th": "ท่องประวัติศาสตร์โซลจากกังนัม", "vi": "Seoul Lịch sử từ Gangnam", "fr": "Séoul Historique depuis Gangnam"})
    s1 = spot(c, 0, "Gangnam Station", "강남역", "Meeting point at Gangnam Station.", "강남역 집합.", 37.4979, 127.0276, 10)
    s2 = spot(c, 1, "Gyeongbokgung Palace", "경복궁", "The main royal palace of the Joseon dynasty.", "조선왕조의 주요 왕궁.", 37.5796, 126.9770, 90)
    s3 = spot(c, 2, "Bukchon Hanok Village", "북촌한옥마을", "Traditional Korean houses between palaces.", "궁궐 사이의 전통 한옥 마을.", 37.5826, 126.9831, 60)
    s4 = spot(c, 3, "Insadong", "인사동", "Traditional culture, tea houses, and galleries.", "전통 문화, 찻집, 갤러리.", 37.5732, 126.9870, 60)
    s5 = spot(c, 4, "Namsan Tower", "남산타워", "Iconic tower with panoramic city views.", "서울 전경을 볼 수 있는 상징적 타워.", 37.5512, 126.9882, 60)
    trans(c, s1, s2, "subway", 35, 10.0)
    trans(c, s2, s3, "walk", 15, 1.0)
    trans(c, s3, s4, "walk", 10, 0.7)
    trans(c, s4, s5, "bus", 15, 3.0)

    # ── Course 8: Healing Nature Walk ──
    c = course("Seoul Healing Nature Walk", "서울 힐링 자연 산책", "Escape the city with peaceful nature trails.", "평화로운 자연 산책로로 도시를 벗어나세요.",
        "half_day", "nature_healing", "moderate", 240, 6.0, 3000, 4.6, 48,
        {"zh_cn": "首尔治愈自然散步", "zh_tw": "首爾療癒自然散步", "ja": "ソウル癒しの自然散歩", "es": "Paseo Natural Sanador en Seúl", "th": "เดินเล่นธรรมชาติเพื่อการเยียวยาในโซล", "vi": "Dạo bộ Thiên nhiên Chữa lành Seoul", "fr": "Promenade Nature Guérison Séoul"})
    s1 = spot(c, 0, "Yangjae Citizens' Forest", "양재시민의숲", "Start at this lush urban forest.", "푸릇한 도시 숲에서 시작.", 37.4708, 127.0378, 45)
    s2 = spot(c, 1, "Umyeonsan Mountain", "우면산", "Easy hiking trail with great views.", "좋은 전망의 쉬운 등산로.", 37.4680, 127.0080, 90)
    s3 = spot(c, 2, "Seoripul Park", "서리풀공원", "Hidden park with walking paths.", "산책로가 있는 숨은 공원.", 37.4922, 127.0098, 40)
    trans(c, s1, s2, "bus", 15, 3.5)
    trans(c, s2, s3, "walk", 20, 1.5)

    # ── Course 9: K-Food & Market Tour ──
    c = course("K-Food & Market Tour", "K-푸드 & 시장 투어", "Discover Korean food culture through local markets.", "현지 시장을 통해 한국 음식 문화를 발견하세요.",
        "full_day", "food_tour", "easy", 360, 8.0, 6000, 4.8, 105,
        {"zh_cn": "K美食与市场之旅", "zh_tw": "K美食與市場之旅", "ja": "Kフード＆マーケットツアー", "es": "Tour K-Food y Mercados", "th": "ทัวร์ K-Food และตลาด", "vi": "Tour K-Food & Chợ", "fr": "Tour K-Food et Marchés"})
    s1 = spot(c, 0, "Seocho Flower Market", "서초 꽃시장", "Start at one of Seoul's largest flower markets.", "서울 최대 꽃시장에서 시작.", 37.4955, 127.0035, 30)
    s2 = spot(c, 1, "Gangnam Yangyeomtongdak Alley", "강남 양념통닭 골목", "Famous Korean fried chicken alley.", "유명 한국식 프라이드 치킨 골목.", 37.4992, 127.0312, 50)
    s3 = spot(c, 2, "Express Bus Terminal Underground Market", "고속터미널 지하 시장", "Hidden food court and traditional goods.", "숨겨진 푸드코트와 전통 물품.", 37.5048, 126.9822, 60)
    s4 = spot(c, 3, "Noryangjin Fish Market", "노량진수산시장", "Fresh seafood market with on-site restaurants.", "현장 식당이 있는 신선 수산 시장.", 37.5130, 126.9412, 90)
    trans(c, s1, s2, "taxi", 8, 2.5)
    trans(c, s2, s3, "subway", 10, 2.0)
    trans(c, s3, s4, "subway", 15, 4.5)

    # ── Course 10: Local Experience Tour ──
    c = course("Gangnam Local Experience", "강남 로컬 체험", "Live like a local in Gangnam.", "강남에서 현지인처럼 살아보세요.",
        "full_day", "local_experience", "easy", 360, 5.0, 5000, 4.4, 38,
        {"zh_cn": "江南本地体验", "zh_tw": "江南本地體驗", "ja": "江南ローカル体験", "es": "Experiencia Local Gangnam", "th": "ประสบการณ์ท้องถิ่นกังนัม", "vi": "Trải nghiệm Địa phương Gangnam", "fr": "Expérience Locale Gangnam"})
    s1 = spot(c, 0, "Dosan Park", "도산공원", "Start at the tranquil Dosan Park.", "고요한 도산공원에서 시작.", 37.5224, 127.0379, 30)
    s2 = spot(c, 1, "Sinsa-dong Cafe Hopping", "신사동 카페 호핑", "Explore unique cafes in Sinsa-dong.", "신사동의 유니크한 카페를 탐험.", 37.5181, 127.0243, 60)
    s3 = spot(c, 2, "Gangnam Traditional Market", "강남 전통시장", "Experience a local Korean market.", "현지 한국 시장 체험.", 37.5050, 127.0286, 60)
    s4 = spot(c, 3, "Jjimjilbang Experience", "찜질방 체험", "Korean spa and sauna experience.", "한국식 스파·사우나 체험.", 37.4995, 127.0278, 120)
    trans(c, s1, s2, "walk", 10, 0.8)
    trans(c, s2, s3, "walk", 15, 1.2)
    trans(c, s3, s4, "walk", 8, 0.5)

    # ── Courses 11-30 (compact generation) ──
    course_defs = [
        ("Teheran-ro Business & Culture Walk", "테헤란로 비즈니스 & 문화", "half_day", "local_experience", "easy", 180, 3.5, 3000, 4.3, 42,
         [("Gangnam Station", "강남역", 37.4979, 127.0276, 15), ("Teheran-ro Skyscrapers", "테헤란로 고층빌딩", 37.5052, 127.0395, 30), ("Samsung Station Area", "삼성역 일대", 37.5088, 127.0632, 45), ("COEX Aquarium", "코엑스 아쿠아리움", 37.5118, 127.0589, 60)],
         [("subway", 8, 1.5), ("walk", 10, 0.8), ("walk", 5, 0.4)]),
        ("Hangang River Cycling Tour", "한강 자전거 투어", "half_day", "nature_healing", "active", 180, 12.0, 2000, 4.7, 76,
         [("Banpo Hangang Park", "반포한강공원", 37.5080, 126.9950, 20), ("Banpo Bridge Rainbow Fountain", "반포대교 달빛무지개 분수", 37.5070, 126.9960, 20), ("Jamwon Hangang Park", "잠원한강공원", 37.5180, 127.0130, 30), ("Yeouido Park", "여의도공원", 37.5256, 126.9241, 45)],
         [("bicycle", 5, 0.5), ("bicycle", 15, 4.0), ("bicycle", 20, 7.0)]),
        ("Seoul Temple Stay Experience", "서울 템플스테이 체험", "overnight", "history_culture", "moderate", 1440, 5.0, 5000, 4.9, 35,
         [("Bongeunsa Temple", "봉은사", 37.5153, 127.0575, 120), ("Temple Stay Program", "템플스테이 프로그램", 37.5153, 127.0575, 480), ("Morning Prayer & Meditation", "새벽 예불 & 명상", 37.5153, 127.0575, 60), ("Traditional Temple Breakfast", "사찰 음식 아침", 37.5153, 127.0575, 60)],
         [("walk", 0, 0), ("walk", 0, 0), ("walk", 0, 0)]),
        ("Seocho Cafe & Dessert Trail", "서초 카페 & 디저트 트레일", "half_day", "food_tour", "easy", 180, 3.0, 2000, 4.5, 63,
         [("Banpo Café Street", "반포 카페거리", 37.5043, 126.9912, 40), ("Seocho-dong Dessert Shops", "서초동 디저트 가게", 37.4920, 127.0088, 40), ("Sapyeong-daero Tea Houses", "사평대로 전통 찻집", 37.4867, 127.0045, 40), ("Seoul National University Area Cafes", "서울대입구역 카페", 37.4812, 126.9527, 40)],
         [("walk", 10, 0.8), ("walk", 10, 0.7), ("bus", 15, 3.5)]),
        ("K-Beauty & Fashion Tour", "K-뷰티 & 패션 투어", "half_day", "shopping", "easy", 210, 4.0, 5000, 4.4, 51,
         [("Garosu-gil Beauty Street", "가로수길 뷰티 거리", 37.5199, 127.0231, 50), ("Gangnam K-Beauty Store", "강남 K-뷰티 매장", 37.4979, 127.0276, 40), ("Cheongdam Fashion District", "청담 패션 지구", 37.5243, 127.0525, 60)],
         [("walk", 15, 1.2), ("taxi", 10, 2.5)]),
        ("Gangnam Architecture Tour", "강남 건축 투어", "half_day", "history_culture", "easy", 180, 4.0, 4000, 4.3, 28,
         [("GT Tower", "GT타워", 37.4981, 127.0276, 20), ("Samsung Town", "삼성타운", 37.5030, 127.0530, 30), ("Trade Tower", "트레이드타워", 37.5088, 127.0612, 20), ("Some Sevit Floating Islands", "세빛섬", 37.5105, 126.9963, 40)],
         [("subway", 10, 2.0), ("walk", 8, 0.5), ("taxi", 12, 3.0)]),
        ("Hanbok Photo Tour", "한복 포토 투어", "full_day", "history_culture", "easy", 360, 10.0, 7000, 4.8, 92,
         [("Gangnam Hanbok Rental", "강남 한복 대여", 37.5014, 127.0262, 40), ("Bongeunsa Temple", "봉은사", 37.5153, 127.0575, 60), ("Gyeongbokgung Palace", "경복궁", 37.5796, 126.9770, 90), ("Bukchon Hanok Village", "북촌한옥마을", 37.5826, 126.9831, 60)],
         [("taxi", 10, 3.0), ("subway", 30, 8.0), ("walk", 15, 1.0)]),
        ("Hallyu Drama Locations Tour", "한류 드라마 촬영지 투어", "full_day", "kpop_hallyu", "easy", 360, 15.0, 10000, 4.6, 84,
         [("COEX Starfield Library (Goblin)", "별마당도서관 (도깨비)", 37.5126, 127.0590, 40), ("Banpo Bridge (Several Dramas)", "반포대교 (여러 드라마)", 37.5070, 126.9960, 30), ("Namsan Tower (My Love from the Star)", "남산타워 (별에서 온 그대)", 37.5512, 126.9882, 60), ("Bukchon Hanok (Winter Sonata)", "북촌한옥 (겨울연가)", 37.5826, 126.9831, 50)],
         [("walk", 5, 0.5), ("bus", 20, 5.0), ("bus", 25, 6.0)]),
        ("Wellness & Spa Day", "웰니스 & 스파 데이", "full_day", "nature_healing", "easy", 420, 5.0, 5000, 4.5, 41,
         [("Gangnam Premium Spa", "강남 프리미엄 스파", 37.5005, 127.0276, 120), ("Yangjae Meditation Center", "양재 명상센터", 37.4708, 127.0378, 60), ("Seocho Traditional Korean Medicine", "서초 한방 체험", 37.4922, 127.0098, 60), ("Banpo Hangang Park Walk", "반포한강공원 산책", 37.5080, 126.9950, 60)],
         [("taxi", 10, 3.0), ("bus", 10, 2.0), ("bus", 15, 3.0)]),
        ("MICE Networking & Sightseeing", "MICE 네트워킹 & 관광", "full_day", "local_experience", "easy", 360, 6.0, 8000, 4.3, 22,
         [("COEX Convention Center", "코엑스 컨벤션센터", 37.5126, 127.0590, 60), ("Teheran-ro Business Lunch", "테헤란로 비즈니스 런치", 37.5052, 127.0395, 60), ("Samsung D'light", "삼성 딜라이트", 37.5014, 127.0262, 40), ("Gangnam Networking Bar", "강남 네트워킹 바", 37.4979, 127.0276, 60)],
         [("walk", 10, 0.8), ("walk", 5, 0.5), ("walk", 10, 0.8)]),
        ("Express Bus Terminal & Banpo Night", "고속터미널 & 반포 야경", "half_day", "nightlife", "easy", 180, 3.0, 3000, 4.6, 58,
         [("Express Bus Terminal Underground", "고속터미널 지하상가", 37.5048, 126.9822, 40), ("Banpo Bridge Rainbow Fountain", "반포대교 무지개 분수", 37.5070, 126.9960, 40), ("Some Sevit Islands", "세빛섬", 37.5105, 126.9963, 40)],
         [("walk", 10, 0.8), ("walk", 10, 0.6)]),
        ("Traditional Korean Cooking Class Tour", "전통 한식 쿠킹 클래스 투어", "half_day", "food_tour", "easy", 240, 3.0, 4000, 4.7, 66,
         [("Gangnam Cooking Studio", "강남 쿠킹 스튜디오", 37.5010, 127.0276, 120), ("Korean BBQ Lunch", "한국식 BBQ 점심", 37.4981, 127.0289, 60), ("Traditional Tea Ceremony", "전통 다도 체험", 37.5199, 127.0231, 40)],
         [("walk", 5, 0.3), ("taxi", 8, 2.0)]),
        ("Seoul by Night Panorama", "서울 야경 파노라마", "half_day", "nightlife", "easy", 210, 10.0, 10000, 4.8, 99,
         [("63 Building Observatory", "63빌딩 전망대", 37.5197, 126.9402, 40), ("Namsan Tower Night View", "남산타워 야경", 37.5512, 126.9882, 50), ("Banpo Bridge Night Fountain", "반포대교 야경분수", 37.5070, 126.9960, 30), ("Gangnam Rooftop Bar", "강남 루프탑 바", 37.4979, 127.0276, 60)],
         [("taxi", 15, 4.0), ("bus", 20, 4.0), ("taxi", 15, 5.0)]),
        ("Kids & Family Seoul Fun", "키즈 & 패밀리 서울 펀", "full_day", "local_experience", "easy", 420, 8.0, 6000, 4.4, 33,
         [("COEX Aquarium", "코엑스 아쿠아리움", 37.5118, 127.0589, 90), ("Lotte World Tower", "롯데월드타워", 37.5126, 127.1026, 90), ("Olympic Park", "올림픽공원", 37.5202, 127.1215, 60), ("Banpo Hangang Park Playground", "반포한강공원 놀이터", 37.5080, 126.9950, 60)],
         [("subway", 15, 4.0), ("subway", 10, 2.0), ("bus", 20, 5.0)]),
        ("Gangnam Rooftop Bar Crawl", "강남 루프탑 바 크롤", "half_day", "nightlife", "easy", 180, 3.5, 8000, 4.3, 44,
         [("Hotel Rooftop Bar Gangnam", "호텔 루프탑 바 강남", 37.5014, 127.0395, 50), ("Sky Lounge Cheongdam", "스카이 라운지 청담", 37.5243, 127.0525, 50), ("Rooftop Garden Bar Sinsa", "루프탑 가든 바 신사", 37.5181, 127.0243, 50)],
         [("taxi", 8, 2.5), ("taxi", 8, 2.0)]),
        ("Seocho Library & Culture Tour", "서초 도서관 & 문화 투어", "half_day", "history_culture", "easy", 180, 3.0, 2000, 4.2, 18,
         [("Seoul Central Library", "서울중앙도서관", 37.4922, 127.0098, 40), ("Seocho Arts Hall", "서초문화예술회관", 37.4910, 127.0120, 30), ("Seoul Arts Center", "예술의전당", 37.4784, 127.0117, 60)],
         [("walk", 5, 0.3), ("bus", 10, 2.0)]),
        ("Gangnam Wellness Morning Routine", "강남 웰니스 모닝 루틴", "half_day", "nature_healing", "moderate", 180, 4.0, 2000, 4.5, 27,
         [("Yangjae Morning Yoga", "양재 모닝 요가", 37.4708, 127.0378, 40), ("Seoul National Cemetery Reflection Walk", "현충원 묵상 산책", 37.5010, 126.9770, 40), ("Healthy Brunch Spot", "건강 브런치 맛집", 37.4979, 127.0276, 50)],
         [("bus", 10, 3.0), ("taxi", 10, 2.5)]),
        ("K-POP Dance & Studio Tour", "K-POP 댄스 & 스튜디오 투어", "half_day", "kpop_hallyu", "active", 210, 3.0, 5000, 4.7, 78,
         [("SM Entertainment Building", "SM엔터 사옥", 37.5134, 127.0585, 20), ("JYP Entertainment Area", "JYP엔터 일대", 37.5230, 127.0489, 20), ("K-POP Dance Studio Class", "K-POP 댄스 스튜디오 수업", 37.4979, 127.0276, 90), ("K-Star Road Photo Stop", "K스타 거리 포토", 37.5111, 127.0596, 30)],
         [("taxi", 8, 1.5), ("subway", 10, 2.5), ("subway", 8, 1.5)]),
        ("Mountain Hiking from Gangnam", "강남에서 떠나는 등산", "full_day", "nature_healing", "active", 420, 12.0, 4000, 4.6, 35,
         [("Gangnam Station", "강남역", 37.4979, 127.0276, 10), ("Umyeonsan Trailhead", "우면산 등산로 입구", 37.4680, 127.0080, 180), ("Gwanaksan Mountain", "관악산", 37.4430, 126.9630, 150)],
         [("bus", 15, 3.0), ("bus", 25, 6.0)]),
        ("Seoul Art Gallery Tour", "서울 아트 갤러리 투어", "full_day", "history_culture", "easy", 360, 8.0, 7000, 4.4, 31,
         [("Kukje Gallery", "국제갤러리", 37.5796, 126.9770, 40), ("Leeum Museum of Art", "리움미술관", 37.5384, 126.9978, 60), ("Hakgojae Gallery", "학고재갤러리", 37.5826, 126.9831, 40), ("Seoul Arts Center Hangaram", "예술의전당 한가람", 37.4784, 127.0117, 60)],
         [("taxi", 10, 3.0), ("taxi", 10, 4.0), ("subway", 25, 8.0)]),
    ]

    for i, (name_en, name_ko, dur_type, theme, diff, total_min, total_km, cost, rating, reviews, spots_data, trans_data) in enumerate(course_defs):
        c = course(name_en, name_ko, f"Explore {name_en.lower()} around Seoul's Gangnam and Seocho areas.", f"{name_ko} 코스를 통해 서울 강남·서초 일대를 탐험하세요.",
            dur_type, theme, diff, total_min, total_km, cost, rating, reviews,
            {"zh_cn": name_en, "zh_tw": name_en, "ja": name_en, "es": name_en, "th": name_en, "vi": name_en, "fr": name_en})

        spot_ids = []
        for j, (sname_en, sname_ko, slat, slng, sstay) in enumerate(spots_data):
            sid = spot(c, j, sname_en, sname_ko, f"Visit {sname_en}.", f"{sname_ko}을(를) 방문합니다.", slat, slng, sstay)
            spot_ids.append(sid)

        for j, (mode, dur, dist) in enumerate(trans_data):
            if j < len(spot_ids) - 1:
                trans(c, spot_ids[j], spot_ids[j+1], mode, dur, dist)

    return courses, spots, transitions
