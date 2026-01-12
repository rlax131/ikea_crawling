```python
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import urllib.request
import os
import sys

url = "https://www.ikea.com/kr/ko/cat/bookcases-10382/"
driver = webdriver.Chrome()

driver.get(url)
time.sleep(1)

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
    time.sleep(2)

    try:
        btn_more = driver.find_element(By.XPATH, '//*[@id="product-list"]/div[3]/a/span')
        driver.execute_script("arguments[0].click();", btn_more) 
        time.sleep(2)
    except:
        print(f"{i+1} 번째 반복에서 더보기 버튼 없음 → 루프 종료")
        break

html_code = driver.page_source
soup = bs(html_code,'html.parser')

root = soup.select_one('#product-list > div.plp-product-list__products.plp-product-list__products--compare-enabled')

names = root.select('div > div > div.plp-mastercard__price-components > a > div > div.plp-price-module__information > h3 > span.plp-price-module__name-decorator.notranslate > span')
sizes = root.select('div > div > div.plp-mastercard__price-components > a > div > div.plp-price-module__information > h3 > span.plp-text.plp-typography-label-m.plp-typography-regular.plp-price-module__description')
prices = root.select(
    'span.plp-price__integer, em span.plp-price__integer'
)
thumbnails = root.select('div > div > div.plp-product__image__container > a > img.plp-image.plp-product__image')
rating_tags = root.select('div > div > div.plp-mastercard__price-components > button > span.plp-rating__stars.plp-rating__stars--small')

import re

ratings = []

# 제품 하나씩:
product_cards = root.select(
    "#product-list > div.plp-product-list__products.plp-product-list__products--compare-enabled > div"
)

for card in product_cards:
    # 제품 card 내부의 rating span 찾기
    rating_tag = card.select_one(
        "div.plp-mastercard__price-components > button > span.plp-rating__stars"
    )

    if rating_tag is None:
        ratings.append("No Rating")
        continue

    aria = rating_tag.get("aria-label", "")

    # 정규식으로 숫자 추출
    m = re.search(r"(\d+(?:\.\d+)?)", aria)

    if m:
        ratings.append(m.group(1))
    else:
        ratings.append("No Rating")

print("=== Rating ===")
for r in ratings:
    print(r)
    
print()

print("=== Name ===")
for name in names:
    print(name.get_text())

print()

print("=== Specific Explanation ===")
for size in sizes:
    print(size.get_text())

print()

"""print("=== Parsed Dimensions (W, D, H) ===")
for size in sizes:
    raw = size.get_text().strip()

    try:
        # tail 추출: 마지막에서 'cm' 앞에 있는 "폭x깊이x높이" or "폭x깊이"
        parts = raw.split()
        dim_str = parts[-2]  # e.g. "80x28x202" or "54x33"

        dims = dim_str.split('x')

        if len(dims) == 3:
            w, d, h = dims
            print(f"W={w}, D={d}, H={h}")

        elif len(dims) == 2:
            w, h = dims
            print(f"W={w}, H={h}")   # 세로 없는 제품

        else:
            print("Unknown pattern:", raw)

    except Exception as e:
        print("Failed to parse:", raw)

print()

print("=== Parsed Colors ===")
for size in sizes:
    raw = size.get_text().strip()

    # 패턴: "제품명, 색상, 치수"
    # → 콤마로 split
    parts = [s.strip() for s in raw.split(',')]

    if len(parts) >= 2:
        color = parts[1]  # 두 번째 항목이 색상
        print(color)
    else:
        print("No color found:", raw)

print()"""

print("=== Parsing Dimensions ===")

widths = []
depths = []
heights = []

for size in sizes:
    raw = size.get_text().strip()

    try:
        parts = raw.split()
        dim_str = parts[-2]  # "80x28x202" or "54x33" 등
        dims = dim_str.split('x')

        # 3개(W,D,H)
        if len(dims) == 3:
            w, d, h = dims
            widths.append(w)
            depths.append(d)
            heights.append(h)

        # 2개(W,H 혹은 W,D)
        elif len(dims) == 2:
            w, h = dims
            widths.append(w)
            depths.append("0")   # 깊이 없음 → 0 처리
            heights.append(h)

        else:
            # Unknown → 0,0,0
            widths.append("0")
            depths.append("0")
            heights.append("0")

    except:
        widths.append("0")
        depths.append("0")
        heights.append("0")

print("\n=== Width ===")
for w in widths:
    print(w)

print("\n=== Depth ===")
for d in depths:
    print(d)

print("\n=== Height ===")
for h in heights:
    print(h)
print()

print("=== Price ===")
for price in prices:
    # 부모 혹은 조상 중에 plp-price_nowrap 이 있으면 정상가 → 제외
    if price.find_parent(class_='plp-price-module__comparison-price'):
        continue
    print(price.get_text())
    
print()

print("===Thumbnails===")
for thumbnail in thumbnails:
    print(thumbnail.get('src'))

```

    === Rating ===
    4.6
    4.6
    4.6
    4.7
    4.6
    4.7
    4.6
    4.6
    No Rating
    4.8
    4.5
    4.7
    4.7
    4.6
    4.5
    4.6
    4.7
    4.1
    4.6
    4.7
    4.7
    4.7
    4.3
    4.2
    4.7
    4.2
    4.6
    4.6
    4.8
    4.6
    4.5
    4.4
    4.6
    4.6
    3.5
    3.7
    No Rating
    4.5
    No Rating
    4
    4.7
    4.7
    4.1
    4.7
    4.8
    4
    4.7
    4.5
    4.7
    4.7
    4.2
    4.5
    4.7
    4.3
    4.9
    3
    4.4
    4.7
    4.2
    4.8
    4.8
    4.7
    4.7
    3.6
    4.8
    4.5
    4.2
    4.7
    No Rating
    5
    4.6
    4.5
    4.5
    4.8
    4.8
    4.3
    4.6
    5
    No Rating
    4.7
    4.7
    No Rating
    No Rating
    4.5
    4.6
    4.3
    5
    5
    4.7
    4.6
    No Rating
    4.6
    4.1
    No Rating
    4.5
    4.2
    4
    3.8
    5
    4.7
    No Rating
    4.8
    4.8
    No Rating
    4.5
    4.5
    4.4
    4.3
    4.7
    1
    No Rating
    5
    5
    No Rating
    3
    4.8
    No Rating
    3
    4.4
    4.2
    5
    4.6
    4.7
    4.6
    No Rating
    4.1
    5
    4.6
    
    === Name ===
    BILLY 빌리
    BILLY 빌리
    BAGGEBO 바게보
    BILLY 빌리
    BILLY 빌리
    BILLY 빌리
    BAGGEBO 바게보
    BILLY 빌리
    KALLAX 칼락스
    LAIVA 라이바
    BRIMNES 브림네스
    BILLY 빌리
    DALRIPA 달리파
    BAGGEBO 바게보
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    SKRUVBY 스크루브뷔
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리
    KALLAX 칼락스
    BILLY 빌리
    EKET 에케트
    HAUGA 하우가
    BILLY 빌리
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리
    KALLAX 칼락스
    BILLY 빌리
    BESTÅ 베스토
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BESTÅ 베스토
    BILLY 빌리 / OXBERG 옥스베리
    KALLAX 칼락스
    HEMNES 헴네스
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    TONSTAD 톤스타드
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리
    KALLAX 칼락스
    BILLY 빌리
    SKRUVBY 스크루브뷔
    BILLY 빌리 / OXBERG 옥스베리
    OXBERG 옥스베리
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리
    SKRUVBY 스크루브뷔
    SKRUVBY 스크루브뷔
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    TONSTAD 톤스타드
    BILLY 빌리
    BILLY 빌리 / HÖGADAL 회가달
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    HAUGA 하우가
    BILLY 빌리 / OXBERG 옥스베리
    HEMNES 헴네스
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    TONSTAD 톤스타드
    HÖGADAL 회가달
    BILLY 빌리 / OXBERG 옥스베리
    TONSTAD 톤스타드
    IDANÄS 이다네스
    BILLY 빌리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / BERGSHULT 베리스훌트
    BILLY 빌리 / OXBERG 옥스베리
    HÖGBO 회그보
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / HÖGADAL 회가달
    SKRUVBY 스크루브뷔
    HÖGBO 회그보
    HEMNES 헴네스
    BILLY 빌리
    BILLY 빌리 / HÖGADAL 회가달
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리 / HÖGADAL 회가달
    BILLY 빌리 / OXBERG 옥스베리
    BILLY 빌리 / OXBERG 옥스베리
    OXBERG 옥스베리
    HÖGADAL 회가달
    IDANÄS 이다네스
    BILLY 빌리
    HAUGA 하우가
    BILLY 빌리 / OXBERG 옥스베리
    OXBERG 옥스베리
    LANESUND 라네순드
    BILLY 빌리
    BILLY 빌리 / EKET 에케트
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리 / HÖGADAL 회가달
    BILLY 빌리 / HÖGADAL 회가달
    TONSTAD 톤스타드
    BILLY 빌리
    HEMNES 헴네스
    BILLY 빌리 / HÖGADAL 회가달
    OXBERG 옥스베리
    IDANÄS 이다네스
    OXBERG 옥스베리
    BILLY 빌리 / HÖGBO 회그보
    BILLY 빌리
    BILLY 빌리
    BILLY 빌리
    
    === Specific Explanation ===
    책장, 화이트, 80x28x202 cm
    책장, 자작나무 효과, 80x28x106 cm
    책장, 화이트, 50x25x160 cm
    책장, 자작나무 효과, 40x28x202 cm
    책장+도어, 화이트, 80x30x202 cm
    책장, 자작나무 효과, 40x28x106 cm
    책장, 화이트, 50x30x80 cm
    책장, 화이트, 240x28x106 cm
    선반유닛+하부프레임, 화이트/화이트, 147x94 cm
    책장, 블랙브라운, 62x165 cm
    책장, 화이트, 60x190 cm
    책장, 화이트, 160x28x202 cm
    책장, 화이트, 60x150 cm
    도어수납장, 화이트, 50x30x80 cm
    상단추가유닛, 화이트, 80x28x35 cm
    책장+패널/유리도어, 자작나무 효과, 80x30x202 cm
    책장, 화이트, 60x140 cm
    책장 코너콤비네이션+확장유닛, 참나무무늬, 136/136x28x237 cm
    책장, 화이트, 80x30x202 cm
    책장, 화이트, 40x28x237 cm
    선반유닛+하부프레임, 화이트/화이트, 147x129 cm
    책장+접이식테이블, 화이트, 80x33/112x106 cm
    수납콤비네이션+발받침, 화이트, 70x35x72 cm
    키큰장+도어2, 화이트, 70x199 cm
    책장 콤비네이션/코너 솔루션, 화이트, 95/95x28x202 cm
    책장, 화이트, 80x28x237 cm
    책장+도어, 화이트, 40x30x106 cm
    책장콤비네이션+도어, 화이트, 160x106 cm
    책장+서랍, 화이트, 80x30x202 cm
    책장+도어, 자작나무 효과, 80x30x106 cm
    책상, 화이트, 76x60 cm
    선반유닛+하부프레임, 화이트/화이트, 77x94 cm
    책장+서랍, 화이트, 80x30x106 cm
    수납콤비네이션+도어, 화이트스테인 참나무무늬/라프비켄/스투바르프 화이트스테인 참나무무늬, 120x42x202 cm
    책장콤비네이션+확장유닛, 자작나무 효과, 120x237 cm
    책장콤비네이션+도어, 화이트, 240x30x202 cm
    책장+상단추가유닛, 화이트, 120x28x237 cm
    책장+도어, 화이트/유리, 200x30x106 cm
    수납장 유닛, 화이트, 60x40x202 cm
    책장+패널/유리도어, 화이트/유리, 40x30x202 cm
    선반유닛+하부프레임, 화이트/화이트, 77x164 cm
    책장, 화이트 스테인/라이트브라운, 90x198 cm
    책장+도어, 화이트/유리, 80x30x106 cm
    책장+유리도어, 화이트, 120x30x202 cm
    책장, 오프화이트, 81x37x201 cm
    책장+유리도어, 화이트/유리, 40x30x202 cm
    책장콤비네이션+확장유닛, 블랙 참나무무늬, 200x28x237 cm
    책장+유리도어/확장유닛, 자작나무 효과, 40x30x237 cm
    책장콤비네이션+유리도어, 화이트, 40x30x202 cm
    책장+유리도어, 화이트, 80x30x202 cm
    선반, 자작나무 효과, 76x26 cm
    선반유닛+하부프레임, 화이트/화이트, 147x164 cm
    상단추가유닛, 자작나무 효과, 40x28x35 cm
    수납콤비네이션, 블랙블루, 130x140 cm
    책장콤비네이션+도어, 화이트, 240x30x106 cm
    도어, 자작나무 효과, 40x97 cm
    책장+유리도어, 화이트, 80x30x202 cm
    책장+책상, 화이트, 80x106 cm
    수납콤비네이션+유리도어, 블랙블루, 190x90 cm
    수납콤비네이션, 화이트, 180x140 cm
    책장, 화이트, 160x30x202 cm
    책장, 화이트, 215/135x28x237 cm
    책장+도어/확장유닛, 화이트, 80x30x237 cm
    수납콤비네이션+미닫이 유리도어, 오프화이트/유리, 120x47x201 cm
    선반, 자작나무 효과, 36x26 cm
    책장+도어, 자작나무 효과, 80x30x106 cm
    책장콤비네이션+유리도어, 화이트, 160x202 cm
    책장+패널/유리도어, 화이트/유리, 160x30x202 cm
    책장콤비네이션+유리도어, 화이트, 160x202 cm
    책장콤비네이션+유리도어, 블랙 참나무무늬, 160x202 cm
    책장+패널/유리도어, 화이트/유리, 120x30x202 cm
    책장콤비네이션+유리도어, 화이트, 40x30x106 cm
    책장+패널/유리도어, 화이트/유리, 160x30x202 cm
    책장+책상, 화이트, 80x202 cm
    책장+책상, 화이트, 80x202 cm
    책장+패널/유리도어, 화이트, 160x30x202 cm
    수납콤비네이션, 화이트, 279x46x199 cm
    책장+도어, 화이트/유리, 80x30x202 cm
    수납콤비네이션+도어/서랍, 그레이그린/라이트 스테인 브라운, 180x197 cm
    책장, 화이트, 80x30x237 cm
    책장+패널/유리도어, 화이트, 160x30x202 cm
    수납콤비네이션+미닫이 유리도어, 오프화이트/유리, 243x47x201 cm
    도어, 화이트/직조한 대나무, 40x97 cm
    책장, 화이트/유리, 120x30x237 cm
    책장, 참나무무늬목, 82x37x201 cm
    수납콤비네이션+유리도어, 다크브라운/스테인, 244x39x211 cm
    책장+책상/서랍, 화이트, 80x202 cm
    책장+상단추가유닛/유리도어, 화이트/유리, 40x30x237 cm
    책장, 화이트, 200x30x237 cm
    책장콤비네이션+접이식테이블, 화이트, 80x106 cm
    책장+상단추가유닛/유리도어, 화이트, 80x30x237 cm
    유리도어, 화이트, 40x97 cm
    책장+상단추가유닛/도어, 화이트/유리, 160x30x237 cm
    책장+도어, 자작나무 효과, 40x30x106 cm
    수납콤비네이션, 블랙블루, 190x90 cm
    유리도어, 화이트, 40x192 cm
    수납콤비네이션+도어/서랍, 화이트 스테인/라이트브라운, 270x198 cm
    책장콤비네이션+접이식테이블, 화이트, 120x202 cm
    책장+도어, 자작나무 효과, 40x30x202 cm
    책장+책상/서랍, 화이트, 80x202 cm
    책장+도어, 화이트, 80x30x202 cm
    책장+상단추가유닛/도어, 화이트, 160x30x237 cm
    책장콤비네이션+패널/유리도어, 화이트, 160x202 cm
    유리도어, 자작나무 효과, 40x35 cm
    도어, 화이트/직조한 대나무, 40x192 cm
    키큰장+유리도어/서랍, 다크브라운 스테인, 81x39x211 cm
    서랍, 화이트/바퀴 있음, 80x28x44 cm
    수납콤비네이션, 화이트, 210x46x199 cm
    책장+상단추가유닛/도어, 화이트/유리, 160x30x237 cm
    유리도어, 화이트, 40x97 cm
    책장, 그레이브라운, 121x37x152 cm
    책장+책상/서랍, 화이트, 80x106 cm
    책장콤비네이션+접이식테이블, 화이트, 80x106 cm
    책장콤비네이션+유리도어, 화이트, 160x202 cm
    책장+도어, 자작나무 효과, 80x30x202 cm
    책장콤비네이션+접이식테이블, 화이트/직조한 대나무, 160x202 cm
    수납콤비네이션+미닫이 유리도어, 오프화이트/유리, 81x47x201 cm
    추가선반, 유리, 76x26 cm
    유리장식장+서랍3, 그레이그린/라이트 스테인 브라운, 90x197 cm
    책장+책상, 화이트/직조한 대나무, 80x202 cm
    패널/유리도어, 자작나무 효과, 40x192 cm
    책장, 다크브라운 스테인, 81x39x211 cm
    유리도어, 자작나무 효과, 40x192 cm
    책장콤비네이션+접이식테이블, 화이트, 160x202 cm
    코너고정장치, 아연도금
    책장, 그린, 160x30x202 cm
    책장+유리도어, 그린, 80x30x202 cm
    
    === Parsing Dimensions ===
    
    === Width ===
    80
    80
    50
    40
    80
    40
    50
    240
    147
    62
    60
    160
    60
    50
    80
    80
    60
    136/136
    80
    40
    147
    80
    70
    70
    95/95
    80
    40
    160
    80
    80
    76
    77
    80
    120
    120
    240
    120
    200
    60
    40
    77
    90
    80
    120
    81
    40
    200
    40
    40
    80
    76
    147
    40
    130
    240
    40
    80
    80
    190
    180
    160
    215/135
    80
    120
    36
    80
    160
    160
    160
    160
    120
    40
    160
    80
    80
    160
    279
    80
    180
    80
    160
    243
    40
    120
    82
    244
    80
    40
    200
    80
    80
    40
    160
    40
    190
    40
    270
    120
    40
    80
    80
    160
    160
    40
    40
    81
    80
    210
    160
    40
    121
    80
    80
    160
    80
    160
    81
    76
    90
    80
    40
    81
    40
    160
    0
    160
    80
    
    === Depth ===
    28
    28
    25
    28
    30
    28
    30
    28
    0
    0
    0
    28
    0
    30
    28
    30
    0
    28
    30
    28
    0
    33/112
    35
    0
    28
    28
    30
    0
    30
    30
    0
    0
    30
    42
    0
    30
    28
    30
    40
    30
    0
    0
    30
    30
    37
    30
    28
    30
    30
    30
    0
    0
    28
    0
    30
    0
    30
    0
    0
    0
    30
    28
    30
    47
    0
    30
    0
    30
    0
    0
    30
    30
    30
    0
    0
    30
    46
    30
    0
    30
    30
    47
    0
    30
    37
    39
    0
    30
    30
    0
    30
    0
    30
    30
    0
    0
    0
    0
    30
    0
    30
    30
    0
    0
    0
    39
    28
    46
    30
    0
    37
    0
    0
    0
    30
    0
    47
    0
    0
    0
    0
    39
    0
    0
    0
    30
    30
    
    === Height ===
    202
    106
    160
    202
    202
    106
    80
    106
    94
    165
    190
    202
    150
    80
    35
    202
    140
    237
    202
    237
    129
    106
    72
    199
    202
    237
    106
    106
    202
    106
    60
    94
    106
    202
    237
    202
    237
    106
    202
    202
    164
    198
    106
    202
    201
    202
    237
    237
    202
    202
    26
    164
    35
    140
    106
    97
    202
    106
    90
    140
    202
    237
    237
    201
    26
    106
    202
    202
    202
    202
    202
    106
    202
    202
    202
    202
    199
    202
    197
    237
    202
    201
    97
    237
    201
    211
    202
    237
    237
    106
    237
    97
    237
    106
    90
    192
    198
    202
    202
    202
    202
    237
    202
    35
    192
    211
    44
    199
    237
    97
    152
    106
    106
    202
    202
    202
    201
    26
    197
    202
    192
    211
    192
    202
    0
    202
    202
    
    === Price ===
    89,900
    52,000
    35,000
    52,000
    149,900
    34,000
    30,000
    179,700
    139,000
    35,000
    139,000
    179,800
    79,900
    35,000
    30,000
    163,900
    99,900
    390,700
    209,900
    79,900
    179,000
    229,000
    95,000
    249,000
    185,700
    119,900
    69,900
    199,700
    134,900
    85,800
    70,000
    84,900
    104,900
    360,000
    215,700
    389,700
    239,700
    279,700
    140,000
    114,900
    134,000
    349,000
    119,900
    329,800
    249,000
    119,900
    384,700
    116,800
    119,900
    209,900
    9,900
    209,000
    19,900
    218,900
    299,700
    16,900
    169,900
    129,900
    368,000
    328,900
    399,800
    445,600
    239,900
    728,000
    6,900
    142,000
    329,700
    359,800
    419,800
    479,800
    314,800
    79,900
    409,800
    159,900
    219,900
    349,800
    797,000
    149,900
    998,000
    269,900
    349,800
    1,006,000
    45,000
    409,800
    299,000
    1,089,000
    204,900
    149,900
    619,700
    276,800
    259,900
    40,000
    479,800
    79,000
    348,000
    60,000
    1,647,000
    288,900
    132,000
    284,900
    179,900
    479,800
    429,700
    9,900
    80,000
    489,000
    45,000
    548,000
    479,800
    30,000
    499,000
    174,900
    319,000
    329,700
    259,900
    408,900
    508,000
    15,000
    649,000
    249,900
    32,000
    300,000
    35,000
    398,900
    6,000
    498,000
    249,000
    
    ===Thumbnails===
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-white__0625599_pe692385_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-birch-effect__1122553_pe874629_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/baggebo-bookcase-white__0981552_pe815388_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-birch-effect__1097088_pe864711_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-with-doors-white__0667808_pe714092_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-birch-effect__1097070_pe864702_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1018918_pe831218_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-white__0644497_pe702733_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/kallax-shelving-unit-with-underframe-white-white__1041422_pe841007_s5.jpg?f=xxs
    https://www.ikea.com/pimg/0644278_pe702556_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/brimnes-bookcase-white__0644268_pe702543_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-white__0644156_pe702452_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/dalripa-bookcase-white__1115153_pe871967_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1016757_pe830615_s5.jpg?f=xxs
    https://www.ikea.com/pimg/0720622_pe732722_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-panel-glass-doors-birch-effect__1096995_pe864659_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1128166_pe876444_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-corner-comb-w-ext-units-oak-effect__1134407_pe878771_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-white__0641255_pe700390_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-white__0644150_pe702446_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/kallax-shelving-unit-with-underframe-white-white__1041456_pe841036_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1417029_pe975803_s5.jpg?f=xxs
    https://www.ikea.com/pimg/0747110_pe744423_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/hauga-high-cabinet-with-2-doors-white__0914112_pe783851_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-combination-crnr-solution-white__0979439_pe814538_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-white__0644152_pe702448_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-door-white__0667888_pe714149_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-combination-with-doors-white__1101219_pe866392_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-with-drawer-white__1124508_pe875187_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-doors-birch-effect__1096921_pe864596_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-desk-white__1287222_pe933878_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/kallax-shelving-unit-with-underframe-white-white__1041385_pe840977_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1124503_pe875183_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/besta-storage-combination-with-doors-white-stained-oak-effect-lappviken-stubbarp-white-stained-oak-effect__0719290_pe731958_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-comb-with-extension-units-birch-effect__1134412_pe878776_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1397714_pe967728_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-w-height-extension-units-white__0644146_pe702444_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1080028_pe857826_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/besta-cabinet-unit-white__0750526_pe746769_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-panel-glass-door-white-glass__0668157_pe714277_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/kallax-shelving-unit-with-underframe-white-white__1041404_pe840990_s5.jpg?f=xxs
    https://www.ikea.com/pimg/0980092_pe814822_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1080019_pe857816_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-glass-doors-white__0668517_pe714545_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1335573_pe947093_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-glass-door-white-glass__0667948_pe714198_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-comb-with-extension-units-black-oak-effect__1134418_pe878780_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-w-glass-doors-ext-unit-birch-effect__1134403_pe878765_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegbo-bookcase-combination-w-glass-doors-white__1125345_pe875419_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegbo-bookcase-with-glass-doors-white__1104264_pe867570_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1097124_pe864757_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/kallax-shelving-unit-with-underframe-white-white__1041472_pe841046_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1134263_pe878649_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1130658_pe877912_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-combination-with-doors-white__1101210_pe866391_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1097130_pe864758_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegbo-bookcase-with-glass-doors-white__1100417_pe866160_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-with-desk-white__1330210_pe945485_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1291711_pe934972_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1281447_pe931867_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-white__0641185_pe700276_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-white__0627027_pe693158_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-w-doors-extension-unit-white__1099545_pe865764_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1335091_pe946960_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1097127_pe864755_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1285409_pe933306_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-combination-w-glass-doors-white__1101228_pe866394_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-panel-glass-doors-white-clear-glass__1080030_pe857828_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegbo-bookcase-combination-w-glass-doors-white__1092051_pe862693_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-combination-w-glass-doors-black-oak-effect__1099640_pe865834_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-panel-glass-doors-white-glass__0668503_pe714528_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1125344_pe875418_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-panel-glass-doors-white-glass__0668632_pe714604_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-with-desk-white__1299769_pe936762_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-desk-white__1330208_pe945483_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-panel-glass-doors-white__0668581_pe714571_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/hauga-storage-combination-white__0917830_pe785980_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-doors-white-clear-glass__1080017_pe857814_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/hemnes-storage-combination-w-doors-drawers-grey-green-light-brown-stained__1421227_pe977589_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-white__0641257_pe700392_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-with-panel-glass-doors-white__1080006_pe857821_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1335090_pe946962_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1250392_pe923730_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-white-glass__0641191_pe700279_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1186263_pe898745_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/idanaes-storage-combination-w-glass-doors-dark-brown-stained__1028825_pe835545_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-with-desk-and-drawer-white__1299770_pe936763_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-w-hght-ext-ut-pnl-glss-drs-white-glass__0668181_pe714296_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-white__0641186_pe700289_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bergshult-bookcase-comb-w-foldable-table-white__1417060_pe975833_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-w-hght-ext-ut-pnl-glss-drs-white__0667766_pe714061_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/hoegbo-glass-door-white__1097160_pe864783_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-w-height-extension-ut-drs-white-clear-glass__1080008_pe857820_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1286178_pe933458_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1333010_pe946381_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/hoegbo-glass-door-white__1091562_pe862498_s5.jpg?f=xxs
    https://www.ikea.com/pimg/0824724_pe776180_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-comb-w-foldable-table-white__1417080_pe975850_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1286176_pe933460_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegbo-bookcase-with-desk-and-drawer-white__1299772_pe936765_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1364343_pe955858_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-w-height-extension-ut-drs-white__0668658_pe714623_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-comb-w-panel-glass-doors-white__1101226_pe866393_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1097146_pe864774_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1250391_pe923729_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/idanaes-high-cabinet-w-gls-drs-and-1-drawer-dark-brown-stained__1008948_pe827389_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1115970_pe872323_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/hauga-storage-combination-white__0917814_pe785997_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-oxberg-bookcase-w-height-extension-ut-drs-white-clear-glass__1080032_pe857830_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1103661_pe867355_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/lanesund-bookcase-grey-brown__1159292_pe888404_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-bookcase-with-desk-and-drawer-white__1330209_pe945484_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-eket-bookcase-comb-w-foldable-table-white__1417073_pe975846_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegbo-bookcase-combination-w-glass-doors-white__1092056_pe862694_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1285406_pe933308_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegadal-bookcase-comb-w-foldable-table-white-woven-bamboo__1417079_pe975849_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1335118_pe946967_s5.jpg?f=xxs
    https://www.ikea.com/pimg/0640692_pe699992_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1421222_pe977587_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegadal-bookcase-with-desk-white-woven-bamboo__1299768_pe936761_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1097143_pe864771_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/idanaes-bookcase-dark-brown-stained__1008945_pe827388_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1097147_pe864775_s5.jpg?f=xxs
    https://www.ikea.com/kr/ko/images/products/billy-hoegbo-bookcase-comb-w-foldable-table-white__1417097_pe975855_s5.jpg?f=xxs
    https://www.ikea.com/pimg/0626846_pe693024_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1384213_pe962918_s5.jpg?f=xxs
    https://www.ikea.com/pimg/1384216_pe962921_s5.jpg?f=xxs
    


```python

```
