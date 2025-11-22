from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CreditCardRequest(BaseModel):
    account_id: Optional[int] = None
    user_id: Optional[int] = None
    requested_limit: Optional[float] = None


class CreditCardResponse(BaseModel):
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
    amount: float = Field(..., gt=0)
    description: str
    installments: int = Field(default=1, ge=1, le=24)


class PurchaseResponse(BaseModel):
    transaction_id: int
    card_id: int
    amount: float
    description: str
    installments: int
    new_bill_amount: float
    available_limit: float
    created_at: datetime


class PayBillRequest(BaseModel):
    amount: float = Field(..., gt=0)


class PayBillResponse(BaseModel):
    transaction_id: int
    card_id: int
    amount_paid: float
    remaining_bill: float
    new_available_limit: float
    created_at: datetime


class AdjustLimitRequest(BaseModel):
    new_limit: float = Field(..., gt=0)


class AdjustLimitResponse(BaseModel):
    card_id: int
    old_limit: float
    new_limit: float
    available_limit: float
    card_category: str
    updated_at: datetime

