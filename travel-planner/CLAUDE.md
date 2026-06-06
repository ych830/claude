# CLAUDE.md

이 파일은 새 세션에서 작업을 이어갈 때 읽는 **프로젝트 가이드**입니다.
컨텍스트가 클리어되어도 이 파일을 먼저 읽으면 맥락을 복원할 수 있습니다.

---

## 0. 작업 규칙 (반드시 지킬 것)

1. **뭘 하기 전에 먼저 사용자에게 질문한다.** 임의로 진행하지 않는다.
2. **기능 명세서와 매뉴얼에 기반해서 작업한다.** (`docs/original/` 기준)
3. **사용자 요청과 명세가 다르면 "틀렸다"고 말한다.** 명세를 바꾸지 말고 **코드를 수정**한다.
4. **`docs/original/` 안의 파일은 절대 수정하지 않는다.** 업로드된 원본 명세서 보존본이다.
5. **한 Python 파일은 500줄 이하**로 유지한다. 넘어가면 Router/Service/Repository/Schema/Helper로 분리한다.
6. REST API로 구현한다. 기능별로 하나씩 나눠서 차근차근 스텝별로 개발한다.
7. 작업 단위가 끝나면 커밋 & 푸시한다. 브랜치: `claude/adoring-hawking-kvwoE`

---

## 1. 프로젝트 개요

사용자의 취향, SNS 게시물, 지도 정보를 기반으로 **개인화된 AI 여행 일정**을 생성하는
FastAPI 백엔드 서비스.

### 기술 스택
| 영역 | 기술 |
|---|---|
| Backend | Python 3.12, FastAPI |
| DB | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (Async) |
| Migration | Alembic |
| Cache/Queue | Redis, Celery |
| AI | Anthropic Claude API |
| 지도 | Google Maps API, Kakao Map API |
| 인증 | JWT, Kakao OAuth |
| 협업 편집 | WebSocket |
| 배포 | Docker, Nginx |

---

## 2. 폴더 구조 결정사항

**기능별 분리 구조**를 채택했다. (레이어별 구조 `models/`, `services/` 가 아님)

> 결정 이유: 한 기능을 수정할 때 관련 파일(router/service/repository/schema/model)이
> 한 폴더 안에 모여 있어 탐색·유지보수가 쉽다. FastAPI 대형 프로젝트 표준 패턴.
> 원본 `03_MODULE_DESIGN.md`는 레이어별 구조를 제안했으나, 사용자 승인 하에 기능별로 변경함.
> (명세서 자체는 보존, 코드 구조만 더 나은 방향으로 결정)

