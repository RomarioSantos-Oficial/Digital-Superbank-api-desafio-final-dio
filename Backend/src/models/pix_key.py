from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, DateTime, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.connection import Base
import enum


class PixKeyType(str, enum.Enum):
    CPF = "CPF"
    CNPJ = "CNPJ"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    RANDOM = "RANDOM"  # Chave aleatória


class PixKey(Base):
    __tablename__ = "pix_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    key_type = Column(SQLEnum(PixKeyType), nullable=False)
    key_value = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="pix_keys")
    account = relationship("Account", back_populates="pix_keys")
    
    def __repr__(self):
        return f"<PixKey(id={self.id}, type={self.key_type}, value={self.key_value})>"
