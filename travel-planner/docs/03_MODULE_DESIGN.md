# 모듈화 설계

## 모듈 목록 및 역할

| 모듈 | 경로 | 역할 |
|---|---|---|
| auth | app/auth/ | 회원가입, 로그인, JWT, OAuth |
| users | app/users/ | 사용자 정보, 취향, 여행 이력 |
| itineraries | app/itineraries/ | 일정 CRUD, AI 생성, SNS 생성 |
| places | app/places/ | 장소 검색, 상세, 주변 추천 |
| reviews | app/reviews/ | 리뷰 작성/조회, 팁 작성/조회 |
| budget | app/budget/ | 예산 계산, 더치페이 |
| notifications | app/notifications/ | 알림 생성/조회/삭제 |
| ai | app/ai/ | LLM 일정 생성, 리뷰 요약 |
| clients | app/clients/ | Google Maps, Kakao, LLM API 클라이언트 |
| core | app/core/ | 설정, DB, 보안, 예외 |
| common | app/common/ | 공통 응답 포맷, 유틸 |

---

## 각 모듈 파일 구성

각 기능 모듈(auth, users, itineraries, places, reviews, budget, notifications)은 아래 파일로 구성됩니다:

```
{module}/
├── __init__.py
├── router.py       # API endpoint (500줄 이하 유지)
├── service.py      # 비즈니스 로직 (500줄 이하 유지)
├── repository.py   # DB 쿼리 (500줄 이하 유지)
├── schema.py       # Pydantic Request/Response
└── model.py        # SQLAlchemy 테이블 정의
```

500줄 초과 시 다음 기준으로 분리:
- `router_v2.py`, `service_helpers.py`, `repository_queries.py` 등으로 분리

---

## 개발 순서 (우선순위)

1. **[완료]** 프로젝트 기초 세팅 (폴더 구조, 환경변수, Docker)
2. **[진행 중]** core 모듈 (config, database, security, exceptions)
3. auth 모듈 (회원가입, 로그인, JWT)
4. users 모듈 (사용자 정보, 취향)
5. places 모듈 (장소 검색, 카테고리)
6. itineraries 모듈 (CRUD, AI 생성)
7. ai 모듈 (LLM 연동, 일정 생성)
8. clients 모듈 (Google Maps, Kakao 연동)
9. reviews 모듈
10. budget 모듈
11. notifications 모듈
12. WebSocket 공동 편집
13. SNS 파서 모듈
