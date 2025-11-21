"""
Geradores de números de conta, cartão, etc.
"""
import random
from datetime import date, timedelta
from src.configs.settings import settings


def generate_account_number(account_type: str) -> str:
    """
    Gera número de conta baseado no tipo
    Formato: XXXXXX-D (D = dígito verificador)
    """
    account_digits = settings.ACCOUNT_TYPES.get(account_type, 1)
    base_number = random.randint(100000, 999999)
    return f"{base_number:06d}-{account_digits}"


def luhn_checksum(card_number: str) -> int:
    """
    Calcula o dígito verificador usando algoritmo de Luhn
    """
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def generate_card_number() -> str:
    """
    Gera número de cartão de crédito usando algoritmo de Luhn
    Formato: 5XXX XXXX XXXX XXXX (Bandeira Aura)
    """
    # Começa com 5 para Bandeira Aura (similar a Mastercard)
    partial = "5" + "".join([str(random.randint(0, 9)) for _ in range(14)])
    
    # Calcula dígito verificador
    check_digit = luhn_checksum(partial + "0")
    if check_digit != 0:
        check_digit = 10 - check_digit
    
    card_number = partial + str(check_digit)
    
    # Formata com espaços
    return f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"


def generate_cvv() -> str:
    """
    Gera CVV de 3 dígitos
    """
    return f"{random.randint(0, 999):03d}"


def generate_card_expiry_date(years: int = 5) -> date:
    """
    Gera data de validade do cartão (X anos a partir de hoje)
    """
    today = date.today()
    expiry = today + timedelta(days=365 * years)
    # Último dia do mês
    if expiry.month == 12:
        return date(expiry.year, 12, 31)
    else:
        next_month = date(expiry.year, expiry.month + 1, 1)
        return next_month - timedelta(days=1)


def calculate_credit_score(account_balance: float, total_deposits: int) -> int:
    """
    Calcula score de crédito simulado (0-100)
    """
    score = 50  # Base
    
    # Adiciona pontos baseado no saldo
    if account_balance >= 50000:
        score += 30
    elif account_balance >= 10000:
        score += 20
    elif account_balance >= 5000:
        score += 10
    
    # Adiciona pontos baseado em número de depósitos
    if total_deposits >= 10:
        score += 20
    elif total_deposits >= 5:
        score += 10
    elif total_deposits >= 2:
        score += 5
    
    return min(score, 100)


def determine_credit_limit(score: int) -> tuple[float, str]:
    """
    Determina limite de crédito baseado no score
    Retorna (limite, categoria)
    """
    if score < 60:
        return 0.0, "REJECTED"
    elif score < 71:
        return 500.0, "Aura Basic"
    elif score < 86:
        return 1500.0, "Aura Plus"
    else:
        return 5000.0, "Aura Premium"
