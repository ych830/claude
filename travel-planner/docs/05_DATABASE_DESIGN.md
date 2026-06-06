# 데이터베이스 설계

## 테이블 목록

| 테이블 | 설명 |
|---|---|
| users | 사용자 계정 |
| user_preferences | 사용자 취향 정보 |
| travel_histories | 과거 여행 이력 |
| itineraries | 여행 일정 |
| itinerary_days | 일정 내 일자 |
| itinerary_items | 일정 항목 (장소) |
| itinerary_collaborators | 공동 편집자 |
| places | 장소 정보 (캐시) |
| reviews | 리뷰 |
| tips | 사용자 팁 |
| budgets | 예산 정보 |
| budget_items | 예산 세부 항목 |
| notifications | 알림 |

---

## 주요 테이블 스키마

### users
```sql
id            UUID PRIMARY KEY
email         VARCHAR UNIQUE NOT NULL
hashed_pw     VARCHAR
oauth_provider VARCHAR
oauth_id      VARCHAR
name          VARCHAR
profile_image VARCHAR
created_at    TIMESTAMP
updated_at    TIMESTAMP
```

### user_preferences
```sql
id            UUID PRIMARY KEY
user_id       UUID FK(users)
gender        VARCHAR
age           INTEGER
travel_styles TEXT[]        -- 여행 목적 배열
companion_type VARCHAR      -- solo, friend, couple, family, group
budget_range  VARCHAR       -- low, mid, high
transport_pref VARCHAR[]    -- 이동 수단 선호
updated_at    TIMESTAMP
```

### itineraries
```sql
id            UUID PRIMARY KEY
user_id       UUID FK(users)
title         VARCHAR
destination   VARCHAR
start_date    DATE
end_date      DATE
source        VARCHAR       -- ai_generated, sns_parsed, manual
status        VARCHAR       -- draft, confirmed
is_public     BOOLEAN
created_at    TIMESTAMP
updated_at    TIMESTAMP
```

### itinerary_items
```sql
id            UUID PRIMARY KEY
itinerary_id  UUID FK(itineraries)
day_number    INTEGER
order_index   INTEGER
place_id      VARCHAR       -- Google/Kakao place_id
place_name    VARCHAR
category      VARCHAR
latitude      FLOAT
longitude     FLOAT
estimated_duration INTEGER  -- 분
transport_to_next VARCHAR
travel_time_to_next INTEGER -- 분
memo          TEXT
estimated_cost INTEGER
created_at    TIMESTAMP
```

### places (캐시 테이블)
```sql
id            UUID PRIMARY KEY
external_id   VARCHAR UNIQUE -- Google/Kakao place_id
name          VARCHAR
category      VARCHAR
address       VARCHAR
latitude      FLOAT
longitude     FLOAT
phone         VARCHAR
opening_hours JSONB
rating        FLOAT
price_level   INTEGER
image_url     VARCHAR
cached_at     TIMESTAMP
```

### reviews
```sql
id            UUID PRIMARY KEY
user_id       UUID FK(users)
place_id      UUID FK(places)
rating        SMALLINT      -- 1:비추, 2:쏘쏘, 3:강추
content       TEXT
ai_summary    TEXT
created_at    TIMESTAMP
```

### tips
```sql
id            UUID PRIMARY KEY
user_id       UUID FK(users)
place_id      UUID FK(places)
content       TEXT
likes         INTEGER DEFAULT 0
created_at    TIMESTAMP
```

### budgets
```sql
id            UUID PRIMARY KEY
itinerary_id  UUID FK(itineraries) UNIQUE
total_estimated INTEGER
total_actual    INTEGER
currency        VARCHAR DEFAULT 'KRW'
updated_at      TIMESTAMP
```

### budget_items
```sql
id            UUID PRIMARY KEY
budget_id     UUID FK(budgets)
category      VARCHAR   -- accommodation, food, transport, ticket, activity, shopping, etc
name          VARCHAR
estimated     INTEGER
actual        INTEGER
payer_user_id UUID FK(users)
```
