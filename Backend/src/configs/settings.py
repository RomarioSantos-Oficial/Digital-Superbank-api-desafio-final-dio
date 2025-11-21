"""
Configurações da aplicação Digital Superbank
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # App
    APP_NAME: str = "Digital Superbank API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./src/database/data/digital_superbank.db"
    CHATBOT_DATABASE_URL: str = "sqlite:///./src/database/data/chatbot.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Bank Info
    BANK_CODE: str = "222"
    BANK_NAME: str = "Digital Superbank"
    DEFAULT_AGENCY: str = "0001"
    
    # Transaction Limits
    DAILY_WITHDRAWAL_LIMIT: float = 5000.00
    MAX_WITHDRAWALS_PER_DAY: int = 3
    MAX_WITHDRAWAL_AMOUNT: float = 2000.00
    
    # Account Types and Digits
    ACCOUNT_TYPES: dict = {
        "CORRENTE": 1,
        "POUPANCA": 3,
        "SALARIO": 4,
        "UNIVERSITARIA": 5,
        "EMPRESARIAL": 7,
        "INVESTIMENTO": 8,
        "BLACK": 9
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Permite campos extras do .env


settings = Settings()
