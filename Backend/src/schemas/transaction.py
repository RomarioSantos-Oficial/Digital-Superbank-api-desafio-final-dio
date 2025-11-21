"""
Schemas para transações
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from src.models.transaction import TransactionType, TransactionStatus


class DepositRequest(BaseModel):
    """Schema para depósito"""
    account_id: int
    amount: float = Field(..., gt=0)
    description: str = "Depósito"


class DepositResponse(BaseModel):
    """Schema de resposta para depósito"""
    id: int
    from_account_id: Optional[int] = None
    transaction_type: TransactionType
    amount: float
    description: Optional[str] = None
    created_at: datetime
    status: TransactionStatus
    
    class Config:
        from_attributes = True


class WithdrawalRequest(BaseModel):
    """Schema para saque"""
    account_id: int
    amount: float = Field(..., gt=0, le=2000.0)
    description: str = "Saque"


class WithdrawalResponse(BaseModel):
    """Schema de resposta para saque"""
    id: int
    from_account_id: Optional[int] = None
    transaction_type: TransactionType
    amount: float
    description: Optional[str] = None
    created_at: datetime
    status: TransactionStatus
    
    class Config:
        from_attributes = True


class TransferRequest(BaseModel):
    """Schema para transferência"""
    from_account_id: int
    to_account_number: str
    amount: float = Field(..., gt=0)
    description: str = "Transferência"


class TransferResponse(BaseModel):
    """Schema de resposta para transferência"""
    debit_transaction_id: int
    credit_transaction_id: int
    from_account_id: int
    to_account_number: str
    amount: float
    description: str
    created_at: datetime
    status: TransactionStatus


class PixSendRequest(BaseModel):
    """Schema para envio de PIX"""
    from_account_id: int
    pix_key: str
    amount: float = Field(..., gt=0)
    description: str = "PIX enviado"


class PixReceiveRequest(BaseModel):
    """Schema para recebimento de PIX"""
    to_account_number: str
    amount: float = Field(..., gt=0)
    pix_key: str
    description: str = "PIX recebido"


class PixResponse(BaseModel):
    """Schema de resposta para PIX"""
    id: int
    from_account_id: int
    amount: float
    pix_key: str
    description: str
    created_at: datetime
    status: TransactionStatus


class BillPaymentRequest(BaseModel):
    """Schema para pagamento de boleto"""
    account_id: int
    bar_code: str = Field(..., min_length=44, max_length=48)
    amount: float = Field(..., gt=0)
    description: str = "Pagamento de boleto"


class BillPaymentResponse(BaseModel):
    """Schema de resposta para pagamento de boleto"""
    id: int
    from_account_id: int
    amount: float
    bar_code: str
    description: str
    transaction_type: TransactionType
    created_at: datetime
    status: TransactionStatus


class TransactionResponse(BaseModel):
    """Schema genérico de resposta de transação"""
    id: int
    from_account_id: int
    transaction_type: TransactionType
    amount: float
    description: str
    created_at: datetime
    status: TransactionStatus
    
    class Config:
        from_attributes = True


class StatementResponse(BaseModel):
    """Schema de resposta para extrato"""
    transactions: List[TransactionResponse]
    total_count: int
    limit: int
    offset: int


class ScheduleTransactionRequest(BaseModel):
    """Schema para agendar transação"""
    account_id: int
    transaction_type: TransactionType
    amount: float = Field(..., gt=0)
    scheduled_date: datetime
    description: str = ""
    to_account_id: Optional[int] = None


class ScheduledTransactionResponse(BaseModel):
    """Schema de resposta para transação agendada"""
    id: int
    from_account_id: int
    transaction_type: TransactionType
    amount: float
    schedule_date: datetime
    description: str
    to_account_id: Optional[int]
    status: TransactionStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

