"""
Rotas de autenticação
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database.connection import get_db
from src.schemas.auth import (
    UserCreate, UserResponse, Token, AddressCreate, LoginRequest,
    UserUpdate, ChangePassword
)
from src.services.auth_service import create_user, authenticate_user
from src.utils.security import create_access_token
from src.configs.settings import settings
from src.api.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Registra um novo usuário"""
    return create_user(db, user_data)


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """"Faz login usando CPF, número da conta corrente ou email"""
    user = authenticate_user(db, login_data.identifier, login_data.password)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/oauth", response_model=Token)
def login_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """"Login alternativo usando OAuth2PasswordRequestForm (para compatibilidade com Swagger)"""
    user = authenticate_user(db, form_data.username, form_data.password)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém perfil do usuário autenticado"""
    return current_user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza dados do usuário"""
    from src.services.auth_service import update_user
    
    # Verifica se o usuário está atualizando seus próprios dados
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode atualizar seus próprios dados"
        )
    
    return update_user(db, user_id, user_data.model_dump(exclude_unset=True))


@router.put("/users/{user_id}/password")
def change_password_endpoint(
    user_id: int,
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Altera senha do usuário"""
    from src.services.auth_service import change_user_password
    
    # Verifica se o usuário está alterando sua própria senha
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode alterar sua própria senha"
        )
    
    change_user_password(db, user_id, password_data.old_password, password_data.new_password)
    return {"message": "Senha alterada com sucesso"}
