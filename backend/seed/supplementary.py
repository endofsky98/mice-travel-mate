import uuid
from datetime import date

def _id():
    return str(uuid.uuid4())

# ═══════════════════════════════════════════════
# 1. ROLLING BANNERS (5)
# ═══════════════════════════════════════════════
def get_banners():
    return [
        {
            "id": _id(), "display_order": 0, "is_active": True, "event_id": None, "rolling_interval": 4,
            "image_url": "/images/placeholder/banner_1.jpg", "link_url": "/courses",
            "title_en": "Seoul After Dark", "title_ko": "어둠 속의 서울",
            "title_zh_cn": "首尔夜色", "title_zh_tw": "首爾夜色",
            "title_ja": "夜のソウル", "title_es": "Seúl de Noche",
            "title_th": "โซลยามค่ำคืน", "title_vi": "Seoul Về Đêm", "title_fr": "Séoul la Nuit",
            "subtitle_en": "Neon lights, rooftop bars & skyline views await you",
            "subtitle_ko": "네온 불빛, 루프탑 바, 스카이라인이 당신을 기다립니다",
            "subtitle_zh_cn": "霓虹灯、屋顶酒吧和天际线美景等着你",
            "subtitle_zh_tw": "霓虹燈、屋頂酒吧和天際線美景等著你",
            "subtitle_ja": "ネオンライト、ルーフトップバー、スカイラインがあなたを待っています",
            "subtitle_es": "Luces de neón, bares en azoteas y vistas del horizonte te esperan",
            "subtitle_th": "ไฟนีออน บาร์บนดาดฟ้า และวิวเส้นขอบฟ้ารอคุณอยู่",
            "subtitle_vi": "Đèn neon, quán bar trên sân thượng và tầm nhìn đường chân trời đang chờ bạn",
            "subtitle_fr": "Néons, bars sur les toits et vues sur la skyline vous attendent",
        },
        {
            "id": _id(), "display_order": 1, "is_active": True, "event_id": None, "rolling_interval": 4,
            "image_url": "/images/placeholder/banner_2.jpg", "link_url": "/restaurants",
            "title_en": "Taste the Real Korea", "title_ko": "진짜 한국을 맛보세요",
            "title_zh_cn": "品味真正的韩国", "title_zh_tw": "品味真正的韓國",
            "title_ja": "本物の韓国を味わう", "title_es": "Saborea la Verdadera Corea",
            "title_th": "ลิ้มรสเกาหลีแท้ๆ", "title_vi": "Nếm Thử Hàn Quốc Đích Thực", "title_fr": "Goûtez la Vraie Corée",
            "subtitle_en": "From sizzling BBQ to hidden street food gems",
            "subtitle_ko": "지글지글 BBQ에서 숨겨진 길거리 음식 보석까지",
            "subtitle_zh_cn": "从滋滋作响的烤肉到隐藏的街头美食",
            "subtitle_zh_tw": "從滋滋作響的烤肉到隱藏的街頭美食",
            "subtitle_ja": "ジュージュー焼けるBBQから隠れたストリートフードまで",
            "subtitle_es": "Desde BBQ chisporroteante hasta joyas ocultas de comida callejera",
            "subtitle_th": "จากบาร์บีคิวร้อนๆ ถึงอัญมณีอาหารริมทางที่ซ่อนอยู่",
            "subtitle_vi": "Từ BBQ xèo xèo đến những viên ngọc ẩm thực đường phố ẩn giấu",
            "subtitle_fr": "Du BBQ grésillant aux joyaux cachés de la street food",
        },
        {
            "id": _id(), "display_order": 2, "is_active": True, "event_id": None, "rolling_interval": 4,
            "image_url": "/images/placeholder/banner_3.jpg", "link_url": "/courses",
            "title_en": "Temples & Traditions", "title_ko": "사찰과 전통",
            "title_zh_cn": "寺庙与传统", "title_zh_tw": "寺廟與傳統",
            "title_ja": "寺院と伝統", "title_es": "Templos y Tradiciones",
            "title_th": "วัดและประเพณี", "title_vi": "Chùa Chiền & Truyền Thống", "title_fr": "Temples et Traditions",
            "subtitle_en": "Ancient beauty meets modern wonder",
            "subtitle_ko": "고대의 아름다움이 현대의 경이로움을 만나다",
            "subtitle_zh_cn": "古老之美遇见现代奇迹", "subtitle_zh_tw": "古老之美遇見現代奇蹟",
            "subtitle_ja": "古の美しさが現代の驚異と出会う",
            "subtitle_es": "La belleza antigua se encuentra con la maravilla moderna",
            "subtitle_th": "ความงามโบราณพบกับความมหัศจรรย์ยุคใหม่",
            "subtitle_vi": "Vẻ đẹp cổ xưa gặp gỡ kỳ quan hiện đại",
            "subtitle_fr": "La beauté ancienne rencontre la merveille moderne",
        },
        {
            "id": _id(), "display_order": 3, "is_active": True, "event_id": None, "rolling_interval": 4,
            "image_url": "/images/placeholder/banner_4.jpg", "link_url": "/products",
            "title_en": "K-Culture is Calling", "title_ko": "K-컬처가 부른다",
            "title_zh_cn": "K文化在召唤", "title_zh_tw": "K文化在召喚",
            "title_ja": "Kカルチャーが呼んでいる", "title_es": "La K-Cultura te Llama",
            "title_th": "K-Culture กำลังเรียก", "title_vi": "Văn Hóa K Đang Gọi", "title_fr": "La K-Culture vous Appelle",
            "subtitle_en": "K-Pop, K-Beauty, K-Food — experience it all",
            "subtitle_ko": "K-POP, K-뷰티, K-푸드 — 모두 경험하세요",
            "subtitle_zh_cn": "K-Pop、K-Beauty、K-Food——全部体验",
            "subtitle_zh_tw": "K-Pop、K-Beauty、K-Food——全部體驗",
            "subtitle_ja": "K-Pop、Kビューティー、Kフード — すべてを体験",
            "subtitle_es": "K-Pop, K-Beauty, K-Food — experiméntalo todo",
            "subtitle_th": "K-Pop, K-Beauty, K-Food — สัมผัสทุกอย่าง",
            "subtitle_vi": "K-Pop, K-Beauty, K-Food — trải nghiệm tất cả",
            "subtitle_fr": "K-Pop, K-Beauty, K-Food — vivez tout cela",
        },
        {
            "id": _id(), "display_order": 4, "is_active": True, "event_id": None, "rolling_interval": 4,
            "image_url": "/images/placeholder/banner_5.jpg", "link_url": "/themes",
            "title_en": "Nature Escapes Near the City", "title_ko": "도시 근처 자연 탈출",
            "title_zh_cn": "城市附近的自然逃逸", "title_zh_tw": "城市附近的自然逃逸",
            "title_ja": "都会の近くの自然の逃避", "title_es": "Escapadas Naturales Cerca de la Ciudad",
            "title_th": "หนีสู่ธรรมชาติใกล้เมือง", "title_vi": "Thoát Vào Thiên Nhiên Gần Thành Phố", "title_fr": "Évasions Nature Près de la Ville",
            "subtitle_en": "Mountains, rivers & coastal trails just minutes away",
            "subtitle_ko": "산, 강, 해안 산책로가 불과 몇 분 거리에",
            "subtitle_zh_cn": "山脉、河流和海岸步道就在几分钟之外",
            "subtitle_zh_tw": "山脈、河流和海岸步道就在幾分鐘之外",
            "subtitle_ja": "山、川、海岸のトレイルがすぐそこに",
            "subtitle_es": "Montañas, ríos y senderos costeros a solo minutos",
            "subtitle_th": "ภูเขา แม่น้ำ และเส้นทางชายฝั่งอยู่ห่างเพียงไม่กี่นาที",
            "subtitle_vi": "Núi, sông và đường mòn ven biển chỉ cách vài phút",
            "subtitle_fr": "Montagnes, rivières et sentiers côtiers à quelques minutes",
        },
    ]


