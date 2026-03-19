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
            "image_url": (['https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=600', 'https://images.unsplash.com/photo-1578637387939-43c525550085?w=600', 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=600', 'https://images.unsplash.com/photo-1538485399081-7191377e8241?w=600', 'https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=600', 'https://images.unsplash.com/photo-1556660738-94df5ce05ef4?w=600', 'https://images.unsplash.com/photo-1568454537842-d933259bb258?w=600', 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=600'])[order % 8],
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
            "image_url": (['https://images.unsplash.com/photo-1545569341-9eb8b30979d9?w=600', 'https://images.unsplash.com/photo-1578637387939-43c525550085?w=600', 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=600', 'https://images.unsplash.com/photo-1538485399081-7191377e8241?w=600', 'https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=600', 'https://images.unsplash.com/photo-1556660738-94df5ce05ef4?w=600', 'https://images.unsplash.com/photo-1568454537842-d933259bb258?w=600', 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=600'])[len(courses) % 8],
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
        # ═══════════════════════════════════════════════
        # ADDITIONAL 70 COURSES (31-100)
        # ═══════════════════════════════════════════════
        # ── History courses ──
        ("Five Grand Palaces Tour", "서울 5대 궁 투어", "full_day", "history", "moderate", 480, 12.0, 8000, 4.8, 142,
         [("Gyeongbokgung Palace", "경복궁", 37.5796, 126.9770, 90), ("Changdeokgung Palace", "창덕궁", 37.5794, 126.9910, 75), ("Changgyeonggung Palace", "창경궁", 37.5791, 126.9952, 60), ("Deoksugung Palace", "덕수궁", 37.5658, 126.9748, 50), ("Gyeonghuigung Palace", "경희궁", 37.5718, 126.9683, 40)],
         [("walk", 15, 1.2), ("walk", 5, 0.4), ("subway", 15, 3.0), ("walk", 10, 0.8)]),
        ("Jongno Traditional Culture Walk", "종로 전통 문화 산책", "half_day", "history", "easy", 210, 4.0, 3000, 4.6, 87,
         [("Gyeongbokgung Palace", "경복궁", 37.5796, 126.9770, 60), ("National Folk Museum", "국립민속박물관", 37.5816, 126.9788, 40), ("Insadong Art Street", "인사동 예술거리", 37.5732, 126.9870, 40), ("Jogyesa Temple", "조계사", 37.5726, 126.9840, 30)],
         [("walk", 5, 0.3), ("walk", 10, 0.8), ("walk", 5, 0.3)]),
        ("Joseon Royal Heritage Trail", "조선 왕실 유산 탐방", "full_day", "history", "moderate", 420, 10.0, 7000, 4.7, 76,
         [("Jongmyo Shrine", "종묘", 37.5735, 126.9940, 60), ("Changdeokgung Secret Garden", "창덕궁 후원", 37.5794, 126.9910, 90), ("Bukchon Hanok Village", "북촌한옥마을", 37.5826, 126.9831, 60), ("Unhyeongung Palace", "운현궁", 37.5738, 126.9868, 40)],
         [("walk", 10, 0.7), ("walk", 10, 0.8), ("walk", 8, 0.5)]),
        ("Seoul City Wall Hiking Trail", "서울 성곽길 등산", "full_day", "history", "active", 420, 18.6, 3000, 4.5, 65,
         [("Naksan Park Gate", "낙산공원 입구", 37.5810, 127.0080, 10), ("Hyehwa Gate", "혜화문", 37.5880, 127.0010, 30), ("Bugaksan Section", "북악산 구간", 37.5937, 126.9810, 120), ("Inwangsan Section", "인왕산 구간", 37.5818, 126.9578, 90)],
         [("walk", 20, 2.0), ("walk", 45, 4.0), ("walk", 40, 3.5)]),
        ("War Memorial & DMZ History", "전쟁기념관 & DMZ 역사", "full_day", "history", "easy", 480, 60.0, 25000, 4.6, 93,
         [("War Memorial of Korea", "전쟁기념관", 37.5344, 126.9772, 90), ("Imjingak Park", "임진각", 37.8890, 126.7410, 60), ("Dora Observatory", "도라전망대", 37.9030, 126.6780, 40), ("Third Tunnel", "제3땅굴", 37.9075, 126.6580, 50)],
         [("bus", 60, 50.0), ("bus", 15, 5.0), ("bus", 10, 3.0)]),

        # ── Nature courses ──
        ("Bukhansan National Park Hiking", "북한산 국립공원 등산", "full_day", "nature", "active", 420, 10.0, 4000, 4.7, 112,
         [("Bukhansan Entrance", "북한산 입구", 37.6580, 126.9880, 10), ("Baegundae Peak", "백운대", 37.6590, 126.9755, 180), ("Jeongreung Valley", "정릉계곡", 37.6200, 127.0050, 40)],
         [("walk", 120, 5.0), ("walk", 60, 4.0)]),
        ("Han River Park Cycling Route", "한강공원 자전거 코스", "half_day", "nature", "moderate", 180, 20.0, 5000, 4.5, 89,
         [("Yeouido Hangang Park", "여의도한강공원", 37.5256, 126.9241, 20), ("Banpo Hangang Park", "반포한강공원", 37.5080, 126.9950, 30), ("Jamwon Hangang Park", "잠원한강공원", 37.5180, 127.0130, 20), ("Ttukseom Hangang Park", "뚝섬한강공원", 37.5312, 127.0662, 30)],
         [("bicycle", 20, 6.0), ("bicycle", 15, 4.0), ("bicycle", 25, 8.0)]),
        ("Namsan Mountain Sunrise Walk", "남산 일출 산책", "half_day", "nature", "moderate", 180, 5.0, 2000, 4.6, 67,
         [("Namsan Cable Car Station", "남산 케이블카역", 37.5565, 126.9810, 10), ("Namsan Botanical Garden", "남산 식물원", 37.5520, 126.9850, 30), ("N Seoul Tower", "N서울타워", 37.5512, 126.9882, 60), ("Namsan Dulle-gil", "남산 둘레길", 37.5480, 126.9830, 45)],
         [("walk", 15, 1.0), ("walk", 10, 0.5), ("walk", 15, 1.2)]),
        ("Seoul Forest & Seongsu Eco Walk", "서울숲 & 성수 에코 워크", "half_day", "nature", "easy", 210, 5.0, 2000, 4.4, 54,
         [("Seoul Forest Main Gate", "서울숲 정문", 37.5445, 127.0375, 60), ("Insect Garden", "곤충원", 37.5430, 127.0360, 30), ("Hangang Wetland", "한강 습지원", 37.5410, 127.0340, 30), ("Seongsu-dong Café Street", "성수동 카페거리", 37.5442, 127.0400, 45)],
         [("walk", 5, 0.3), ("walk", 10, 0.5), ("walk", 10, 0.8)]),
        ("Achasan Sunrise & Seoul Forest", "아차산 일출 & 서울숲", "full_day", "nature", "moderate", 360, 12.0, 4000, 4.5, 43,
         [("Achasan Trailhead", "아차산 등산로 입구", 37.5720, 127.1030, 10), ("Achasan Peak", "아차산 정상", 37.5700, 127.0950, 120), ("Gwangnaru Hangang Park", "광나루 한강공원", 37.5450, 127.0800, 40), ("Seoul Forest", "서울숲", 37.5445, 127.0375, 60)],
         [("walk", 60, 3.0), ("bus", 15, 3.0), ("subway", 10, 3.0)]),

        # ── Night view courses ──
        ("Seoul Night Skyline Tour", "서울 야경 스카이라인 투어", "half_day", "nightview", "easy", 210, 12.0, 12000, 4.8, 134,
         [("N Seoul Tower Observatory", "N서울타워 전망대", 37.5512, 126.9882, 50), ("Lotte Tower Seoul Sky", "롯데타워 서울스카이", 37.5126, 127.1026, 50), ("Banpo Bridge Fountain", "반포대교 분수", 37.5070, 126.9960, 30), ("Hannam Bridge Night Walk", "한남대교 야간 산책", 37.5200, 127.0100, 30)],
         [("taxi", 15, 5.0), ("taxi", 15, 5.0), ("walk", 10, 0.8)]),
        ("Rooftop Bar Night Tour", "루프탑 바 나이트 투어", "half_day", "nightview", "easy", 180, 5.0, 15000, 4.3, 56,
         [("JW Marriott Rooftop", "JW 메리어트 루프탑", 37.5066, 127.0010, 50), ("Signiel Bar", "시그니엘 바", 37.5126, 127.1026, 50), ("La Muse Seongsu", "라뮤즈 성수", 37.5440, 127.0400, 50)],
         [("taxi", 10, 4.0), ("taxi", 15, 5.0)]),
        ("Cheonggyecheon Night Stream Walk", "청계천 야간 수변 산책", "half_day", "nightview", "easy", 150, 4.0, 2000, 4.4, 78,
         [("Cheonggyecheon Spring", "청계광장", 37.5696, 126.9780, 20), ("Cheonggyecheon Stream Walk", "청계천 산책로", 37.5680, 126.9850, 40), ("DDP Night View", "DDP 야경", 37.5672, 127.0094, 30), ("Euljiro Night Street", "을지로 야간 거리", 37.5660, 126.9920, 30)],
         [("walk", 10, 1.0), ("walk", 10, 1.0), ("walk", 5, 0.5)]),

        # ── Shopping courses ──
        ("Myeongdong & Namdaemun Shopping Blitz", "명동 & 남대문 쇼핑 블리츠", "half_day", "shopping", "easy", 240, 3.0, 4000, 4.3, 112,
         [("Myeongdong Shopping Street", "명동 쇼핑거리", 37.5636, 126.9862, 90), ("Namdaemun Market", "남대문시장", 37.5597, 126.9768, 60), ("Shinsegae Department Store", "신세계 백화점", 37.5610, 126.9803, 40)],
         [("walk", 10, 0.8), ("walk", 5, 0.3)]),
        ("Hongdae & Yeonnam Shopping Walk", "홍대 & 연남 쇼핑 워크", "half_day", "shopping", "easy", 210, 3.5, 3000, 4.4, 87,
         [("Hongdae Shopping Street", "홍대 쇼핑거리", 37.5563, 126.9233, 60), ("Yeonnam-dong Vintage Shops", "연남동 빈티지 숍", 37.5608, 126.9248, 45), ("Gyeongui Line Forest Park", "경의선 숲길", 37.5594, 126.9218, 30), ("Mangwon Market", "망원시장", 37.5563, 126.9080, 40)],
         [("walk", 10, 0.8), ("walk", 5, 0.5), ("walk", 10, 1.0)]),
        ("Dongdaemun Fashion Tour", "동대문 패션 투어", "half_day", "shopping", "easy", 210, 2.5, 3000, 4.2, 98,
         [("Dongdaemun Design Plaza", "동대문디자인플라자", 37.5672, 127.0094, 30), ("Dongdaemun Night Market", "동대문 야시장", 37.5710, 127.0130, 60), ("Doota Mall", "두타몰", 37.5695, 127.0095, 60), ("Gwangjang Market", "광장시장", 37.5700, 127.0100, 40)],
         [("walk", 5, 0.3), ("walk", 5, 0.3), ("walk", 5, 0.4)]),
        ("Seongsu-dong Trendy Shopping", "성수동 트렌디 쇼핑", "half_day", "shopping", "easy", 180, 3.0, 3000, 4.5, 67,
         [("LCDC Seoul", "LCDC 서울", 37.5445, 127.0375, 30), ("Seongsu Shoe Street", "성수 수제화 거리", 37.5420, 127.0550, 40), ("POINT OF VIEW", "포인트오브뷰", 37.5440, 127.0400, 30), ("Onion Seongsu", "어니언 성수", 37.5447, 127.0565, 40)],
         [("walk", 10, 0.8), ("walk", 5, 0.5), ("walk", 5, 0.4)]),

        # ── Food courses ──
        ("Jongno Traditional Food Trail", "종로 전통 맛집 탐방", "half_day", "food", "easy", 210, 3.5, 4000, 4.7, 134,
         [("Gwangjang Market", "광장시장", 37.5700, 127.0100, 50), ("Jongno Bindaetteok Alley", "종로 빈대떡 골목", 37.5704, 126.9920, 40), ("Insadong Traditional Tea", "인사동 전통 찻집", 37.5732, 126.9870, 40), ("Tongin Market Dosirak", "통인시장 도시락", 37.5761, 126.9700, 40)],
         [("walk", 10, 0.8), ("walk", 10, 0.8), ("walk", 10, 0.8)]),
        ("Itaewon World Food Tour", "이태원 세계 음식 투어", "half_day", "food", "easy", 210, 3.0, 5000, 4.4, 87,
         [("Itaewon Main Street", "이태원 메인거리", 37.5340, 126.9930, 30), ("Halal Food Street", "할랄 음식 거리", 37.5322, 126.9895, 40), ("Haebangchon", "해방촌", 37.5405, 126.9880, 45), ("Gyeongnidan-gil", "경리단길", 37.5380, 126.9900, 45)],
         [("walk", 5, 0.4), ("walk", 10, 0.6), ("walk", 5, 0.5)]),
        ("Seoul BBQ & Soju Trail", "서울 BBQ & 소주 탐방", "half_day", "food", "easy", 180, 4.0, 6000, 4.6, 98,
         [("Mapo Galmaegi-sal Alley", "마포 갈매기살 골목", 37.5398, 126.9462, 50), ("Yeongdeungpo Gopchang Street", "영등포 곱창 거리", 37.5152, 126.9065, 40), ("Noryangjin Fish Market", "노량진수산시장", 37.5133, 126.9408, 50)],
         [("subway", 15, 4.0), ("subway", 10, 2.5)]),
        ("Hongdae Café & Dessert Crawl", "홍대 카페 & 디저트 크롤", "half_day", "food", "easy", 180, 2.5, 3000, 4.3, 76,
         [("Zapangi Café", "자판기 카페", 37.5500, 126.9170, 30), ("Cafe Onion Anguk", "어니언 안국점", 37.5805, 126.9855, 40), ("Gentle Monster Haus Dosan", "젠틀몬스터 하우스 도산", 37.5230, 127.0395, 40), ("Nudake Dosan", "누데이크 도산", 37.5230, 127.0395, 30)],
         [("subway", 20, 5.0), ("subway", 15, 4.0), ("walk", 3, 0.2)]),

        # ── K-Pop/Hallyu courses ──
        ("K-Pop Agency Tour", "K-POP 기획사 투어", "half_day", "kpop", "easy", 240, 6.0, 5000, 4.7, 156,
         [("HYBE Insight", "하이브 인사이트", 37.5275, 127.0050, 60), ("SM Entertainment", "SM엔터테인먼트", 37.5134, 127.0585, 30), ("JYP Entertainment", "JYP엔터테인먼트", 37.5230, 127.0489, 20), ("K-Star Road", "K스타의 거리", 37.5111, 127.0596, 30)],
         [("subway", 15, 4.0), ("taxi", 10, 2.0), ("walk", 10, 0.8)]),
        ("Hallyu Drama Pilgrimage", "한류 드라마 성지순례", "full_day", "kpop", "easy", 420, 15.0, 10000, 4.5, 112,
         [("COEX Starfield Library", "별마당도서관", 37.5126, 127.0590, 30), ("Namsan Tower Love Locks", "남산타워 사랑의 자물쇠", 37.5512, 126.9882, 45), ("Ikseon-dong Hanok Street", "익선동 한옥거리", 37.5740, 126.9890, 40), ("Gyeongbokgung Night", "경복궁 야간", 37.5796, 126.9770, 60)],
         [("subway", 20, 5.0), ("taxi", 15, 4.0), ("walk", 10, 0.8)]),
        ("K-Pop Dance & Fan Culture", "K-POP 댄스 & 팬문화", "half_day", "kpop", "active", 210, 3.0, 6000, 4.6, 98,
         [("K-Pop Dance Academy", "K-POP 댄스 아카데미", 37.5563, 126.9233, 90), ("Hongdae Busking Street", "홍대 버스킹거리", 37.5555, 126.9235, 30), ("K-Star Merchandise Shop", "K스타 굿즈샵", 37.5111, 127.0596, 40)],
         [("walk", 10, 0.5), ("subway", 15, 4.0)]),

        # ── Tradition courses ──
        ("Hanbok & Palace Photo Experience", "한복 & 궁궐 포토 체험", "half_day", "tradition", "easy", 240, 3.0, 5000, 4.8, 167,
         [("Hanbok Rental Shop", "한복 대여점", 37.5790, 126.9750, 30), ("Gyeongbokgung Palace", "경복궁", 37.5796, 126.9770, 90), ("Bukchon Hanok Village", "북촌한옥마을", 37.5826, 126.9831, 50), ("Samcheong-dong Street", "삼청동 거리", 37.5833, 126.9819, 30)],
         [("walk", 5, 0.3), ("walk", 10, 0.7), ("walk", 5, 0.4)]),
        ("Korean Tea Ceremony & Craft Workshop", "한국 다도 & 공예 워크숍", "half_day", "tradition", "easy", 210, 2.5, 4000, 4.6, 56,
         [("Insadong Tea House", "인사동 찻집", 37.5732, 126.9870, 50), ("Korean Craft Workshop", "한국 공예 워크숍", 37.5740, 126.9860, 60), ("Ssamziegil Market", "쌈지길", 37.5733, 126.9868, 30), ("Jogyesa Temple", "조계사", 37.5726, 126.9840, 30)],
         [("walk", 3, 0.2), ("walk", 3, 0.2), ("walk", 5, 0.3)]),
        ("Bukchon & Ikseon Hanok Experience", "북촌 & 익선 한옥 체험", "half_day", "tradition", "easy", 210, 3.5, 3000, 4.5, 87,
         [("Bukchon Hanok Village", "북촌한옥마을", 37.5826, 126.9831, 60), ("Bukchon 8 Scenic Views", "북촌 8경", 37.5820, 126.9840, 30), ("Ikseon-dong Hanok Street", "익선동 한옥거리", 37.5740, 126.9890, 45), ("Tapgol Park", "탑골공원", 37.5715, 126.9885, 20)],
         [("walk", 10, 0.7), ("walk", 10, 0.8), ("walk", 5, 0.5)]),

        # ── Art courses ──
        ("Seoul Museum Masterpiece Tour", "서울 뮤지엄 명작 투어", "full_day", "art", "easy", 420, 10.0, 7000, 4.5, 65,
         [("National Museum of Korea", "국립중앙박물관", 37.5239, 126.9803, 120), ("Leeum Museum", "리움미술관", 37.5384, 126.9978, 60), ("National Museum of Modern Art", "국립현대미술관 서울관", 37.5795, 126.9791, 60), ("Arario Museum", "아라리오뮤지엄", 37.5732, 126.9870, 40)],
         [("subway", 10, 3.0), ("taxi", 10, 3.0), ("subway", 15, 4.0)]),
        ("Seongsu Art & Design District Walk", "성수 아트 & 디자인 지구 워크", "half_day", "art", "easy", 180, 3.0, 2000, 4.4, 54,
         [("Daelim Changgo Gallery", "대림창고 갤러리", 37.5418, 127.0565, 30), ("POINT OF VIEW Gallery", "포인트오브뷰 갤러리", 37.5440, 127.0400, 30), ("Under Stand Avenue", "언더스탠드에비뉴", 37.5437, 127.0437, 40), ("Seoul Forest Art Space", "서울숲 아트 스페이스", 37.5445, 127.0375, 40)],
         [("walk", 10, 0.8), ("walk", 5, 0.4), ("walk", 5, 0.5)]),
        ("Seoul Mural Village & Street Art Tour", "서울 벽화마을 & 스트리트 아트 투어", "half_day", "art", "moderate", 210, 4.0, 3000, 4.3, 43,
         [("Ihwa Mural Village", "이화벽화마을", 37.5810, 127.0050, 40), ("Daehangno Art Street", "대학로 아트거리", 37.5822, 127.0010, 30), ("Mullae Art Village", "문래예술촌", 37.5137, 126.8945, 40), ("Seongsu Art Warehouses", "성수 아트 창고", 37.5420, 127.0550, 30)],
         [("walk", 10, 0.5), ("subway", 20, 5.0), ("subway", 15, 4.0)]),

        # ── Two-day courses ──
        ("Seoul Heritage & Modern Two-Day Tour", "서울 유산 & 현대 2일 투어", "two_day", "history", "moderate", 960, 25.0, 15000, 4.7, 54,
         [("Gyeongbokgung Palace", "경복궁", 37.5796, 126.9770, 90), ("Bukchon Hanok Village", "북촌한옥마을", 37.5826, 126.9831, 60), ("Insadong", "인사동", 37.5732, 126.9870, 50), ("Myeongdong", "명동", 37.5636, 126.9862, 60), ("COEX Mall", "코엑스몰", 37.5126, 127.0590, 50), ("Gangnam Shopping", "강남 쇼핑", 37.4979, 127.0276, 60)],
         [("walk", 15, 1.0), ("walk", 10, 0.7), ("subway", 15, 3.0), ("subway", 20, 5.0), ("subway", 8, 1.5)]),
        ("Nature & Temple Two-Day Retreat", "자연 & 사찰 2일 리트릿", "two_day", "nature", "moderate", 960, 30.0, 12000, 4.6, 38,
         [("Bukhansan National Park", "북한산 국립공원", 37.6580, 126.9880, 240), ("Geumsunsa Temple", "금선사", 37.6200, 126.9700, 60), ("Cheonggyecheon Walk", "청계천 산책", 37.5696, 126.9780, 40), ("Bongeunsa Temple Stay", "봉은사 템플스테이", 37.5153, 127.0575, 480)],
         [("bus", 15, 3.0), ("subway", 25, 8.0), ("subway", 20, 5.0)]),
        ("K-Culture Immersion Two-Day Tour", "K-컬처 몰입 2일 투어", "two_day", "kpop", "easy", 960, 20.0, 18000, 4.7, 87,
         [("HYBE Insight", "하이브 인사이트", 37.5275, 127.0050, 60), ("K-Pop Dance Class", "K-POP 댄스 수업", 37.5563, 126.9233, 90), ("Hongdae Night Out", "홍대 나이트", 37.5555, 126.9235, 120), ("COEX K-Star Road", "코엑스 K스타의 거리", 37.5111, 127.0596, 30), ("Gangnam K-Beauty Shopping", "강남 K-뷰티 쇼핑", 37.4979, 127.0276, 60), ("Seoul Arts Center Performance", "예술의전당 공연", 37.4784, 127.0117, 120)],
         [("subway", 15, 4.0), ("walk", 10, 0.5), ("subway", 20, 5.0), ("walk", 10, 0.8), ("bus", 15, 3.0)]),

        # ── Three-day courses ──
        ("Seoul Complete Three-Day Tour", "서울 완벽 3일 투어", "three_day", "history", "moderate", 1440, 40.0, 25000, 4.8, 112,
         [("Gyeongbokgung & Bukchon", "경복궁 & 북촌", 37.5796, 126.9770, 180), ("Insadong & Jongno", "인사동 & 종로", 37.5732, 126.9870, 120), ("Namsan Tower", "남산타워", 37.5512, 126.9882, 60), ("Gangnam & COEX", "강남 & 코엑스", 37.5126, 127.0590, 120), ("Hongdae & Yeonnam", "홍대 & 연남", 37.5563, 126.9233, 120), ("Itaewon World Food", "이태원 세계 음식", 37.5340, 126.9930, 90)],
         [("walk", 15, 1.0), ("bus", 15, 3.0), ("subway", 20, 5.0), ("subway", 25, 8.0), ("subway", 15, 3.0)]),
        ("Three-Day K-Culture & Shopping", "3일 K-컬처 & 쇼핑", "three_day", "shopping", "easy", 1440, 35.0, 20000, 4.5, 67,
         [("Myeongdong Shopping", "명동 쇼핑", 37.5636, 126.9862, 120), ("K-Pop Agency Tour", "K-POP 기획사 투어", 37.5275, 127.0050, 90), ("Gangnam Luxury Shopping", "강남 럭셔리 쇼핑", 37.5243, 127.0525, 120), ("Hongdae Vintage Markets", "홍대 빈티지 마켓", 37.5563, 126.9233, 90), ("Dongdaemun Night Shopping", "동대문 야간 쇼핑", 37.5672, 127.0094, 120), ("Duty Free & Departure", "면세점 & 출발", 37.4602, 126.4407, 60)],
         [("subway", 15, 3.0), ("subway", 15, 4.0), ("subway", 20, 5.0), ("subway", 15, 3.0), ("subway", 15, 3.0)]),

        # ── More diverse courses ──
        ("Yeouido & Mapo Half Day", "여의도 & 마포 반나절", "half_day", "food", "easy", 210, 5.0, 4000, 4.3, 56,
         [("Yeouido Park", "여의도공원", 37.5256, 126.9241, 30), ("63 Square", "63스퀘어", 37.5197, 126.9402, 40), ("Mapo Salt BBQ Alley", "마포 소금구이 골목", 37.5398, 126.9462, 50), ("Mangwon Market", "망원시장", 37.5563, 126.9080, 40)],
         [("walk", 10, 0.8), ("subway", 10, 3.0), ("bus", 10, 2.0)]),
        ("Yongsan Electronics & Culture", "용산 전자 & 문화", "half_day", "shopping", "easy", 210, 4.0, 3000, 4.1, 43,
         [("National Museum of Korea", "국립중앙박물관", 37.5239, 126.9803, 60), ("War Memorial", "전쟁기념관", 37.5344, 126.9772, 40), ("Yongsan Electronics Market", "용산전자상가", 37.5295, 126.9651, 40), ("Itaewon Craft Beer", "이태원 크래프트 맥주", 37.5340, 126.9930, 30)],
         [("walk", 10, 0.8), ("walk", 10, 0.8), ("walk", 10, 1.0)]),
        ("Songpa Lake & Lotte World Tour", "송파호수 & 롯데월드 투어", "full_day", "shopping", "easy", 420, 6.0, 8000, 4.4, 87,
         [("Seokchon Lake Park", "석촌호수공원", 37.5100, 127.0980, 40), ("Lotte World Tower Seoul Sky", "롯데월드타워 서울스카이", 37.5126, 127.1026, 60), ("Lotte World Adventure", "롯데월드 어드벤처", 37.5111, 127.0980, 180), ("Olympic Park Night Walk", "올림픽공원 야간 산책", 37.5202, 127.1215, 45)],
         [("walk", 5, 0.3), ("walk", 3, 0.2), ("bus", 10, 2.0)]),
        ("Euljiro & Jongno Retro Walk", "을지로 & 종로 레트로 워크", "half_day", "tradition", "easy", 180, 3.5, 3000, 4.4, 65,
         [("Euljiro Nogarijip Alley", "을지로 노가리 골목", 37.5660, 126.9925, 30), ("Sewoon Sangga", "세운상가", 37.5700, 126.9930, 30), ("Cheonggyecheon Walk", "청계천 산책", 37.5696, 126.9780, 30), ("Gwangjang Market", "광장시장", 37.5700, 127.0100, 50)],
         [("walk", 5, 0.3), ("walk", 5, 0.4), ("walk", 10, 0.8)]),
        ("Hangang SUP & Picnic", "한강 SUP & 피크닉", "half_day", "nature", "active", 180, 3.0, 5000, 4.5, 45,
         [("Ttukseom SUP Zone", "뚝섬 SUP 존", 37.5312, 127.0662, 60), ("Ttukseom Hangang Park", "뚝섬한강공원", 37.5312, 127.0662, 30), ("Seonyudo Park", "선유도공원", 37.5440, 126.9000, 40)],
         [("walk", 5, 0.2), ("subway", 20, 5.0)]),
        ("Jamsil Sports & Entertainment", "잠실 스포츠 & 엔터테인먼트", "half_day", "shopping", "easy", 210, 4.0, 5000, 4.3, 54,
         [("Jamsil Baseball Stadium", "잠실 야구장", 37.5152, 127.0720, 40), ("Lotte World Mall", "롯데월드몰", 37.5126, 127.1026, 60), ("Seokchon Lake Cherry Walk", "석촌호수 벚꽃길", 37.5100, 127.0980, 30), ("Songpa Naru Park", "송파나루공원", 37.5120, 127.1070, 30)],
         [("walk", 10, 0.8), ("walk", 5, 0.5), ("walk", 10, 0.8)]),
        ("Gwanghwamun & Sejong Heritage", "광화문 & 세종 유산", "half_day", "history", "easy", 210, 3.0, 2000, 4.6, 89,
         [("Gwanghwamun Square", "광화문광장", 37.5721, 126.9769, 30), ("Sejong Story Museum", "세종이야기", 37.5721, 126.9769, 40), ("National Palace Museum", "국립고궁박물관", 37.5760, 126.9741, 40), ("Cheongwadae (Former Blue House)", "청와대", 37.5866, 126.9748, 50)],
         [("walk", 2, 0.1), ("walk", 5, 0.3), ("walk", 15, 1.0)]),
        ("Seoul Craft Brewery Tour", "서울 크래프트 브루어리 투어", "half_day", "food", "easy", 180, 5.0, 8000, 4.3, 45,
         [("Amazing Brewing Co.", "어메이징 브루잉", 37.5445, 127.0375, 40), ("Magpie Brewing Itaewon", "맥파이 브루잉 이태원", 37.5340, 126.9930, 40), ("Seoul Brewery Gangnam", "서울 브루어리 강남", 37.4979, 127.0276, 40)],
         [("subway", 10, 3.0), ("subway", 15, 4.0)]),
        ("Olympic Park Art & Sports Walk", "올림픽공원 아트 & 스포츠 워크", "half_day", "art", "easy", 210, 5.0, 2000, 4.4, 56,
         [("Olympic Museum", "올림픽 박물관", 37.5202, 127.1215, 40), ("SOMA Museum of Art", "소마미술관", 37.5210, 127.1230, 40), ("Peace Gate", "평화의 문", 37.5220, 127.1250, 20), ("Mongchontoseong Fortress", "몽촌토성", 37.5190, 127.1200, 40)],
         [("walk", 5, 0.3), ("walk", 5, 0.3), ("walk", 10, 0.8)]),
        ("Gwanaksan Mountain Day Hike", "관악산 일일 등산", "full_day", "nature", "active", 360, 8.0, 3000, 4.5, 67,
         [("Gwanaksan Trailhead Sadang", "관악산 등산로 사당입구", 37.4830, 126.9630, 10), ("Yeonjuam Hermitage", "연주암", 37.4560, 126.9580, 30), ("Gwanaksan Peak", "관악산 정상", 37.4430, 126.9630, 120), ("Seoul National Univ Area", "서울대입구역 일대", 37.4812, 126.9527, 40)],
         [("walk", 60, 2.5), ("walk", 60, 2.5), ("bus", 20, 3.0)]),
        ("DDP & Dongdaemun Design Walk", "DDP & 동대문 디자인 워크", "half_day", "art", "easy", 180, 2.5, 2000, 4.3, 54,
         [("DDP Design Lab", "DDP 디자인랩", 37.5672, 127.0094, 40), ("DDP Design Market", "DDP 디자인 마켓", 37.5672, 127.0094, 30), ("Dongdaemun History & Culture Park", "동대문역사문화공원", 37.5670, 127.0090, 30), ("Cheonggyecheon Art Walk", "청계천 아트 워크", 37.5696, 126.9780, 30)],
         [("walk", 3, 0.1), ("walk", 5, 0.2), ("walk", 10, 0.8)]),
        ("Gangnam Hidden Gem Spots", "강남 숨은 명소", "half_day", "tradition", "easy", 180, 4.0, 3000, 4.2, 38,
         [("Dosan Park", "도산공원", 37.5224, 127.0379, 30), ("Garosu-gil Back Streets", "가로수길 뒷골목", 37.5199, 127.0231, 40), ("Samsung Museum Plateau", "삼성 뮤지엄 플라토", 37.5384, 126.9978, 30), ("Seolleung & Jeongneung Royal Tombs", "선릉·정릉", 37.5084, 127.0469, 40)],
         [("walk", 10, 0.8), ("taxi", 8, 2.0), ("walk", 10, 0.8)]),
        ("Mangwon & Hapjeong Local Tour", "망원 & 합정 로컬 투어", "half_day", "food", "easy", 180, 3.0, 3000, 4.4, 56,
         [("Mangwon Market", "망원시장", 37.5563, 126.9080, 40), ("Mangwon Hangang Park", "망원한강공원", 37.5520, 126.8960, 30), ("Hapjeong Café Street", "합정 카페거리", 37.5490, 126.9140, 40), ("Mecenatpolis Mall", "메세나폴리스", 37.5490, 126.9150, 30)],
         [("walk", 10, 0.8), ("walk", 10, 0.8), ("walk", 3, 0.2)]),
        ("Bukaksan Skyway Trail", "북악산 스카이웨이 트레일", "half_day", "nature", "active", 210, 6.0, 2000, 4.6, 43,
         [("Waryong Park Entrance", "와룡공원 입구", 37.5880, 126.9950, 10), ("Bukaksan Summit", "북악산 정상", 37.5937, 126.9810, 90), ("Changuimun Gate", "창의문", 37.5922, 126.9700, 20), ("Buam-dong Café Area", "부암동 카페 거리", 37.5910, 126.9690, 30)],
         [("walk", 40, 2.0), ("walk", 20, 1.5), ("walk", 10, 0.5)]),
        ("Korean Cooking Class & Market Tour", "한식 쿠킹 클래스 & 시장 투어", "half_day", "food", "easy", 210, 3.0, 5000, 4.7, 78,
         [("Tongin Market Shopping", "통인시장 장보기", 37.5761, 126.9700, 30), ("Korean Cooking Studio", "한식 쿠킹 스튜디오", 37.5730, 126.9750, 90), ("Samcheong-dong Tea Time", "삼청동 티타임", 37.5833, 126.9819, 30)],
         [("walk", 5, 0.3), ("walk", 10, 0.8)]),
        ("Naksan Park Sunrise & Daehangno", "낙산공원 일출 & 대학로", "half_day", "nature", "moderate", 180, 4.0, 2000, 4.4, 45,
         [("Naksan Park Sunrise", "낙산공원 일출", 37.5810, 127.0080, 40), ("Seoul City Wall Walk", "서울 성곽길", 37.5840, 127.0050, 40), ("Daehangno Theater Street", "대학로 극장거리", 37.5822, 127.0010, 30), ("Marronnier Park", "마로니에공원", 37.5815, 127.0020, 20)],
         [("walk", 15, 1.0), ("walk", 10, 0.8), ("walk", 3, 0.2)]),
        ("Seoul Sustainable & Eco Tour", "서울 친환경 에코 투어", "full_day", "nature", "easy", 360, 10.0, 5000, 4.3, 32,
         [("Seoul Upcycling Plaza", "서울새활용플라자", 37.5445, 127.0375, 40), ("Seoul Energy Dream Center", "서울에너지드림센터", 37.5681, 126.8976, 40), ("Noeul Park", "노을공원", 37.5700, 126.8800, 60), ("Seonyudo Park Eco Walk", "선유도공원 에코 산책", 37.5440, 126.9000, 60)],
         [("subway", 15, 4.0), ("bus", 10, 2.0), ("bus", 15, 3.0)]),
        ("Gaesong-style Temple Food Experience", "개성식 사찰음식 체험", "half_day", "tradition", "easy", 210, 3.0, 4000, 4.6, 34,
         [("Jogyesa Temple Visit", "조계사 방문", 37.5726, 126.9840, 30), ("Balwoo Gongyang Temple Food", "발우공양 사찰음식", 37.5726, 126.9840, 60), ("Anguk-dong Walk", "안국동 산책", 37.5790, 126.9850, 30), ("Unhyeongung Palace", "운현궁", 37.5738, 126.9868, 30)],
         [("walk", 2, 0.1), ("walk", 5, 0.3), ("walk", 5, 0.4)]),
        ("Seoul City Bus Night Tour", "서울 시티버스 야경 투어", "half_day", "nightview", "easy", 150, 15.0, 5000, 4.5, 89,
         [("Gwanghwamun Departure", "광화문 출발", 37.5721, 126.9769, 10), ("Namdaemun Night View", "남대문 야경", 37.5597, 126.9768, 15), ("Namsan Tower Night", "남산타워 야경", 37.5512, 126.9882, 30), ("Hangang Bridge Night Drive", "한강대교 야간 드라이브", 37.5100, 126.9500, 15)],
         [("bus", 10, 2.0), ("bus", 10, 2.0), ("bus", 15, 4.0)]),
        ("Seocho Healing & Wellness Walk", "서초 힐링 & 웰니스 워크", "half_day", "nature", "easy", 210, 4.0, 3000, 4.4, 42,
         [("Seoul Arts Center Garden", "예술의전당 정원", 37.4784, 127.0117, 30), ("Umyeonsan Eco Trail", "우면산 에코 트레일", 37.4680, 127.0080, 60), ("Seoripul Park Forest Bath", "서리풀공원 산림욕", 37.4922, 127.0098, 40), ("Seocho Herb Tea Café", "서초 허브차 카페", 37.4920, 127.0100, 30)],
         [("walk", 10, 1.0), ("walk", 15, 1.5), ("walk", 5, 0.3)]),
        ("Incheon Day Trip from Seoul", "인천 당일치기 여행", "full_day", "tradition", "easy", 480, 40.0, 10000, 4.3, 54,
         [("Seoul Station", "서울역", 37.5547, 126.9706, 10), ("Incheon Chinatown", "인천 차이나타운", 37.4749, 126.6176, 60), ("Wolmi Island", "월미도", 37.4710, 126.5940, 60), ("Songdo Central Park", "송도센트럴파크", 37.3792, 126.6600, 60)],
         [("subway", 50, 30.0), ("bus", 10, 3.0), ("bus", 20, 6.0)]),
        ("Jamsil & Songpa Night Market Tour", "잠실 & 송파 야시장 투어", "half_day", "food", "easy", 180, 3.0, 4000, 4.2, 45,
         [("Seokchon Lake Night Walk", "석촌호수 야간 산책", 37.5100, 127.0980, 30), ("Songpa Sundae Town", "송파 순대타운", 37.5115, 127.1095, 40), ("Bangi Food Alley", "방이 먹자골목", 37.5120, 127.1180, 40), ("Lotte Tower Night View", "롯데타워 야경", 37.5126, 127.1026, 30)],
         [("walk", 10, 0.8), ("walk", 10, 0.8), ("walk", 10, 0.7)]),
        ("Seodaemun Independence Trail", "서대문 독립 트레일", "half_day", "history", "moderate", 210, 4.0, 3000, 4.5, 43,
         [("Seodaemun Prison History Hall", "서대문형무소역사관", 37.5725, 126.9595, 60), ("Dongnimmun Gate", "독립문", 37.5724, 126.9580, 20), ("Inwangsan Shamanism Trail", "인왕산 무당길", 37.5818, 126.9578, 60), ("Sajik Park", "사직공원", 37.5759, 126.9660, 30)],
         [("walk", 3, 0.2), ("walk", 20, 1.5), ("walk", 10, 0.8)]),
        ("Hangang Night Cruise & Dinner", "한강 나이트 크루즈 & 디너", "half_day", "nightview", "easy", 180, 8.0, 15000, 4.6, 67,
         [("Yeouido E-Land Cruise", "여의도 이랜드크루즈", 37.5256, 126.9241, 10), ("Han River Cruise", "한강 유람선", 37.5200, 126.9600, 60), ("Banpo Bridge View Point", "반포대교 뷰포인트", 37.5070, 126.9960, 30), ("Banpo Night Walk", "반포 야간 산책", 37.5080, 126.9950, 30)],
         [("cruise", 60, 8.0), ("walk", 5, 0.3), ("walk", 5, 0.3)]),
        # ── Additional courses to reach 100 ──
        ("Yeongdeungpo Market & Night Food", "영등포 시장 & 야식", "half_day", "food", "easy", 180, 3.0, 4000, 4.2, 43,
         [("Yeongdeungpo Market", "영등포시장", 37.5152, 126.9065, 40), ("Yeongdeungpo Gopchang Street", "영등포 곱창거리", 37.5150, 126.9070, 40), ("Times Square Mall", "타임스퀘어", 37.5171, 126.9035, 30)],
         [("walk", 5, 0.3), ("walk", 5, 0.3)]),
        ("Gangdong Eco & Riverside Walk", "강동 에코 & 수변 산책", "half_day", "nature", "easy", 180, 5.0, 2000, 4.3, 32,
         [("Amsa-dong Prehistoric Settlement", "암사동 선사유적지", 37.5530, 127.1320, 40), ("Gwangnaru Hangang Park", "광나루 한강공원", 37.5450, 127.0800, 40), ("Cheonho Lake Park", "천호호수공원", 37.5460, 127.1280, 30)],
         [("bus", 10, 2.0), ("bus", 10, 2.0)]),
        ("Seoullyo 7017 & Namdaemun Walk", "서울로7017 & 남대문 산책", "half_day", "tradition", "easy", 180, 3.0, 2000, 4.4, 67,
         [("Seoullo 7017 Skygarden", "서울로7017 하늘정원", 37.5560, 126.9720, 40), ("Namdaemun Market", "남대문시장", 37.5597, 126.9768, 50), ("Sungnyemun Gate", "숭례문", 37.5597, 126.9753, 20), ("Deoksugung Stonewall Road", "덕수궁 돌담길", 37.5658, 126.9748, 30)],
         [("walk", 5, 0.3), ("walk", 3, 0.2), ("walk", 5, 0.4)]),
        ("Hannam-dong Art & Brunch", "한남동 아트 & 브런치", "half_day", "art", "easy", 180, 2.5, 4000, 4.5, 54,
         [("Blue Square", "블루스퀘어", 37.5365, 127.0000, 30), ("Leeum Museum of Art", "리움미술관", 37.5384, 126.9978, 50), ("Hannam Brunch Street", "한남 브런치 거리", 37.5370, 127.0010, 40), ("Anthracite Café", "앤트러사이트 카페", 37.5365, 127.0015, 20)],
         [("walk", 5, 0.3), ("walk", 5, 0.4), ("walk", 3, 0.2)]),
        ("K-Food Cooking & Market Full Day", "K-푸드 쿠킹 & 시장 풀데이", "full_day", "food", "easy", 420, 8.0, 8000, 4.7, 76,
         [("Gwangjang Market Ingredients", "광장시장 재료 구매", 37.5700, 127.0100, 40), ("Korean Cooking Academy", "한식 조리 아카데미", 37.5730, 126.9750, 120), ("Namdaemun Market Spices", "남대문시장 향신료", 37.5597, 126.9768, 40), ("Noryangjin Fish Market Dinner", "노량진 수산시장 저녁", 37.5133, 126.9408, 60)],
         [("taxi", 10, 2.0), ("subway", 10, 3.0), ("subway", 15, 4.0)]),
        ("Dongjak & Noryangjin Seafood Tour", "동작 & 노량진 해산물 투어", "half_day", "food", "easy", 180, 3.0, 5000, 4.3, 45,
         [("National Cemetery Park", "현충원 공원", 37.5010, 126.9770, 30), ("Noryangjin Fish Market", "노량진수산시장", 37.5133, 126.9408, 60), ("Nodeul Island Café", "노들섬 카페", 37.5180, 126.9570, 30)],
         [("bus", 10, 2.0), ("walk", 10, 1.0)]),
        ("Mapo Hipster & Local Tour", "마포 힙스터 & 로컬 투어", "half_day", "tradition", "easy", 180, 3.0, 3000, 4.4, 56,
         [("Yeonnam-dong Gyeongui Line Forest", "연남동 경의선숲길", 37.5608, 126.9248, 30), ("Yeonnam-dong Trendy Street", "연남동 트렌디 거리", 37.5610, 126.9250, 40), ("Hapjeong Café Alley", "합정 카페 골목", 37.5490, 126.9140, 30), ("Sangsu-dong Vintage Shops", "상수동 빈티지숍", 37.5480, 126.9200, 30)],
         [("walk", 5, 0.3), ("walk", 10, 0.8), ("walk", 5, 0.4)]),
        ("Gangseo Magok & Botanical Garden", "강서 마곡 & 식물원", "half_day", "nature", "easy", 210, 4.0, 2000, 4.3, 38,
         [("Seoul Botanic Park", "서울식물원", 37.5700, 126.8350, 60), ("Magok Naru Park", "마곡나루공원", 37.5680, 126.8280, 30), ("LG Science Park Walk", "LG사이언스파크 산책", 37.5680, 126.8330, 30), ("Gaehwasan Mountain Trail", "개화산 등산로", 37.5750, 126.8120, 40)],
         [("walk", 10, 0.8), ("walk", 5, 0.5), ("bus", 10, 2.0)]),
        ("Nowon & Dobongsan Mountain Trail", "노원 & 도봉산 등산", "full_day", "nature", "active", 360, 10.0, 3000, 4.6, 45,
         [("Dobongsan Station", "도봉산역", 37.6890, 127.0460, 10), ("Dobongsan Trailhead", "도봉산 등산로 입구", 37.6950, 127.0160, 10), ("Dobongsan Peak Jaunbong", "도봉산 자운봉", 37.6980, 127.0150, 180), ("Mangwolsa Temple", "망월사", 37.6920, 127.0130, 40)],
         [("walk", 10, 1.0), ("walk", 90, 3.0), ("walk", 30, 2.0)]),
        ("Gwacheon Art & Science Day", "과천 아트 & 사이언스 데이", "full_day", "art", "easy", 420, 8.0, 5000, 4.4, 34,
         [("National Museum of Modern Art Gwacheon", "국립현대미술관 과천관", 37.4285, 126.9887, 90), ("Seoul Grand Park", "서울대공원", 37.4270, 126.9945, 60), ("Seoul Land Theme Park", "서울랜드", 37.4330, 126.9900, 120), ("Gwacheon Science Museum", "국립과천과학관", 37.4350, 127.0010, 60)],
         [("walk", 10, 0.5), ("walk", 10, 0.5), ("bus", 10, 1.5)]),
        ("Seoul Fortress Complete Circumnavigation", "서울 성곽 완전 일주", "full_day", "history", "active", 480, 18.6, 3000, 4.7, 56,
         [("Heunginjimun Gate", "흥인지문", 37.5710, 127.0090, 10), ("Naksan Park Section", "낙산공원 구간", 37.5810, 127.0080, 60), ("Bugaksan Summit", "북악산 정상", 37.5937, 126.9810, 120), ("Inwangsan Section", "인왕산 구간", 37.5818, 126.9578, 90), ("Namsan Section", "남산 구간", 37.5512, 126.9882, 60)],
         [("walk", 30, 3.0), ("walk", 50, 4.0), ("walk", 40, 3.5), ("walk", 40, 4.0)]),
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
