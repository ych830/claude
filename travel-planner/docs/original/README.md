# AI 여행 일정 생성 앱 설계 문서

## 1. 프로젝트 개요

이 프로젝트는 사용자의 취향, SNS 게시물, 지도 정보, 관광지 실시간 정보 등을 기반으로 개인화된 여행 일정을 생성하고 수정할 수 있는 여행 플래너 서비스입니다.

백엔드는 Python + FastAPI 기반으로 개발하며, 기능별 모듈화를 원칙으로 합니다.  
각 Python 파일은 유지보수성을 위해 500줄 이하로 관리합니다.

## 2. 핵심 목표

- 사용자 취향 기반 AI 여행 일정 생성
- SNS 링크 기반 여행 일정 생성
- 지도 기반 일정 시각화
- 일정표 열람, 수정, 공동 편집
- 관광지 실시간 정보 및 사용자 팁 제공
- 카테고리 기반 장소 추천
- 평균 예산 계산
- 알람 및 선택적 더치페이 기능

## 3. 우선 개발 순서

1. 기본 프로젝트 구조 및 인증/사용자 모델 설계
2. 장소/일정 데이터 모델 설계
3. AI 일정 생성 모듈 구현
4. 지도 API 연동
5. 일정 수정 및 저장 기능 구현
6. SNS 링크 파싱 모듈 구현
7. 관광지 정보/리뷰/팁 기능 구현
8. 예산/알람/더치페이 확장 기능 구현

## 4. 기술 스택 초안

| 영역 | 기술 |
|---|---|
| Backend | Python, FastAPI |
| DB | PostgreSQL |
| ORM | SQLAlchemy 또는 SQLModel |
| Migration | Alembic |
| Cache/Queue | Redis, Celery 또는 RQ |
| AI | LLM API |
| 지도 | Google Maps API, Kakao Map API |
| 인증 | JWT, OAuth |
| 협업 편집 | WebSocket |
| 배포 | Docker, Nginx, Cloud VM 또는 managed service |

## 5. 문서 구성

- `01_PRODUCT_MANUAL.md`: 제품 기능 매뉴얼
- `02_SYSTEM_ARCHITECTURE.md`: 시스템 아키텍처
- `03_MODULE_DESIGN.md`: 모듈화 설계
- `04_API_PROCESS.md`: API 처리 흐름
- `05_DATABASE_DESIGN.md`: 데이터베이스 설계
- `06_DEV_RULES.md`: 개발 규칙
- `07_IMPLEMENTATION_ROADMAP.md`: 구현 로드맵
