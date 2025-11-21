"""
Modelo de Conta Bancária
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.connection import Base
import enum


class AccountType(str, enum.Enum):
    """Tipos de conta"""
    CORRENTE = "CORRENTE"
    POUPANCA = "POUPANCA"
    SALARIO = "SALARIO"
    UNIVERSITARIA = "UNIVERSITARIA"
    EMPRESARIAL = "EMPRESARIAL"
    INVESTIMENTO = "INVESTIMENTO"
    BLACK = "BLACK"


class Account(Base):
    """Modelo de conta bancária"""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False, index=True)
    account_type = Column(SQLEnum(AccountType), nullable=False)
    agency = Column(String(10), default="0001", nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    transactions_from = relationship(
        "Transaction",
        foreign_keys="Transaction.from_account_id",
        back_populates="from_account"
    )
    transactions_to = relationship(
        "Transaction",
        foreign_keys="Transaction.to_account_id",
        back_populates="to_account"
    )
    credit_cards = relationship("CreditCard", back_populates="account", cascade="all, delete-orphan")
    portfolio_items = relationship("PortfolioItem", back_populates="account", cascade="all, delete-orphan")
    pix_keys = relationship("PixKey", back_populates="account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Account(id={self.id}, number={self.account_number}, type={self.account_type})>"
