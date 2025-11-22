from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Boolean,
    Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.connection import Base
import enum


class TransactionType(str, enum.Enum):
    """Tipos de transação"""
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    PIX_SEND = "PIX_SEND"
    PIX_RECEIVE = "PIX_RECEIVE"
    BILL_PAYMENT = "BILL_PAYMENT"
    CARD_DEBIT = "CARD_DEBIT"
    CARD_CREDIT = "CARD_CREDIT"
    INVESTMENT_BUY = "INVESTMENT_BUY"
    INVESTMENT_SELL = "INVESTMENT_SELL"


class TransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(500))
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.COMPLETED)
    category = Column(String(50))  # Para categorização de gastos
    pix_key = Column(String(255))  # Chave PIX quando aplicável
    bar_code = Column(String(100))  # Código de barras para boletos
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="transactions_from")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="transactions_to")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"


class ScheduledTransaction(Base):
    __tablename__ = "scheduled_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(500))
    schedule_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="PENDING")  # PENDING, EXECUTED, FAILED
    bar_code = Column(String(100))
    pix_key = Column(String(255))
    is_recurring = Column(Boolean, default=False)
    recurrence_period = Column(String(20))  # DAILY, WEEKLY, MONTHLY, YEARLY
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<ScheduledTransaction(id={self.id}, schedule_date={self.schedule_date})>"
