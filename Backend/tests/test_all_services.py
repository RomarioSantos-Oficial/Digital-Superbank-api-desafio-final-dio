"""
Script de teste completo para todos os serviços da Digital Superbank API
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api/v1"
token = None
user_data = None
accounts = {}
credit_cards = {}

def print_section(title):
    """Imprime seção do teste"""
    print("\n" + "="*80)
    print(f"🧪 {title}")
    print("="*80)

def print_result(test_name, response):
    """Imprime resultado do teste"""
    status_icon = "✅" if response.status_code < 400 else "❌"
    print(f"\n{status_icon} {test_name}")
    print(f"   Status: {response.status_code}")
    try:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"   Response: {response.text}")
    return response

def generate_valid_cpf():
    """Gera um CPF válido para testes"""
    import random
    
    # Gera 9 dígitos aleatórios
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    # Calcula primeiro dígito verificador
    sum1 = sum([(10 - i) * cpf[i] for i in range(9)])
    digit1 = 11 - (sum1 % 11)
    digit1 = 0 if digit1 >= 10 else digit1
    cpf.append(digit1)
    
    # Calcula segundo dígito verificador
    sum2 = sum([(11 - i) * cpf[i] for i in range(10)])
    digit2 = 11 - (sum2 % 11)
    digit2 = 0 if digit2 >= 10 else digit2
    cpf.append(digit2)
    
    # Formata CPF
    return f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"

def test_auth_register():
    """Teste 1: Registrar usuário"""
    print_section("AUTENTICAÇÃO - Registro")
    
    timestamp = datetime.now().strftime("%H%M%S")
    data = {
        "full_name": f"Teste Completo {timestamp}",
        "cpf": generate_valid_cpf(),
        "birth_date": "1995-03-20",
        "email": f"teste{timestamp}@digitalbank.com",
        "phone": "(21) 99999-8888",
        "password": "senha123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    result = print_result("Registrar Usuário", response)
    
    if response.status_code == 201:
        global user_data
        user_data = data
        return True
    return False

def test_auth_login_email():
    """Teste 2: Login com Email"""
    print_section("AUTENTICAÇÃO - Login com Email")
    
    data = {
        "identifier": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    result = print_result("Login com Email", response)
    
    if response.status_code == 200:
        global token
        token = result.json()["access_token"]
        print(f"\n🔑 Token obtido: {token[:50]}...")
        return True
    return False

def test_auth_login_cpf():
    """Teste 3: Login com CPF"""
    print_section("AUTENTICAÇÃO - Login com CPF")
    
    data = {
        "identifier": user_data["cpf"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print_result("Login com CPF", response)
    return response.status_code == 200

def test_account_create_corrente():
    """Teste 4: Criar Conta Corrente"""
    print_section("CONTAS - Criar Conta Corrente")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {"account_type": "CORRENTE"}
    
    response = requests.post(f"{BASE_URL}/accounts/", json=data, headers=headers)
    result = print_result("Criar Conta Corrente", response)
    
    if response.status_code in [200, 201]:
        accounts["CORRENTE"] = result.json()
        return True
    return False

def test_auth_login_account():
    """Teste 5: Login com Número da Conta"""
    print_section("AUTENTICAÇÃO - Login com Número da Conta")
    
    account_number = accounts["CORRENTE"]["account_number"]
    data = {
        "identifier": account_number,
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print_result(f"Login com Conta {account_number}", response)
    return response.status_code == 200

def test_account_list():
    """Teste 6: Listar Contas"""
    print_section("CONTAS - Listar")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/accounts/", headers=headers)
    print_result("Listar Contas", response)
    return response.status_code == 200

def test_account_balance():
    """Teste 7: Consultar Saldo"""
    print_section("CONTAS - Consultar Saldo")
    
    headers = {"Authorization": f"Bearer {token}"}
    account_id = accounts["CORRENTE"]["id"]
    response = requests.get(f"{BASE_URL}/accounts/{account_id}/balance", headers=headers)
    print_result("Consultar Saldo", response)
    return response.status_code == 200

def test_account_create_poupanca():
    """Teste 8: Criar Conta Poupança"""
    print_section("CONTAS - Criar Conta Poupança")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {"account_type": "POUPANCA"}
    
    response = requests.post(f"{BASE_URL}/accounts/", json=data, headers=headers)
    result = print_result("Criar Conta Poupança", response)
    
    if response.status_code in [200, 201]:
        accounts["POUPANCA"] = result.json()
        return True
    return False

def test_transaction_deposit():
    """Teste 9: Fazer Depósito"""
    print_section("TRANSAÇÕES - Depósito")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "account_id": accounts["CORRENTE"]["id"],
        "amount": 5000.00,
        "description": "Depósito inicial para testes"
    }
    
    response = requests.post(f"{BASE_URL}/transactions/deposit", json=data, headers=headers)
    print_result("Depósito de R$ 5.000,00", response)
    return response.status_code in [200, 201]

def test_transaction_withdraw():
    """Teste 10: Fazer Saque"""
    print_section("TRANSAÇÕES - Saque")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "account_id": accounts["CORRENTE"]["id"],
        "amount": 500.00,
        "description": "Saque para testes"
    }
    
    response = requests.post(f"{BASE_URL}/transactions/withdraw", json=data, headers=headers)
    print_result("Saque de R$ 500,00", response)
    return response.status_code in [200, 201]

def test_transaction_transfer():
    """Teste 11: Fazer Transferência"""
    print_section("TRANSAÇÕES - Transferência")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "from_account_id": accounts["CORRENTE"]["id"],
        "to_account_number": accounts["POUPANCA"]["account_number"],
        "amount": 1000.00,
        "description": "Transferência entre contas"
    }
    
    response = requests.post(f"{BASE_URL}/transactions/transfer", json=data, headers=headers)
    print_result("Transferência de R$ 1.000,00", response)
    return response.status_code in [200, 201]

def test_transaction_pix_send():
    """Teste 12: Enviar PIX"""
    print_section("TRANSAÇÕES - PIX Enviar")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "from_account_id": accounts["CORRENTE"]["id"],
        "pix_key": "12345678909",
        "amount": 250.00,
        "description": "PIX de teste"
    }
    
    response = requests.post(f"{BASE_URL}/transactions/pix/send", json=data, headers=headers)
    print_result("PIX de R$ 250,00", response)
    return response.status_code in [200, 201]

def test_transaction_bill_payment():
    """Teste 13: Pagar Conta"""
    print_section("TRANSAÇÕES - Pagamento de Conta")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "account_id": accounts["CORRENTE"]["id"],
        "bar_code": "23791234500000100009876543210123456789012345",
        "amount": 150.00,
        "description": "Conta de luz"
    }
    
    response = requests.post(f"{BASE_URL}/transactions/pay-bill", json=data, headers=headers)
    print_result("Pagamento de R$ 150,00", response)
    return response.status_code in [200, 201]

def test_transaction_statement():
    """Teste 14: Extrato"""
    print_section("TRANSAÇÕES - Extrato")
    
    headers = {"Authorization": f"Bearer {token}"}
    account_id = accounts["CORRENTE"]["id"]
    response = requests.get(f"{BASE_URL}/transactions/statement?account_id={account_id}", headers=headers)
    print_result("Consultar Extrato", response)
    return response.status_code == 200

def test_transaction_schedule():
    """Teste 15: Agendar Transação"""
    print_section("TRANSAÇÕES - Agendamento")
    
    headers = {"Authorization": f"Bearer {token}"}
    future_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    
    data = {
        "account_id": accounts["CORRENTE"]["id"],
        "transaction_type": "TRANSFER",
        "amount": 100.00,
        "scheduled_date": future_date,
        "description": "Transferência agendada",
        "to_account_id": accounts["POUPANCA"]["id"]
    }
    
    response = requests.post(f"{BASE_URL}/transactions/schedule", json=data, headers=headers)
    print_result(f"Agendar para {future_date}", response)
    return response.status_code in [200, 201]

def test_credit_card_request():
    """Teste 16: Solicitar Cartão de Crédito"""
    print_section("CARTÕES - Solicitar")
    
    # Primeiro faz depósito para melhorar score de crédito
    headers = {"Authorization": f"Bearer {token}"}
    deposit_data = {
        "account_id": accounts["CORRENTE"]["id"],
        "amount": 5000.00,
        "description": "Depósito para score de crédito"
    }
    requests.post(
        f"{BASE_URL}/transactions/deposit",
        json=deposit_data,
        headers=headers
    )
    
    # Agora solicita o cartão
    data = {
        "account_id": accounts["CORRENTE"]["id"],
        "requested_limit": 500.00  # Limite compatível com score
    }
    
    response = requests.post(
        f"{BASE_URL}/credit-cards/",
        json=data,
        headers=headers
    )
    result = print_result("Solicitar Cartão Platinum", response)
    
    if response.status_code in [200, 201]:
        credit_cards["PLATINUM"] = result.json()
        cvv = result.json().get('cvv')
        print(f"\n⚠️  ATENÇÃO: CVV = {cvv} (Salve agora!)")
        return True
    return False

def test_credit_card_list():
    """Teste 17: Listar Cartões"""
    print_section("CARTÕES - Listar")
    
    headers = {"Authorization": f"Bearer {token}"}
    account_id = accounts["CORRENTE"]["id"]
    response = requests.get(f"{BASE_URL}/credit-cards/?account_id={account_id}", headers=headers)
    print_result("Listar Cartões", response)
    return response.status_code == 200

def test_credit_card_purchase():
    """Teste 18: Fazer Compra no Cartão"""
    print_section("CARTÕES - Compra")
    
    if "PLATINUM" not in credit_cards:
        print("❌ ERRO em Compra Cartão: Cartão não foi criado")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    card_id = credit_cards["PLATINUM"]["id"]
    
    data = {
        "amount": 400.00,
        "merchant": "Loja de Eletrônicos",
        "installments": 3,
        "description": "Notebook"
    }
    
    response = requests.post(
        f"{BASE_URL}/credit-cards/{card_id}/purchase",
        json=data,
        headers=headers
    )
    print_result("Compra de R$ 400,00 em 3x", response)
    return response.status_code in [200, 201]

def test_credit_card_pay_bill():
    """Teste 19: Pagar Fatura do Cartão"""
    print_section("CARTÕES - Pagar Fatura")
    
    if "PLATINUM" not in credit_cards:
        print("❌ ERRO em Pagar Fatura: Cartão não foi criado")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    card_id = credit_cards["PLATINUM"]["id"]
    
    data = {
        "amount": 400.00
    }
    
    response = requests.post(
        f"{BASE_URL}/credit-cards/{card_id}/pay-bill",
        json=data,
        headers=headers
    )
    print_result("Pagar R$ 400,00", response)
    return response.status_code in [200, 201]


def test_account_create_investment():
    """Teste 20: Criar Conta Investimento"""
    print_section("CONTAS - Criar Conta Investimento")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {"account_type": "INVESTIMENTO"}
    
    response = requests.post(f"{BASE_URL}/accounts/", json=data, headers=headers)
    result = print_result("Criar Conta Investimento", response)
    
    if response.status_code in [200, 201]:
        accounts["INVESTIMENTO"] = result.json()
        return True
    return False

def test_investment_deposit():
    """Teste 21: Depositar na Conta Investimento"""
    print_section("INVESTIMENTOS - Depósito")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "account_id": accounts["INVESTIMENTO"]["id"],
        "amount": 10000.00,
        "description": "Capital para investimentos"
    }
    
    response = requests.post(f"{BASE_URL}/transactions/deposit", json=data, headers=headers)
    print_result("Depósito de R$ 10.000,00", response)
    return response.status_code in [200, 201]

def test_investment_list_assets():
    """Teste 22: Listar Ativos Disponíveis"""
    print_section("INVESTIMENTOS - Listar Ativos")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/investments/assets", headers=headers)
    print_result("Listar Ativos", response)
    return response.status_code == 200

def test_investment_buy_stock():
    """Teste 23: Comprar Ação"""
    print_section("INVESTIMENTOS - Comprar Ação")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "account_id": accounts["INVESTIMENTO"]["id"],
        "asset_id": 1,  # PETR4
        "quantity": 100
    }
    
    response = requests.post(f"{BASE_URL}/investments/buy", json=data, headers=headers)
    print_result("Comprar 100 PETR4", response)
    return response.status_code in [200, 201]

def test_investment_buy_fund():
    """Teste 24: Comprar Fundo Imobiliário"""
    print_section("INVESTIMENTOS - Comprar FII")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "account_id": accounts["INVESTIMENTO"]["id"],
        "asset_id": 5,  # HASH11
        "quantity": 50
    }
    
    response = requests.post(f"{BASE_URL}/investments/buy", json=data, headers=headers)
    print_result("Comprar 50 HASH11", response)
    return response.status_code in [200, 201]

def test_investment_portfolio():
    """Teste 25: Ver Portfólio"""
    print_section("INVESTIMENTOS - Portfólio")
    
    headers = {"Authorization": f"Bearer {token}"}
    account_id = accounts["INVESTIMENTO"]["id"]
    response = requests.get(f"{BASE_URL}/investments/portfolio?account_id={account_id}", headers=headers)
    print_result("Consultar Portfólio", response)
    return response.status_code == 200

def test_investment_sell():
    """Teste 26: Vender Ativo"""
    print_section("INVESTIMENTOS - Vender")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "account_id": accounts["INVESTIMENTO"]["id"],
        "asset_id": 5,  # HASH11
        "quantity": 25
    }
    
    response = requests.post(f"{BASE_URL}/investments/sell", json=data, headers=headers)
    print_result("Vender 25 HASH11", response)
    return response.status_code == 200

def test_investment_summary():
    """Teste 27: Resumo do Portfólio"""
    print_section("INVESTIMENTOS - Resumo")
    
    headers = {"Authorization": f"Bearer {token}"}
    account_id = accounts["INVESTIMENTO"]["id"]
    response = requests.get(f"{BASE_URL}/investments/portfolio/summary?account_id={account_id}", headers=headers)
    print_result("Resumo do Portfólio", response)
    return response.status_code == 200

def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "🚀"*40)
    print(" TESTE COMPLETO - DIGITAL SUPERBANK API ")
    print("🚀"*40)
    
    tests = [
        # Autenticação
        ("Registro", test_auth_register),
        ("Login Email", test_auth_login_email),
        ("Login CPF", test_auth_login_cpf),
        
        # Contas
        ("Criar Conta Corrente", test_account_create_corrente),
        ("Login com Conta", test_auth_login_account),
        ("Listar Contas", test_account_list),
        ("Consultar Saldo", test_account_balance),
        ("Criar Poupança", test_account_create_poupanca),
        
        # Transações
        ("Depósito", test_transaction_deposit),
        ("Saque", test_transaction_withdraw),
        ("Transferência", test_transaction_transfer),
        ("PIX", test_transaction_pix_send),
        ("Pagamento Conta", test_transaction_bill_payment),
        ("Extrato", test_transaction_statement),
        ("Agendamento", test_transaction_schedule),
        
        # Cartões
        ("Solicitar Cartão", test_credit_card_request),
        ("Listar Cartões", test_credit_card_list),
        ("Compra Cartão", test_credit_card_purchase),
        ("Pagar Fatura", test_credit_card_pay_bill),
        
        # Investimentos
        ("Conta Investimento", test_account_create_investment),
        ("Depósito Investimento", test_investment_deposit),
        ("Listar Ativos", test_investment_list_assets),
        ("Comprar Ação", test_investment_buy_stock),
        ("Comprar FII", test_investment_buy_fund),
        ("Ver Portfólio", test_investment_portfolio),
        ("Vender Ativo", test_investment_sell),
        ("Resumo Portfólio", test_investment_summary),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ ERRO em {name}: {str(e)}")
            results.append((name, False))
    
    # Resumo final
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES")
    print("="*80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        icon = "✅" if success else "❌"
        print(f"{icon} {name}")
    
    print(f"\n{'='*80}")
    print(f"📈 Resultado: {passed}/{total} testes passaram ({(passed/total)*100:.1f}%)")
    print("="*80)

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {str(e)}")
