# 🏦 Digital Superbank — Guia Completo

> 🌍 **Idiomas:** [Português](README.pt-BR.md) | [English](README.en.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Español](README.es.md)

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

## 📦 Visão Geral

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
* **Navegação por comandos** ("ir para investimentos", "ver cartões", etc.)
* **Persistência** entre abas (localStorage)
* **Delay de digitação** (3 segundos) para efeito realista

---

## ⚙️ Pré-requisitos

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

---

## 🚀 Instalação Rápida (Primeiro Uso)

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

---

## 🖥️ Como Usar Diariamente

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

---

## ✨ Funcionalidades

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

### 💸 Transações

* ✅ **Depósito** (instantâneo)
* ✅ **Saque** (com validação de saldo)
* ✅ **Transferência** entre contas
* ✅ **PIX** (envio e recebimento)
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

---

## 📂 Estrutura do Projeto

```
Digital-Superbank-api-desafio-final-dio/
│
├── 📄 start.ps1                          # Instalador e launcher principal
├── 📄 README.md                          # Este arquivo
├── 📄 README.pt-BR.md                   # Versão em Português
├── 📄 README.en.md                      # English Version
├── 📄 README.ja.md                      # 日本語版
├── 📄 README.zh.md                      # 中文版
├── 📄 README.es.md                      # Versión en Español
│
├── 📁 demo/                              # Dados fictícios para teste
│   ├── pessoa.txt                       # 37 usuários demo
│   ├── acao.txt                         # Ações de investimento
│   ├── fundo_investimento.txt           # Fundos de investimento
│   └── chatbot_conhecimento.txt         # Base de conhecimento (31 Q&A)
│
├── 📁 Backend/                           # API FastAPI
│   ├── main.py                          # Entry point da API
│   ├── requirements.txt                 # Dependências Python
│   ├── digital_superbank.db             # Banco principal (SQLite)
│   ├── chatbot.db                       # Banco do chatbot (SQLite)
│   ├── 📁 src/                          # Código fonte
│   ├── 📁 scripts/                      # Scripts de manutenção (16 arquivos)
│   ├── 📁 tests/                        # Testes automatizados
│   └── 📁 docs/                         # Documentação técnica
│
└── 📁 Frontend/                          # Interface React
    ├── package.json                     # Dependências Node.js
    └── 📁 src/                          # Código fonte React
```

---

## 🛠️ Scripts Úteis

Todos os scripts estão em `Backend/scripts/`. Use com o ambiente virtual ativado.

### 📊 População de Dados

#### Ações de Investimento
```powershell
cd Backend
python scripts/generate_stocks.py --update
```

#### Fundos de Investimento
```powershell
python scripts/generate_funds.py --update
```

#### Chatbot (Base de Conhecimento)
```powershell
python scripts/populate_chatbot_from_file.py --update
```

### 📈 Velas Históricas

```powershell
# Últimos 7 dias
python scripts/generate_historical_candles.py --days 7
```

### 🔍 Verificação

```powershell
# Verificar bancos de dados
python scripts/check_databases.py
```

---

## 📊 Simulador de Mercado e Velas

O sistema inclui um **simulador de mercado** que atualiza preços de ações em tempo real:

* **Atualização:** A cada 60 segundos
* **Variação:** ±1.5% por atualização
* **Velas:** Geradas automaticamente (OHLCV)
* **WebSocket:** Transmite atualizações para o frontend

### Como funciona:

1. O simulador roda automaticamente quando você inicia o Backend
2. Preços são atualizados usando random walk realista
3. Velas (candlesticks) são geradas e armazenadas no banco
4. WebSocket envia atualizações para todos os clientes conectados

---

## 🌐 WebSocket (Tempo Real)

O sistema usa WebSocket para comunicação em tempo real:

### Endpoint
```
ws://localhost:8000/ws/market-feed
```

### O que é transmitido:
* **Preços de ações** atualizados
* **Novas velas** (candlesticks)
* **Estatísticas** (máxima/mínima 24h, variação %)

### Como conectar (JavaScript):
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market-feed');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Atualização de mercado:', data);
};
```

---

## 🧪 Testes

Execute os testes automatizados:

```powershell
cd Backend/tests

# Teste completo do sistema
python test_complete_system.py

# Teste de todos os serviços
python test_all_services.py

# Teste do chatbot
python test_chatbot.py

# Teste do WebSocket
python test_websocket.py
```

---

## ❓ Troubleshooting

### ❗ `database is locked`

Feche o uvicorn antes de rodar scripts que escrevem no banco.

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

## 🛠️ Tecnologias

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

### Frontend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **React** | 18+ | Framework UI |
| **Vite** | 4+ | Build tool |
| **Tailwind CSS** | 3+ | Estilização |
| **Framer Motion** | - | Animações |
| **React Router** | 6+ | Roteamento |
| **Axios** | - | HTTP client |
| **Chart.js** | - | Gráficos |

---

## 📚 Documentação Adicional

### 📖 Documentos Técnicos

| Documento | Localização | Descrição |
|-----------|-------------|-----------|
| **Status do Projeto** | `Backend/docs/FALTA.md` | 99% completo |
| **Últimas Implementações** | `Backend/docs/IMPLEMENTACAO_FINAL.md` | Features recentes |
| **Estrutura do Banco** | `Backend/docs/DATABASE_STRUCTURE.md` | Tabelas e relacionamentos |
| **Chatbot** | `Backend/docs/CHATBOT_README.md` | Conhecimento e uso |
| **Scripts** | `Backend/scripts/README.md` | Guia dos scripts |

### 📊 API Documentation

Quando a API estiver rodando:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📞 Contato

### 👨‍💻 Desenvolvedor

**Romário Santos**  
📧 Email: [Euoromario@gmail.com](mailto:Euoromario@gmail.com)  
🐱 GitHub: [RomarioSantos-Oficial](https://github.com/RomarioSantos-Oficial)

### 📝 Licença

Este projeto foi desenvolvido para fins **educacionais** como parte do bootcamp da **Digital Innovation One (DIO)**.

**Uso Comercial:** Entre em contato pelo email acima.

---

## 🙏 Agradecimentos

- **Digital Innovation One (DIO)** — Bootcamp e desafio
- **FastAPI** — Framework incrível
- **React** — Biblioteca poderosa
- **Comunidade Open Source** — Ferramentas e bibliotecas

---

**⭐ Se este projeto foi útil, deixe uma estrela no GitHub!**

**📝 Desenvolvido com ❤️ para a comunidade de desenvolvedores**

*Última atualização: 1 de dezembro de 2025*
