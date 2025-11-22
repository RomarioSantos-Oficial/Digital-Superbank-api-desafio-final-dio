from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AccountCreate(BaseModel):
    """Schema para criação de conta"""
    account_type: str = Field(..., pattern=r'^(CORRENTE|POUPANCA|SALARIO|UNIVERSITARIA|EMPRESARIAL|INVESTIMENTO|BLACK)$')
    initial_deposit: float = Field(default=0.0, ge=0)


class AccountResponse(BaseModel):
    """Schema para resposta de conta"""
    id: int
    user_id: int
    account_number: str
    account_type: str
    agency: str
    balance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class BalanceResponse(BaseModel):
    """Schema para consulta de saldo"""
    account_id: int
    account_number: str
    balance: float
    account_type: str
