# AI 여행 일정 생성 앱 - Travel Planner

사용자의 취향, SNS 게시물, 지도 정보를 기반으로 개인화된 여행 일정을 생성하는 FastAPI 백엔드 서비스입니다.

## 기술 스택

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

## 빠른 시작

```bash
# 환경변수 설정
cp .env.example .env
# .env 파일 편집 후

# Docker로 실행
docker-compose up -d

# API 문서 확인
open http://localhost:8000/docs
```

## 프로젝트 구조

```
travel-planner/
├── app/
│   ├── main.py               # FastAPI 앱 진입점
│   ├── core/                 # 설정, DB, 보안, 예외
│   ├── common/               # 공통 응답 포맷, 유틸
│   ├── auth/                 # 인증 (회원가입/로그인/JWT/OAuth)
│   ├── users/                # 사용자 정보 및 취향
│   ├── itineraries/          # 여행 일정 CRUD + AI 생성
│   ├── places/               # 장소 검색 및 추천
│   ├── reviews/              # 리뷰 및 팁
│   ├── budget/               # 예산 계산 및 더치페이
│   ├── notifications/        # 알림
│   ├── ai/                   # LLM 일정 생성, 리뷰 요약
│   └── clients/              # 외부 API 클라이언트
├── docs/                     # 설계 문서
├── tests/                    # 테스트
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 설계 문서

- [01 제품 기능 매뉴얼](docs/01_PRODUCT_MANUAL.md)
- [02 시스템 아키텍처](docs/02_SYSTEM_ARCHITECTURE.md)
- [03 모듈화 설계](docs/03_MODULE_DESIGN.md)
- [04 API 프로세스](docs/04_API_PROCESS.md)
- [05 데이터베이스 설계](docs/05_DATABASE_DESIGN.md)
- [06 개발 규칙](docs/06_DEV_RULES.md)
- [07 구현 로드맵](docs/07_IMPLEMENTATION_ROADMAP.md)

## 개발 진행 현황

- [x] Phase 1: 기초 세팅 (폴더 구조, 환경변수, Docker, core 모듈)
- [x] Phase 1: auth 모듈 (회원가입, 로그인, JWT, 카카오 OAuth)
- [x] Phase 1: users 모듈 (내 정보, 취향 설정, 여행 이력)
- [ ] Phase 2: places 모듈
- [ ] Phase 3: itineraries 모듈 + AI 생성
- [ ] Phase 4: reviews, budget, notifications
- [ ] Phase 5: WebSocket 공동 편집, SNS 파서
