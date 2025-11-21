"""
Transaction Endpoints
Rotas para todas as operações de transações bancárias
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.api.dependencies import get_current_user
from src.models.user import User
from src.models.transaction import TransactionType
from src.schemas.transaction import (
    DepositRequest, DepositResponse,
    WithdrawalRequest, WithdrawalResponse,
    TransferRequest, TransferResponse,
    PixSendRequest, PixReceiveRequest, PixResponse,
    BillPaymentRequest, BillPaymentResponse,
    StatementResponse, TransactionResponse,
    ScheduleTransactionRequest, ScheduledTransactionResponse
)
from src.services import transaction_service
from src.services.account_service import get_account_by_id

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/deposit", response_model=DepositResponse)
def deposit(
    request: DepositRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Realizar depósito em conta"""
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        transaction = transaction_service.create_deposit(
            db, request.account_id, request.amount, request.description
        )
        return DepositResponse(
            id=transaction.id,
            from_account_id=transaction.from_account_id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            description=transaction.description,
            created_at=transaction.created_at,
            status=transaction.status
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/withdraw", response_model=WithdrawalResponse)
def withdraw(
    request: WithdrawalRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Realizar saque com validação de limites:
    - Máximo R$ 2.000 por saque
    - Máximo 3 saques por dia
    - Limite total diário de R$ 5.000
    """
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        transaction = transaction_service.create_withdrawal(
            db, request.account_id, request.amount, request.description
        )
        return WithdrawalResponse(
            id=transaction.id,
            from_account_id=transaction.from_account_id,
            transaction_type=transaction.transaction_type,
            amount=transaction.amount,
            description=transaction.description,
            created_at=transaction.created_at,
            status=transaction.status
        )
    except transaction_service.InsufficientBalanceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except transaction_service.TransactionLimitError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transfer", response_model=TransferResponse)
def transfer(
    request: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Transferência interna entre contas"""
    # Verifica se a conta origem pertence ao usuário
    account = get_account_by_id(db, request.from_account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(
            status_code=404, detail="Conta origem não encontrada"
        )
    
    try:
        debit_tx, credit_tx = transaction_service.create_transfer(
            db, request.from_account_id, request.to_account_number,
            request.amount, request.description
        )
        return TransferResponse(
            debit_transaction_id=debit_tx.id,
            credit_transaction_id=credit_tx.id,
            from_account_id=debit_tx.from_account_id,
            to_account_number=request.to_account_number,
            amount=request.amount,
            description=request.description,
            created_at=debit_tx.created_at,
            status=debit_tx.status
        )
    except transaction_service.InsufficientBalanceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pix/send", response_model=PixResponse)
def pix_send(
    request: PixSendRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enviar PIX"""
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.from_account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        transaction = transaction_service.create_pix_send(
            db, request.from_account_id, request.pix_key,
            request.amount, request.description
        )
        return PixResponse(
            id=transaction.id,
            from_account_id=transaction.from_account_id,
            amount=transaction.amount,
            pix_key=request.pix_key,
            description=transaction.description,
            created_at=transaction.created_at,
            status=transaction.status
        )
    except transaction_service.InsufficientBalanceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pix/receive", response_model=PixResponse)
def pix_receive(
    request: PixReceiveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Receber PIX (simulação)
    Na vida real, isso seria chamado pelo sistema PIX externo
    """
    try:
        transaction = transaction_service.create_pix_receive(
            db, request.to_account_number, request.amount,
            request.pix_key, request.description
        )
        
        # Verifica se a conta pertence ao usuário para retornar info completa
        account = get_account_by_id(db, transaction.account_id)
        if account and account.user_id != current_user.id:
            # Se não for do usuário, retorna resposta genérica
            return PixResponse(
                id=transaction.id,
                from_account_id=transaction.from_account_id,
                amount=transaction.amount,
                pix_key=request.pix_key,
                description="PIX recebido",
                created_at=transaction.created_at,
                status=transaction.status
            )
        
        return PixResponse(
            id=transaction.id,
            from_account_id=transaction.from_account_id,
            amount=transaction.amount,
            pix_key=request.pix_key,
            description=transaction.description,
            created_at=transaction.created_at,
            status=transaction.status
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pay-bill", response_model=BillPaymentResponse)
def pay_bill(
    request: BillPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pagar boleto/conta"""
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        transaction = transaction_service.pay_bill(
            db, request.account_id, request.bar_code,
            request.amount, request.description
        )
        return BillPaymentResponse(
            id=transaction.id,
            from_account_id=transaction.from_account_id,
            amount=transaction.amount,
            bar_code=request.bar_code,
            description=transaction.description,
            transaction_type=transaction.transaction_type,
            created_at=transaction.created_at,
            status=transaction.status
        )
    except transaction_service.InsufficientBalanceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/statement", response_model=StatementResponse)
def get_statement(
    account_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    transaction_type: Optional[TransactionType] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter extrato com filtros opcionais:
    - start_date: data inicial
    - end_date: data final
    - transaction_type: tipo de transação
    - min_amount/max_amount: faixa de valores
    - limit/offset: paginação
    """
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    transactions, total_count = transaction_service.get_statement(
        db, account_id, start_date, end_date, transaction_type,
        min_amount, max_amount, limit, offset
    )
    
    return StatementResponse(
        transactions=[
            TransactionResponse(
                id=t.id,
                from_account_id=t.from_account_id,
                transaction_type=t.transaction_type,
                amount=t.amount,
                description=t.description or "",
                created_at=t.created_at,
                status=t.status
            ) for t in transactions
        ],
        total_count=total_count,
        limit=limit,
        offset=offset
    )


@router.post("/schedule", response_model=ScheduledTransactionResponse)
def schedule_transaction(
    request: ScheduleTransactionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Agendar transação futura"""
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        scheduled = transaction_service.schedule_transaction(
            db, request.account_id, request.transaction_type,
            request.amount, request.scheduled_date, request.description,
            request.to_account_id
        )
        return ScheduledTransactionResponse(
            id=scheduled.id,
            from_account_id=scheduled.from_account_id,
            transaction_type=scheduled.transaction_type,
            amount=scheduled.amount,
            schedule_date=scheduled.schedule_date,
            description=scheduled.description,
            to_account_id=scheduled.to_account_id,
            status=scheduled.status,
            created_at=scheduled.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scheduled", response_model=List[ScheduledTransactionResponse])
def list_scheduled_transactions(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar transações agendadas de uma conta"""
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    scheduled_list = transaction_service.get_scheduled_transactions(
        db, account_id
    )
    
    return [
        ScheduledTransactionResponse(
            id=s.id,
            account_id=s.account_id,
            type=s.type,
            amount=s.amount,
            scheduled_date=s.scheduled_date,
            description=s.description,
            destination_account=s.destination_account,
            status=s.status,
            created_at=s.created_at
        ) for s in scheduled_list
    ]
