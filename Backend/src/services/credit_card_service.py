from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session

from src.models.credit_card import CreditCard
from src.models.account import Account
from src.models.user import User
from src.models.transaction import Transaction, TransactionType, TransactionStatus
from src.utils.generators import generate_card_number, calculate_credit_score
from src.configs.settings import settings
import random


def _generate_cvv() -> str:
    #Gera CVV de 3 dígitos
    return str(random.randint(100, 999))


def _generate_expiry_date() -> datetime:
    #Gera data de validade (5 anos a partir de hoje)
    return datetime.utcnow() + timedelta(days=365 * 5)


def _determine_limit_by_score(score: int) -> float:
    #
    # Determina limite baseado no score:
    # - 60-70: R$ 500 (Aura Basic)
    # - 71-85: R$ 1.500 (Aura Plus)
    # - 86-100: R$ 5.000 (Aura Premium)
    #
    if score < 60:
        return 0.0  # Não aprovado
    elif score <= 70:
        return 500.0
    elif score <= 85:
        return 1500.0
    else:
        return 5000.0


def _determine_card_tier(limit: float) -> str:
    #Determina categoria do cartão baseado no limite
    if limit <= 500:
        return "Aura Basic"
    elif limit <= 1500:
        return "Aura Plus"
    else:
        return "Aura Premium"


def create_credit_card(
    db: Session,
    account_id: int,
    requested_limit: Optional[float] = None
) -> tuple[CreditCard, str]:
    #
    # Criar cartão de crédito com análise de crédito
    # Retorna: (cartão, cvv)
    # ATENÇÃO: CVV só é retornado na criação!
    # LIMITAÇÃO: Apenas 1 cartão de crédito por usuário
    #
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Busca usuário
    user = db.query(User).filter(User.id == account.user_id).first()
    if not user:
        raise ValueError("Usuário não encontrado")
    
    # Verifica se já possui cartão de crédito
    from src.services.account_service import get_accounts_by_user_id
    user_accounts = get_accounts_by_user_id(db, user.id)
    user_account_ids = [acc.id for acc in user_accounts]
    
    existing_card = db.query(CreditCard).filter(
        CreditCard.account_id.in_(user_account_ids)
    ).first()
    
    if existing_card:
        raise ValueError(
            "Você já possui um cartão de crédito/débito. "
            "Cada usuário pode ter apenas 1 cartão."
        )
    
    # Verifica idade mínima (18+)
    from src.utils.validators import calculate_age
    age = calculate_age(user.birth_date)
    if age < 18:
        raise ValueError("Idade mínima para cartão de crédito: 18 anos")
    
    # Recalcula score de crédito
    score = calculate_credit_score(account.balance, 0)
    score = calculate_credit_score(account.balance, 0)
    
    # Determina limite
    if score < 60:
        raise ValueError(
            f"Score de crédito insuficiente ({score}/100). "
            "Mínimo necessário: 60"
        )
    
    approved_limit = _determine_limit_by_score(score)
    
    # Se usuário solicitou limite específico, usa o menor
    if requested_limit is not None:
        if requested_limit > approved_limit:
            raise ValueError(
                f"Limite solicitado (R$ {requested_limit}) "
                f"excede limite aprovado (R$ {approved_limit})"
            )
        final_limit = requested_limit
    else:
        final_limit = approved_limit
    
    # Gera dados do cartão
    card_number = generate_card_number()
    cvv = _generate_cvv()
    expiry_date = _generate_expiry_date()
    card_tier = _determine_card_tier(final_limit)
    
    # Cria cartão
    card = CreditCard(
        account_id=account_id,
        card_number=card_number,
        card_holder_name=user.full_name,
        cvv=cvv,  # Salvo criptografado no DB real
        expiry_date=expiry_date,
        credit_limit=final_limit,
        available_limit=final_limit,
        current_bill_amount=0.0,
        card_category=card_tier,
        status="ACTIVE",
        is_virtual=False
    )
    
    db.add(card)
    db.commit()
    db.refresh(card)
    
    # Retorna CVV apenas uma vez
    return card, cvv


def get_cards_by_account(db: Session, account_id: int) -> List[CreditCard]:
    #Listar cartões de uma conta
    return db.query(CreditCard).filter(
        CreditCard.account_id == account_id
    ).all()


def get_card_by_id(db: Session, card_id: int) -> Optional[CreditCard]:
    # Buscar cartão por ID
    return db.query(CreditCard).filter(CreditCard.id == card_id).first()


def block_card(db: Session, card_id: int) -> CreditCard:
    # Bloquear cartão
    card = get_card_by_id(db, card_id)
    if not card:
        raise ValueError("Cartão não encontrado")
    
    if card.status == "CANCELLED":
        raise ValueError("Não é possível bloquear cartão cancelado")
    
    # Permite bloquear mesmo se já estiver bloqueado
    card.status = "BLOCKED"
    card.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(card)
    
    return card


