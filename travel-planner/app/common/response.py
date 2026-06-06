from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.exceptions import AppException


class SuccessResponse(BaseModel):
    success: bool = True
    data: Any = None
    message: str = "OK"


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


def ok(data: Any = None, message: str = "OK") -> dict:
    return {"success": True, "data": data, "message": message}


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
        },
    )
