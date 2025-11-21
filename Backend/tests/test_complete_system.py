"""
Teste completo de todas as funcionalidades do Digital Superbank
"""
import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

# Dados de teste (gerar CPF novo a cada execução para evitar duplicatas)
import random

def generate_cpf():
    """Gera CPF válido aleatório"""
    def calculate_digit(digs):
        s = 0
        qtd = len(digs) + 1
        for i in range(len(digs)):
            s += int(digs[i]) * (qtd - i)
        res = 11 - (s % 11)
        return 0 if res > 9 else res
    
    cpf_base = [random.randint(0, 9) for _ in range(9)]
    d1 = calculate_digit(cpf_base)
    d2 = calculate_digit(cpf_base + [d1])
    cpf_numbers = cpf_base + [d1, d2]
    cpf_str = ''.join(map(str, cpf_numbers))
    return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"

test_user = {
    "full_name": "João Silva Teste",
    "email": f"joao.teste.{int(time.time())}@example.com",
    "cpf": generate_cpf(),
    "birth_date": "1990-01-15",
    "phone": "(11) 99999-9999",
    "password": "senha12345"
}

token = None
user_data = None
account_id = None
card_id = None


def print_header(title):
    """Imprime cabeçalho de seção"""
    print(f"\n{'='*80}")
    print(f"{CYAN}{title}{RESET}")
    print(f"{'='*80}")


def print_test(name, success, details=""):
    """Imprime resultado de teste"""
    status = f"{GREEN}✅ PASS{RESET}" if success else f"{RED}❌ FAIL{RESET}"
    print(f"{status} - {name}")
    if details:
        print(f"    {YELLOW}{details}{RESET}")