# ═══════════════════════════════════════════════
# 2. EVENTS (3 exhibitions)
# ═══════════════════════════════════════════════
def get_events():
    return [
        {
            "id": _id(), "slug": "coex-mice-expo-2026",
            "name_en": "COEX MICE Expo 2026", "name_ko": "코엑스 MICE 엑스포 2026",
            "name_zh_cn": "COEX MICE博览会2026", "name_zh_tw": "COEX MICE博覽會2026",
            "name_ja": "COEX MICEエキスポ2026", "name_es": "COEX MICE Expo 2026",
            "name_th": "COEX MICE Expo 2026", "name_vi": "COEX MICE Expo 2026", "name_fr": "COEX MICE Expo 2026",
            "description_en": "Asia's largest MICE industry exhibition at COEX Convention Center.",
            "description_ko": "코엑스 컨벤션센터에서 열리는 아시아 최대 MICE 산업 전시회.",
            "description_zh_cn": "在COEX会议中心举办的亚洲最大MICE行业展览。",
            "description_zh_tw": "在COEX會議中心舉辦的亞洲最大MICE行業展覽。",
            "description_ja": "COEXコンベンションセンターで開催されるアジア最大のMICE産業展示会。",
            "description_es": "La mayor exposición de la industria MICE de Asia en el Centro de Convenciones COEX.",
            "description_th": "นิทรรศการอุตสาหกรรม MICE ที่ใหญ่ที่สุดในเอเชียที่ศูนย์ประชุม COEX",
            "description_vi": "Triển lãm ngành MICE lớn nhất châu Á tại Trung tâm Hội nghị COEX.",
            "description_fr": "La plus grande exposition de l'industrie MICE d'Asie au Centre de Conventions COEX.",
            "venue_name": "COEX Convention Center", "venue_address": "513 Yeongdong-daero, Gangnam-gu, Seoul",
            "latitude": 37.5126, "longitude": 127.0590,
            "start_date": date(2026, 4, 15), "end_date": date(2026, 4, 18),
            "banner_image_url": "/images/placeholder/event_coex.jpg", "is_active": True,
        },
        {
            "id": _id(), "slug": "bexco-tech-summit-2026",
            "name_en": "BEXCO Tech Summit 2026", "name_ko": "벡스코 테크 서밋 2026",
            "name_zh_cn": "BEXCO科技峰会2026", "name_zh_tw": "BEXCO科技峰會2026",
            "name_ja": "BEXCOテックサミット2026", "name_es": "BEXCO Tech Summit 2026",
            "name_th": "BEXCO Tech Summit 2026", "name_vi": "BEXCO Tech Summit 2026", "name_fr": "BEXCO Tech Summit 2026",
            "description_en": "International technology summit at BEXCO in Busan.",
            "description_ko": "부산 벡스코에서 열리는 국제 기술 서밋.",
            "description_zh_cn": "在釜山BEXCO举办的国际技术峰会。", "description_zh_tw": "在釜山BEXCO舉辦的國際技術峰會。",
            "description_ja": "釜山BEXCOで開催される国際テクノロジーサミット。", "description_es": "Cumbre tecnológica internacional en BEXCO, Busan.",
            "description_th": "การประชุมสุดยอดเทคโนโลยีระหว่างประเทศที่ BEXCO ปูซาน", "description_vi": "Hội nghị thượng đỉnh công nghệ quốc tế tại BEXCO, Busan.",
            "description_fr": "Sommet technologique international au BEXCO à Busan.",
            "venue_name": "BEXCO", "venue_address": "55 APEC-ro, Haeundae-gu, Busan",
            "latitude": 35.1695, "longitude": 129.1362,
            "start_date": date(2026, 5, 20), "end_date": date(2026, 5, 23),
            "banner_image_url": "/images/placeholder/event_bexco.jpg", "is_active": True,
        },
        {
            "id": _id(), "slug": "kintex-global-fair-2026",
            "name_en": "KINTEX Global Fair 2026", "name_ko": "킨텍스 글로벌 페어 2026",
            "name_zh_cn": "KINTEX全球博览会2026", "name_zh_tw": "KINTEX全球博覽會2026",
            "name_ja": "KINTEXグローバルフェア2026", "name_es": "KINTEX Global Fair 2026",
            "name_th": "KINTEX Global Fair 2026", "name_vi": "KINTEX Global Fair 2026", "name_fr": "KINTEX Global Fair 2026",
            "description_en": "International business fair at KINTEX in Goyang, Gyeonggi-do.",
            "description_ko": "경기도 고양 킨텍스에서 열리는 국제 비즈니스 페어.",
            "description_zh_cn": "在京畿道高阳KINTEX举办的国际商业博览会。", "description_zh_tw": "在京畿道高陽KINTEX舉辦的國際商業博覽會。",
            "description_ja": "京畿道高陽のKINTEXで開催される国際ビジネスフェア。", "description_es": "Feria de negocios internacional en KINTEX, Goyang.",
            "description_th": "งานแสดงธุรกิจระหว่างประเทศที่ KINTEX โกยาง", "description_vi": "Hội chợ kinh doanh quốc tế tại KINTEX, Goyang.",
            "description_fr": "Foire commerciale internationale au KINTEX à Goyang.",
            "venue_name": "KINTEX", "venue_address": "217-60 Kintex-ro, Ilsanseo-gu, Goyang-si, Gyeonggi-do",
            "latitude": 37.6695, "longitude": 126.7463,
            "start_date": date(2026, 6, 10), "end_date": date(2026, 6, 13),
            "banner_image_url": "/images/placeholder/event_kintex.jpg", "is_active": True,
        },
    ]


