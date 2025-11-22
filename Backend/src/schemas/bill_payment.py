from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PayBillRequest(BaseModel):
    account_id: int
    bill_type: str  # water, electricity, phone, internet, gas, other
    company: Optional[str] = None
    barcode: str = Field(..., min_length=10)
    amount: float = Field(..., gt=0)
    description: Optional[str] = None


class PayBillResponse(BaseModel):
    transaction_id: int
    account_id: int
    bill_type: str
    company: Optional[str]
    amount: float
    barcode: str
    new_balance: float
    paid_at: datetime
    status: str


class BillPaymentHistoryResponse(BaseModel):
    transaction_id: int
    account_id: int
    amount: float
    description: str
    status: str
    paid_at: datetime
