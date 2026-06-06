from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.model import User
from app.auth.repository import AuthRepository
from app.core.database import get_db
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_token

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedException()

    user_id = payload.get("sub")
    repo = AuthRepository(db)
    user = await repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise UnauthorizedException("사용자를 찾을 수 없습니다.")
    return user
