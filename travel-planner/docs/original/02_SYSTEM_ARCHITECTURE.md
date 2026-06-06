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
  ├─ LLM API
  ├─ Google Maps API
  ├─ Kakao Map API
  ├─ Blog/SNS Data Source
  ├─ Ticket/Reservation Links
  └─ Payment APIs

Data Layer
  ├─ PostgreSQL
  ├─ Redis
  └─ Object Storage
```

## 2. 기본 요청 흐름

```text
사용자 입력
  ↓
FastAPI Router
  ↓
Service Layer
  ↓
Repository Layer
  ↓
Database / External API
  ↓
Response Schema
  ↓
Client
```

## 3. AI 일정 생성 흐름

```text
사용자 취향 입력
  ↓
Preference Normalizer
  ↓
Candidate Place Search
  ↓
LLM Itinerary Generator
  ↓
Route Optimizer
  ↓
Budget Estimator
  ↓
Itinerary 저장
  ↓
지도/일정표 응답
```

## 4. SNS 기반 일정 생성 흐름

```text
SNS/블로그 링크 입력
  ↓
URL Validator
  ↓
Crawler 또는 Parser
  ↓
Text Extractor
  ↓
Place Entity Extractor
  ↓
Map API Geocoding
  ↓
Place Deduplication
  ↓
Itinerary Generator
```

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

## 6. 권장 아키텍처 스타일

- Router: API endpoint만 담당
- Service: 비즈니스 로직 담당
- Repository: DB 접근 담당
- Schema: 요청/응답 데이터 검증
- Model: DB 테이블 구조
- Client: 외부 API 호출 담당
- Worker: 오래 걸리는 작업 담당
