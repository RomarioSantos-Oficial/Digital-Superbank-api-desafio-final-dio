from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from src.models.pix_key import PixKeyType
import re


class PixKeyCreate(BaseModel):
    account_id: int = Field(..., description="ID da conta")
    key_type: PixKeyType = Field(..., description="Tipo da chave")
    key_value: str = Field(..., description="Valor da chave")
    
    @validator('key_value')
    def validate_key_value(cls, v, values):
        if 'key_type' not in values:
            return v
            
        key_type = values['key_type']
        
        if key_type == PixKeyType.CPF:
            # Remove pontuação
            cpf = re.sub(r'[^\d]', '', v)
            if len(cpf) != 11:
                raise ValueError('CPF deve ter 11 dígitos')
            return cpf
            
        elif key_type == PixKeyType.CNPJ:
            # Remove pontuação
            cnpj = re.sub(r'[^\d]', '', v)
            if len(cnpj) != 14:
                raise ValueError('CNPJ deve ter 14 dígitos')
            return cnpj
            
        elif key_type == PixKeyType.EMAIL:
            # Validação básica de email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
                raise ValueError('Email inválido')
            return v.lower()
            
        elif key_type == PixKeyType.PHONE:
            # Remove pontuação e espaços
            phone = re.sub(r'[^\d]', '', v)
            if len(phone) < 10 or len(phone) > 11:
                raise ValueError('Telefone deve ter 10 ou 11 dígitos')
            return phone
            
        elif key_type == PixKeyType.RANDOM:
            # Chave aleatória deve ter formato UUID
            if not re.match(
                r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
                v.lower()
            ):
                raise ValueError('Chave aleatória deve ser um UUID válido')
            return v.lower()
            
        return v


class PixKeyResponse(BaseModel):
    id: int
    user_id: int
    account_id: int
    key_type: PixKeyType
    key_value: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PixKeyListResponse(BaseModel):
    keys: list[PixKeyResponse]
    total: int


class PixKeyDeleteResponse(BaseModel):
    message: str
    key_id: int