def test_health_check():
    """Testa health check"""
    print_header("🏥 HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        success = response.status_code == 200
        print_test("GET /", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    App: {data.get('app')}")
            print(f"    Status: {data.get('status')}")
            
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        success = response.status_code == 200
        print_test("GET /health", success, f"Status: {response.status_code}")
        
        return True
    except Exception as e:
        print_test("Health Check", False, str(e))
        return False


def test_user_registration():
    """Testa registro de usuário"""
    global user_data
    print_header("👤 REGISTRO DE USUÁRIO")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json=test_user,
            timeout=10
        )
        
        success = response.status_code == 201
        print_test("POST /auth/register", success, f"Status: {response.status_code}")
        
        if success:
            user_data = response.json()
            print(f"    ID: {user_data.get('id')}")
            print(f"    Nome: {user_data.get('full_name')}")
            print(f"    Email: {user_data.get('email')}")
        else:
            print(f"    {RED}Erro: {response.text}{RESET}")
            
        return success
    except Exception as e:
        print_test("Registro de usuário", False, str(e))
        return False


def test_user_login():
    """Testa login de usuário"""
    global token
    print_header("🔐 LOGIN")
    
    try:
        # Login com email
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "identifier": test_user["email"],
                "password": test_user["password"]
            },
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("POST /auth/login (email)", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            token = data.get("access_token")
            print(f"    Token: {token[:50]}...")
            print(f"    Tipo: {data.get('token_type')}")
        else:
            print(f"    {RED}Erro: {response.text}{RESET}")
            
        return success
    except Exception as e:
        print_test("Login", False, str(e))
        return False


def test_get_profile():
    """Testa obter perfil do usuário"""
    print_header("📋 PERFIL DO USUÁRIO")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("GET /auth/me", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Nome: {data.get('full_name')}")
            print(f"    Email: {data.get('email')}")
            print(f"    CPF: {data.get('cpf')}")
            
        return success
    except Exception as e:
        print_test("Obter perfil", False, str(e))
        return False


def test_create_account():
    """Testa criação de conta"""
    global account_id
    print_header("🏦 CRIAÇÃO DE CONTA")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Criar conta corrente
        response = requests.post(
            f"{API_URL}/accounts/",
            headers=headers,
            json={
                "account_type": "CORRENTE",
                "initial_deposit": 0
            },
            timeout=10
        )
        
        success = response.status_code in [200, 201]
        print_test("POST /accounts/ (CORRENTE)", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            account_id = data.get("id")
            print(f"    ID: {account_id}")
            print(f"    Número: {data.get('account_number')}-{data.get('digit')}")
            print(f"    Tipo: {data.get('account_type')}")
            print(f"    Saldo: R$ {data.get('balance'):.2f}")
            
        return success
    except Exception as e:
        print_test("Criar conta", False, str(e))
        return False


def test_list_accounts():
    """Testa listagem de contas"""
    print_header("📊 LISTAGEM DE CONTAS")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/accounts/",
            headers=headers,
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("GET /accounts/", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Total de contas: {len(data)}")
            for account in data:
                print(f"    - {account['account_type']}: R$ {account['balance']:.2f}")
                
        return success
    except Exception as e:
        print_test("Listar contas", False, str(e))
        return False


def test_deposit():
    """Testa depósito"""
    print_header("💰 DEPÓSITO")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Fazer múltiplos depósitos para aumentar score de crédito
        amounts = [5000.00, 2000.00, 1000.00]
        total = 0
        
        for i, amount in enumerate(amounts, 1):
            response = requests.post(
                f"{API_URL}/transactions/deposit",
                headers=headers,
                json={
                    "account_id": account_id,
                    "amount": amount,
                    "description": f"Depósito {i} teste"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                total += amount
        
        # Verifica último depósito
        success = response.status_code == 200
        print_test("POST /transactions/deposit", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Total depositado: R$ {total:.2f}")
            print(f"    Status: {data.get('status')}")
        elif response.status_code == 422:
            print(f"    {RED}Erro de validação: {response.json()}{RESET}")
        else:
            print(f"    {RED}Erro: {response.text}{RESET}")
            
        return success
    except Exception as e:
        print_test("Depósito", False, str(e))
        return False


def test_get_balance():
    """Testa consulta de saldo"""
    print_header("💵 CONSULTA DE SALDO")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/accounts/{account_id}/balance",
            headers=headers,
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("GET /accounts/{id}/balance", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Saldo: R$ {data.get('balance'):.2f}")
            
        return success
    except Exception as e:
        print_test("Consultar saldo", False, str(e))
        return False


def test_withdrawal():
    """Testa saque"""
    print_header("🏧 SAQUE")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/transactions/withdraw",
            headers=headers,
            json={
                "account_id": account_id,
                "amount": 100.00,
                "description": "Saque teste"
            },
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("POST /transactions/withdraw", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Valor: R$ {data.get('amount'):.2f}")
            print(f"    Status: {data.get('status')}")
        elif response.status_code == 422:
            print(f"    {RED}Erro de validação: {response.json()}{RESET}")
        else:
            print(f"    {RED}Erro: {response.text}{RESET}")
            
        return success
    except Exception as e:
        print_test("Saque", False, str(e))
        return False


def test_get_statement():
    """Testa extrato"""
    print_header("📜 EXTRATO")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/accounts/{account_id}/statement",
            headers=headers,
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("GET /accounts/{id}/statement", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Total de transações: {len(data)}")
            for tx in data[:3]:
                print(f"    - {tx['transaction_type']}: R$ {tx['amount']:.2f}")
                
        return success
    except Exception as e:
        print_test("Obter extrato", False, str(e))
        return False


def test_create_credit_card():
    """Testa criação de cartão"""
    global card_id
    print_header("💳 CARTÃO DE CRÉDITO")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_URL}/credit-cards/",
            headers=headers,
            json={
                "account_id": account_id
                # Sem requested_limit - deixa o sistema definir
            },
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("POST /credit-cards/", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            card_id = data.get("id")
            print(f"    ID: {card_id}")
            print(f"    Número: {data.get('card_number')}")
            print(f"    Categoria: {data.get('card_category')}")
            print(f"    Limite: R$ {data.get('credit_limit'):.2f}")
            print(f"    CVV: {data.get('cvv')}")
        elif response.status_code == 400:
            print(f"    {RED}Erro: {response.json().get('detail')}{RESET}")
        else:
            print(f"    {RED}Erro: {response.text}{RESET}")
            
        return success
    except Exception as e:
        print_test("Criar cartão", False, str(e))
        return False


def test_list_investments():
    """Testa listagem de investimentos"""
    print_header("📈 INVESTIMENTOS DISPONÍVEIS")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/investments/assets",
            headers=headers,
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("GET /investments/assets", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Total de ativos: {len(data)}")
            for asset in data[:5]:
                print(f"    - {asset['symbol']}: R$ {asset['current_price']:.2f}")
                
        return success
    except Exception as e:
        print_test("Listar investimentos", False, str(e))
        return False


def test_chatbot():
    """Testa chatbot"""
    print_header("🤖 CHATBOT")
    
    try:
        # Teste 1: Pergunta sobre saldo
        response = requests.post(
            f"{API_URL}/chatbot/message",
            json={"message": "Como consultar meu saldo?"},
            timeout=10
        )
        
        success = response.status_code == 200
        print_test("POST /chatbot/message (pergunta 1)", success, f"Status: {response.status_code}")
        
        if success:
            data = response.json()
            print(f"    Resposta: {data['response'][:100]}...")
            print(f"    Intenção: {data.get('intent')}")
            print(f"    Confiança: {data.get('confidence')}")
            session_id = data.get('session_id')
            
            # Teste 2: Outra pergunta na mesma sessão
            response = requests.post(
                f"{API_URL}/chatbot/message",
                json={
                    "message": "Como fazer PIX?",
                    "session_id": session_id
                },
                timeout=10
            )
            
            success2 = response.status_code == 200
            print_test("POST /chatbot/message (pergunta 2)", success2, f"Status: {response.status_code}")
            
            if success2:
                data2 = response.json()
                print(f"    Resposta: {data2['response'][:100]}...")
                print(f"    Intenção: {data2.get('intent')}")
                
        # Teste 3: Sugestões
        response = requests.get(
            f"{API_URL}/chatbot/suggestions?limit=3",
            timeout=10
        )
        
        success3 = response.status_code == 200
        print_test("GET /chatbot/suggestions", success3, f"Status: {response.status_code}")
        
        if success3:
            suggestions = response.json()
            print(f"    Sugestões: {len(suggestions)} perguntas")
            
        return success and success2 and success3
    except Exception as e:
        print_test("Chatbot", False, str(e))
        return False


def run_all_tests():
    """Executa todos os testes"""
    print(f"\n{CYAN}{'='*80}{RESET}")
    print(f"{CYAN}🧪 TESTANDO TODAS AS FUNCIONALIDADES - DIGITAL SUPERBANK{RESET}")
    print(f"{CYAN}{'='*80}{RESET}")
    print(f"{YELLOW}Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{RESET}")
    print(f"{YELLOW}URL: {BASE_URL}{RESET}")
    
    # Aguardar servidor iniciar
    print(f"\n{YELLOW}⏳ Aguardando servidor iniciar...{RESET}")
    time.sleep(3)
    
    results = []
    
    # Executar testes em ordem
    results.append(("Health Check", test_health_check()))
    results.append(("Registro de Usuário", test_user_registration()))
    results.append(("Login", test_user_login()))
    results.append(("Perfil do Usuário", test_get_profile()))
    results.append(("Criação de Conta", test_create_account()))
    results.append(("Listagem de Contas", test_list_accounts()))
    results.append(("Depósito", test_deposit()))
    results.append(("Consulta de Saldo", test_get_balance()))
    results.append(("Saque", test_withdrawal()))
    results.append(("Extrato", test_get_statement()))
    results.append(("Cartão de Crédito", test_create_credit_card()))
    results.append(("Investimentos", test_list_investments()))
    results.append(("Chatbot", test_chatbot()))
    
    # Resumo
    print_header("📊 RESUMO DOS TESTES")
    
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    print(f"\n{GREEN}✅ Testes aprovados: {passed}/{len(results)}{RESET}")
    if failed > 0:
        print(f"{RED}❌ Testes falhados: {failed}/{len(results)}{RESET}")
        print(f"\n{RED}Testes que falharam:{RESET}")
        for name, success in results:
            if not success:
                print(f"  - {name}")
    
    success_rate = (passed / len(results)) * 100
    print(f"\n{CYAN}Taxa de sucesso: {success_rate:.1f}%{RESET}")
    
    if success_rate == 100:
        print(f"\n{GREEN}{'='*80}{RESET}")
        print(f"{GREEN}🎉 TODOS OS TESTES PASSARAM! APLICAÇÃO 100% FUNCIONAL!{RESET}")
        print(f"{GREEN}{'='*80}{RESET}")
    elif success_rate >= 80:
        print(f"\n{YELLOW}{'='*80}{RESET}")
        print(f"{YELLOW}⚠️  APLICAÇÃO FUNCIONAL COM ALGUMAS FALHAS{RESET}")
        print(f"{YELLOW}{'='*80}{RESET}")
    else:
        print(f"\n{RED}{'='*80}{RESET}")
        print(f"{RED}❌ APLICAÇÃO COM PROBLEMAS CRÍTICOS{RESET}")
        print(f"{RED}{'='*80}{RESET}")
    
    print()


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⛔ Testes interrompidos pelo usuário{RESET}")
    except Exception as e:
        print(f"\n\n{RED}❌ Erro durante execução dos testes: {e}{RESET}")
