# 개발 규칙

## 1. 코드 길이 규칙

- Python 파일 하나는 **500줄 이하**로 작성한다.
- 전체 기능 파일은 **2000줄 이하**를 기준으로 모듈 분리를 검토한다.
- 500줄에 가까워지면 다음 기준으로 분리한다:
  - Router 분리
  - Service 분리
  - Repository 분리
  - Schema 분리
  - Helper/Util 분리

---

## 2. 레이어 규칙

### Router
- 요청을 받는다.
- 인증 의존성을 확인한다.
- Service를 호출한다.
- **비즈니스 로직을 넣지 않는다.**

### Service
- 핵심 비즈니스 로직을 담당한다.
- 여러 Repository와 Client를 조합한다.
- 트랜잭션 단위를 관리한다.

### Repository
- DB 접근만 담당한다.
- SQLAlchemy/SQLModel 쿼리를 작성한다.

### Client
- 외부 API 호출만 담당한다.
- Google Maps, Kakao Map, LLM API 등을 호출한다.

### Schema
- Pydantic Request/Response 모델만 정의한다.

---

## 3. 네이밍 규칙

| 대상 | 규칙 | 예시 |
|---|---|---|
| 파일명 | snake_case | `itinerary_service.py` |
| 클래스명 | PascalCase | `ItineraryService` |
| 함수명 | snake_case | `create_itinerary()` |
| API endpoint | snake_case | `/api/v1/itineraries/ai-generate` |
| DB 테이블명 | snake_case 복수형 | `itinerary_items` |
| 환경변수 | UPPER_SNAKE_CASE | `DATABASE_URL` |

---

## 4. 예외 처리 규칙

- 공통 예외 클래스를 `app/core/exceptions.py`에 정의한다.
- 외부 API 실패 시 raw error를 사용자에게 직접 노출하지 않는다.
- 로그에는 상세 에러를 남기고 응답에는 안전한 메시지만 반환한다.
- HTTP 상태코드를 의미에 맞게 사용한다:
  - 400: 잘못된 요청
  - 401: 미인증
  - 403: 권한 없음
  - 404: 리소스 없음
  - 422: 검증 실패
  - 500: 서버 내부 오류

---

## 5. 환경변수 규칙

`.env` 예시:
```env
APP_ENV=local
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/travel_app
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
LLM_API_KEY=change-me
LLM_MODEL=claude-sonnet-4-6
GOOGLE_MAPS_API_KEY=change-me
KAKAO_REST_API_KEY=change-me
KAKAO_CLIENT_ID=change-me
```

---

## 6. Git 브랜치 규칙

```text
main
develop
feature/auth
feature/users
feature/itinerary-ai
feature/itinerary-sns
feature/places
feature/reviews
feature/budget
feature/notifications
feature/websocket
```

---

## 7. 커밋 메시지 규칙

```text
feat: AI 일정 생성 API 추가
fix: 장소 좌표 검증 오류 수정
docs: API 프로세스 문서 추가
refactor: 일정 서비스 모듈 분리
test: 장소 검색 테스트 추가
chore: Docker 설정 추가
```

---

## 8. 테스트 규칙

- Service 단위 테스트 필수
- API Router 테스트 권장
- 외부 API는 mock 처리
- 크롤링/SNS 파싱은 샘플 HTML 기반 테스트 작성
- 테스트 파일명: `test_{module}.py`
