from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    KakaoOAuthRequest,
)
from app.auth.service import AuthService
from app.common.response import ok
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    tokens = await service.signup(body.email, body.password, body.name)
    return ok(tokens.model_dump(), "회원가입 성공")


@router.post("/login")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    tokens = await service.login(body.email, body.password)
    return ok(tokens.model_dump(), "로그인 성공")


@router.post("/refresh")
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    tokens = await service.refresh(body.refresh_token)
    return ok(tokens.model_dump(), "토큰 재발급 성공")


@router.post("/oauth/kakao")
async def kakao_oauth(body: KakaoOAuthRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    tokens = await service.kakao_login(body.code)
    return ok(tokens.model_dump(), "카카오 로그인 성공")
