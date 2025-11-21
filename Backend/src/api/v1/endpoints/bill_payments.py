"""
Bill Payment Endpoints
Rotas para pagamento de contas (água, luz, telefone, etc.)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.api.dependencies import get_current_user
from src.models.user import User
from src.models.account import Account
from src.models.transaction import Transaction, TransactionType, TransactionStatus
from src.schemas.bill_payment import (
    PayBillRequest, PayBillResponse, BillPaymentHistoryResponse
)
from datetime import datetime

router = APIRouter(prefix="/bills", tags=["Bill Payments"])


@router.post("/pay", response_model=PayBillResponse)
def pay_bill(
    request: PayBillRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Pagar conta (água, luz, telefone, etc.)
    Debita da conta corrente ou especificada
    """
    # Busca conta
    account = db.query(Account).filter(
        Account.id == request.account_id,
        Account.user_id == current_user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    # Verifica saldo
    if account.balance < request.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Saldo insuficiente. Disponível: R$ {account.balance:.2f}"
        )
    
    # Valida valor
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")
    
    # Cria descrição
    description = f"Pagamento {request.bill_type}"
    if request.company:
        description += f" - {request.company}"
    if request.description:
        description += f" ({request.description})"
    
    # Cria transação
    transaction = Transaction(
        from_account_id=account.id,
        transaction_type=TransactionType.BILL_PAYMENT,
        amount=request.amount,
        description=description,
        status=TransactionStatus.COMPLETED,
        created_at=datetime.utcnow()
    )
    
    # Debita da conta
    account.balance -= request.amount
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(account)
    
    return PayBillResponse(
        transaction_id=transaction.id,
        account_id=account.id,
        bill_type=request.bill_type,
        company=request.company,
        amount=request.amount,
        barcode=request.barcode,
        new_balance=account.balance,
        paid_at=transaction.created_at,
        status="COMPLETED"
    )


@router.get("/history", response_model=List[BillPaymentHistoryResponse])
def get_bill_payment_history(
    account_id: int = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Histórico de pagamentos de contas
    """
    query = db.query(Transaction).filter(
        Transaction.transaction_type == TransactionType.BILL_PAYMENT
    )
    
    if account_id:
        # Verifica se a conta pertence ao usuário
        account = db.query(Account).filter(
            Account.id == account_id,
            Account.user_id == current_user.id
        ).first()
        
        if not account:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
        
        query = query.filter(Transaction.from_account_id == account_id)
    else:
        # Busca todas as contas do usuário
        user_accounts = db.query(Account).filter(
            Account.user_id == current_user.id
        ).all()
        account_ids = [acc.id for acc in user_accounts]
        query = query.filter(Transaction.from_account_id.in_(account_ids))
    
    transactions = query.order_by(
        Transaction.created_at.desc()
    ).limit(limit).all()
    
    return [
        BillPaymentHistoryResponse(
            transaction_id=t.id,
            account_id=t.from_account_id,
            amount=t.amount,
            description=t.description,
            status=t.status.value,
            paid_at=t.created_at
        ) for t in transactions
    ]
