"""
Credit Card Endpoints
Rotas para gerenciamento de cartões de crédito
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.api.dependencies import get_current_user
from src.models.user import User
from src.schemas.credit_card import (
    CreditCardRequest, CreditCardResponse,
    CreditCardCreateResponse,
    PurchaseRequest, PurchaseResponse,
    PayBillRequest, PayBillResponse,
    AdjustLimitRequest, AdjustLimitResponse
)
from src.services import credit_card_service
from src.services.account_service import get_account_by_id

router = APIRouter(prefix="/credit-cards", tags=["Credit Cards"])


@router.post("/", response_model=CreditCardCreateResponse)
def request_credit_card(
    request: CreditCardRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Solicitar cartão de crédito
    Realiza análise de crédito automática
    ATENÇÃO: CVV só é retornado nesta chamada!
    Aceita account_id ou user_id (usa primeira conta corrente)
    """
    # Determina o account_id
    account_id = request.account_id
    
    # Se não forneceu account_id mas forneceu user_id
    if not account_id and request.user_id:
        if request.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Busca primeira conta corrente do usuário
        from src.services.account_service import get_accounts_by_user_id
        accounts = get_accounts_by_user_id(db, request.user_id)
        corrente_accounts = [acc for acc in accounts if acc.account_type == "CORRENTE"]
        
        if not corrente_accounts:
            raise HTTPException(
                status_code=400,
                detail="Usuário não possui conta corrente"
            )
        
        account_id = corrente_accounts[0].id
    
    if not account_id:
        raise HTTPException(
            status_code=400,
            detail="account_id ou user_id é obrigatório"
        )
    
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        card, cvv = credit_card_service.create_credit_card(
            db, account_id, request.requested_limit
        )
        
        return CreditCardCreateResponse(
            id=card.id,
            account_id=card.account_id,
            card_number=card.card_number,
            cvv=cvv,  # ÚNICO momento em que CVV é retornado
            expiry_date=card.expiry_date,
            credit_limit=card.credit_limit,
            available_limit=card.available_limit,
            current_bill_amount=card.current_bill_amount,
            card_category=card.card_category,
            card_brand=card.card_brand,
            status=card.status,

            is_virtual=card.is_virtual,
            created_at=card.created_at,
            message=(
                "Cartão criado com sucesso! "
                "Guarde o CVV em local seguro, ele não será exibido novamente."
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CreditCardResponse])
def list_user_cards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todos os cartões do usuário autenticado"""
    # Busca todas as contas do usuário
    from src.services.account_service import get_accounts_by_user_id
    accounts = get_accounts_by_user_id(db, current_user.id)
    
    # Busca cartões de todas as contas
    all_cards = []
    for account in accounts:
        cards = credit_card_service.get_cards_by_account(db, account.id)
        all_cards.extend(cards)
    
    return [
        CreditCardResponse(
            id=card.id,
            account_id=card.account_id,
            card_number=card.card_number,
            cvv=card.cvv,  # Adicionado CVV
            expiry_date=card.expiry_date,
            credit_limit=card.credit_limit,
            available_limit=card.available_limit,
            current_bill_amount=card.current_bill_amount,
            card_category=card.card_category,
            card_brand=card.card_brand,
            status=card.status,
            is_virtual=card.is_virtual,
            created_at=card.created_at
        ) for card in all_cards
    ]


@router.get("/{card_id}", response_model=CreditCardResponse)
def get_card_details(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter detalhes de um cartão específico"""
    card = credit_card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    # Verifica se o cartão pertence ao usuário
    account = get_account_by_id(db, card.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    return CreditCardResponse(
        id=card.id,
        account_id=card.account_id,
        card_number=card.card_number,
        cvv=card.cvv,  # Adicionado CVV
        expiry_date=card.expiry_date,
        credit_limit=card.credit_limit,
        available_limit=card.available_limit,
        current_bill_amount=card.current_bill_amount,
        card_category=card.card_category,
        card_brand=card.card_brand,
        status=card.status,

        is_virtual=card.is_virtual,
        created_at=card.created_at
    )


@router.post("/{card_id}/block", response_model=CreditCardResponse)
def block_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Bloquear cartão"""
    # Verifica se o cartão pertence ao usuário
    card = credit_card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    account = get_account_by_id(db, card.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    try:
        card = credit_card_service.block_card(db, card_id)
        return CreditCardResponse(
            id=card.id,
            account_id=card.account_id,
            card_number=card.card_number,
            expiry_date=card.expiry_date,
            credit_limit=card.credit_limit,
            available_limit=card.available_limit,
            current_bill_amount=card.current_bill_amount,
            card_category=card.card_category,
            card_brand=card.card_brand,
            status=card.status,

            is_virtual=card.is_virtual,
            created_at=card.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}/unblock", response_model=CreditCardResponse)
def unblock_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Desbloquear cartão"""
    # Verifica se o cartão pertence ao usuário
    card = credit_card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    account = get_account_by_id(db, card.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    try:
        card = credit_card_service.unblock_card(db, card_id)
        return CreditCardResponse(
            id=card.id,
            account_id=card.account_id,
            card_number=card.card_number,
            cvv=card.cvv,
            expiry_date=card.expiry_date,
            credit_limit=card.credit_limit,
            available_limit=card.available_limit,
            current_bill_amount=card.current_bill_amount,
            card_category=card.card_category,
            card_brand=card.card_brand,
            status=card.status,
            is_virtual=card.is_virtual,
            created_at=card.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}/purchase", response_model=PurchaseResponse)
def make_purchase(
    card_id: int,
    request: PurchaseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Realizar compra no cartão de crédito"""
    # Verifica se o cartão pertence ao usuário
    card = credit_card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    account = get_account_by_id(db, card.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    try:
        transaction = credit_card_service.make_purchase(
            db, card_id, request.amount, request.description,
            request.installments
        )
        
        # Recarrega cartão atualizado
        db.refresh(card)
        
        return PurchaseResponse(
            transaction_id=transaction.id,
            card_id=card_id,
            amount=request.amount,
            description=transaction.description,
            installments=request.installments,
            new_bill_amount=card.current_bill_amount,
            available_limit=card.available_limit,
            created_at=transaction.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}/pay-bill", response_model=PayBillResponse)
def pay_card_bill(
    card_id: int,
    request: PayBillRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pagar fatura do cartão (débito da conta corrente vinculada)"""
    # Verifica se o cartão pertence ao usuário
    card = credit_card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    account = get_account_by_id(db, card.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    try:
        transaction, updated_card = credit_card_service.pay_bill(
            db, card_id, request.amount
        )
        
        return PayBillResponse(
            transaction_id=transaction.id,
            card_id=card_id,
            amount_paid=request.amount,
            remaining_bill=updated_card.current_bill_amount,
            new_available_limit=updated_card.available_limit,
            created_at=transaction.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{card_id}/adjust-limit", response_model=AdjustLimitResponse)
def adjust_card_limit(
    card_id: int,
    request: AdjustLimitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ajustar limite do cartão
    Validação automática baseada em score de crédito
    """
    # Verifica se o cartão pertence ao usuário
    card = credit_card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    account = get_account_by_id(db, card.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    try:
        updated_card = credit_card_service.adjust_limit(
            db, card_id, request.new_limit
        )
        
        return AdjustLimitResponse(
            card_id=card_id,
            old_limit=card.credit_limit,
            new_limit=updated_card.credit_limit,
            available_limit=updated_card.available_limit,
            card_tier=updated_card.card_category,
            updated_at=updated_card.updated_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/virtual", response_model=CreditCardCreateResponse)
def create_virtual_card(
    request: CreditCardRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Criar cartão virtual
    Mesmo processo de análise de crédito do cartão físico
    """
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        card, cvv = credit_card_service.create_virtual_card(
            db, request.account_id
        )
        
        return CreditCardCreateResponse(
            id=card.id,
            account_id=card.account_id,
            card_number=card.card_number,
            cvv=cvv,
            expiry_date=card.expiry_date,
            credit_limit=card.credit_limit,
            available_limit=card.available_limit,
            current_bill_amount=card.current_bill_amount,
            card_category=card.card_category,
            status=card.status,

            is_virtual=card.is_virtual,
            created_at=card.created_at,
            message=(
                "Cartão virtual criado com sucesso! "
                "Guarde o CVV em local seguro, ele não será exibido novamente."
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