# ═══════════════════════════════════════════════
# 3. FESTIVALS (12)
# ═══════════════════════════════════════════════
def get_festivals():
    fests = [
        ("Seoul Lantern Festival", "서울 빛초롱 축제", "A magical display of traditional and modern lanterns along Cheonggyecheon Stream.", "청계천을 따라 전통·현대 등이 어우러진 환상적인 축제.", "festival", "Cheonggyecheon Stream", "서울 종로구 청계천로", 37.5696, 126.9780, "2026-03-20", "2026-04-05", "https://www.seoullantern.com"),
        ("Jinhae Cherry Blossom Festival", "진해 벚꽃축제", "Korea's largest cherry blossom festival with stunning pink canopies.", "분홍빛 꽃터널이 장관인 한국 최대 벚꽃축제.", "festival", "Jinhae", "경남 창원시 진해구", 35.1349, 128.7152, "2026-03-25", "2026-04-04", "https://www.changwon.go.kr"),
        ("Seoul Jazz Festival", "서울 재즈 페스티벌", "International jazz performances at Olympic Park.", "올림픽공원에서 열리는 국제 재즈 공연.", "performance", "Olympic Park", "서울 송파구 올림픽로 424", 37.5202, 127.1215, "2026-05-22", "2026-05-24", "https://www.seouljazz.co.kr"),
        ("COEX Food Week", "코엑스 푸드위크", "Korea's largest food industry exhibition and tasting event.", "한국 최대 식품산업 전시회 및 시식 행사.", "exhibition", "COEX", "서울 강남구 영동대로 513", 37.5126, 127.0590, "2026-04-08", "2026-04-11", "https://www.coexfoodweek.com"),
        ("Seoul Fashion Week", "서울패션위크", "Asia's premier fashion event featuring Korean and international designers.", "한국·해외 디자이너가 참가하는 아시아 최고 패션 이벤트.", "exhibition", "DDP (Dongdaemun Design Plaza)", "서울 중구 을지로 281", 37.5672, 127.0094, "2026-03-18", "2026-03-23", "https://www.seoulfashionweek.org"),
        ("Seoul International Book Fair", "서울국제도서전", "The largest book fair in Korea with international publishers.", "해외 출판사가 참여하는 한국 최대 도서전.", "exhibition", "COEX", "서울 강남구 영동대로 513", 37.5126, 127.0590, "2026-06-17", "2026-06-21", "https://www.sibf.or.kr"),
        ("Gangnam Festival", "강남 페스티벌", "Annual cultural festival celebrating Gangnam with performances and food.", "공연과 음식으로 강남을 축하하는 연례 문화 축제.", "festival", "Yeongdong-daero", "서울 강남구 영동대로", 37.5088, 127.0612, "2026-10-01", "2026-10-05", "https://www.gangnamfestival.com"),
        ("Seoul Drum Festival", "서울 드럼 페스티벌", "A festival celebrating percussion and rhythms from around the world.", "전 세계의 타악기와 리듬을 축하하는 축제.", "performance", "Seoul Plaza", "서울 중구 세종대로 110", 37.5662, 126.9779, "2026-05-08", "2026-05-10", "https://www.seouldrum.go.kr"),
        ("Seoul Street Art Festival", "서울 거리예술축전", "Street performances, music, and art throughout the city.", "도시 곳곳의 거리 공연, 음악, 예술.", "festival", "Various Locations in Seoul", "서울 마포구 홍익로 일대", 37.5563, 126.9233, "2026-05-01", "2026-05-05", "https://www.ssaf.or.kr"),
        ("Bukchon Hanok Village Cultural Event", "북촌한옥마을 문화행사", "Traditional cultural experiences in the historic Bukchon area.", "역사적인 북촌 지역에서 전통 문화를 체험.", "festival", "Bukchon Hanok Village", "서울 종로구 북촌로", 37.5826, 126.9831, "2026-04-25", "2026-04-27", "https://www.bukchon.seoul.go.kr"),
        ("Yeouido Spring Flower Festival", "여의도 봄꽃축제", "Beautiful cherry blossoms along the Yeouido riverside.", "여의도 강변의 아름다운 벚꽃 축제.", "festival", "Yeouido", "서울 영등포구 여의도동", 37.5256, 126.9241, "2026-04-01", "2026-04-13", "https://www.ydp.go.kr"),
        ("Seoul Coffee Festival", "서울 커피 페스티벌", "Korea's largest coffee festival with tastings from top roasters.", "최고 로스터의 시음이 있는 한국 최대 커피 축제.", "market", "COEX", "서울 강남구 영동대로 513", 37.5126, 127.0590, "2026-04-24", "2026-04-27", "https://www.coffeefestival.co.kr"),
    ]
    result = []
    for name_en, name_ko, desc_en, desc_ko, cat, venue, addr, lat, lng, sd, ed, url in fests:
        result.append({
            "id": _id(),
            "name_en": name_en, "name_ko": name_ko,
            "name_zh_cn": name_en, "name_zh_tw": name_en,
            "name_ja": name_en, "name_es": name_en,
            "name_th": name_en, "name_vi": name_en, "name_fr": name_en,
            "description_en": desc_en, "description_ko": desc_ko,
            "description_zh_cn": desc_en, "description_zh_tw": desc_en,
            "description_ja": desc_en, "description_es": desc_en,
            "description_th": desc_en, "description_vi": desc_en, "description_fr": desc_en,
            "category": cat, "image_url": f"/images/placeholder/festival_{len(result)+1}.jpg",
            "images": [f"/images/placeholder/festival_{len(result)+1}_{j}.jpg" for j in range(3)],
            "venue_name": venue, "address": addr,
            "latitude": lat, "longitude": lng,
            "start_date": date.fromisoformat(sd), "end_date": date.fromisoformat(ed),
            "website_url": url, "is_active": True,
        })
    return result


