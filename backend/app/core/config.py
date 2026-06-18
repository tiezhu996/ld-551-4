from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduFlow"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://eduflow:eduflow@localhost:5432/eduflow"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    cors_origins: str = "http://localhost:38401,http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
