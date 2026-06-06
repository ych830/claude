# 데이터베이스 설계 초안

## 1. 주요 엔티티

```text
User
Preference
TravelHistory
Place
Itinerary
ItineraryDay
ItineraryItem
Review
Tip
Budget
Notification
Invitation
SplitBill
```

## 2. User

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 사용자 ID |
| email | string | 이메일 |
| nickname | string | 닉네임 |
| age | int | 나이 |
| gender | string | 성별 |
| created_at | datetime | 생성일 |
| updated_at | datetime | 수정일 |

## 3. Preference

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 취향 ID |
| user_id | UUID | 사용자 ID |
| travel_purposes | array | 여행 목적 |
| companion_type | string | 동반자 유형 |
| preferred_transport | string | 선호 이동수단 |
| budget_level | string | 예산 수준 |
| disliked_categories | array | 비선호 카테고리 |

## 4. Place

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 장소 ID |
| name | string | 장소명 |
| category | string | 카테고리 |
| address | string | 주소 |
| latitude | float | 위도 |
| longitude | float | 경도 |
| opening_hours | json | 운영시간 |
| ticket_price | json | 입장권 가격 |
| source | string | 데이터 출처 |

## 5. Itinerary

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 일정 ID |
| owner_id | UUID | 소유자 |
| title | string | 일정 제목 |
| destination | string | 여행지 |
| start_date | date | 시작일 |
| end_date | date | 종료일 |
| status | string | draft/confirmed |
| created_at | datetime | 생성일 |

## 6. ItineraryDay

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 일차 ID |
| itinerary_id | UUID | 일정 ID |
| day_number | int | 며칠차 |
| date | date | 날짜 |

## 7. ItineraryItem

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 일정 항목 ID |
| itinerary_day_id | UUID | 일차 ID |
| place_id | UUID | 장소 ID |
| order_index | int | 순서 |
| start_time | time | 시작 시간 |
| end_time | time | 종료 시간 |
| memo | text | 메모 |
| estimated_cost | int | 예상 비용 |
| transport_to_next | json | 다음 장소까지 이동 정보 |

## 8. Review

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 리뷰 ID |
| user_id | UUID | 작성자 |
| place_id | UUID | 장소 |
| rating_level | string | 비추/쏘쏘/강추 |
| content | text | 리뷰 내용 |
| created_at | datetime | 작성일 |

## 9. Tip

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 팁 ID |
| user_id | UUID | 작성자 |
| place_id | UUID | 장소 |
| content | text | 팁 내용 |
| created_at | datetime | 작성일 |

## 10. Budget

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 예산 ID |
| itinerary_id | UUID | 일정 ID |
| category | string | 숙박/식비/교통/입장권 등 |
| amount | int | 금액 |
| currency | string | 통화 |

## 11. Invitation

| 필드 | 타입 | 설명 |
|---|---|---|
| id | UUID | 초대 ID |
| itinerary_id | UUID | 일정 ID |
| inviter_id | UUID | 초대한 사용자 |
| invitee_id | UUID | 초대받은 사용자 |
| role | string | viewer/editor |
| status | string | pending/accepted/rejected |
