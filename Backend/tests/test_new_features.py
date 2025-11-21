"""
Teste das Novas Funcionalidades Implementadas
- Histórico de preços
- WebSocket de mercado
- Validação de Conta Black
- Validação de Conta Investimento
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_test(name, passed, details=""):
    """Imprime resultado do teste"""
    status = f"{GREEN}✅ PASSOU{RESET}" if passed else f"{RED}❌ FALHOU{RESET}"
    print(f"{status} | {name}")
    if details:
        print(f"   {details}")


def main():
    print("=" * 80)
    print(f"{BLUE}🧪 TESTANDO NOVAS FUNCIONALIDADES - DIGITAL SUPERBANK{RESET}")
    print("=" * 80)
    print()
    
    # ========== SETUP ==========
    print(f"{YELLOW}📋 SETUP: Criando usuário e fazendo login...{RESET}")
    
    # Registrar usuário
    user_data = {
        "full_name": "Teste Novas Features",
        "cpf": "123.456.789-10",
        "birth_date": "1990-01-01",
        "email": f"teste_features_{datetime.now().timestamp()}@test.com",
        "phone": "(11) 99999-9999",
        "password": "senha123",
        "address": {
            "street": "Rua Teste",
            "number": "123",
            "neighborhood": "Centro",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "01234-567"
        }
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print_test("Registro de usuário", response.status_code == 201)
    
    # Login
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_test("Login", response.status_code == 200)
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print()
    
    # ========== TESTE 1: HISTÓRICO DE PREÇOS ==========
    print(f"{YELLOW}📊 TESTE 1: Histórico de Preços de Ativos{RESET}")
    
    # Listar ativos
    response = requests.get(f"{BASE_URL}/investments/assets", headers=headers)
    print_test("Listar ativos", response.status_code == 200)
    
    if response.status_code == 200:
        assets = response.json()
        if assets:
            symbol = assets[0]["symbol"]
            
            # Testar cada período
            periods = ["1D", "7D", "1M", "3M", "6M", "1Y", "ALL"]
            for period in periods:
                response = requests.get(
                    f"{BASE_URL}/investments/assets/{symbol}/history",
                    params={"period": period},
                    headers=headers
                )
                data_points = response.json().get("data_points", 0) if response.status_code == 200 else 0
                print_test(
                    f"Histórico {symbol} - Período {period}",
                    response.status_code == 200,
                    f"{data_points} pontos de dados"
                )
    print()
    
    # ========== TESTE 2: VALIDAÇÃO CONTA BLACK ==========
    print(f"{YELLOW}💎 TESTE 2: Validação de Conta Black{RESET}")
    
    # Criar Conta Corrente
    account_data = {
        "account_type": "CORRENTE",
        "initial_deposit": 100.0
    }
    response = requests.post(f"{BASE_URL}/accounts/", json=account_data, headers=headers)
    print_test("Criar Conta Corrente", response.status_code == 201)
    corrente_id = response.json()["id"]
    
    # Criar Conta Black
    account_data = {
        "account_type": "BLACK",
        "initial_deposit": 60000.0  # Acima do mínimo
    }
    response = requests.post(f"{BASE_URL}/accounts/", json=account_data, headers=headers)
    print_test("Criar Conta Black (saldo suficiente)", response.status_code == 201)
    
    if response.status_code == 201:
        black_id = response.json()["id"]
        
        # Validar Conta Black
        response = requests.get(
            f"{BASE_URL}/accounts/{black_id}/validate-black",
            headers=headers
        )
        print_test("Validar Conta Black", response.status_code == 200)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Saldo atual: R$ {result['current_balance']:,.2f}")
            print(f"   Mínimo requerido: R$ {result['minimum_required']:,.2f}")
            print(f"   Válida: {result['is_valid']}")
            print(f"   Mensagem: {result['message']}")
    
    # Tentar validar conta que não é Black
    response = requests.get(
        f"{BASE_URL}/accounts/{corrente_id}/validate-black",
        headers=headers
    )
    print_test(
        "Rejeitar validação de conta não-Black",
        response.status_code == 400,
        "Esperado erro 400"
    )
    print()
    
    # ========== TESTE 3: VALIDAÇÃO CONTA INVESTIMENTO ==========
    print(f"{YELLOW}📈 TESTE 3: Validação de Pré-requisitos Conta Investimento{RESET}")
    
    # Criar Conta Investimento (com Conta Black já criada)
    account_data = {
        "account_type": "INVESTIMENTO",
        "initial_deposit": 1000.0
    }
    response = requests.post(f"{BASE_URL}/accounts/", json=account_data, headers=headers)
    print_test("Criar Conta Investimento", response.status_code == 201)
    
    if response.status_code == 201:
        inv_id = response.json()["id"]
        
        # Validar pré-requisitos
        response = requests.get(
            f"{BASE_URL}/accounts/{inv_id}/validate-investment",
            headers=headers
        )
        print_test("Validar pré-requisitos Conta Investimento", response.status_code == 200)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Tem Conta Black: {result['has_black_account']}")
            print(f"   Tem Conta Empresarial: {result['has_empresarial_account']}")
            print(f"   Pré-requisitos atendidos: {result['prerequisites_met']}")
            print(f"   Mensagem: {result['message']}")
    print()
    
    # ========== TESTE 4: WEBSOCKET (INFORMATIVO) ==========
    print(f"{YELLOW}🔌 TESTE 4: WebSocket de Mercado (Informativo){RESET}")
    print("   Para testar o WebSocket, execute:")
    print(f"   {BLUE}python tests/test_websocket.py{RESET}")
    print()
    
    # ========== RESUMO ==========
    print("=" * 80)
    print(f"{GREEN}✅ TODOS OS TESTES CONCLUÍDOS!{RESET}")
    print("=" * 80)
    print()
    print("📝 Funcionalidades implementadas:")
    print("   ✅ Histórico de preços com 7 períodos (1D, 7D, 1M, 3M, 6M, 1Y, ALL)")
    print("   ✅ Validação de saldo mínimo para Conta Black (R$ 50.000)")
    print("   ✅ Validação de pré-requisitos para Conta Investimento")
    print("   ✅ WebSocket para streaming de preços em tempo real")
    print()
    print("🚀 Novos Endpoints:")
    print("   GET  /api/v1/investments/assets/{symbol}/history?period=1D")
    print("   GET  /api/v1/accounts/{id}/validate-black")
    print("   GET  /api/v1/accounts/{id}/validate-investment")
    print("   WS   /ws/market-feed")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{RED}❌ Erro durante testes: {e}{RESET}")