# ═══════════════════════════════════════════════
# 4. TRANSPORT ROUTES (8)
# ═══════════════════════════════════════════════
def get_transport_routes():
    routes_data = [
        ("Incheon Airport", "인천공항", 37.4602, 126.4407, "COEX", "코엑스", 37.5126, 127.0590,
         [{"mode": "bus", "duration_minutes": 70, "cost_krw": 16000, "transfers": 0, "tip_en": "Take Airport Limousine Bus 6006.", "tip_ko": "공항리무진 6006번 탑승."},
          {"mode": "subway", "duration_minutes": 90, "cost_krw": 4750, "transfers": 2, "tip_en": "Airport Railroad Express to Seoul Station, transfer to Line 2.", "tip_ko": "공항철도 직통열차 → 서울역 → 2호선 환승."},
          {"mode": "taxi", "duration_minutes": 55, "cost_krw": 75000, "transfers": 0, "tip_en": "International taxi from airport arrival hall.", "tip_ko": "공항 도착층 국제택시 이용."}]),
        ("Gimpo Airport", "김포공항", 37.5585, 126.7945, "COEX", "코엑스", 37.5126, 127.0590,
         [{"mode": "subway", "duration_minutes": 55, "cost_krw": 1550, "transfers": 1, "tip_en": "Line 9 Express to Bongeunsa Station.", "tip_ko": "9호선 급행 → 봉은사역."},
          {"mode": "bus", "duration_minutes": 50, "cost_krw": 7500, "transfers": 0, "tip_en": "Airport Bus 6000.", "tip_ko": "공항버스 6000번."},
          {"mode": "taxi", "duration_minutes": 35, "cost_krw": 35000, "transfers": 0, "tip_en": "Regular taxi from departure level.", "tip_ko": "일반택시 이용."}]),
        ("Seoul Station", "서울역", 37.5547, 126.9706, "COEX", "코엑스", 37.5126, 127.0590,
         [{"mode": "subway", "duration_minutes": 35, "cost_krw": 1350, "transfers": 1, "tip_en": "Line 4 → Line 2 at Sadang, or Line 1 → Line 2 at City Hall.", "tip_ko": "4호선 → 사당역 환승 2호선, 또는 1호선 → 시청역 환승 2호선."},
          {"mode": "bus", "duration_minutes": 40, "cost_krw": 1350, "transfers": 0, "tip_en": "Bus 740 direct to COEX.", "tip_ko": "740번 버스 직행."},
          {"mode": "taxi", "duration_minutes": 20, "cost_krw": 12000, "transfers": 0, "tip_en": "Taxi from station front.", "tip_ko": "역 앞 택시 이용."}]),
        ("Gangnam Station", "강남역", 37.4979, 127.0276, "COEX", "코엑스", 37.5126, 127.0590,
         [{"mode": "subway", "duration_minutes": 8, "cost_krw": 1350, "transfers": 0, "tip_en": "Line 2 to Samsung Station (3 stops).", "tip_ko": "2호선 삼성역 (3정거장)."},
          {"mode": "bus", "duration_minutes": 15, "cost_krw": 1350, "transfers": 0, "tip_en": "Bus 143, 362 direct.", "tip_ko": "143번, 362번 직행."},
          {"mode": "taxi", "duration_minutes": 10, "cost_krw": 6000, "transfers": 0, "tip_en": "Short taxi ride.", "tip_ko": "짧은 택시 이동."}]),
        ("Hongdae", "홍대", 37.5563, 126.9233, "COEX", "코엑스", 37.5126, 127.0590,
         [{"mode": "subway", "duration_minutes": 40, "cost_krw": 1350, "transfers": 0, "tip_en": "Line 2 direct to Samsung Station.", "tip_ko": "2호선 삼성역 직행."},
          {"mode": "taxi", "duration_minutes": 25, "cost_krw": 18000, "transfers": 0, "tip_en": "Taxi across the river.", "tip_ko": "한강 건너 택시."}]),
        ("Myeongdong", "명동", 37.5636, 126.9869, "COEX", "코엑스", 37.5126, 127.0590,
         [{"mode": "subway", "duration_minutes": 25, "cost_krw": 1350, "transfers": 1, "tip_en": "Line 4 → Line 2 at Dongdaemun History & Culture Park.", "tip_ko": "4호선 → 동대문역사문화공원역 환승 2호선."},
          {"mode": "taxi", "duration_minutes": 15, "cost_krw": 10000, "transfers": 0, "tip_en": "Quick taxi ride.", "tip_ko": "빠른 택시 이동."}]),
        ("COEX", "코엑스", 37.5126, 127.0590, "Gyeongbokgung Palace", "경복궁", 37.5796, 126.9770,
         [{"mode": "subway", "duration_minutes": 35, "cost_krw": 1350, "transfers": 1, "tip_en": "Line 2 → Line 3 at Jongno 3-ga.", "tip_ko": "2호선 → 종로3가역 환승 3호선."},
          {"mode": "bus", "duration_minutes": 40, "cost_krw": 1350, "transfers": 0, "tip_en": "Bus 472 to Gyeongbokgung.", "tip_ko": "472번 경복궁행."},
          {"mode": "taxi", "duration_minutes": 25, "cost_krw": 15000, "transfers": 0, "tip_en": "Direct taxi.", "tip_ko": "택시 직행."}]),
        ("COEX", "코엑스", 37.5126, 127.0590, "Namsan Tower", "남산타워", 37.5512, 126.9882,
         [{"mode": "subway", "duration_minutes": 30, "cost_krw": 1350, "transfers": 1, "tip_en": "Line 2 → Line 4 at Chungmuro, then Namsan cable car.", "tip_ko": "2호선 → 충무로역 환승 4호선, 남산 케이블카."},
          {"mode": "taxi", "duration_minutes": 20, "cost_krw": 12000, "transfers": 0, "tip_en": "Taxi to Namsan cable car station.", "tip_ko": "남산 케이블카 탑승장까지 택시."}]),
    ]
    result = []
    for from_en, from_ko, flat, flng, to_en, to_ko, tlat, tlng, modes in routes_data:
        result.append({
            "id": _id(),
            "from_name_en": from_en, "from_name_ko": from_ko,
            "from_name_zh_cn": from_en, "from_name_zh_tw": from_en,
            "from_name_ja": from_en, "from_name_es": from_en,
            "from_name_th": from_en, "from_name_vi": from_en, "from_name_fr": from_en,
            "to_name_en": to_en, "to_name_ko": to_ko,
            "to_name_zh_cn": to_en, "to_name_zh_tw": to_en,
            "to_name_ja": to_en, "to_name_es": to_en,
            "to_name_th": to_en, "to_name_vi": to_en, "to_name_fr": to_en,
            "from_latitude": flat, "from_longitude": flng,
            "to_latitude": tlat, "to_longitude": tlng,
            "transport_modes": modes, "route_polyline": None, "is_active": True,
        })
    return result


