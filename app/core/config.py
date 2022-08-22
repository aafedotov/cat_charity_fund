from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Настройки фаст-апи проекта."""
    app_title: str = 'Фонд помощи котикам!'
    app_description: str = 'Сервис для пожертвований на кошачьи проекты'
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
