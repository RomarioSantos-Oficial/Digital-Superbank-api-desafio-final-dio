"""
Modelo de Cartão de Crédito
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.connection import Base


class CreditCard(Base):
    """Modelo de cartão de crédito"""
    __tablename__ = "credit_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    card_number = Column(String(19), unique=True, nullable=False)  # 16 dígitos formatados
    card_holder_name = Column(String(255), nullable=False)
    cvv = Column(String(4), nullable=False)
    expiry_date = Column(Date, nullable=False)
    credit_limit = Column(Float, nullable=False)
    available_limit = Column(Float, nullable=False)
    current_bill_amount = Column(Float, default=0.0)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, BLOCKED, CANCELLED
    is_virtual = Column(Boolean, default=False)
    card_category = Column(String(50))  # Aura Basic, Aura Plus, Aura Premium
    card_brand = Column(String(20), default="Mastercard")  # Visa, Mastercard, Elo
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    account = relationship("Account", back_populates="credit_cards")
    
    def __repr__(self):
        return f"<CreditCard(id={self.id}, number=****{self.card_number[-4:]}, category={self.card_category})>"