```text
travel-planner/
├── app/
│   ├── main.py                # FastAPI 진입점, 라우터 등록, 예외 핸들러
│   ├── core/
│   │   ├── config.py          # 환경변수 (pydantic-settings)
│   │   ├── database.py        # async engine, get_db 세션
│   │   ├── security.py        # JWT 발급/검증, 비밀번호 해싱
│   │   └── exceptions.py      # 공통 예외 클래스
│   ├── common/
│   │   ├── response.py        # 공통 응답 포맷 ok(), 예외 핸들러
│   │   └── utils.py           # new_uuid, utcnow, is_valid_url
│   ├── auth/                  # [완료] 회원가입/로그인/JWT/카카오 OAuth
│   │   ├── model.py           # User 테이블
│   │   ├── schema.py          # Signup/Login/Token 스키마
│   │   ├── repository.py      # User DB 접근
│   │   ├── service.py         # 인증 비즈니스 로직
│   │   ├── router.py          # /api/v1/auth/*
│   │   └── dependencies.py    # get_current_user 의존성
│   ├── users/                 # [완료] 내 정보/취향/여행이력
│   │   ├── model.py           # UserPreference, TravelHistory 테이블
│   │   ├── schema.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── router.py          # /api/v1/users/*
│   ├── itineraries/           # [비어있음] 일정 CRUD + AI 생성
│   ├── places/                # [비어있음] 장소 검색/추천  ← 다음 작업
│   ├── reviews/               # [비어있음] 리뷰/팁
│   ├── budget/                # [비어있음] 예산/더치페이
│   ├── notifications/         # [비어있음] 알림
│   ├── ai/                    # [비어있음] LLM 일정 생성, 리뷰 요약
│   └── clients/               # [비어있음] 외부 API 클라이언트
├── docs/
│   ├── original/              # ★ 원본 명세서 보존 (절대 수정 금지)
│   └── 01~07_*.md             # 개발용 참고 문서
├── migrations/                # [비어있음] Alembic
├── tests/
│   ├── conftest.py            # httpx 비동기 클라이언트 픽스처
│   └── test_auth.py           # auth service 단위 테스트
├── .env.example
├── docker-compose.yml         # app + postgres + redis
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

---

## 3. 진행 현황 (원본 07_IMPLEMENTATION_ROADMAP.md 기준)

| Phase | 내용 | 상태 |
|---|---|---|
| Phase 1 | 프로젝트 초기 세팅 (구조, 환경변수, DB, 공통 응답/예외) | ✅ 완료 |
| Phase 2 | 사용자/인증 (User, Preference, 회원가입, 로그인, JWT, 내 정보) | 🟡 코드 완료, **Alembic 마이그레이션 미완** |
| Phase 3 | 장소/지도 (Place 모델, 검색 API, Google/Kakao Client, Geocoding) | ⬜ **다음 작업** |
| Phase 4 | AI 일정 생성 MVP | ⬜ |
| Phase 5 | 일정 수정 | ⬜ |
| Phase 6 | SNS 링크 기반 일정 생성 | ⬜ |
| Phase 7 | 공동 편집 (WebSocket) | ⬜ |
| Phase 8 | 리뷰/팁/관광지 정보 | ⬜ |
| Phase 9 | 예산/알람/더치페이 | ⬜ |
| Phase 10 | 배포 준비 | ⬜ |

### 아직 안 된 것 (주의)
- **Alembic 마이그레이션 미설정** → 현재 DB 테이블 생성 안 됨. Phase 2 완료 기준 미충족.
- `/health` 는 동작하지만 실제 DB 연결 테스트는 미검증.
- 의존성 설치(`pip install -r requirements.txt`) 및 실행 검증 안 됨.

---

## 4. API 규칙 (원본 04_API_PROCESS.md 기준)

- 모든 API는 `/api/v1` prefix 사용.
- 성공 응답: `{"success": true, "data": {}, "message": "OK"}`
- 에러 응답: `{"success": false, "error": {"code": "...", "message": "..."}}`
- 인증 필요 API는 JWT Bearer Token.

### 구현된 엔드포인트
```
POST /api/v1/auth/signup
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/oauth/kakao
GET  /api/v1/users/me
PUT  /api/v1/users/me/preferences
GET  /api/v1/users/me/travel-history
POST /api/v1/users/me/travel-history
GET  /health
```

---

## 5. DB 모델 명세 (원본 05_DATABASE_DESIGN.md 기준)

원본이 정의한 엔티티:
`User, Preference, TravelHistory, Place, Itinerary, ItineraryDay, ItineraryItem,
Review, Tip, Budget, Notification, Invitation, SplitBill`

### 구현된 모델
- `User` (auth/model.py)
- `UserPreference`, `TravelHistory` (users/model.py)

> 참고: 원본 명세의 Preference 필드명은 `travel_purposes, companion_type,
> preferred_transport, budget_level, disliked_categories`.
> 현재 코드는 `travel_styles, companion_type, transport_pref, budget_range` 로 일부 다름.
> **다음에 맞출지 사용자에게 확인 필요.** (TODO)

### 다음에 만들 모델 (Phase 3)
`Place` — id, name, category, address, latitude, longitude, opening_hours(json),
ticket_price(json), source

---

## 6. 다음 스텝

**Phase 3: 장소/지도 기본 기능** (원본 로드맵 기준)

작업 항목:
1. `places/model.py` — Place 모델 (원본 05 명세 필드 기준)
2. `clients/google_maps_client.py` — Google Maps Geocoding/Places
3. `clients/kakao_map_client.py` — Kakao 로컬 검색
4. `places/schema.py`, `repository.py`, `service.py`, `router.py`
5. 장소 검색 API: `GET /api/v1/places/search`, `GET /api/v1/places/{id}`,
   `GET /api/v1/places/{id}/nearby`

완료 기준: 장소명 입력 시 좌표를 저장할 수 있고, 일정에 등록된 장소를
지도에 표시할 데이터를 반환한다.

> **작업 시작 전 사용자에게 먼저 질문할 것:**
> - 외부 API는 mock으로 갈지 실제 키 연동을 가정할지
> - Preference 필드명을 원본 명세에 맞게 수정할지

---

## 7. 커밋 규칙 (원본 06_DEV_RULES.md 기준)

```text
feat: 기능 추가
fix: 버그 수정
docs: 문서
refactor: 리팩터링
test: 테스트
chore: 설정
```
브랜치: `claude/adoring-hawking-kvwoE` 에 개발 → 커밋 → 푸시.
