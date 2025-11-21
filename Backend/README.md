# 🏦 Digital Superbank - Backend API

> Sistema bancário completo com investimentos, cartões de crédito e streaming de dados em tempo real

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Status](https://img.shields.io/badge/Status-99%25%20Completo-success.svg)](docs/FALTA.md)

---

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Inicializar banco de dados
python scripts/init_db.py

# 3. Iniciar API (Terminal 1)
uvicorn main:app --reload

# 4. Iniciar simulador de mercado (Terminal 2)
python scripts/market_simulator.py --interval 5

# 5. Testar
python tests/test_all_services.py
```

**Acesse:** http://localhost:8000/docs

---

## 📁 Estrutura do Projeto

```
Backend/
├── 📂 src/                      # Código fonte
│   ├── api/v1/endpoints/        # Endpoints REST
│   ├── models/                  # Modelos SQLAlchemy
│   ├── services/                # Lógica de negócio
│   ├── configs/                 # Configurações
│   └── database/                # Conexão e sessões
│
├── 📂 tests/                    # Testes
│   ├── test_all_services.py    # Teste completo
│   ├── test_new_features.py    # Teste de features novas
│   ├── test_websocket.py       # Teste WebSocket
│   └── README.md               # Documentação dos testes
│
├── 📂 scripts/                  # Scripts utilitários
│   ├── init_db.py              # Inicializar banco
│   ├── market_simulator.py     # Simulador de mercado
│   ├── check_database.py       # Verificar banco
│   └── README.md               # Documentação dos scripts
│
├── 📂 docs/                     # Documentação
│   ├── FALTA.md                # Status e roadmap
│   ├── IMPLEMENTACAO_FINAL.md  # Últimas features
│   ├── Docmuntes.md            # Documentação geral
│   └── README.md               # Índice da documentação
│
├── 📂 alembic/                  # Migrações de banco
│
├── main.py                      # Entrada da aplicação
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

---

## ✨ Funcionalidades

### 🔐 Autenticação
- ✅ Registro de usuários com validação de CPF
- ✅ Login via Email / CPF / Número da Conta
- ✅ JWT com refresh token
- ✅ Proteção de rotas

### 💰 Contas Bancárias
- ✅ 7 tipos: Corrente, Poupança, Salário, Universitária, Empresarial, Investimento, Black
- ✅ Consulta de saldo e extrato
- ✅ Validação de saldo mínimo (Black: R$ 50.000)
- ✅ Validação de pré-requisitos (Investimento requer Black OU Empresarial)

### 💸 Transações
- ✅ Depósito
- ✅ Saque
- ✅ Transferência entre contas
- ✅ PIX (envio e recebimento)
- ✅ Pagamento de boletos
- ✅ Agendamento de transações

### 💳 Cartões de Crédito
- ✅ 4 bandeiras: Visa, Mastercard, Elo, American Express
- ✅ 3 categorias: Basic, Platinum, Black
- ✅ Solicitação com análise de score
- ✅ Compras parceladas
- ✅ Pagamento de fatura

### 📈 Investimentos
- ✅ 11 ativos (9 ações + 2 fundos)
- ✅ Compra e venda de ativos
- ✅ Portfolio consolidado
- ✅ Histórico de preços (7 períodos: 1D, 7D, 1M, 3M, 6M, 1Y, ALL)
- ✅ Simulador de mercado em tempo real
- ✅ **WebSocket com streaming de preços**

---

## 🔌 WebSocket - Tempo Real

### Endpoint: `ws://localhost:8000/ws/market-feed`

**Receba atualizações de preços em tempo real!**

```python
import asyncio
import websockets

async def watch_market():
    async with websockets.connect("ws://localhost:8000/ws/market-feed") as ws:
        while True:
            data = await ws.recv()
            print(data)  # {"type": "price_update", "symbol": "NEXG", ...}

asyncio.run(watch_market())
```

**Ou use nosso script pronto:**
```bash
python tests/test_websocket.py
```

---

## 📊 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| **Autenticação** |
| POST | `/api/v1/auth/register` | Registrar usuário |
| POST | `/api/v1/auth/login` | Login |
| **Contas** |
| POST | `/api/v1/accounts/` | Criar conta |
| GET | `/api/v1/accounts/` | Listar contas |
| GET | `/api/v1/accounts/{id}/balance` | Consultar saldo |
| GET | `/api/v1/accounts/{id}/validate-black` | 🆕 Validar Conta Black |
| GET | `/api/v1/accounts/{id}/validate-investment` | 🆕 Validar pré-requisitos |
| **Transações** |
| POST | `/api/v1/transactions/deposit` | Depósito |
| POST | `/api/v1/transactions/withdraw` | Saque |
| POST | `/api/v1/transactions/transfer` | Transferência |
| POST | `/api/v1/transactions/pix/send` | Enviar PIX |
| POST | `/api/v1/transactions/pay-bill` | Pagar boleto |
| GET | `/api/v1/transactions/statement` | Extrato |
| **Cartões** |
| POST | `/api/v1/credit-cards/` | Solicitar cartão |
| POST | `/api/v1/credit-cards/{id}/purchase` | Fazer compra |
| POST | `/api/v1/credit-cards/{id}/pay-bill` | Pagar fatura |
| **Investimentos** |
| GET | `/api/v1/investments/assets` | Listar ativos |
| GET | `/api/v1/investments/assets/{symbol}/history` | 🆕 Histórico de preços |
| POST | `/api/v1/investments/portfolio/buy` | Comprar ativo |
| POST | `/api/v1/investments/portfolio/sell` | Vender ativo |
| GET | `/api/v1/investments/portfolio` | Ver portfolio |
| **WebSocket** |
| WS | `/ws/market-feed` | 🆕 Streaming de preços |

**Total:** 35 endpoints (34 REST + 1 WebSocket)

---

## 🧪 Testes

### Teste Completo
```bash
python tests/test_all_services.py
```
Testa todos os módulos: autenticação, contas, transações, cartões e investimentos.

### Teste de Novas Features
```bash
python tests/test_new_features.py
```
Testa: histórico de preços, validações de Black/Investimento.

### Teste WebSocket
```bash
python tests/test_websocket.py
```
Conecta ao WebSocket e exibe preços em tempo real.

📖 **Mais detalhes:** [tests/README.md](tests/README.md)

---

## 🔧 Scripts Utilitários

### Inicializar Banco
```bash
python scripts/init_db.py
```
Cria tabelas e popula com 11 ativos de investimento.

### Simulador de Mercado
```bash
python scripts/market_simulator.py --interval 5
```
Atualiza preços a cada 5 segundos + notifica WebSocket.

### Verificar Banco
```bash
python scripts/check_database.py
```
Exibe estatísticas do banco de dados.

📖 **Mais detalhes:** [scripts/README.md](scripts/README.md)

---

## 📚 Documentação

- **[FALTA.md](docs/FALTA.md)** - Status do projeto (99% completo)
- **[IMPLEMENTACAO_FINAL.md](docs/IMPLEMENTACAO_FINAL.md)** - Últimas features implementadas
- **[Swagger UI](http://localhost:8000/docs)** - Documentação interativa (quando API estiver rodando)
- **[ReDoc](http://localhost:8000/redoc)** - Documentação alternativa

📖 **Mais detalhes:** [docs/README.md](docs/README.md)

---

## 🛠️ Tecnologias

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados (dev)
- **Alembic** - Migrações de banco
- **Pydantic** - Validação de dados
- **JWT** - Autenticação
- **WebSockets** - Comunicação em tempo real

---

## 📊 Status do Projeto

### ✅ Completude: 99%

| Módulo | Status | Endpoints |
|--------|--------|-----------|
| Autenticação | ✅ 100% | 3/3 |
| Usuários | ✅ 100% | 3/3 |
| Contas | ✅ 100% | 7/7 |
| Transações | ✅ 100% | 10/10 |
| Cartões | ✅ 100% | 5/5 |
| Investimentos | ✅ 100% | 7/7 |
| WebSocket | ✅ 100% | 1/1 |

### 🎯 Próximos Passos (1% restante)
- ⏰ Executor de agendamentos (cron job)
- 🧪 Testes unitários completos
- 📧 Notificações por email/SMS (opcional)
- 🔐 2FA (opcional)
- 🤖 Chatbot de atendimento (opcional)

---

## 🚦 Como Usar

### 1️⃣ Setup Inicial
```bash
# Clone o repositório
git clone <repo-url>
cd Backend

# Instale dependências
pip install -r requirements.txt

# Inicialize o banco
python scripts/init_db.py
```

### 2️⃣ Desenvolvimento
```bash
# Terminal 1: API com hot-reload
uvicorn main:app --reload

# Terminal 2: Simulador de mercado
python scripts/market_simulator.py --interval 5

# Terminal 3: Testes
python tests/test_websocket.py
```

### 3️⃣ Explorar API
Abra: http://localhost:8000/docs

---

## 💡 Exemplos de Uso

### Registrar e Fazer Login
```python
import requests

# Registrar
response = requests.post("http://localhost:8000/api/v1/auth/register", json={
    "full_name": "João Silva",
    "cpf": "123.456.789-10",
    "email": "joao@email.com",
    "password": "senha123",
    "birth_date": "1990-01-01",
    "phone": "(11) 99999-9999"
})

# Login
response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "identifier": "joao@email.com",
    "password": "senha123"
})

token = response.json()["access_token"]
```

### Criar Conta e Fazer Depósito
```python
headers = {"Authorization": f"Bearer {token}"}

# Criar conta
response = requests.post("http://localhost:8000/api/v1/accounts/", 
    json={"account_type": "CORRENTE"},
    headers=headers
)
account_id = response.json()["id"]

# Depositar
requests.post("http://localhost:8000/api/v1/transactions/deposit",
    json={
        "account_id": account_id,
        "amount": 1000.00,
        "description": "Depósito inicial"
    },
    headers=headers
)
```

### Conectar ao WebSocket
```python
import asyncio
import websockets
import json

async def watch_prices():
    async with websockets.connect("ws://localhost:8000/ws/market-feed") as ws:
        async for message in ws:
            data = json.loads(message)
            if data["type"] == "price_update":
                print(f"{data['symbol']}: R$ {data['price']:.2f}")

asyncio.run(watch_prices())
```

---

## 📞 Suporte

- **Documentação:** [docs/](docs/)
- **Testes:** [tests/](tests/)
- **Scripts:** [scripts/](scripts/)

---

## 📄 Licença

Este é um projeto educacional da DIO (Digital Innovation One).

---

**Desenvolvido com ❤️ usando FastAPI**

*Última atualização: 20 de novembro de 2025*
