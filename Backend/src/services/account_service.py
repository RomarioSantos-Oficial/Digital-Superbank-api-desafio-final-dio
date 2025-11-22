from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.account import Account
from src.models.user import User
from src.utils.generators import generate_account_number
from src.utils.validators import validate_account_age_for_type
from src.configs.settings import settings


def create_account(db: Session, user_id: int, account_type: str, initial_deposit: float = 0.0) -> Account:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Valida idade para tipo de conta
    is_valid, message = validate_account_age_for_type(user.birth_date, account_type)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    # Conta corrente é obrigatória como primeira conta
    existing_accounts = db.query(Account).filter(
        Account.user_id == user_id
    ).all()
    if len(existing_accounts) == 0 and account_type != "CORRENTE":
        raise HTTPException(
            status_code=400,
            detail="Primeira conta deve ser Corrente"
        )
    
    # Verifica se já existe conta do mesmo tipo
    account_exists = any(
        acc.account_type == account_type for acc in existing_accounts
    )
    if account_exists:
        tipo_nome = {
            'CORRENTE': 'Conta Corrente',
            'POUPANCA': 'Poupança',
            'SALARIO': 'Conta Salário',
            'UNIVERSITARIA': 'Conta Universitária',
            'INVESTIMENTO': 'Conta Investimento',
            'EMPRESARIAL': 'Conta Empresarial',
            'BLACK': 'Conta Black'
        }.get(account_type, account_type)
        raise HTTPException(
            status_code=400,
            detail=(
                f"Você já possui uma {tipo_nome}. "
                f"Cada tipo de conta pode ser criado apenas uma vez."
            )
        )
    
    # Gera número da conta
    account_number = generate_account_number(account_type)
    
    # Cria conta
    account = Account(
        user_id=user_id,
        account_number=account_number,
        account_type=account_type,
        agency=settings.DEFAULT_AGENCY,
        balance=initial_deposit
    )
    
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_account_by_id(db: Session, account_id: int) -> Account:
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account


def get_account_by_number(db: Session, account_number: str) -> Account:
    account = db.query(Account).filter(Account.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account


def get_user_accounts(db: Session, user_id: int):
    return db.query(Account).filter(Account.user_id == user_id).all()


def get_accounts_by_user_id(db: Session, user_id: int):
    return get_user_accounts(db, user_id)
    return get_user_accounts(db, user_id)


def update_balance(db: Session, account: Account, amount: float):
    account.balance += amount
    db.commit()
    db.refresh(account)
    return account