# ═══════════════════════════════════════════════
# 5. TRANSPORT TIPS (6)
# ═══════════════════════════════════════════════
def get_transport_tips():
    tips = [
        ("How to Use T-money Card", "T-money 카드 사용법", "<p>T-money is a rechargeable transit card...</p>", "<p>T-money는 충전식 교통카드입니다...</p>", "tmoney", "CreditCard"),
        ("Taxi Tips for Foreigners", "외국인을 위한 택시 팁", "<p>Korean taxis are safe and metered...</p>", "<p>한국 택시는 안전하고 미터제입니다...</p>", "taxi", "Car"),
        ("Essential Transportation Apps", "필수 교통 앱", "<p>Download KakaoMap and Naver Map...</p>", "<p>카카오맵과 네이버지도를 설치하세요...</p>", "app", "Smartphone"),
        ("Tourist Transit Passes", "외국인 교통 패스", "<p>Korea has several tourist transit passes...</p>", "<p>한국에는 다양한 외국인 교통 패스가 있습니다...</p>", "pass", "Ticket"),
        ("Seoul Subway Guide", "서울 지하철 가이드", "<p>Seoul's subway system is extensive...</p>", "<p>서울 지하철은 방대한 네트워크입니다...</p>", "subway", "Train"),
        ("Bus System Guide", "버스 시스템 가이드", "<p>Seoul buses are color-coded...</p>", "<p>서울 버스는 색상별로 구분됩니다...</p>", "bus", "Bus"),
    ]
    result = []
    for title_en, title_ko, content_en, content_ko, cat, icon in tips:
        result.append({
            "id": _id(),
            "title_en": title_en, "title_ko": title_ko,
            "title_zh_cn": title_en, "title_zh_tw": title_en,
            "title_ja": title_en, "title_es": title_en,
            "title_th": title_en, "title_vi": title_en, "title_fr": title_en,
            "content_en": content_en, "content_ko": content_ko,
            "content_zh_cn": content_en, "content_zh_tw": content_en,
            "content_ja": content_en, "content_es": content_en,
            "content_th": content_en, "content_vi": content_en, "content_fr": content_en,
            "category": cat, "icon": icon,
            "display_order": len(result), "is_active": True,
        })
    return result


# ═══════════════════════════════════════════════
# 6. LIVING GUIDE CATEGORIES (8)
# ═══════════════════════════════════════════════
_cat_ids = {}

def get_living_guide_categories():
    cats = [
        ("Transportation", "교통", "🚗"),
        ("Food Culture", "음식 문화", "🍽"),
        ("Shopping", "쇼핑", "🛍"),
        ("Emergency", "긴급 상황", "🏥"),
        ("Communication", "통신", "📱"),
        ("Currency Exchange", "환전", "💱"),
        ("Culture & Etiquette", "문화·에티켓", "🎌"),
        ("Weather & Clothing", "날씨·옷차림", "☀️"),
    ]
    result = []
    for name_en, name_ko, icon in cats:
        cid = _id()
        _cat_ids[name_en] = cid
        result.append({
            "id": cid,
            "name_en": name_en, "name_ko": name_ko,
            "name_zh_cn": name_en, "name_zh_tw": name_en,
            "name_ja": name_en, "name_es": name_en,
            "name_th": name_en, "name_vi": name_en, "name_fr": name_en,
            "icon": icon, "display_order": len(result), "is_active": True,
        })
    return result


