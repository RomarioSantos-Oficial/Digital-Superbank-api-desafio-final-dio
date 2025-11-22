from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.user import User, Address
from src.schemas.auth import UserCreate, AddressCreate
from src.utils.security import get_password_hash, verify_password
from src.utils.validators import format_cpf


def create_user(db: Session, user_data: UserCreate, address_data: AddressCreate = None) -> User:
    from src.services.account_service import create_account
    
    # Verifica se CPF já existe
    cpf_formatted = format_cpf(user_data.cpf)
    existing_user = db.query(User).filter(User.cpf == cpf_formatted).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado"
        )
    
    # Verifica se email já existe
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria usuário
    db_user = User(
        full_name=user_data.full_name,
        cpf=cpf_formatted,
        birth_date=user_data.birth_date,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Cria conta corrente automaticamente
    try:
        create_account(db, user_id=db_user.id, account_type="CORRENTE", initial_deposit=0.0)
    except Exception as e:
        # Se falhar ao criar conta, não bloqueia o cadastro
        print(f"Erro ao criar conta corrente: {e}")
    
    # Adiciona endereço se fornecido
    if address_data:
        db_address = Address(
            user_id=db_user.id,
            **address_data.model_dump()
        )
        db.add(db_address)
        db.commit()
    
    return db_user


def authenticate_user(db: Session, identifier: str, password: str) -> User:
    from src.models.account import Account
    
    user = None
    
    # Tenta buscar por email (se contém @)
    if '@' in identifier:
        user = db.query(User).filter(User.email == identifier).first()
    
    # Tenta buscar por CPF (se está no formato XXX.XXX.XXX-XX com pontos)
    elif '.' in identifier:
        cpf_formatted = format_cpf(identifier)
        user = db.query(User).filter(User.cpf == cpf_formatted).first()
    
    # Tenta buscar por número da conta (formato: XXXXXX-X)
    elif '-' in identifier and len(identifier.split('-')[0]) >= 6:
        # Busca a conta pelo número exato
        account = db.query(Account).filter(
            Account.account_number == identifier,
            Account.account_type == "CORRENTE"
        ).first()
        
        if account:
            user = db.query(User).filter(User.id == account.user_id).first()
    
    # Tenta buscar por CPF sem formatação (apenas números)
    elif identifier.replace('-', '').replace('.', '').isdigit():
        cpf_formatted = format_cpf(identifier)
        user = db.query(User).filter(User.cpf == cpf_formatted).first()
    
    # Caso contrário, não encontrou
    else:
        user = None
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas"
        )
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user


def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user


def update_user(db: Session, user_id: int, user_data: dict) -> User:
    user = get_user_by_id(db, user_id)
    
    # Verifica se email já está em uso por outro usuário
    if 'email' in user_data and user_data['email']:
        existing_email = db.query(User).filter(
            User.email == user_data['email'],
            User.id != user_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
    
    # Atualiza campos
    for key, value in user_data.items():
        if value is not None and hasattr(user, key):
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user


def change_user_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
    user = get_user_by_id(db, user_id)
    
    # Verifica senha antiga
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualiza senha
    user.password_hash = get_password_hash(new_password)
    db.commit()
    return True
