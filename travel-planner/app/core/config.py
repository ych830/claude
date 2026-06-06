from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Travel Planner API"
    app_version: str = "0.1.0"
    app_env: str = "local"

    database_url: str
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    llm_api_key: str = ""
    llm_model: str = "claude-sonnet-4-6"

    google_maps_api_key: str = ""
    kakao_rest_api_key: str = ""
    kakao_client_id: str = ""
    kakao_client_secret: str = ""
    kakao_redirect_uri: str = "http://localhost:8000/api/v1/auth/oauth/kakao/callback"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
