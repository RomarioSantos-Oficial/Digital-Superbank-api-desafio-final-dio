# 🧪 Testes - Digital Superbank

Esta pasta contém todos os scripts de teste da aplicação.

## 📋 Arquivos de Teste

### `test_all_services.py`
**Teste completo de todos os serviços da API**

Testa de forma integrada:
- ✅ Autenticação (registro, login com email/CPF/conta)
- ✅ Contas (criação, listagem, consulta de saldo)
- ✅ Transações (depósito, saque, transferência, PIX, pagamentos)
- ✅ Cartões de Crédito (solicitação, compras, pagamento de fatura)
- ✅ Investimentos (compra/venda de ativos, portfolio)

**Como executar:**
```bash
python tests/test_all_services.py
```

**Pré-requisitos:**
- API rodando em `http://localhost:8000`
- Banco de dados inicializado com ativos (`python scripts/init_db.py`)

---

### `test_new_features.py`
**Teste das funcionalidades mais recentes**

Testa especificamente:
- 📊 **Histórico de preços** - 7 períodos (1D, 7D, 1M, 3M, 6M, 1Y, ALL)
- 💎 **Validação Conta Black** - Saldo mínimo R$ 50.000
- 📈 **Validação Conta Investimento** - Pré-requisitos (Black OU Empresarial)

**Como executar:**
```bash
python tests/test_new_features.py
```

**Endpoints testados:**
- `GET /api/v1/investments/assets/{symbol}/history?period=1D`
- `GET /api/v1/accounts/{id}/validate-black`
- `GET /api/v1/accounts/{id}/validate-investment`

---

### `test_websocket.py`
**Teste de WebSocket em tempo real**

Conecta ao WebSocket e recebe streaming de preços:
- 🔌 Conexão ao endpoint `/ws/market-feed`
- 📡 Recebimento de atualizações em tempo real
- 📊 Exibição formatada dos preços

**Como executar:**
```bash
python tests/test_websocket.py
```

**Pré-requisitos:**
- API rodando em `http://localhost:8000`
- Simulador de mercado ativo (`python scripts/market_simulator.py`)

**O que você verá:**
```
📊 [2025-11-20 21:30:15] NEXG   - NexGen Innovations           | R$    45.32
📊 [2025-11-20 21:30:15] AETH   - AetherNet Solutions         | R$    72.58
```

---

## 🚀 Executar Todos os Testes

Para rodar todos os testes em sequência:

```bash
# Windows PowerShell
# Estando na raiz do projeto
python tests/test_all_services.py ; python tests/test_new_features.py
```

---

## 📊 Estrutura de Teste Recomendada

1. **Inicialize o banco:**
   ```bash
   python scripts/init_db.py
   ```

2. **Inicie a API:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Inicie o simulador (terminal separado):**
   ```bash
   python scripts/market_simulator.py --interval 5
   ```

4. **Execute os testes:**
   ```bash
   python tests/test_all_services.py
   python tests/test_new_features.py
   python tests/test_websocket.py
   ```

---

## 🔧 Dependências

Certifique-se de ter instalado:
```bash
pip install requests websockets
```

---

## 📝 Notas

- Todos os testes usam `http://localhost:8000` por padrão
- CPFs são gerados automaticamente nos testes
- Cada teste cria seus próprios usuários temporários
- Os testes são **não-destrutivos** - não afetam dados existentes
