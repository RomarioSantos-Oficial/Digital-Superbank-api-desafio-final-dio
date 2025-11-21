"""
Modelo de Usuário
"""
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.connection import Base


class User(Base):
    """Modelo de usuário do sistema"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    birth_date = Column(Date, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    pix_keys = relationship("PixKey", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.full_name}, cpf={self.cpf})>"


class Address(Base):
    """Modelo de endereço"""
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    street = Column(String(255), nullable=False)
    number = Column(String(10), nullable=False)
    complement = Column(String(100))
    neighborhood = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(9), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city}, state={self.state})>"