# ═══════════════════════════════════════════════
# 7. LIVING GUIDE ARTICLES (3 per category = 24)
# ═══════════════════════════════════════════════
def get_living_guide_articles():
    articles_data = {
        "Transportation": [
            ("Getting Around Seoul by Subway", "지하철로 서울 이동하기", "<p>Seoul's subway system has 23 lines covering the entire metropolitan area. Buy a T-money card at any convenience store for 2,500 KRW and recharge as needed. Basic fare is 1,350 KRW. The subway runs from approximately 5:30 AM to midnight.</p>", "<p>서울 지하철은 23개 노선으로 수도권 전역을 연결합니다. 편의점에서 T-money 카드를 2,500원에 구매하고 필요할 때 충전하세요. 기본 요금은 1,350원입니다. 지하철은 약 오전 5시 30분부터 자정까지 운행합니다.</p>"),
            ("Taxi Guide for Visitors", "방문객을 위한 택시 가이드", "<p>Korean taxis are safe, clean, and metered. Regular taxis (silver/white) start at 4,800 KRW. International taxis are available at airports with English-speaking drivers. Use KakaoT app to call a taxi easily.</p>", "<p>한국 택시는 안전하고 깨끗하며 미터제입니다. 일반택시(은색/흰색) 기본요금은 4,800원입니다. 공항에서는 영어 가능한 국제택시를 이용할 수 있습니다. 카카오T 앱으로 쉽게 호출하세요.</p>"),
            ("Airport to Gangnam Transportation", "공항에서 강남까지 교통", "<p>From Incheon Airport: Airport Limousine Bus 6006 (70 min, 16,000 KRW) or Airport Railroad + Subway (90 min, 4,750 KRW). From Gimpo Airport: Subway Line 9 Express (55 min, 1,550 KRW).</p>", "<p>인천공항에서: 공항리무진 6006번 (70분, 16,000원) 또는 공항철도+지하철 (90분, 4,750원). 김포공항에서: 9호선 급행 (55분, 1,550원).</p>"),
        ],
        "Food Culture": [
            ("Korean Dining Etiquette", "한국 식사 예절", "<p>In Korea, the eldest person starts eating first. Use both hands when receiving items. Don't blow your nose at the table. Tipping is not customary. Many restaurants provide free side dishes (banchan).</p>", "<p>한국에서는 어른이 먼저 수저를 드셔야 합니다. 물건을 받을 때 두 손을 사용하세요. 식탁에서 코를 풀지 마세요. 팁 문화가 없습니다. 많은 식당에서 무료 반찬을 제공합니다.</p>"),
            ("Popular Korean Foods to Try", "꼭 먹어봐야 할 한국 음식", "<p>Must-try Korean dishes: Bibimbap (mixed rice), Korean BBQ (Galbi, Samgyeopsal), Kimchi Jjigae (kimchi stew), Tteokbokki (spicy rice cakes), Japchae (glass noodles), and Hotteok (sweet pancake).</p>", "<p>꼭 먹어봐야 할 한국 음식: 비빔밥, 한국 BBQ (갈비, 삼겹살), 김치찌개, 떡볶이, 잡채, 호떡.</p>"),
            ("How to Order Food in Korea", "한국에서 음식 주문하는 법", "<p>Many restaurants have picture menus or kiosks with English. Use KakaoMap to find restaurants and see menus. At BBQ restaurants, staff will help you grill. Water and banchan are typically free and self-service.</p>", "<p>많은 식당에 사진 메뉴판이나 영어 키오스크가 있습니다. 카카오맵으로 식당을 찾고 메뉴를 확인하세요. BBQ 식당에서는 직원이 고기 굽는 것을 도와줍니다. 물과 반찬은 보통 무료 셀프서비스입니다.</p>"),
        ],
        "Shopping": [
            ("Duty-Free & Tax Refund Guide", "면세점·세금 환급 가이드", "<p>Foreign visitors can get a tax refund on purchases over 30,000 KRW at participating stores. Look for the 'Tax Free' sign. Process your refund at the airport before departure. Duty-free shops are available at airports and downtown.</p>", "<p>외국인 방문객은 가맹점에서 3만원 이상 구매 시 세금 환급을 받을 수 있습니다. 'Tax Free' 표시를 찾으세요. 출국 전 공항에서 환급 절차를 밟으세요. 면세점은 공항과 시내에 있습니다.</p>"),
            ("Best Shopping Areas in Gangnam", "강남 최고 쇼핑 지역", "<p>Gangnam offers diverse shopping: COEX Mall (underground shopping), Garosu-gil (boutiques), Cheongdam-dong (luxury brands), Express Bus Terminal Underground (affordable fashion). Most shops are open 10 AM - 10 PM.</p>", "<p>강남에는 다양한 쇼핑 명소가 있습니다: 코엑스몰 (지하 쇼핑), 가로수길 (부티크), 청담동 (명품), 고속터미널 지하상가 (저렴한 패션). 대부분 오전 10시~오후 10시 영업.</p>"),
            ("Korean Size Guide", "한국 사이즈 가이드", "<p>Korean clothing sizes tend to run smaller than Western sizes. Common system uses S/M/L/XL or numbered sizes (44, 55, 66, 77). For shoes, Korean sizes are in mm (250mm = US 7). Always try on before purchasing.</p>", "<p>한국 의류 사이즈는 서양 사이즈보다 작게 나옵니다. S/M/L/XL 또는 숫자 사이즈(44, 55, 66, 77)를 사용합니다. 신발은 mm 단위(250mm = US 7). 구매 전 꼭 입어보세요.</p>"),
        ],
        "Emergency": [
            ("Emergency Numbers in Korea", "한국 긴급 전화번호", "<p>Emergency: 119 (Fire/Ambulance), 112 (Police). Tourist Helpline: 1330 (24h, multilingual). Immigration: 1345. These services are available in English, Chinese, Japanese, and other languages.</p>", "<p>긴급: 119 (소방/구급), 112 (경찰). 관광 핫라인: 1330 (24시간, 다국어). 출입국: 1345. 영어, 중국어, 일본어 등 다국어 서비스가 가능합니다.</p>"),
            ("Hospitals & Pharmacies for Foreigners", "외국인을 위한 병원·약국", "<p>Major hospitals with international clinics: Samsung Medical Center (Gangnam), Asan Medical Center, Severance Hospital. Look for pharmacies (약국) near any subway station. Many pharmacists speak basic English.</p>", "<p>국제 클리닉이 있는 대형 병원: 삼성서울병원 (강남), 서울아산병원, 세브란스병원. 지하철역 근처에서 약국을 찾으세요. 많은 약사가 기본 영어를 할 수 있습니다.</p>"),
            ("Embassy & Consulate Information", "대사관·영사관 정보", "<p>Most embassies are located in Yongsan-gu and Jongno-gu areas. Contact your embassy before traveling for emergency registration. Keep a copy of your passport and visa at all times.</p>", "<p>대부분의 대사관은 용산구와 종로구에 있습니다. 여행 전 대사관에 긴급 등록을 하세요. 여권과 비자 사본을 항상 지참하세요.</p>"),
        ],
        "Communication": [
            ("Getting a Korean SIM Card", "한국 SIM 카드 구매", "<p>Tourist SIM cards are available at airports and convenience stores. KT, SKT, and LG U+ offer tourist plans starting from 20,000 KRW for 5 days with unlimited data. Activate at airport kiosks with your passport.</p>", "<p>관광객용 SIM 카드는 공항과 편의점에서 구매 가능합니다. KT, SKT, LG U+에서 5일 무제한 데이터 2만원부터 관광 요금제를 제공합니다. 공항 키오스크에서 여권으로 활성화하세요.</p>"),
            ("Free Wi-Fi in Seoul", "서울 무료 와이파이", "<p>Seoul offers free public Wi-Fi ('Seoul WiFi' or 'Korea Free WiFi') at subway stations, tourist spots, and public areas. Most cafes and restaurants also offer free Wi-Fi. Speed is generally very fast.</p>", "<p>서울에는 지하철역, 관광지, 공공장소에서 무료 공공 와이파이('서울 와이파이' 또는 'Korea Free WiFi')를 제공합니다. 대부분의 카페와 식당에서도 무료 와이파이를 제공합니다.</p>"),
            ("Essential Korean Apps", "필수 한국 앱", "<p>Must-have apps: KakaoMap (navigation), KakaoT (taxi), Naver Map, Papago (translation), T-money (transit), Coupang (delivery). Most are available in English.</p>", "<p>필수 앱: 카카오맵 (길찾기), 카카오T (택시), 네이버지도, 파파고 (번역), T-money (교통), 쿠팡 (배달). 대부분 영어를 지원합니다.</p>"),
        ],
        "Currency Exchange": [
            ("Best Places to Exchange Money", "최적의 환전 장소", "<p>Best rates at licensed money changers in Myeongdong and Itaewon. Avoid airport exchanges (worst rates). Banks offer decent rates but charge fees. ATMs at convenience stores accept international cards.</p>", "<p>명동과 이태원의 공인 환전소에서 가장 좋은 환율을 받을 수 있습니다. 공항 환전은 피하세요 (가장 나쁜 환율). 은행은 적당한 환율이지만 수수료가 있습니다. 편의점 ATM에서 해외 카드를 사용할 수 있습니다.</p>"),
            ("Credit Cards & Mobile Payment", "신용카드·모바일 결제", "<p>Credit cards (Visa, Mastercard) are accepted almost everywhere in Seoul. Samsung Pay and Apple Pay work in many stores. Cash is still useful for small street vendors and traditional markets.</p>", "<p>신용카드(비자, 마스터카드)는 서울 거의 모든 곳에서 사용 가능합니다. 삼성페이, 애플페이도 많은 매장에서 사용됩니다. 노점이나 전통시장에서는 현금이 유용합니다.</p>"),
            ("Understanding Korean Won", "한국 원화 이해하기", "<p>Korean Won (KRW): Coins (10, 50, 100, 500 won), Bills (1,000, 5,000, 10,000, 50,000 won). Roughly: 1 USD ≈ 1,300 KRW. Most prices include tax. Tipping is not expected.</p>", "<p>한국 원(KRW): 동전(10, 50, 100, 500원), 지폐(1,000, 5,000, 10,000, 50,000원). 대략 1달러 ≈ 1,300원. 대부분 가격에 세금이 포함되어 있습니다. 팁은 불필요합니다.</p>"),
        ],
        "Culture & Etiquette": [
            ("Korean Social Etiquette", "한국 사회 예절", "<p>Bow slightly when greeting. Remove shoes when entering homes. Use both hands when giving/receiving. Respect for elders is very important. Don't point with one finger; use your whole hand.</p>", "<p>인사할 때 가볍게 고개를 숙이세요. 집에 들어갈 때 신발을 벗으세요. 물건을 주고받을 때 양손을 사용하세요. 어른에 대한 존경이 매우 중요합니다. 한 손가락으로 가리키지 말고 손 전체를 사용하세요.</p>"),
            ("Temple Visit Etiquette", "사찰 방문 예절", "<p>Dress modestly when visiting temples. Remove shoes before entering main halls. Don't touch Buddha statues. Photography may be restricted in some areas. Speak quietly. Bow when entering the main hall.</p>", "<p>사찰 방문 시 단정한 복장을 갖추세요. 법당에 들어갈 때 신발을 벗으세요. 불상을 만지지 마세요. 일부 구역에서는 촬영이 제한될 수 있습니다. 조용히 하세요. 법당에 들어갈 때 합장하세요.</p>"),
            ("Dos and Don'ts for Tourists", "관광객을 위한 주의사항", "<p>DO: Try local food, learn basic Korean greetings, respect local customs. DON'T: Write names in red ink (associated with death), refuse drinks from elders, be loud in residential areas at night.</p>", "<p>해야 할 것: 현지 음식 시식, 기본 한국어 인사 배우기, 현지 관습 존중. 하지 말 것: 이름을 빨간색으로 쓰지 마세요 (죽음과 연관), 어른의 술잔을 거절하지 마세요, 밤에 주거지역에서 시끄럽게 하지 마세요.</p>"),
        ],
        "Weather & Clothing": [
            ("Seoul Weather by Season", "계절별 서울 날씨", "<p>Spring (Mar-May): 5-20°C, cherry blossoms. Summer (Jun-Aug): 25-35°C, humid with monsoon. Autumn (Sep-Nov): 10-25°C, beautiful foliage. Winter (Dec-Feb): -10-5°C, cold and dry.</p>", "<p>봄 (3-5월): 5-20°C, 벚꽃. 여름 (6-8월): 25-35°C, 습하고 장마. 가을 (9-11월): 10-25°C, 아름다운 단풍. 겨울 (12-2월): -10-5°C, 춥고 건조.</p>"),
            ("What to Pack for Seoul", "서울 여행 준비물", "<p>Always bring: comfortable walking shoes, portable charger, umbrella. Spring/Fall: light jacket. Summer: light breathable clothes, rain gear. Winter: heavy coat, layers, thermal wear, warm accessories.</p>", "<p>항상 준비: 편한 워킹화, 보조배터리, 우산. 봄/가을: 가벼운 재킷. 여름: 가볍고 통기성 좋은 옷, 우비. 겨울: 두꺼운 코트, 레이어링, 발열내의, 방한용품.</p>"),
            ("UV & Air Quality Tips", "자외선·대기질 팁", "<p>Check air quality daily on AirVisual app. Wear masks on high PM2.5 days. Use SPF 50+ sunscreen even in winter. Seoul summers can be very humid with heat advisories — stay hydrated.</p>", "<p>에어비주얼 앱으로 매일 대기질을 확인하세요. 미세먼지가 심한 날에는 마스크를 착용하세요. 겨울에도 SPF 50+ 자외선차단제를 사용하세요. 서울 여름은 매우 습하고 폭염주의보가 있으니 수분을 충분히 섭취하세요.</p>"),
        ],
    }
    result = []
    for cat_name, articles in articles_data.items():
        cat_id = _cat_ids.get(cat_name, _id())
        for title_en, title_ko, content_en, content_ko in articles:
            result.append({
                "id": _id(), "category_id": cat_id,
                "title_en": title_en, "title_ko": title_ko,
                "title_zh_cn": title_en, "title_zh_tw": title_en,
                "title_ja": title_en, "title_es": title_en,
                "title_th": title_en, "title_vi": title_en, "title_fr": title_en,
                "content_en": content_en, "content_ko": content_ko,
                "content_zh_cn": content_en, "content_zh_tw": content_en,
                "content_ja": content_en, "content_es": content_en,
                "content_th": content_en, "content_vi": content_en, "content_fr": content_en,
                "image_url": f"/images/placeholder/guide_article_{len(result)+1}.jpg",
                "display_order": len(result) % 3, "is_active": True,
            })
    return result


