from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(status_code=status_code, detail={"code": code, "message": message})


class UnauthorizedException(AppException):
    def __init__(self, message: str = "인증이 필요합니다."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED", message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "권한이 없습니다."):
        super().__init__(status.HTTP_403_FORBIDDEN, "FORBIDDEN", message)


class NotFoundException(AppException):
    def __init__(self, message: str = "리소스를 찾을 수 없습니다."):
        super().__init__(status.HTTP_404_NOT_FOUND, "NOT_FOUND", message)


class ConflictException(AppException):
    def __init__(self, message: str = "이미 존재하는 리소스입니다."):
        super().__init__(status.HTTP_409_CONFLICT, "CONFLICT", message)


class BadRequestException(AppException):
    def __init__(self, message: str = "잘못된 요청입니다."):
        super().__init__(status.HTTP_400_BAD_REQUEST, "INVALID_REQUEST", message)


class ExternalAPIException(AppException):
    def __init__(self, message: str = "외부 서비스 오류가 발생했습니다."):
        super().__init__(status.HTTP_502_BAD_GATEWAY, "EXTERNAL_API_ERROR", message)
