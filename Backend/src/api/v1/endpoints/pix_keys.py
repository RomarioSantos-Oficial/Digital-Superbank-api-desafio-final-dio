"""
Endpoints para gerenciamento de chaves PIX
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.api.dependencies import get_db, get_current_user
from src.models.user import User
from src.models.pix_key import PixKey, PixKeyType
from src.models.account import Account
from src.schemas.pix_key import (
    PixKeyCreate, PixKeyResponse, PixKeyListResponse, PixKeyDeleteResponse
)
import uuid

router = APIRouter(prefix="/pix-keys", tags=["PIX Keys"])


@router.post("", response_model=PixKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_pix_key(
    pix_key: PixKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova chave PIX para a conta do usuário"""
    
    # Verifica se a conta pertence ao usuário
    account = db.query(Account).filter(
        Account.id == pix_key.account_id,
        Account.user_id == current_user.id,
        Account.is_active == True
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada ou inativa"
        )
    
    # Verifica se a chave já existe
    existing_key = db.query(PixKey).filter(
        PixKey.key_value == pix_key.key_value,
        PixKey.is_active == True
    ).first()
    
    if existing_key:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta chave PIX já está cadastrada"
        )
    
    # Se for chave aleatória, gera um UUID
    key_value = pix_key.key_value
    if pix_key.key_type == PixKeyType.RANDOM and not key_value:
        key_value = str(uuid.uuid4())
    
    # Cria a chave PIX
    new_key = PixKey(
        user_id=current_user.id,
        account_id=pix_key.account_id,
        key_type=pix_key.key_type,
        key_value=key_value,
        is_active=True
    )
    
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    
    return new_key


@router.get("", response_model=PixKeyListResponse)
async def list_pix_keys(
    account_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todas as chaves PIX do usuário"""
    
    query = db.query(PixKey).filter(
        PixKey.user_id == current_user.id,
        PixKey.is_active == True
    )
    
    # Filtra por conta se especificado
    if account_id:
        # Verifica se a conta pertence ao usuário
        account = db.query(Account).filter(
            Account.id == account_id,
            Account.user_id == current_user.id
        ).first()
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta não encontrada"
            )
        
        query = query.filter(PixKey.account_id == account_id)
    
    keys = query.all()
    
    return {
        "keys": keys,
        "total": len(keys)
    }


@router.delete("/{key_id}", response_model=PixKeyDeleteResponse)
async def delete_pix_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove uma chave PIX do usuário"""
    
    # Busca a chave PIX
    pix_key = db.query(PixKey).filter(
        PixKey.id == key_id,
        PixKey.user_id == current_user.id,
        PixKey.is_active == True
    ).first()
    
    if not pix_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave PIX não encontrada"
        )
    
    # Desativa a chave (soft delete)
    pix_key.is_active = False
    db.commit()
    
    return {
        "message": "Chave PIX removida com sucesso",
        "key_id": key_id
    }


@router.get("/{key_id}", response_model=PixKeyResponse)
async def get_pix_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtém detalhes de uma chave PIX específica"""
    
    pix_key = db.query(PixKey).filter(
        PixKey.id == key_id,
        PixKey.user_id == current_user.id,
        PixKey.is_active == True
    ).first()
    
    if not pix_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chave PIX não encontrada"
        )
    
    return pix_key
