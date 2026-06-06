import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthRepository
from app.auth.schema import TokenResponse
from app.core.config import settings
from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    UnauthorizedException,
    ExternalAPIException,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = AuthRepository(db)

    async def signup(self, email: str, password: str, name: str) -> TokenResponse:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ConflictException("이미 사용 중인 이메일입니다.")

        hashed = hash_password(password)
        user = await self.repo.create(email=email, hashed_password=hashed, name=name)
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self.repo.get_by_email(email)
        if not user or not user.hashed_password:
            raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다.")
        if not verify_password(password, user.hashed_password):
            raise UnauthorizedException("이메일 또는 비밀번호가 올바르지 않습니다.")
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("유효하지 않은 토큰입니다.")

        user_id = payload.get("sub")
        user = await self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("사용자를 찾을 수 없습니다.")

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def kakao_login(self, code: str) -> TokenResponse:
        token_url = "https://kauth.kakao.com/oauth/token"
        async with httpx.AsyncClient() as client:
            try:
                token_res = await client.post(token_url, data={
                    "grant_type": "authorization_code",
                    "client_id": settings.kakao_client_id,
                    "client_secret": settings.kakao_client_secret,
                    "redirect_uri": settings.kakao_redirect_uri,
                    "code": code,
                })
                token_res.raise_for_status()
                kakao_token = token_res.json()["access_token"]

                profile_res = await client.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {kakao_token}"},
                )
                profile_res.raise_for_status()
                profile = profile_res.json()
            except httpx.HTTPError:
                raise ExternalAPIException("카카오 로그인 처리 중 오류가 발생했습니다.")

        kakao_id = str(profile["id"])
        kakao_account = profile.get("kakao_account", {})
        email = kakao_account.get("email", f"kakao_{kakao_id}@kakao.local")
        nickname = profile.get("properties", {}).get("nickname")
        profile_image = profile.get("properties", {}).get("profile_image")

        user = await self.repo.get_by_oauth("kakao", kakao_id)
        if not user:
            existing = await self.repo.get_by_email(email)
            if existing:
                raise ConflictException("이미 해당 이메일로 가입된 계정이 있습니다.")
            user = await self.repo.create(
                email=email,
                hashed_password=None,
                name=nickname,
                oauth_provider="kakao",
                oauth_id=kakao_id,
                profile_image=profile_image,
            )

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
