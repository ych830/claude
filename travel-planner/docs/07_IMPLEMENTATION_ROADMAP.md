# 구현 로드맵

## Phase 1 - 기초 세팅 (현재)

- [x] 프로젝트 폴더 구조 생성
- [x] 설계 문서 작성 (docs/)
- [x] 환경변수 설정 (.env.example)
- [x] Docker 설정 (docker-compose.yml, Dockerfile)
- [x] 의존성 정의 (requirements.txt)
- [x] FastAPI 앱 진입점 (app/main.py)
- [x] core 모듈 (config, database, security, exceptions)
- [x] 공통 응답 포맷 (common/response.py)

## Phase 2 - 인증 및 사용자

- [ ] auth 모듈 (회원가입, 로그인, JWT 발급)
- [ ] OAuth (카카오 로그인)
- [ ] users 모듈 (내 정보, 취향 설정)
- [ ] Alembic 마이그레이션 설정
- [ ] auth/users 단위 테스트

## Phase 3 - 장소 및 일정 기본

- [ ] places 모듈 (장소 검색, 상세, 주변 추천)
- [ ] Google Maps Client
- [ ] Kakao Map Client
- [ ] itineraries 모듈 (CRUD)
- [ ] 일정 상세/수정/삭제 API

## Phase 4 - AI 일정 생성

- [ ] LLM Client 구현
- [ ] ai/itinerary_generator.py
- [ ] POST /api/v1/itineraries/ai-generate 완성
- [ ] 예산 추정 로직
- [ ] 경로 최적화 로직

## Phase 5 - SNS 파서

- [ ] SNS/블로그 크롤러
- [ ] 텍스트에서 장소 추출 (LLM 활용)
- [ ] POST /api/v1/itineraries/from-sns 완성

## Phase 6 - 리뷰 및 예산

- [ ] reviews 모듈 (리뷰, 팁 CRUD)
- [ ] ai/review_summarizer.py
- [ ] budget 모듈 (예산 계산, 더치페이)

## Phase 7 - 알림 및 협업

- [ ] notifications 모듈
- [ ] WebSocket 공동 편집
- [ ] 실시간 지도 반영

## Phase 8 - 배포

- [ ] Docker Compose 최종 설정
- [ ] Nginx 리버스 프록시
- [ ] Cloud VM 배포 (또는 managed service)
- [ ] 환경별 설정 분리 (local, staging, production)