# ═══════════════════════════════════════════════
# 8. THEMES (7)
# ═══════════════════════════════════════════════
def get_themes():
    themes = [
        ("K-POP Pilgrimage", "K-POP 성지순례", "Visit entertainment company buildings, K-Star Road, and fan culture hotspots.", "엔터사 사옥, K스타의 거리, 팬문화 핫스팟 방문.", "🎤", "#E91E63"),
        ("Traditional Markets", "전통시장", "Explore bustling traditional markets for authentic Korean food and goods.", "활기찬 전통시장에서 진짜 한국 음식과 물건을 탐색.", "🏪", "#FF9800"),
        ("Night View Spots", "야경 스팟", "Discover the best spots for stunning Seoul night panoramas.", "멋진 서울 야경 파노라마를 볼 수 있는 최고의 명소.", "🌃", "#3F51B5"),
        ("Cafe Streets", "카페거리", "Wander through Seoul's best cafe streets and unique coffee shops.", "서울 최고의 카페거리와 유니크한 커피숍 탐방.", "☕", "#795548"),
        ("Hallyu Filming Locations", "한류 촬영지", "Visit filming locations of famous K-Dramas and movies.", "유명 K-드라마와 영화 촬영지 방문.", "🎬", "#9C27B0"),
        ("Historical Sites", "역사 유적", "Explore ancient palaces, temples, and cultural heritage sites.", "고대 궁궐, 사찰, 문화유산 탐방.", "🏛", "#607D8B"),
        ("Nature & Parks", "자연·공원", "Find peace in Seoul's beautiful parks, mountains, and riverside paths.", "서울의 아름다운 공원, 산, 강변길에서 평화를 찾으세요.", "🌿", "#4CAF50"),
    ]
    result = []
    for name_en, name_ko, desc_en, desc_ko, icon, color in themes:
        result.append({
            "id": _id(),
            "name_en": name_en, "name_ko": name_ko,
            "name_zh_cn": name_en, "name_zh_tw": name_en,
            "name_ja": name_en, "name_es": name_en,
            "name_th": name_en, "name_vi": name_en, "name_fr": name_en,
            "description_en": desc_en, "description_ko": desc_ko,
            "icon": icon, "color": color,
            "display_order": len(result), "is_active": True,
        })
    return result
