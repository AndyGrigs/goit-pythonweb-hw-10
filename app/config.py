
from pydantic_settings import BaseSettings 
from typing import Optional

class Settings(BaseSettings):
    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "contacts_db"
    db_user: str = "contacts_user"
    db_password: str = "contacts_password"
    
    # Application
    app_name: str = "Contact Management API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security
    secret_key: str = "your-secret-key-here"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()