# 모듈화 설계

## 1. 기본 원칙

- 한 Python 파일은 500줄 이하로 유지한다.
- Router, Service, Repository, Schema, Model을 분리한다.
- 외부 API 호출 코드는 `clients/` 폴더에 둔다.
- AI 프롬프트는 코드와 분리하여 `prompts/` 또는 별도 모듈에서 관리한다.
- 크롤링/파싱처럼 오래 걸리는 작업은 Worker로 분리한다.

## 2. 추천 폴더 구조

```text
app/
  main.py
  core/
    config.py
    security.py
    exceptions.py
  db/
    session.py
    base.py
  models/
    user.py
    place.py
    itinerary.py
    review.py
    budget.py
  schemas/
    user.py
    place.py
    itinerary.py
    review.py
    budget.py
  routers/
    auth.py
    users.py
    itineraries.py
    places.py
    sns.py
    reviews.py
    budgets.py
    notifications.py
  services/
    auth_service.py
    preference_service.py
    itinerary_service.py
    ai_itinerary_service.py
    sns_parser_service.py
    map_service.py
    route_service.py
    review_service.py
    budget_service.py
    notification_service.py
  repositories/
    user_repository.py
    place_repository.py
    itinerary_repository.py
    review_repository.py
    budget_repository.py
  clients/
    llm_client.py
    google_maps_client.py
    kakao_map_client.py
    ticket_client.py
    payment_client.py
  workers/
    crawler_worker.py
    itinerary_worker.py
  prompts/
    itinerary_prompt.py
    review_summary_prompt.py
  utils/
    date_utils.py
    geo_utils.py
    text_utils.py
tests/
  test_itineraries.py
  test_places.py
  test_sns.py
```

## 3. 주요 모듈 역할

### Auth Module
- 회원가입
- 로그인
- JWT 발급
- OAuth 연동

### User Preference Module
- 사용자 취향 저장
- 여행 목적 저장
- 여행 이력 관리

### AI Itinerary Module
- LLM 프롬프트 생성
- 일정 생성
- 일정 품질 검증
- 장소 순서 최적화

### SNS Parser Module
- URL 검증
- 게시물 텍스트 수집
- 장소명 추출
- 지도 API와 매칭

### Place Module
- 장소 검색
- 장소 상세정보 조회
- 카테고리 분류
- 주변 장소 추천

### Map/Route Module
- 위도/경도 변환
- 이동 거리 계산
- 이동 시간 계산
- 경로 표시 데이터 생성

### Schedule Module
- 일정 생성
- 일정 조회
- 일정 수정
- 드래그 앤 드롭 순서 변경
- 공동 편집 이벤트 처리

### Review/Tip Module
- 리뷰 작성
- 비추/쏘쏘/강추 평가
- AI 리뷰 요약
- 사용자 팁 관리

### Budget Module
- 예상 예산 계산
- 카테고리별 예산 집계
- 더치페이 계산

### Notification Module
- 일정 알람
- 예약 알람
- 일정 변경 알림
