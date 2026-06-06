# 개발 규칙

## 1. 코드 길이 규칙

- Python 파일 하나는 500줄 이하로 작성한다.
- 500줄에 가까워지면 다음 기준으로 분리한다.
  - Router 분리
  - Service 분리
  - Repository 분리
  - Schema 분리
  - Helper/Util 분리

## 2. 레이어 규칙

### Router
- 요청을 받는다.
- 인증 의존성을 확인한다.
- Service를 호출한다.
- 비즈니스 로직을 넣지 않는다.

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

## 3. 네이밍 규칙

- 파일명: snake_case
- 클래스명: PascalCase
- 함수명: snake_case
- API endpoint: kebab-case 또는 snake_case 중 하나로 통일
- DB table: snake_case 복수형 권장

## 4. 예외 처리 규칙

- 공통 예외 클래스를 만든다.
- 외부 API 실패 시 사용자에게 직접 raw error를 노출하지 않는다.
- 로그에는 상세 에러를 남기고 응답에는 안전한 메시지만 반환한다.

## 5. 환경변수 규칙

`.env` 예시:

```env
APP_ENV=local
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/travel_app
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=change-me
LLM_API_KEY=change-me
GOOGLE_MAPS_API_KEY=change-me
KAKAO_REST_API_KEY=change-me
```

## 6. Git 브랜치 규칙

```text
main
develop
feature/auth
feature/itinerary-ai
feature/sns-parser
feature/map-route
feature/review-tip
feature/budget
feature/notification
```

## 7. 커밋 메시지 규칙

```text
feat: AI 일정 생성 API 추가
fix: 장소 좌표 검증 오류 수정
docs: API 프로세스 문서 추가
refactor: 일정 서비스 모듈 분리
test: 장소 검색 테스트 추가
```

## 8. 테스트 규칙

- Service 단위 테스트 필수
- API Router 테스트 권장
- 외부 API는 mock 처리
- 크롤링/SNS 파싱은 샘플 HTML 기반 테스트 작성
