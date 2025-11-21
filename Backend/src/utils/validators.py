"""
Validadores customizados
"""
import re
from datetime import date


def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro usando algoritmo de dígitos verificadores
    """
    # Remove caracteres não numéricos
    cpf_numbers = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_numbers) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf_numbers == cpf_numbers[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    sum_digits = sum(int(cpf_numbers[i]) * (10 - i) for i in range(9))
    first_digit = (sum_digits * 10 % 11) % 10
    
    if int(cpf_numbers[9]) != first_digit:
        return False
    
    # Calcula segundo dígito verificador
    sum_digits = sum(int(cpf_numbers[i]) * (11 - i) for i in range(10))
    second_digit = (sum_digits * 10 % 11) % 10
    
    if int(cpf_numbers[10]) != second_digit:
        return False
    
    return True


def format_cpf(cpf: str) -> str:
    """
    Formata CPF para o padrão XXX.XXX.XXX-XX
    """
    cpf_numbers = re.sub(r'\D', '', cpf)
    if len(cpf_numbers) != 11:
        return cpf
    return f"{cpf_numbers[:3]}.{cpf_numbers[3:6]}.{cpf_numbers[6:9]}-{cpf_numbers[9:]}"


def validate_cep(cep: str) -> bool:
    """
    Valida formato de CEP brasileiro
    """
    pattern = r'^\d{5}-?\d{3}$'
    return bool(re.match(pattern, cep))


def format_cep(cep: str) -> str:
    """
    Formata CEP para o padrão XXXXX-XXX
    """
    cep_numbers = re.sub(r'\D', '', cep)
    if len(cep_numbers) != 8:
        return cep
    return f"{cep_numbers[:5]}-{cep_numbers[5:]}"


def validate_phone(phone: str) -> bool:
    """
    Valida formato de telefone brasileiro
    """
    pattern = r'^\(\d{2}\)\s?\d{4,5}-?\d{4}$'
    return bool(re.match(pattern, phone))


def calculate_age(birth_date: date) -> int:
    """
    Calcula idade a partir da data de nascimento
    """
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def validate_account_age_for_type(birth_date: date, account_type: str) -> tuple[bool, str]:
    """
    Valida se a idade permite criar determinado tipo de conta
    """
    age = calculate_age(birth_date)
    
    age_rules = {
        "CORRENTE": 13,
        "POUPANCA": 13,
        "SALARIO": 16,
        "UNIVERSITARIA": 16,
        "EMPRESARIAL": 21,
        "INVESTIMENTO": 18,
        "BLACK": 18
    }
    
    min_age = age_rules.get(account_type, 18)
    
    if age < min_age:
        return False, f"Idade mínima para {account_type}: {min_age} anos"
    
    return True, "OK"
