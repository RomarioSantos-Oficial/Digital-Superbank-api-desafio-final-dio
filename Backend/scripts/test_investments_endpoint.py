"""
Script para testar o endpoint de investimentos
"""
import requests

BASE_URL = "http://localhost:8000"

print("\n🧪 TESTANDO ENDPOINT DE INVESTIMENTOS")
print("="*70)

try:
    # Testa GET /api/v1/investments/assets
    print("\n📡 GET /api/v1/investments/assets")
    response = requests.get(f"{BASE_URL}/api/v1/investments/assets")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total de ativos: {len(data)}")
        
        stocks = [a for a in data if a.get('asset_type') == 'STOCK']
        funds = [a for a in data if a.get('asset_type') == 'FUND']
        
        print(f"Ações: {len(stocks)}")
        print(f"Fundos: {len(funds)}")
        
        if stocks:
            print(f"\n📈 Primeira ação: {stocks[0].get('symbol')} - {stocks[0].get('name')}")
        if funds:
            print(f"💰 Primeiro fundo: {funds[0].get('symbol')} - {funds[0].get('name')}")
    else:
        print(f"Erro: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Erro: Backend não está rodando!")
    print("Execute: cd Backend && python main.py")
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "="*70)
