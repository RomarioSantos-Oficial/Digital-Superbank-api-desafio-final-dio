"""
Rotas de contas bancárias
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.database.connection import get_db
from src.schemas.account import AccountCreate, AccountResponse, BalanceResponse
from src.services.account_service import (
    create_account, get_account_by_id, get_user_accounts
)
from src.api.dependencies import get_current_user
from src.models.user import User
from src.models.account import AccountType

router = APIRouter(prefix="/accounts", tags=["Contas"])


@router.post("/", response_model=AccountResponse)
def create_new_account(
    account_data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria uma nova conta bancária"""
    return create_account(
        db,
        current_user.id,
        account_data.account_type,
        account_data.initial_deposit
    )


@router.get("/", response_model=List[AccountResponse])
def list_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas as contas do usuário"""
    return get_user_accounts(db, current_user.id)


@router.get("/{account_id}/balance", response_model=BalanceResponse)
def get_balance(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Consulta saldo de uma conta"""
    account = get_account_by_id(db, account_id)
    
    # Verifica se a conta pertence ao usuário
    if account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    return {
        "account_id": account.id,
        "account_number": account.account_number,
        "balance": account.balance,
        "account_type": account.account_type
    }


@router.get("/{account_id}/statement")
def get_account_statement(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém extrato da conta"""
    from src.models.transaction import Transaction
    
    account = get_account_by_id(db, account_id)
    
    # Verifica se a conta pertence ao usuário
    if account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    # Busca todas as transações da conta
    transactions = db.query(Transaction).filter(
        (Transaction.from_account_id == account_id) |
        (Transaction.to_account_id == account_id)
    ).order_by(Transaction.created_at.desc()).all()
    
    return transactions


@router.get("/{account_id}/validate-black")
def validate_black_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Valida se a Conta Black atende ao saldo mínimo de R$ 50.000
    """
    account = get_account_by_id(db, account_id)
    
    # Verifica se a conta pertence ao usuário
    if account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    # Verifica se é Conta Black
    if account.account_type != AccountType.BLACK:
        raise HTTPException(
            status_code=400, 
            detail="Esta validação é apenas para Contas Black"
        )
    
    # Verifica saldo mínimo
    minimum_balance = 50000.00
    is_valid = account.balance >= minimum_balance
    
    return {
        "account_id": account.id,
        "account_type": account.account_type.value,
        "current_balance": account.balance,
        "minimum_required": minimum_balance,
        "is_valid": is_valid,
        "difference": account.balance - minimum_balance,
        "message": (
            "Conta Black válida - saldo mínimo atingido" 
            if is_valid 
            else f"Saldo insuficiente. Faltam R$ {minimum_balance - account.balance:,.2f}"
        )
    }


@router.get("/{account_id}/validate-investment")
def validate_investment_account_prerequisites(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Valida se usuário atende aos pré-requisitos para Conta Investimento
    Requer: Conta Black OU Conta Empresarial
    """
    account = get_account_by_id(db, account_id)
    
    # Verifica se a conta pertence ao usuário
    if account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    # Verifica se é Conta Investimento
    if account.account_type != AccountType.INVESTIMENTO:
        raise HTTPException(
            status_code=400,
            detail="Esta validação é apenas para Contas Investimento"
        )
    
    # Busca todas as contas do usuário
    user_accounts = get_user_accounts(db, current_user.id)
    
    # Verifica se tem Conta Black ou Empresarial
    has_black = any(acc.account_type == AccountType.BLACK for acc in user_accounts)
    has_empresarial = any(acc.account_type == AccountType.EMPRESARIAL for acc in user_accounts)
    
    is_valid = has_black or has_empresarial
    
    return {
        "account_id": account.id,
        "account_type": account.account_type.value,
        "has_black_account": has_black,
        "has_empresarial_account": has_empresarial,
        "prerequisites_met": is_valid,
        "required_accounts": ["BLACK", "EMPRESARIAL"],
        "requirement_type": "OR",
        "message": (
            "Pré-requisitos atendidos para Conta Investimento"
            if is_valid
            else "Usuário precisa ter Conta Black OU Conta Empresarial para operar Conta Investimento"
        )
    }
