# 🏦 Digital Superbank — README Oficial (Versão Focada e Organizada)

Bem-vindo ao **Digital Superbank**, um sistema bancário completo criado para fins **didáticos e educacionais**, simulando um banco real com:

* **Backend FastAPI**
* **Frontend React + Vite**
* **Chatbot integrado**
* **Simulador de mercado com velas (candles)**

> ⚠️ **Aviso:** Todos os dados aqui são fictícios. Para uso comercial, entre em contato: **[Euoromario@gmail.com](mailto:Euoromario@gmail.com)**

---

## 📌 Índice

* Visão Geral do Projeto
* Pré‑requisitos
* Instalação inicial (primeiro uso)
* Uso diário
* Scripts de manutenção
* Flags úteis
* Estrutura de pastas
* Solução de problemas
* Contato / Licença

---

# 📦 1) Visão Geral do Projeto

### 🔧 Backend — FastAPI

* Autenticação JWT
* Contas, transações, cartões, investimentos
* WebSocket com preços em tempo real
* Gráficos de velas (OHLCV)
* Banco SQLite

### 💻 Frontend — React + Vite

* Dashboard completo
* Cartões 3D
* Sistema de investimentos profissional
* Chatbot integrado
* Tema moderno com Tailwind + animações

### 🤖 Chatbot

* Base de conhecimento própria
* Busca semântica

### 🛠️ Scripts

* População de usuários, ativos, fundos, velas
* População do banco do chatbot
* Reset e manutenção geral

---

# ⚙️ 2) Pré‑requisitos

* **Windows + PowerShell**
* **Python 3.8+** configurado no PATH
* **Node.js 16+**
* Recomendado: Fechar servidores antes de rodar scripts que escrevem no banco

---

# 🚀 3) Instalação Inicial (Primeiro Uso)

Este passo prepara TUDO: venv, pacotes, bancos de dados, chatbot.

### 📍 Etapas

Abra o PowerShell na raiz do projeto e rode:

```powershell
cd Digital-Superbank-api-desafio-final-dio
.\start.ps1 -InitSetup
```

### O que este comando faz automaticamente:

* Cria ambiente virtual `.venv` (se não existir)
* Instala dependências do Backend
* Instala as dependências do Frontend (`npm install`)
* Popula o banco principal e o banco do Chatbot
* Gera arquivos: `pessoa.txt`, `acao.txt`, `fundo_investimento.txt`, `chatbot.txt`

### Opções adicionais:

Gerar velas históricas:

```powershell
.\start.ps1 -InitSetup -RunCandles -CandlesDays 7
```

Pular população do Chatbot:

```powershell
.\start.ps1 -InitSetup -ExcludeChatbot
```

---

# 🖥️ 4) Uso Diário (iniciar sistema normalmente)

Após a primeira instalação, use:

```powershell
.\1.ps1
```

Isso irá:

* Ativar ou criar o venv caso falte
* Instalar dependências faltantes
* Se necessário, executar `populate_all.ps1` (criação de tabelas e popular dados) — isto acontece quando `venv` foi criado agora, quando o DB principal está ausente, ou se você passou `-InitSetup`.
* Iniciar Backend (8000)
* Iniciar Frontend (3000)

> Dica: `start.ps1` também funciona sem flags como inicializador rápido.

### Parâmetros úteis para `1.ps1`
- `-InitSetup` : força a execução de `populate_all.ps1` (útil para repopular os DBs antes de iniciar)
- `-RunCandles` : gerar velas durante a execução do populate
- `-CandlesDays <N>` : dias de velas a gerar
- `-ExcludeChatbot` : pular popular o banco do Chatbot
- `-IncludeInteractiveChatbot` : usar o populate interativo do Chatbot
- `-ContinueOnError` : continuar mesmo após erros (útil em CI)

Exemplos:
```powershell
# Iniciar normalmente
.\1.ps1

# Forçar setup + popular antes de iniciar
.\1.ps1 -InitSetup

# Forçar setup com velas
.\1.ps1 -InitSetup -RunCandles -CandlesDays 7
```

---

# 🔧 5) Scripts Úteis de Manutenção

Localizados em: `Backend/scripts`

### 📌 Banco principal

Criar tabelas:

```powershell
python Backend/scripts/init_db.py
```

Ações:

```powershell
python Backend/scripts/generate_stocks.py
```

Fundos:

```powershell
python Backend/scripts/generate_funds.py
```

Renda fixa:

```powershell
python Backend/scripts/add_fixed_income_assets.py
```

Usuários demo:

```powershell
python Backend/scripts/generate_demo_users.py
```

Usuários variados:

```powershell
python Backend/scripts/generate_varied_users.py
```

### 📌 Banco do Chatbot

Criar tabelas:

```powershell
python Backend/scripts/update_chatbot_db.py
```

População completa:

```powershell
python Backend/scripts/populate_chatbot_full.py
```

Interativo:

```powershell
python Backend/scripts/populate_chatbot.py
```

### 📌 Velas (candles)

```powershell
python Backend/scripts/generate_historical_candles.py --days 7
```

---

# 🏷️ 6) Flags Principais

### `start.ps1`

* `-InitSetup` → instala tudo e popula bancos
* `-RunCandles` → gerar velas
* `-CandlesDays N` → quantidade de dias
* `-ExcludeChatbot` → não popular chatbot
* `-IncludeInteractiveChatbot` → versão interativa

### `populate_all.ps1`

* `-InstallDeps` → instala dependências
* `-RunCandles`
* `-Days N`
* `-ExcludeChatbot`
* `-IncludeInteractiveChatbot`
* `-ContinueOnError`

---

# 📂 7) Estrutura do Projeto (Resumo)

```
Digital Superbank/
├── Backend/
│   ├── main.py
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── database/
│   │   └── configs/
│   └── scripts/
│
├── Frontend/
│   ├── src/components/
│   ├── src/pages/
│   ├── src/services/
│   ├── vite.config.js
│
└── start.ps1
```

---

# 🐛 8) Troubleshooting Rápido

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

# 🏷️ 6) Main Flags

### `start.ps1`

* `-InitSetup` → full installation and database population
* `-RunCandles` → generate candlesticks
* `-CandlesDays N` → number of days
* `-ExcludeChatbot` → skip chatbot setup
* `-IncludeInteractiveChatbot` → interactive chatbot mode

### `populate_all.ps1`

* `-InstallDeps` → install dependencies
* `-RunCandles`
* `-Days N`
* `-ExcludeChatbot`
* `-IncludeInteractiveChatbot`
* `-ContinueOnError`

---

# 📂 7) Project Structure

```
Digital Superbank/
├── Backend/
│   ├── main.py
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── database/
│   │   └── configs/
│   └── scripts/
│
├── Frontend/
│   ├── src/components/
│   ├── src/pages/
│   ├── src/services/
│   ├── vite.config.js
│
└── start.ps1
```

---

# 🐛 8) Troubleshooting

### ❗ `database is locked`

Close uvicorn before running scripts.

### ❗ `no such table: knowledge_base`

Run:

```powershell
python Backend/scripts/update_chatbot_db.py
```

### ❗ Frontend errors

* Delete `node_modules`
* Run `npm install`
* Ensure port 3000 is free

### ❗ Backend errors

* Activate venv: `./.venv/Scripts/Activate.ps1`
* Reinstall: `pip install -r requirements.txt`

---

# 📬 9) Contact / License

Educational project. For commercial use:
**[Euoromario@gmail.com](mailto:Euoromario@gmail.com)**

---
