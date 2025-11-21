"""
Schemas para cartões de crédito
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CreditCardRequest(BaseModel):
    """Schema para solicitação de cartão de crédito"""
    account_id: Optional[int] = None
    user_id: Optional[int] = None
    requested_limit: Optional[float] = None


class CreditCardResponse(BaseModel):
    """Schema para resposta de cartão"""
    id: int
    account_id: int
    card_number: str
    expiry_date: datetime
    credit_limit: float
    available_limit: float
    current_bill_amount: float
    card_category: str
    card_brand: str
    status: str

    is_virtual: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreditCardCreateResponse(BaseModel):
    """Schema com CVV para criação do cartão"""
    id: int
    account_id: int
    card_number: str
    cvv: str  # Retornado apenas na criação
    expiry_date: datetime
    credit_limit: float
    available_limit: float
    current_bill_amount: float
    card_category: str
    card_brand: str
    status: str

    is_virtual: bool
    created_at: datetime
    message: str


class PurchaseRequest(BaseModel):
    """Schema para compra no cartão"""
    amount: float = Field(..., gt=0)
    description: str
    installments: int = Field(default=1, ge=1, le=24)


class PurchaseResponse(BaseModel):
    """Schema de resposta para compra"""
    transaction_id: int
    card_id: int
    amount: float
    description: str
    installments: int
    new_bill_amount: float
    available_limit: float
    created_at: datetime


class PayBillRequest(BaseModel):
    """Schema para pagamento de fatura"""
    amount: float = Field(..., gt=0)


class PayBillResponse(BaseModel):
    """Schema de resposta para pagamento de fatura"""
    transaction_id: int
    card_id: int
    amount_paid: float
    remaining_bill: float
    new_available_limit: float
    created_at: datetime


class AdjustLimitRequest(BaseModel):
    """Schema para ajuste de limite"""
    new_limit: float = Field(..., gt=0)


class AdjustLimitResponse(BaseModel):
    """Schema de resposta para ajuste de limite"""
    card_id: int
    old_limit: float
    new_limit: float
    available_limit: float
    card_category: str
    updated_at: datetime

