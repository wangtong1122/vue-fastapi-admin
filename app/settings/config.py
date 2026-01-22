import os
import typing

from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_cors_origins(value: typing.Any) -> list[str]:
    """Parse CORS origins from env/config.

    Supports:
    - "*"
    - comma-separated string: "https://a.com,https://b.com"
    - JSON array string: '["https://a.com", "https://b.com"]'
    - python list/tuple
    """
    if value is None:
        return []

    if isinstance(value, (list, tuple, set)):
        return [str(v).strip() for v in value if str(v).strip()]

    s = str(value).strip()
    if not s:
        return []

    if s == "*":
        return ["*"]

    # Try JSON array
    if s.startswith("["):
        try:
            import json

            data = json.loads(s)
            if isinstance(data, list):
                return [str(v).strip() for v in data if str(v).strip()]
        except Exception:
            # fall back to comma-splitting
            pass

    # Comma-separated
    return [item.strip() for item in s.split(",") if item.strip()]


class Settings(BaseSettings):
    # Load from `.env` (local dev) and real environment variables (prod)
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)), ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    VERSION: str = "0.1.0"
    APP_TITLE: str = "Vue FastAPI Admin"
    PROJECT_NAME: str = "Vue FastAPI Admin"
    APP_DESCRIPTION: str = "Description"

    # CORS_ORIGINS supports:
    # - "*"
    # - comma-separated string: "http://localhost:5173,http://127.0.0.1:5173"
    # - JSON array string: '["http://localhost:5173"]'
    CORS_ORIGINS: typing.Any = ["*"]

    @property
    def cors_origins_list(self) -> list[str]:
        return _parse_cors_origins(self.CORS_ORIGINS)

    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List = ["*"]
    CORS_ALLOW_HEADERS: typing.List = ["*"]

    DEBUG: bool = True

    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")

    # --- Security ---
    # Keep secrets out of source control. Configure via environment variables or `.env`.
    SECRET_KEY: str = "change-me"  # Generate: python -c "import secrets; print(secrets.token_hex(32))"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 day

    # --- Database (MySQL) ---
    DB_CONNECTION_NAME: str = "mysql"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "change-me"
    DB_NAME: str = "vue_fastapi_admin"
    # Optional DSN override. If set, it will be used directly.
    DB_DSN: str = ""

    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    @property
    def TORTOISE_ORM(self) -> dict:
        credentials: dict
        if self.DB_DSN:
            # Tortoise MySQL backend supports a DSN string in credentials.
            credentials = {"dsn": self.DB_DSN}
        else:
            credentials = {
                "host": self.DB_HOST,
                "port": self.DB_PORT,
                "user": self.DB_USER,
                "password": self.DB_PASSWORD,
                "database": self.DB_NAME,
            }

        return {
            "connections": {
                self.DB_CONNECTION_NAME: {
                    "engine": "tortoise.backends.mysql",
                    "credentials": credentials,
                },
            },
            "apps": {
                "models": {
                    "models": ["app.models", "aerich.models"],
                    "default_connection": self.DB_CONNECTION_NAME,
                },
            },
            "use_tz": False,
            "timezone": "Asia/Shanghai",
        }


settings = Settings()
