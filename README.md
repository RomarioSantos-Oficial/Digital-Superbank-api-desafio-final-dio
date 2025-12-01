# 🏦 Digital Superbank — Guia Completo

Bem-vindo ao **Digital Superbank**, um sistema bancário completo criado para fins **didáticos e educacionais**, simulando um banco digital moderno com todas as funcionalidades de uma instituição financeira real.

> ⚠️ **Aviso:** Todos os dados são fictícios. Para uso comercial, entre em contato: **[Euoromario@gmail.com](mailto:Euoromario@gmail.com)**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)
[![Status](https://img.shields.io/badge/Status-99%25%20Completo-success.svg)](Backend/docs/FALTA.md)

---

## 📌 Índice

1. [Visão Geral](#-visão-geral)
2. [Pré-requisitos](#-pré-requisitos)
3. [Instalação Rápida](#-instalação-rápida-primeiro-uso)
4. [Como Usar Diariamente](#-como-usar-diariamente)
5. [Funcionalidades](#-funcionalidades)
6. [Estrutura do Projeto](#-estrutura-do-projeto)
7. [Scripts Úteis](#-scripts-úteis)
8. [Simulador de Mercado e Velas](#-simulador-de-mercado-e-velas)
9. [WebSocket (Tempo Real)](#-websocket-tempo-real)
10. [Testes](#-testes)
11. [Troubleshooting](#-troubleshooting)
12. [Tecnologias](#-tecnologias)
13. [Documentação Adicional](#-documentação-adicional)
14. [Contato](#-contato)

---

# 📦 Visão Geral


O **Digital Superbank** é uma aplicação full-stack que simula um banco digital completo, desenvolvida para fins educacionais com todas as funcionalidades de um banco moderno.

### 🎯 Componentes Principais

#### 🔧 **Backend — FastAPI**
* **Autenticação JWT** com refresh tokens
* **11 tipos de contas** (Corrente, Poupança, Black, Investimento, etc.)
* **Sistema completo de transações** (Depósito, Saque, Transferência, PIX, Boletos)
* **Cartões de crédito** (4 bandeiras, 3 categorias)
* **Investimentos** (Ações, Fundos, Renda Fixa)
* **WebSocket** com preços em tempo real
* **Gráficos de velas (OHLCV)** para análise técnica
* **Chatbot IA** com conhecimento bancário
* **SQLite** (2 bancos: principal + chatbot)

#### 💻 **Frontend — React + Vite**
* **Dashboard interativo** com visão geral
* **Cartões 3D** com flip animation
* **Sistema de investimentos profissional** com gráficos
* **Chatbot integrado** (Luna AI)
* **Notificações em tempo real**
* **Tema moderno** com Tailwind CSS + Framer Motion
* **Totalmente responsivo**

#### 🤖 **Chatbot — Luna AI**
* **Base de conhecimento** editável (31+ perguntas/respostas)
* **Busca semântica** inteligente
* **Sistema de aprendizado** (salva novas perguntas)
* **Navegação por comandos** (ir para investimentos, ver cartões, etc.)
* **Persistência** entre abas (localStorage)
* **Delay de digitação** (3 segundos) para efeito realista

#### 🛠️ **Scripts e Ferramentas**
* **Instalador automático** (`start.ps1`)
* **População de dados** (usuários demo, ativos, fundos, chatbot)
* **Gerador de velas históricas** (1 a 365 dias)
* **Simulador de mercado** em tempo real
* **Verificação de bancos** e integridade
* **Sistema de backup** para proteção de dados

---

# ⚙️ Pré-requisitos


Antes de começar, certifique-se de ter instalado:

### 📋 Requisitos Obrigatórios

| Software | Versão Mínima | Como Verificar | Download |
|----------|---------------|----------------|----------|
| **Windows** | 10+ | - | - |
| **PowerShell** | 5.1+ | `$PSVersionTable.PSVersion` | Incluído no Windows |
| **Python** | 3.8+ | `python --version` | [python.org](https://www.python.org/) |
| **Node.js** | 16+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 8+ | `npm --version` | Incluído com Node.js |
| **Git** | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com/) |

### ✅ Verificação Rápida

Execute no PowerShell para verificar tudo de uma vez:

```powershell
Write-Host "Python: " -NoNewline; python --version
Write-Host "Node.js: " -NoNewline; node --version
Write-Host "npm: " -NoNewline; npm --version
Write-Host "Git: " -NoNewline; git --version
```

### ⚠️ Importante

* **Python** deve estar no PATH do sistema
* **Feche servidores** antes de rodar scripts que escrevem no banco
* Recomendado: use o **Windows Terminal** para melhor experiência

---

# 🚀 Instalação Rápida (Primeiro Uso)


Este passo prepara **TUDO AUTOMATICAMENTE**: venv, pacotes, bancos de dados, ativos, fundos e chatbot.

### 📍 Passo a Passo

#### 1️⃣ Clone o Repositório

```powershell
git clone https://github.com/RomarioSantos-Oficial/Digital-Superbank-api-desafio-final-dio.git
cd Digital-Superbank-api-desafio-final-dio
```

#### 2️⃣ Execute o Instalador

```powershell
.\start.ps1
```

### 🎬 O que o instalador faz automaticamente:

```
🔧 ETAPA 1: Ambiente Python
   ✅ Cria .venv (se não existir)
   ✅ Ativa ambiente virtual
   ✅ Instala dependências do Backend

🔧 ETAPA 2: Ambiente Node.js
   ✅ cd Frontend
   ✅ npm install
   ✅ Volta para raiz

🔧 ETAPA 3: Banco de Dados Principal
   ✅ Cria tabelas (11 tabelas)
   ✅ init_db.py

🔧 ETAPA 4: Ações (OBRIGATÓRIO)
   ✅ Popula 30 ações variadas
   ✅ Salva em demo/acao.txt

🔧 ETAPA 5: Fundos de Investimento (OBRIGATÓRIO)
   ✅ Popula 25 fundos de investimento
   ✅ Salva em demo/fundo_investimento.txt

🔧 ETAPA 6: Chatbot (OBRIGATÓRIO)
   ✅ Popula 31 conhecimentos bancários
   ✅ Lê de demo/chatbot_conhecimento.txt
   ✅ Salva em chatbot.db

🔧 ETAPA 7: Usuários Demo (OPCIONAL)
   ❓ Pergunta se deseja criar
   ✅ Se SIM: cria 5 usuários de teste
   ✅ Salva em demo/pessoa.txt
```

### ⏱️ Tempo estimado: 2-3 minutos

### 📊 Resultado Final

Após a instalação, você terá:

| Item | Quantidade | Arquivo Gerado |
|------|------------|----------------|
| Tabelas no banco principal | 11 | `digital_superbank.db` |
| Tabelas no banco chatbot | 7 | `chatbot.db` |
| Ações de investimento | 30 | `demo/acao.txt` |
| Fundos de investimento | 25 | `demo/fundo_investimento.txt` |
| Conhecimentos chatbot | 31 | `demo/chatbot_conhecimento.txt` |
| Usuários demo (opcional) | 5 | `demo/pessoa.txt` |

### 🎯 Opções Adicionais do Instalador

#### Gerar Velas Históricas (para gráficos)

```powershell
.\start.ps1 -RunCandles -CandlesDays 7
```

Isso gera velas (OHLCV) dos últimos 7 dias para análise técnica.

#### Pular População do Chatbot

```powershell
.\start.ps1 -ExcludeChatbot
```

Útil se você já populou o chatbot antes.

#### Forçar Reinstalação Completa

```powershell
.\start.ps1 -InitSetup
```

Força a execução de todos os passos mesmo se já foram feitos.

---

# 🖥️ Como Usar Diariamente

Após a instalação inicial, inicie o sistema com **um único comando**:

### 🎯 Comando Principal

```powershell
.\start.ps1
```

### 🚀 O que acontece:

```
🔍 Verificando ambiente...
   ✅ Ativando .venv
   ✅ Instalando dependências faltantes

🌐 Iniciando Backend (porta 8000)...
   ✅ API rodando em http://localhost:8000
   ✅ Documentação em http://localhost:8000/docs
   ✅ Simulador de mercado ativo
   ✅ WebSocket disponível

💻 Iniciando Frontend (porta 3000)...
   ✅ Interface em http://localhost:3000
   ✅ Hot reload ativo

🎉 SISTEMA PRONTO!
```

### 📱 Acesse a Aplicação

| Interface | URL | Descrição |
|-----------|-----|------------|
| **Frontend** | http://localhost:3000 | Interface principal |
| **API Docs** | http://localhost:8000/docs | Swagger UI interativo |
| **ReDoc** | http://localhost:8000/redoc | Documentação alternativa |
| **WebSocket** | ws://localhost:8000/ws/market-feed | Feed em tempo real |

### 🛑 Como Parar

Pressione `Ctrl + C` nos terminais do Backend e Frontend.

### 🔄 Repopular Dados (se necessário)

Se precisar resetar ou adicionar mais dados:

```powershell
# Apenas repopular (mantém dados existentes com --update)
cd Backend
python scripts/populate_chatbot_from_file.py --update
python scripts/generate_stocks.py --update
python scripts/generate_funds.py --update
```

---

# ✨ Funcionalidades

### 🔐 Autenticação e Usuários

* ✅ **Registro** com validação de CPF e email
* ✅ **Login múltiplo** (Email, CPF ou Número da Conta)
* ✅ **JWT Tokens** com refresh automático
* ✅ **Proteção de rotas** no frontend e backend
* ✅ **Score de crédito** dinâmico
* ✅ **Perfil completo** editável

### 💰 Contas Bancárias

| Tipo | Requisitos | Saldo Mínimo | Características |
|------|------------|--------------|------------------|
| **Corrente** | Nenhum | R$ 0 | Conta padrão |
| **Poupança** | Nenhum | R$ 0 | Rendimento automático |
| **Salário** | Nenhum | R$ 0 | Para recebimento |
| **Universitária** | Nenhum | R$ 0 | Para estudantes |
| **Empresarial** | Nenhum | R$ 0 | Para empresas |
| **Investimento** | Black OU Empresarial | R$ 0 | Acesso a investimentos |
| **Black** | Score ≥ 700 | R$ 50.000 | Benefícios exclusivos |

* ✅ **Consulta de saldo** em tempo real
* ✅ **Extrato detalhado** com filtros
* ✅ **Validações automáticas** de pré-requisitos

### 💸 Transações

* ✅ **Depósito** (instantâneo)
* ✅ **Saque** (com validação de saldo)
* ✅ **Transferência** entre contas
* ✅ **PIX** (envio e recebimento)
  - Chave: CPF, Email, Telefone, Aleatória
  - QR Code dinâmico
* ✅ **Pagamento de boletos**
* ✅ **Agendamento** de transações futuras
* ✅ **Histórico completo** com busca

### 💳 Cartões de Crédito

#### Bandeiras Disponíveis
* 💳 Visa
* 💳 Mastercard
* 💳 Elo
* 💳 American Express

#### Categorias

| Categoria | Limite Inicial | Anuidade | Cashback |
|-----------|----------------|----------|----------|
| **Basic** | R$ 1.000 | R$ 0 | 0% |
| **Platinum** | R$ 5.000 | R$ 120/ano | 1% |
| **Black** | R$ 20.000 | R$ 500/ano | 3% |

* ✅ **Solicitação** com análise de score
* ✅ **Compras parceladas** (até 12x)
* ✅ **Pagamento de fatura** (total ou mínimo)
* ✅ **Bloqueio/Desbloqueio** instantâneo
* ✅ **Design 3D** com flip animation

### 📈 Investimentos

#### Ativos Disponíveis
* 📊 **30 Ações** (setores variados)
* 💼 **25 Fundos de Investimento**
* 💰 **Renda Fixa** (CDB, LCI, LCA)

#### Funcionalidades
* ✅ **Compra e venda** em tempo real
* ✅ **Portfolio consolidado** com rentabilidade
* ✅ **Histórico de preços** (7 períodos: 1D, 7D, 1M, 3M, 6M, 1Y, ALL)
* ✅ **Gráficos de velas (candlesticks)** para ações
* ✅ **Estatísticas** (Máxima/Mínima 24h, Variação %)
* ✅ **WebSocket** com preços atualizando a cada 60 segundos
* ✅ **Simulador de mercado** realista

### 🤖 Chatbot — Luna AI

* ✅ **31+ perguntas/respostas** sobre o banco
* ✅ **Busca semântica** inteligente
* ✅ **Sistema de aprendizado** (salva perguntas não conhecidas)
* ✅ **Navegação por comandos** ("ir para investimentos", "ver meus cartões")
* ✅ **Persistência** (conversa mantida entre abas)
* ✅ **Delay de digitação** (3s) para efeito realista
* ✅ **Sugestões contextuais** baseadas na conversa
* ✅ **Editable knowledge base** (arquivo TXT)

---

# 📂 Estrutura do Projeto

```
Digital-Superbank-api-desafio-final-dio/
│
├── 📄 start.ps1                          # Instalador e launcher principal
├── 📄 populate_all.ps1                   # Popula todos os bancos de dados
├── 📄 CHANGELOG_LIMPEZA.md              # Histórico de limpeza de código
├── 📄 README.md                         # Este arquivo
│
├── 📁 demo/                              # Dados gerados (editáveis)
│   ├── pessoa.txt                       # Usuários demo criados
│   ├── acao.txt                         # Ações populadas
│   ├── fundo_investimento.txt           # Fundos populados
│   └── chatbot_conhecimento.txt         # Base de conhecimento (31 Q&A)
│
├── 📁 Backend/                           # API FastAPI
│   ├── main.py                          # Entry point da API
│   ├── requirements.txt                 # Dependências Python
│   ├── digital_superbank.db             # Banco principal (SQLite)
│   ├── chatbot.db                       # Banco do chatbot (SQLite)
│   │
│   ├── 📁 src/                          # Código fonte
│   │   ├── 📁 api/v1/endpoints/         # 35 endpoints REST + WebSocket
│   │   ├── 📁 models/                   # 11 modelos SQLAlchemy
│   │   ├── 📁 services/                 # Lógica de negócio
│   │   ├── 📁 schemas/                  # Validação Pydantic
│   │   ├── 📁 database/                 # Conexões e sessões
│   │   ├── 📁 configs/                  # Configurações
│   │   └── 📁 utils/                    # Utilitários
│   │
│   ├── 📁 scripts/                      # Scripts de manutenção (16 arquivos)
│   │   ├── init_db.py                   # Cria tabelas
│   │   ├── generate_stocks.py           # Popula ações
│   │   ├── generate_funds.py            # Popula fundos
│   │   ├── add_fixed_income_assets.py   # Renda fixa
│   │   ├── generate_demo_users.py       # Usuários de teste
│   │   ├── generate_varied_users.py     # Usuários variados
│   │   ├── populate_chatbot_from_file.py # Popula chatbot (TXT)
│   │   ├── generate_historical_candles.py # Gera velas históricas
│   │   ├── market_simulator.py          # Simulador standalone
│   │   ├── check_databases.py           # Verifica ambos os bancos
│   │   ├── check_assets.py              # Verifica ativos
│   │   ├── check_investment_conditions.py # Valida investimentos
│   │   ├── clear_personal_data.py       # Limpa dados pessoais
│   │   ├── fix_user_data.py             # Corrige dados de usuários
│   │   ├── clean_old_candles.py         # Limpa velas antigas
│   │   └── README.md                    # Documentação dos scripts
│   │
│   ├── 📁 tests/                        # Testes automatizados
│   │   ├── test_all_services.py         # Teste completo
│   │   ├── test_new_features.py         # Features recentes
│   │   ├── test_complete_system.py      # Sistema completo
│   │   ├── test_chatbot.py              # Chatbot
│   │   ├── test_websocket.py            # WebSocket
│   │   └── README.md                    # Documentação dos testes
│   │
│   ├── 📁 docs/                         # Documentação técnica
│   │   ├── FALTA.md                     # Status (99% completo)
│   │   ├── IMPLEMENTACAO_FINAL.md       # Últimas features
│   │   ├── RELATORIO_COMPLETO_APROVACAO.md
│   │   ├── RELATORIO_TESTES_FINAL.md
│   │   ├── DATABASE_STRUCTURE.md        # Estrutura dos bancos
│   │   ├── CHATBOT_README.md            # Documentação chatbot
│   │   └── README.md                    # Índice da documentação
│   │
│   └── 📁 logs/                         # Logs da aplicação
│       ├── .gitignore                   # Ignora *.log
│       └── .gitkeep                     # Mantém pasta no git
│
└── 📁 Frontend/                          # Interface React
    ├── package.json                     # Dependências Node.js
    ├── vite.config.js                   # Configuração Vite
    ├── tailwind.config.js               # Configuração Tailwind
    ├── index.html                       # Entry point HTML
    │
    └── 📁 src/
        ├── App.jsx                      # Componente raiz
        ├── main.jsx                     # Entry point React
        ├── router.jsx                   # Rotas
        │
        ├── 📁 components/
        │   ├── 📁 common/               # Componentes reutilizáveis
        │   │   ├── FloatingChatbot.jsx  # Chatbot (Luna AI)
        │   │   ├── NotificationBell.jsx # Notificações
        │   │   └── ...outros
        │   ├── 📁 layout/               # Layout (Header, Sidebar)
        │   ├── 📁 cards/                # Cartões 3D
        │   └── 📁 investments/          # Gráficos e modais
        │       ├── CandlestickChart.jsx # Gráfico de velas
        │       └── CandlestickModal.jsx # Modal com estatísticas
        │
        ├── 📁 pages/                    # Páginas principais
        │   ├── Dashboard.jsx            # Dashboard
        │   ├── Accounts.jsx             # Contas
        │   ├── Transactions.jsx         # Transações
        │   ├── Cards.jsx                # Cartões
        │   ├── Investments.jsx          # Investimentos
        │   └── Profile.jsx              # Perfil
        │
        ├── 📁 services/                 # Comunicação API
        │   ├── api.js                   # Axios config
        │   ├── authService.js
        │   ├── accountService.js
        │   └── ...outros
        │
        ├── 📁 context/                  # Context API
        │   ├── AuthContext.jsx
        │   └── ...outros
        │
        ├── 📁 hooks/                    # Custom Hooks
        └── 📁 styles/                   # Estilos globais
```

### 📊 Estatísticas do Projeto

| Categoria | Quantidade |
|-----------|------------|
| **Backend** |
| Endpoints REST | 34 |
| WebSocket Endpoints | 1 |
| Modelos SQLAlchemy | 11 |
| Tabelas (banco principal) | 11 |
| Tabelas (banco chatbot) | 7 |
| Scripts de manutenção | 16 |
| Testes automatizados | 5 |
| **Frontend** |
| Páginas | 10+ |
| Componentes | 50+ |
| Rotas | 15+ |
| **Dados** |
| Ações | 30 |
| Fundos | 25 |
| Conhecimentos chatbot | 31 |
| Usuários demo (opcional) | 5 |

---

# 🛠️ Scripts Úteis


Todos os scripts estão em `Backend/scripts/`. Use com o ambiente virtual ativado.

### 📊 População de Dados

#### Ações de Investimento
```powershell
cd Backend
python scripts/generate_stocks.py
# Com flag --update (não deleta existentes)
python scripts/generate_stocks.py --update
```
**Gera:** 30 ações em 10 setores diferentes

#### Fundos de Investimento
```powershell
python scripts/generate_funds.py
# Ou com --update
python scripts/generate_funds.py --update
```
**Gera:** 25 fundos (Renda Fixa, Multimercado, Ações)

#### Renda Fixa
```powershell
python scripts/add_fixed_income_assets.py
```
**Adiciona:** CDB, LCI, LCA com taxas reais

#### Usuários Demo
```powershell
python scripts/generate_demo_users.py
```
**Cria:** 5 usuários de teste com contas e transações

#### Usuários Variados
```powershell
python scripts/generate_varied_users.py
```
**Cria:** Múltiplos usuários com perfis diferentes

#### Chatbot (Base de Conhecimento)
```powershell
python scripts/populate_chatbot_from_file.py --update
```
**Lê:** `demo/chatbot_conhecimento.txt` (31 Q&A)  
**Popula:** Banco `chatbot.db`

### 📈 Velas Históricas

Gera dados OHLCV para gráficos de análise técnica:

```powershell
# Últimos 7 dias
python scripts/generate_historical_candles.py --days 7

# Último mês
python scripts/generate_historical_candles.py --days 30

# Últimos 3 meses
python scripts/generate_historical_candles.py --days 90
```

**Características:**
- Gera velas de 1 minuto
- Apenas para AÇÕES (fundos têm valor fixo)
- Horário comercial: 9h-18h em dias úteis
- Random walk realista com volatilidade ±1.5%

### 🔍 Verificação e Manutenção

#### Verificar Bancos de Dados
```powershell
python scripts/check_databases.py
```
**Mostra:**
- Total de ativos (ações + fundos)
- Total de usuários
- Total de contas
- Total de conhecimentos do chatbot

#### Verificar Ativos
```powershell
python scripts/check_assets.py
```
**Detalha:** Todos os ativos com preços

#### Verificar Condições de Investimento
```powershell
python scripts/check_investment_conditions.py
```
**Valida:** Pré-requisitos para conta Black e Investimento

### 🧹 Limpeza

#### Limpar Dados Pessoais (CUIDADO!)
```powershell
python scripts/clear_personal_data.py
```
⚠️ **ATENÇÃO:** Deleta TODOS os usuários e dados relacionados!

#### Limpar Velas Antigas
```powershell
python scripts/clean_old_candles.py --days 30
```
Remove velas com mais de 30 dias

### 🔧 Correção

#### Corrigir Dados de Usuários
```powershell
python scripts/fix_user_data.py
```
Corrige inconsistências nos dados

### 🔄 População Completa (All-in-One)

```powershell
.\populate_all.ps1
```

**Flags disponíveis:**
- `-InstallDeps` — Instala dependências antes
- `-RunCandles` — Gera velas após popular
- `-Days N` — Quantidade de dias de velas (padrão: 7)
- `-ExcludeChatbot` — Pula população do chatbot
- `-ContinueOnError` — Continua mesmo com erros

**Exemplo completo:**
```powershell
.\populate_all.ps1 -InstallDeps -RunCandles -Days 30
```

---

# 📊 Simulador de Mercado e Velas

### ❗ `database is locked`

Feche o uvicorn antes de rodar scripts.

### ❗ `no such table: knowledge_base`

Execute primeiro:

```powershell
python Backend/scripts/update_chatbot_db.py
```

### ❗ Erros no Frontend

* Apague `node_modules`
* Rode `npm install`
* Verifique porta 3000

### ❗ Erros no Backend

* Ative venv: `.\.venv\Scripts\Activate.ps1`
* Reinstale: `pip install -r requirements.txt`

---

# 📬 9) Contato / Licença

Projeto educacional. Para uso comercial:
**[Euoromario@gmail.com](mailto:Euoromario@gmail.com)**

---


# 🏦 Digital Superbank — Official README (English Version)

Welcome to **Digital Superbank**, a complete educational banking system that simulates a real digital bank, featuring:

* **FastAPI Backend**
* **React + Vite Frontend**
* **Integrated AI Chatbot**
* **Market Simulator with Candlesticks (OHLCV)**

> ⚠️ **Notice:** All data in this project is fictional. For commercial use, contact: **[Euoromario@gmail.com](mailto:Euoromario@gmail.com)**

---

## 📌 Index

* Project Overview
* Requirements
* First‑time Installation
* Daily Usage
* Maintenance Scripts
* Useful Flags
* Project Structure
* Troubleshooting
* Contact / License

---

# 📦 1) Project Overview

### 🔧 Backend — FastAPI

* JWT Authentication
* Accounts, transactions, cards, investments
* Real‑time prices via WebSocket
* Candlestick chart generation (OHLCV)
* SQLite database

### 💻 Frontend — React + Vite

* Full dashboard
* 3D cards
* Professional investments module
* Integrated chatbot
* Modern UI with Tailwind + animations

### 🤖 Chatbot

* Dedicated knowledge‑base database
* Semantic search

### 🛠️ Scripts

* Populate users, assets, funds, candles
* Populate chatbot database
* Reset, cleanup, and maintenance

---

# ⚙️ 2) Requirements

* **Windows + PowerShell**
* **Python 3.8+** in PATH
* **Node.js 16+**
* Recommended: close servers before running scripts that modify the database

---

# 🚀 3) First‑time Installation

This step prepares EVERYTHING: venv, dependencies, databases, chatbot.

Run in PowerShell from the project root:

```powershell
cd Digital-Superbank-api-desafio-final-dio
./start.ps1 -InitSetup
```

### This command automatically:

* Creates `.venv` (if missing)
* Installs backend dependencies
* Installs frontend dependencies (`npm install`)
* Populates main database and Chatbot database
* Generates data files: `pessoa.txt`, `acao.txt`, `fundo_investimento.txt`, `chatbot.txt`

### Optional additions:

Generate historical candles:

```powershell
./start.ps1 -InitSetup -RunCandles -CandlesDays 7
```

Skip chatbot population:

```powershell
./start.ps1 -InitSetup -ExcludeChatbot
```

---

# 🖥️ 4) Daily Usage

After initial setup, use:

```powershell
./1.ps1
```

This script:

* Activates or creates venv
* Installs missing dependencies
* Starts Backend (port 8000)
* Starts Frontend (port 3000)

> Tip: `start.ps1` without flags also works as a quick starter.

---

# 🔧 5) Maintenance Scripts

Located in: `Backend/scripts`

### 📌 Main Database

Initialize tables:

```powershell
python Backend/scripts/init_db.py
```

Generate stocks:

```powershell
python Backend/scripts/generate_stocks.py
```

Generate funds:

```powershell
python Backend/scripts/generate_funds.py
```

Add fixed income assets:

```powershell
python Backend/scripts/add_fixed_income_assets.py
```

Demo users:

```powershell
python Backend/scripts/generate_demo_users.py
```

Varied users:

```powershell
python Backend/scripts/generate_varied_users.py
```

### 📌 Chatbot Database

Initialize tables:

```powershell
python Backend/scripts/update_chatbot_db.py
```

Full population:

```powershell
python Backend/scripts/populate_chatbot_full.py
```

Interactive mode:

```powershell
python Backend/scripts/populate_chatbot.py
```

### 📌 Candlesticks

```powershell
python Backend/scripts/generate_historical_candles.py --days 7
```

---

# 🛠️ Tecnologias

### Backend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem principal |
| **FastAPI** | 0.100+ | Framework web |
| **SQLAlchemy** | 2.0+ | ORM |
| **SQLite** | 3 | Banco de dados |
| **Pydantic** | 2.0+ | Validação |
| **JWT** | - | Autenticação |
| **WebSockets** | - | Tempo real |
| **Uvicorn** | - | Servidor ASGI |

### Frontend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **React** | 18+ | Framework UI |
| **Vite** | 4+ | Build tool |
| **Tailwind CSS** | 3+ | Estilização |
| **Framer Motion** | - | Animações |
| **React Router** | 6+ | Roteamento |
| **Axios** | - | HTTP client |
| **React Query** | - | State management |
| **Chart.js** | - | Gráficos |

---

# 📚 Documentação Adicional

### 📖 Documentos Técnicos

| Documento | Localização | Descrição |
|-----------|-------------|-----------|
| **Status do Projeto** | `Backend/docs/FALTA.md` | 99% completo, próximos passos |
| **Últimas Implementações** | `Backend/docs/IMPLEMENTACAO_FINAL.md` | Features recentes |
| **Estrutura do Banco** | `Backend/docs/DATABASE_STRUCTURE.md` | Tabelas e relacionamentos |
| **Chatbot** | `Backend/docs/CHATBOT_README.md` | Conhecimento e uso |
| **Relatório de Testes** | `Backend/docs/RELATORIO_TESTES_FINAL.md` | Resultados de testes |
| **Scripts** | `Backend/scripts/README.md` | Guia dos scripts |
| **Testes** | `Backend/tests/README.md` | Guia de testes |
| **Frontend** | `Frontend/README.md` | Componentes e rotas |
| **Limpeza de Código** | `CHANGELOG_LIMPEZA.md` | Histórico de refatoração |

### 📊 API Documentation

Quando a API estiver rodando:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 🎓 Tutoriais Incluídos

- **Como Iniciar com Mercado:** `Backend/COMO_INICIAR_COM_MERCADO.md`
- **Simulador README:** `Backend/SIMULADOR_README.md`
- **Sistema de Velas:** `Backend/SISTEMA_VELAS_README.md`

---

# 📊 Status do Projeto

### ✅ Completude: 99%

| Módulo | Status | Endpoints | Features |
|--------|--------|-----------|----------|
| **Autenticação** | ✅ 100% | 3/3 | Registro, Login, JWT |
| **Usuários** | ✅ 100% | 3/3 | Perfil, Score, Atualização |
| **Contas** | ✅ 100% | 7/7 | 7 tipos, Validações |
| **Transações** | ✅ 100% | 10/10 | 6 tipos, Agendamento |
| **Cartões** | ✅ 100% | 5/5 | 4 bandeiras, 3 categorias |
| **Investimentos** | ✅ 100% | 7/7 | Ações, Fundos, Velas |
| **WebSocket** | ✅ 100% | 1/1 | Preços, Velas |
| **Chatbot** | ✅ 100% | - | 31+ conhecimentos, Aprendizado |

**Total:** 36 endpoints (35 REST + 1 WebSocket)

### 🎯 1% Restante (Melhorias Futuras)

- [ ] Executor de agendamentos (cron job)
- [ ] Testes unitários completos (100% coverage)
- [ ] Notificações por email/SMS
- [ ] 2FA (autenticação de dois fatores)
- [ ] Modo escuro completo
- [ ] Exportação de extratos (PDF, CSV)
- [ ] Indicadores técnicos avançados (RSI, MACD)
- [ ] Open Banking API

---

# 🎯 Casos de Uso

### 👤 Para Estudantes

- **Aprender FastAPI** — Código bem estruturado e documentado
- **Entender JWT** — Sistema de autenticação completo
- **Praticar React** — Componentes modernos e hooks
- **Estudar SQLAlchemy** — ORM com relacionamentos complexos
- **Conhecer WebSockets** — Comunicação em tempo real

### 💼 Para Desenvolvedores

- **Portfolio** — Projeto full-stack completo
- **Template** — Base para projetos bancários
- **Referência** — Boas práticas e padrões
- **Testes** — Exemplos de testes automatizados

### 🏫 Para Professores

- **Material Didático** — Projeto real e funcional
- **Exercícios** — Base para atividades práticas
- **Demonstrações** — Sistema completo para aulas

---

# 🚀 Deploy (Produção)

### ⚠️ Importante

Este projeto é **educacional**. Para produção, considere:

1. **Banco de Dados:**
   - Migre de SQLite para PostgreSQL/MySQL
   - Configure backups automáticos

2. **Segurança:**
   - Use variáveis de ambiente (.env)
   - Configure HTTPS (SSL/TLS)
   - Implemente rate limiting
   - Adicione 2FA

3. **Performance:**
   - Configure cache (Redis)
   - Use CDN para frontend
   - Otimize queries do banco

4. **Monitoramento:**
   - Configure logs estruturados
   - Implemente APM (Sentry, New Relic)
   - Configure alertas

5. **Infraestrutura:**
   - Use containers (Docker)
   - Configure CI/CD
   - Use load balancer

### 📦 Build para Produção

#### Backend
```powershell
cd Backend
pip install -r requirements.txt
# Configure variáveis de ambiente
# Execute com Gunicorn ou similar
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

#### Frontend
```powershell
cd Frontend
npm run build
# Deploy pasta dist/ para servidor web (Nginx, Apache, Vercel, Netlify)
```

---

# 📞 Contato

### 👨‍💻 Desenvolvedor

**Romário Santos**  
📧 Email: [Euoromario@gmail.com](mailto:Euoromario@gmail.com)  
🐱 GitHub: [RomarioSantos-Oficial](https://github.com/RomarioSantos-Oficial)

### 📝 Licença

Este projeto foi desenvolvido para fins **educacionais** como parte do bootcamp da **Digital Innovation One (DIO)**.

**Uso Comercial:** Entre em contato pelo email acima.

---

# 🙏 Agradecimentos

- **Digital Innovation One (DIO)** — Bootcamp e desafio
- **FastAPI** — Framework incrível
- **React** — Biblioteca poderosa
- **Comunidade Open Source** — Ferramentas e bibliotecas

---

# 📋 Checklist Inicial

Use este checklist para garantir que tudo está funcionando:

### Primeira Vez

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Node.js 16+ instalado (`node --version`)
- [ ] Git instalado (`git --version`)
- [ ] Repositório clonado
- [ ] Executou `.\start.ps1` (instalação completa)
- [ ] Backend rodando (http://localhost:8000/docs)
- [ ] Frontend rodando (http://localhost:3000)
- [ ] WebSocket funcionando (teste com script)
- [ ] Criou usuário de teste
- [ ] Fez login no frontend

### Verificações

- [ ] **Banco Principal:** 55 ativos (30 ações + 25 fundos)
- [ ] **Banco Chatbot:** 31 conhecimentos
- [ ] **Usuários Demo:** 5 criados (opcional)
- [ ] **Velas:** Pelo menos 1 dia de histórico
- [ ] **Simulador:** Preços atualizando a cada 60s
- [ ] **Chatbot:** Respondendo perguntas
- [ ] **Gráficos:** Exibindo velas nas ações
- [ ] **Notificações:** Funcionando no sino

### Testes Funcionais

- [ ] Registro de novo usuário
- [ ] Login com email
- [ ] Criação de conta corrente
- [ ] Depósito de R$ 1.000
- [ ] Solicitação de cartão
- [ ] Compra de ação
- [ ] Visualização de gráfico de velas
- [ ] Conversa com chatbot
- [ ] WebSocket recebendo updates

---

# ❓ FAQ (Perguntas Frequentes)

### 1. Preciso pagar alguma coisa?

**Não!** Tudo é gratuito e open source.

### 2. Posso usar em produção?

Para uso **educacional**, sim. Para uso **comercial**, entre em contato.

### 3. Como adicionar mais ações/fundos?

Edite `Backend/scripts/generate_stocks.py` ou `generate_funds.py` e execute com `--update`.

### 4. Como editar as respostas do chatbot?

Edite `demo/chatbot_conhecimento.txt` e execute:
```powershell
python Backend/scripts/populate_chatbot_from_file.py --update
```

### 5. Preciso de Node.js se só quero testar o backend?

Não! Você pode usar apenas a API via Swagger UI (http://localhost:8000/docs).

### 6. Posso mudar as cores do frontend?

Sim! Edite `Frontend/tailwind.config.js` e `Frontend/src/styles/`.

### 7. Como adicionar novos endpoints?

Crie em `Backend/src/api/v1/endpoints/`, adicione a lógica em `services/` e registre em `main.py`.

### 8. O simulador de mercado funciona fora do horário comercial?

Sim! Ele roda 24/7. Para simular horário comercial (9h-18h), edite `candle_service.py`.

### 9. Quantos usuários simultâneos o sistema suporta?

Em desenvolvimento (SQLite), ~100 usuários. Para produção, migre para PostgreSQL.

### 10. Tem aplicativo mobile?

Não, apenas web. Mas o frontend é responsivo e funciona em smartphones.

---

# 🎉 Pronto para Começar!

```powershell
# Clone o projeto
git clone https://github.com/RomarioSantos-Oficial/Digital-Superbank-api-desafio-final-dio.git
cd Digital-Superbank-api-desafio-final-dio

# Execute o instalador
.\start.ps1

# Aguarde 2-3 minutos...

# Acesse http://localhost:3000

# 🚀 Bem-vindo ao Digital Superbank!
```

---

**⭐ Se este projeto foi útil, deixe uma estrela no GitHub!**

**📝 Desenvolvido com ❤️ para a comunidade de desenvolvedores**

*Última atualização: 1 de dezembro de 2025*

