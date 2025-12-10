from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # For async postgres, the URL should be in the format:
    # "postgresql+asyncpg://user:password@host:port/dbname"    
    DATABASE_URL: str = "postgresql+asyncpg://neondb_owner:npg_y1lw7LhaEdep@ep-green-forest-ad3av5lu-pooler.c-2.us-east-1.aws.neon.tech/neondb"
    ALEMBIC_DATABASE_URL: str | None = None
    ADMIN_EMAIL: str = "admin@admin.com"
    ADMIN_PASSWORD: str = "admin123"
    SECRET_KEY: str = "Supremeboss232"  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @model_validator(mode='after')
    def set_alembic_database_url(self) -> 'Settings':
        if self.DATABASE_URL and not self.ALEMBIC_DATABASE_URL:
            self.ALEMBIC_DATABASE_URL = self.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
        return self

settings = Settings()