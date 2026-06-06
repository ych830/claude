# API 프로세스 설계

## 1. API 기본 규칙

- 모든 API는 `/api/v1` prefix를 사용한다.
- Request/Response는 Pydantic Schema로 검증한다.
- 인증이 필요한 API는 JWT Bearer Token을 사용한다.
- 응답 형식은 일관되게 유지한다.

## 2. 공통 응답 형식

```json
{
  "success": true,
  "data": {},
  "message": "OK"
}
```

## 3. 에러 응답 형식

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "잘못된 요청입니다."
  }
}
```

## 4. 주요 API 목록

### Auth

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/v1/auth/signup` | 회원가입 |
| POST | `/api/v1/auth/login` | 로그인 |
| POST | `/api/v1/auth/oauth/kakao` | 카카오 로그인 |
| POST | `/api/v1/auth/refresh` | 토큰 재발급 |

### User Preference

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/v1/users/me` | 내 정보 조회 |
| PUT | `/api/v1/users/me/preferences` | 취향 수정 |
| GET | `/api/v1/users/me/travel-history` | 여행 이력 조회 |

### Itinerary

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/v1/itineraries/ai-generate` | 취향 기반 AI 일정 생성 |
| POST | `/api/v1/itineraries/from-sns` | SNS 링크 기반 일정 생성 |
| GET | `/api/v1/itineraries` | 내 일정 목록 |
| GET | `/api/v1/itineraries/{itinerary_id}` | 일정 상세 조회 |
| PATCH | `/api/v1/itineraries/{itinerary_id}` | 일정 기본 정보 수정 |
| PATCH | `/api/v1/itineraries/{itinerary_id}/items/reorder` | 일정 순서 변경 |
| DELETE | `/api/v1/itineraries/{itinerary_id}` | 일정 삭제 |

### Place

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/v1/places/search` | 장소 검색 |
| GET | `/api/v1/places/{place_id}` | 장소 상세 |
| GET | `/api/v1/places/{place_id}/nearby` | 주변 장소 추천 |

### Review / Tip

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/v1/places/{place_id}/reviews` | 리뷰 작성 |
| GET | `/api/v1/places/{place_id}/reviews` | 리뷰 조회 |
| GET | `/api/v1/places/{place_id}/tips` | 팁 조회 |
| POST | `/api/v1/places/{place_id}/tips` | 팁 작성 |

### Budget

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/v1/itineraries/{itinerary_id}/budget` | 예산 조회 |
| PATCH | `/api/v1/itineraries/{itinerary_id}/budget` | 예산 수정 |
| POST | `/api/v1/itineraries/{itinerary_id}/split-bill` | 더치페이 계산 |

### Notification

| Method | Endpoint | 설명 |
|---|---|---|
| POST | `/api/v1/notifications` | 알림 생성 |
| GET | `/api/v1/notifications` | 알림 목록 |
| DELETE | `/api/v1/notifications/{notification_id}` | 알림 삭제 |

## 5. AI 일정 생성 API 처리 순서

```text
POST /api/v1/itineraries/ai-generate
  1. 사용자 인증 확인
  2. 요청 스키마 검증
  3. 사용자 취향 정규화
  4. 후보 장소 검색
  5. LLM 일정 생성 요청
  6. 장소 좌표 검증
  7. 이동 경로 계산
  8. 예산 추정
  9. DB 저장
  10. 일정 상세 응답
```

## 6. SNS 일정 생성 API 처리 순서

```text
POST /api/v1/itineraries/from-sns
  1. 사용자 인증 확인
  2. URL 검증
  3. 게시물 텍스트 수집
  4. 장소 후보 추출
  5. 지도 API로 장소 검증
  6. 일정 또는 장소 리스트 생성
  7. DB 저장
  8. 지도 표시 데이터 응답
```