def unblock_card(db: Session, card_id: int) -> CreditCard:
    # Desbloquear cartão
    card = get_card_by_id(db, card_id)
    if not card:
        raise ValueError("Cartão não encontrado")
    
    if card.status == "CANCELLED":
        raise ValueError("Não é possível desbloquear cartão cancelado")
    
    # Verifica se não está vencido
    if card.expiry_date < datetime.utcnow().date():
        raise ValueError("Não é possível desbloquear cartão vencido")
    
    # Permite desbloquear mesmo se já estiver ativo
    card.status = "ACTIVE"
    card.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(card)
    
    return card


def make_purchase(
    db: Session,
    card_id: int,
    amount: float,
    description: str = "Compra no cartão",
    installments: int = 1
) -> Transaction:
    # Realizar compra no cartão de crédito
    if amount <= 0:
        raise ValueError("Valor da compra deve ser positivo")
    
    if installments < 1 or installments > 24:
        raise ValueError("Número de parcelas deve estar entre 1 e 24")
    
    # Busca cartão
    card = get_card_by_id(db, card_id)
    if not card:
        raise ValueError("Cartão não encontrado")
    
    # Validações
    if card.status != "ACTIVE":
        raise ValueError("Cartão não está ativo ou está bloqueado")
    
    if card.expiry_date < datetime.utcnow().date():
        raise ValueError("Cartão vencido")
    
    if card.available_limit < amount:
        raise ValueError(
            f"Limite insuficiente. Disponível: R$ {card.available_limit}"
        )
    
    # Registra transação
    installment_info = f" ({installments}x)" if installments > 1 else ""
    transaction = Transaction(
        from_account_id=card.account_id,
        transaction_type=TransactionType.CARD_CREDIT,
        amount=amount,
        description=f"{description}{installment_info}",
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza cartão
    card.current_bill_amount += amount
    card.available_limit -= amount
    card.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(card)
    
    return transaction


def pay_bill(
    db: Session,
    card_id: int,
    amount: float
) -> tuple[Transaction, CreditCard]:
    # Pagar fatura do cartão de crédito
    if amount <= 0:
        raise ValueError("Valor do pagamento deve ser positivo")
    
    # Busca cartão
    card = get_card_by_id(db, card_id)
    if not card:
        raise ValueError("Cartão não encontrado")
    
    # Busca conta vinculada
    account = db.query(Account).filter(Account.id == card.account_id).first()
    if not account:
        raise ValueError("Conta vinculada não encontrada")
    
    # Verifica saldo na conta
    if account.balance < amount:
        raise ValueError(
            f"Saldo insuficiente na conta. Disponível: R$ {account.balance}"
        )
    
    # Valor não pode ser maior que a fatura
    if amount > card.current_bill_amount:
        raise ValueError(
            f"Valor do pagamento (R$ {amount}) "
            f"maior que fatura (R$ {card.current_bill_amount})"
        )
    
    # Registra transação
    transaction = Transaction(
        from_account_id=card.account_id,
        transaction_type=TransactionType.BILL_PAYMENT,
        amount=amount,
        description=f"Pagamento fatura cartão {card.card_number[-4:]}",
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza conta
    account.balance -= amount
    account.updated_at = datetime.utcnow()
    
    # Atualiza cartão
    card.current_bill_amount -= amount
    card.available_limit += amount
    card.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(card)
    
    return transaction, card


def adjust_limit(
    db: Session,
    card_id: int,
    new_limit: float
) -> CreditCard:
    #Ajustar limite do cartão, validação baseada no score/histórico
    if new_limit <= 0:
        raise ValueError("Novo limite deve ser positivo")
    
    # Busca cartão
    card = get_card_by_id(db, card_id)
    if not card:
        raise ValueError("Cartão não encontrado")
    
    # Busca conta e usuário
    account = db.query(Account).filter(Account.id == card.account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    user = db.query(User).filter(User.id == account.user_id).first()
    if not user:
        raise ValueError("Usuário não encontrado")
    
    # Recalcula score
    score = calculate_credit_score(user.cpf, account.balance)
    max_limit = _determine_limit_by_score(score)
    
    # Valida novo limite
    if new_limit > max_limit:
        raise ValueError(
            f"Novo limite (R$ {new_limit}) excede máximo aprovado "
            f"(R$ {max_limit}) baseado no score atual ({score}/100)"
        )
    
    # Não pode ser menor que o já utilizado
    used_limit = card.credit_limit - card.available_limit
    if new_limit < used_limit:
        raise ValueError(
            f"Novo limite (R$ {new_limit}) menor que valor já utilizado "
            f"(R$ {used_limit})"
        )
    
    # Calcula diferença
    difference = new_limit - card.credit_limit
    
    # Atualiza limites
    card.credit_limit = new_limit
    card.available_limit += difference
    card.card_tier = _determine_card_tier(new_limit)
    card.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(card)
    
    return card


def create_virtual_card(
    db: Session,
    account_id: int
) -> tuple[CreditCard, str]:
    # Criar cartão virtual
    # Mesmo processo de análise de crédito
    # Reutiliza lógica de criação
    card, cvv = create_credit_card(db, account_id)
    
    # Marca como virtual
    card.is_virtual = True
    card.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(card)
    
    return card, cvv
