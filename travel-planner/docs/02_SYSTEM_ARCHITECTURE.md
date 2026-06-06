# 시스템 아키텍처 설계

## 1. 전체 구조

```text
Client
  ├─ Web / Mobile App
  └─ Map UI

Backend - FastAPI
  ├─ Auth Module
  ├─ User Preference Module
  ├─ AI Itinerary Module
  ├─ SNS Parser Module
  ├─ Place Module
  ├─ Map/Route Module
  ├─ Schedule Module
  ├─ Review/Tip Module
  ├─ Budget Module
  ├─ Notification Module
  └─ Collaboration Module

External APIs
  ├─ LLM API (Claude / OpenAI)
  ├─ Google Maps API
  ├─ Kakao Map API
  ├─ Blog/SNS Data Source
  ├─ Ticket/Reservation Links
  └─ Payment APIs (KakaoPay, Toss)

Data Layer
  ├─ PostgreSQL (주 데이터)
  ├─ Redis (캐시, 세션, 큐)
  └─ Object Storage (이미지 등)
```

---

## 2. 기본 요청 흐름

```text
사용자 입력
  ↓
FastAPI Router  (endpoint만 담당)
  ↓
Service Layer   (비즈니스 로직)
  ↓
Repository Layer (DB 접근)
  ↓
Database / External API
  ↓
Response Schema (Pydantic 검증)
  ↓
Client
```

---

## 3. AI 일정 생성 흐름

```text
POST /api/v1/itineraries/ai-generate
  ↓
사용자 인증 확인
  ↓
Preference Normalizer
  ↓
Candidate Place Search (Google Maps / Kakao)
  ↓
LLM Itinerary Generator
  ↓
Route Optimizer
  ↓
Budget Estimator
  ↓
Itinerary 저장 (PostgreSQL)
  ↓
지도/일정표 응답
```

---

## 4. SNS 기반 일정 생성 흐름

```text
POST /api/v1/itineraries/from-sns
  ↓
URL Validator
  ↓
Crawler 또는 Parser
  ↓
Text Extractor
  ↓
Place Entity Extractor (LLM 활용)
  ↓
Map API Geocoding
  ↓
Place Deduplication
  ↓
Itinerary Generator
  ↓
DB 저장 & 응답
```

---

## 5. 실시간 공동 편집 흐름

```text
사용자 A 일정 수정
  ↓
WebSocket Event 발생
  ↓
Schedule Service 검증
  ↓
DB 저장
  ↓
초대 사용자들에게 변경 사항 Broadcast
  ↓
지도와 일정표 UI 갱신
```

---

## 6. 레이어 역할 정의

| 레이어 | 역할 |
|---|---|
| Router | API endpoint 수신, 인증 의존성 확인, Service 호출 |
| Service | 핵심 비즈니스 로직, Repository/Client 조합, 트랜잭션 관리 |
| Repository | DB 접근 전담 (SQLAlchemy/SQLModel 쿼리) |
| Client | 외부 API 호출 전담 (Google Maps, Kakao, LLM 등) |
| Schema | Pydantic Request/Response 모델 정의 |
| Model | SQLAlchemy DB 테이블 정의 |
| Worker | 비동기 장시간 작업 (Celery/RQ) |

---

## 7. 폴더 구조

```text
travel-planner/
├── app/
│   ├── main.py                   # FastAPI 앱 진입점
│   ├── core/
│   │   ├── config.py             # 환경변수, 설정
│   │   ├── database.py           # DB 연결, 세션
│   │   ├── security.py           # JWT, 패스워드 해싱
│   │   └── exceptions.py         # 공통 예외 클래스
│   ├── common/
│   │   ├── response.py           # 공통 응답 포맷
│   │   └── utils.py              # 공통 유틸
│   ├── auth/                     # 인증 모듈
│   ├── users/                    # 사용자/취향 모듈
│   ├── itineraries/              # 일정 모듈
│   ├── places/                   # 장소 모듈
│   ├── reviews/                  # 리뷰/팁 모듈
│   ├── budget/                   # 예산 모듈
│   ├── notifications/            # 알림 모듈
│   ├── ai/                       # AI 일정 생성, 리뷰 요약
│   └── clients/                  # 외부 API 클라이언트
├── migrations/                   # Alembic 마이그레이션
├── tests/                        # 테스트
├── docs/                         # 설계 문서
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
