"""
Schemas para autenticação e usuários
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from typing import Optional
from src.utils.validators import validate_cpf, validate_phone, calculate_age


class UserCreate(BaseModel):
    """Schema para criação de usuário"""
    full_name: str = Field(..., min_length=3, max_length=255)
    cpf: str = Field(..., pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    birth_date: date
    email: EmailStr
    phone: str
    password: str = Field(..., min_length=8)
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf_format(cls, v):
        if not validate_cpf(v):
            raise ValueError('CPF inválido')
        return v
    
    @field_validator('birth_date')
    @classmethod
    def validate_age(cls, v):
        age = calculate_age(v)
        if age < 13:
            raise ValueError('Idade mínima: 13 anos')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v):
        if not validate_phone(v):
            raise ValueError('Telefone inválido. Use formato: (XX) XXXXX-XXXX')
        return v


class UserResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: int
    full_name: str
    cpf: str
    birth_date: date
    email: str
    phone: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class AddressCreate(BaseModel):
    """Schema para criação de endereço"""
    street: str = Field(..., min_length=3)
    number: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str = Field(..., pattern=r'^[A-Z]{2}$')
    zip_code: str = Field(..., pattern=r'^\d{5}-\d{3}$')
    is_primary: bool = False


class AddressResponse(BaseModel):
    """Schema para resposta de endereço"""
    id: int
    street: str
    number: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    is_primary: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema para token de acesso"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para dados do token"""
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    identifier: str = Field(..., description="CPF (XXX.XXX.XXX-XX), número da conta ou email")
    password: str
    
    @field_validator('identifier')
    @classmethod
    def validate_identifier(cls, v):
        # Remove espaços em branco
        v = v.strip()
        
        # Verifica se é vazio
        if not v:
            raise ValueError('Identificador não pode ser vazio')
        
        # Aceita CPF, número de conta ou email
        # CPF: XXX.XXX.XXX-XX ou apenas números
        # Conta: números (4-10 dígitos)
        # Email: contém @
        
        return v


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    full_name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone_format(cls, v):
        if v and not validate_phone(v):
            raise ValueError('Telefone inválido. Use formato: (XX) XXXXX-XXXX')
        return v


class ChangePassword(BaseModel):
    """Schema para mudança de senha"""
    old_password: str
    new_password: str = Field(..., min_length=8)
