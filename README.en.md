# 🏦 Digital Superbank — Complete Guide

> 🌍 **Languages:** [Português](README.pt-BR.md) | [English](README.en.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Español](README.es.md)

Welcome to **Digital Superbank**, a complete banking system created for **educational and didactic purposes**, simulating a modern digital bank with all the functionalities of a real financial institution.

> ⚠️ **Notice:** All data is fictional. For commercial use, contact: **[Euoromario@gmail.com](mailto:Euoromario@gmail.com)**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)
[![Status](https://img.shields.io/badge/Status-99%25%20Complete-success.svg)](Backend/docs/FALTA.md)

---

## 📌 Index

1. [Overview](#-overview)
2. [Prerequisites](#-prerequisites)
3. [Quick Installation](#-quick-installation-first-time)
4. [Daily Usage](#-daily-usage)
5. [Features](#-features)
6. [Project Structure](#-project-structure)
7. [Useful Scripts](#-useful-scripts)
8. [Market Simulator and Candles](#-market-simulator-and-candles)
9. [WebSocket (Real-Time)](#-websocket-real-time)
10. [Tests](#-tests)
11. [Troubleshooting](#-troubleshooting)
12. [Technologies](#-technologies)
13. [Additional Documentation](#-additional-documentation)
14. [Contact](#-contact)

---

## 📦 Overview

**Digital Superbank** is a full-stack application that simulates a complete digital bank, developed for educational purposes with all the features of a modern bank.

### 🎯 Main Components

#### 🔧 **Backend — FastAPI**
* **JWT Authentication** with refresh tokens
* **11 account types** (Checking, Savings, Black, Investment, etc.)
* **Complete transaction system** (Deposit, Withdrawal, Transfer, PIX, Bills)
* **Credit cards** (4 brands, 3 categories)
* **Investments** (Stocks, Funds, Fixed Income)
* **WebSocket** with real-time prices
* **Candlestick charts (OHLCV)** for technical analysis
* **AI Chatbot** with banking knowledge
* **SQLite** (2 databases: main + chatbot)

#### 💻 **Frontend — React + Vite**
* **Interactive dashboard** with overview
* **3D cards** with flip animation
* **Professional investment system** with charts
* **Integrated chatbot** (Luna AI)
* **Real-time notifications**
* **Modern theme** with Tailwind CSS + Framer Motion
* **Fully responsive**

#### 🤖 **Chatbot — Luna AI**
* **Editable knowledge base** (31+ questions/answers)
* **Intelligent semantic search**
* **Learning system** (saves new questions)
* **Command navigation** ("go to investments", "view cards", etc.)
* **Persistence** between tabs (localStorage)
* **Typing delay** (3 seconds) for realistic effect

---

## ⚙️ Prerequisites

Before starting, make sure you have installed:

### 📋 Required Software

| Software | Minimum Version | How to Check | Download |
|----------|----------------|--------------|----------|
| **Windows** | 10+ | - | - |
| **PowerShell** | 5.1+ | `$PSVersionTable.PSVersion` | Included in Windows |
| **Python** | 3.8+ | `python --version` | [python.org](https://www.python.org/) |
| **Node.js** | 16+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | 8+ | `npm --version` | Included with Node.js |
| **Git** | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com/) |

### ✅ Quick Check

Run in PowerShell to check everything at once:

```powershell
Write-Host "Python: " -NoNewline; python --version
Write-Host "Node.js: " -NoNewline; node --version
Write-Host "npm: " -NoNewline; npm --version
Write-Host "Git: " -NoNewline; git --version
```

---

## 🚀 Quick Installation (First Time)

This step prepares **EVERYTHING AUTOMATICALLY**: venv, packages, databases, assets, funds, and chatbot.

### 📍 Step by Step

#### 1️⃣ Clone the Repository

```powershell
git clone https://github.com/RomarioSantos-Oficial/Digital-Superbank-api-desafio-final-dio.git
cd Digital-Superbank-api-desafio-final-dio
```

#### 2️⃣ Run the Installer

```powershell
.\start.ps1
```

### 🎬 What the installer does automatically:

```
🔧 STEP 1: Python Environment
   ✅ Creates .venv (if it doesn't exist)
   ✅ Activates virtual environment
   ✅ Installs Backend dependencies

🔧 STEP 2: Node.js Environment
   ✅ cd Frontend
   ✅ npm install
   ✅ Returns to root

🔧 STEP 3: Main Database
   ✅ Creates tables (11 tables)
   ✅ init_db.py

🔧 STEP 4: Stocks (REQUIRED)
   ✅ Populates 30 varied stocks
   ✅ Saves to demo/acao.txt

🔧 STEP 5: Investment Funds (REQUIRED)
   ✅ Populates 25 investment funds
   ✅ Saves to demo/fundo_investimento.txt

🔧 STEP 6: Chatbot (REQUIRED)
   ✅ Populates 31 banking knowledge items
   ✅ Reads from demo/chatbot_conhecimento.txt
   ✅ Saves to chatbot.db

🔧 STEP 7: Demo Users (OPTIONAL)
   ❓ Asks if you want to create
   ✅ If YES: creates 5 test users
   ✅ Saves to demo/pessoa.txt
```

### ⏱️ Estimated time: 2-3 minutes

---

## 🖥️ Daily Usage

After initial installation, start the system with **a single command**:

### 🎯 Main Command

```powershell
.\start.ps1
```

### 🚀 What happens:

```
🔍 Checking environment...
   ✅ Activating .venv
   ✅ Installing missing dependencies

🌐 Starting Backend (port 8000)...
   ✅ API running at http://localhost:8000
   ✅ Documentation at http://localhost:8000/docs
   ✅ Market simulator active
   ✅ WebSocket available

💻 Starting Frontend (port 3000)...
   ✅ Interface at http://localhost:3000
   ✅ Hot reload active

🎉 SYSTEM READY!
```

### 📱 Access the Application

| Interface | URL | Description |
|-----------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main interface |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Alternative documentation |
| **WebSocket** | ws://localhost:8000/ws/market-feed | Real-time feed |

---

## ✨ Features

### 🔐 Authentication and Users

* ✅ **Registration** with CPF and email validation
* ✅ **Multiple login** (Email, CPF, or Account Number)
* ✅ **JWT Tokens** with automatic refresh
* ✅ **Route protection** on frontend and backend
* ✅ **Dynamic credit score**
* ✅ **Editable complete profile**

### 💰 Bank Accounts

| Type | Requirements | Minimum Balance | Features |
|------|--------------|-----------------|----------|
| **Checking** | None | R$ 0 | Standard account |
| **Savings** | None | R$ 0 | Automatic yield |
| **Salary** | None | R$ 0 | For income receipt |
| **University** | None | R$ 0 | For students |
| **Business** | None | R$ 0 | For companies |
| **Investment** | Black OR Business | R$ 0 | Investment access |
| **Black** | Score ≥ 700 | R$ 50,000 | Exclusive benefits |

### 💸 Transactions

* ✅ **Deposit** (instant)
* ✅ **Withdrawal** (with balance validation)
* ✅ **Transfer** between accounts
* ✅ **PIX** (send and receive)
* ✅ **Bill payment**
* ✅ **Scheduled** future transactions
* ✅ **Complete history** with search

### 💳 Credit Cards

#### Available Brands
* 💳 Visa
* 💳 Mastercard
* 💳 Elo
* 💳 American Express

#### Categories

| Category | Initial Limit | Annual Fee | Cashback |
|----------|---------------|------------|----------|
| **Basic** | R$ 1,000 | R$ 0 | 0% |
| **Platinum** | R$ 5,000 | R$ 120/year | 1% |
| **Black** | R$ 20,000 | R$ 500/year | 3% |

### 📈 Investments

#### Available Assets
* 📊 **30 Stocks** (various sectors)
* 💼 **25 Investment Funds**
* 💰 **Fixed Income** (CDB, LCI, LCA)

#### Features
* ✅ **Buy and sell** in real-time
* ✅ **Consolidated portfolio** with profitability
* ✅ **Price history** (7 periods: 1D, 7D, 1M, 3M, 6M, 1Y, ALL)
* ✅ **Candlestick charts** for stocks
* ✅ **Statistics** (24h High/Low, % Change)
* ✅ **WebSocket** with prices updating every 60 seconds
* ✅ **Realistic market simulator**

---

## 📂 Project Structure

```
Digital-Superbank-api-desafio-final-dio/
│
├── 📄 start.ps1                          # Main installer and launcher
├── 📄 README.md                          # Main README
├── 📄 README.pt-BR.md                   # Portuguese Version
├── 📄 README.en.md                      # This file
├── 📄 README.ja.md                      # Japanese Version
├── 📄 README.zh.md                      # Chinese Version
├── 📄 README.es.md                      # Spanish Version
│
├── 📁 demo/                              # Fictional test data
│   ├── pessoa.txt                       # 37 demo users
│   ├── acao.txt                         # Investment stocks
│   ├── fundo_investimento.txt           # Investment funds
│   └── chatbot_conhecimento.txt         # Knowledge base (31 Q&A)
│
├── 📁 Backend/                           # FastAPI API
│   ├── main.py                          # API entry point
│   ├── requirements.txt                 # Python dependencies
│   ├── digital_superbank.db             # Main database (SQLite)
│   ├── chatbot.db                       # Chatbot database (SQLite)
│   ├── 📁 src/                          # Source code
│   ├── 📁 scripts/                      # Maintenance scripts (16 files)
│   ├── 📁 tests/                        # Automated tests
│   └── 📁 docs/                         # Technical documentation
│
└── 📁 Frontend/                          # React interface
    ├── package.json                     # Node.js dependencies
    └── 📁 src/                          # React source code
```

---

## 🛠️ Useful Scripts

All scripts are in `Backend/scripts/`. Use with virtual environment activated.

### 📊 Data Population

#### Investment Stocks
```powershell
cd Backend
python scripts/generate_stocks.py --update
```

#### Investment Funds
```powershell
python scripts/generate_funds.py --update
```

#### Chatbot (Knowledge Base)
```powershell
python scripts/populate_chatbot_from_file.py --update
```

### 📈 Historical Candles

```powershell
# Last 7 days
python scripts/generate_historical_candles.py --days 7
```

### 🔍 Verification

```powershell
# Check databases
python scripts/check_databases.py
```

---

## 📊 Market Simulator and Candles

The system includes a **market simulator** that updates stock prices in real-time:

* **Update:** Every 60 seconds
* **Variation:** ±1.5% per update
* **Candles:** Generated automatically (OHLCV)
* **WebSocket:** Transmits updates to frontend

### How it works:

1. The simulator runs automatically when you start the Backend
2. Prices are updated using realistic random walk
3. Candles (candlesticks) are generated and stored in database
4. WebSocket sends updates to all connected clients

---

## 🌐 WebSocket (Real-Time)

The system uses WebSocket for real-time communication:

### Endpoint
```
ws://localhost:8000/ws/market-feed
```

### What is transmitted:
* **Updated stock prices**
* **New candles** (candlesticks)
* **Statistics** (24h high/low, % change)

### How to connect (JavaScript):
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market-feed');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Market update:', data);
};
```

---

## 🧪 Tests

Run automated tests:

```powershell
cd Backend/tests

# Complete system test
python test_complete_system.py

# All services test
python test_all_services.py

# Chatbot test
python test_chatbot.py

# WebSocket test
python test_websocket.py
```

---

## ❓ Troubleshooting

### ❗ `database is locked`

Close uvicorn before running scripts that write to the database.

### ❗ `no such table: knowledge_base`

Run first:

```powershell
python Backend/scripts/update_chatbot_db.py
```

### ❗ Frontend Errors

* Delete `node_modules`
* Run `npm install`
* Check port 3000

### ❗ Backend Errors

* Activate venv: `.\.venv\Scripts\Activate.ps1`
* Reinstall: `pip install -r requirements.txt`

---

## 🛠️ Technologies

### Backend

| Technology | Version | Usage |
|------------|---------|-------|
| **Python** | 3.11+ | Main language |
| **FastAPI** | 0.100+ | Web framework |
| **SQLAlchemy** | 2.0+ | ORM |
| **SQLite** | 3 | Database |
| **Pydantic** | 2.0+ | Validation |
| **JWT** | - | Authentication |
| **WebSockets** | - | Real-time |

### Frontend

| Technology | Version | Usage |
|------------|---------|-------|
| **React** | 18+ | UI Framework |
| **Vite** | 4+ | Build tool |
| **Tailwind CSS** | 3+ | Styling |
| **Framer Motion** | - | Animations |
| **React Router** | 6+ | Routing |
| **Axios** | - | HTTP client |
| **Chart.js** | - | Charts |

---

## 📚 Additional Documentation

### 📖 Technical Documents

| Document | Location | Description |
|----------|----------|-------------|
| **Project Status** | `Backend/docs/FALTA.md` | 99% complete |
| **Latest Implementations** | `Backend/docs/IMPLEMENTACAO_FINAL.md` | Recent features |
| **Database Structure** | `Backend/docs/DATABASE_STRUCTURE.md` | Tables and relationships |
| **Chatbot** | `Backend/docs/CHATBOT_README.md` | Knowledge and usage |
| **Scripts** | `Backend/scripts/README.md` | Scripts guide |

### 📊 API Documentation

When the API is running:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📞 Contact

### 👨‍💻 Developer

**Romário Santos**  
📧 Email: [Euoromario@gmail.com](mailto:Euoromario@gmail.com)  
🐱 GitHub: [RomarioSantos-Oficial](https://github.com/RomarioSantos-Oficial)

### 📝 License

This project was developed for **educational purposes** as part of the **Digital Innovation One (DIO)** bootcamp.

**Commercial Use:** Contact via email above.

---

## 🙏 Acknowledgments

- **Digital Innovation One (DIO)** — Bootcamp and challenge
- **FastAPI** — Amazing framework
- **React** — Powerful library
- **Open Source Community** — Tools and libraries

---

**⭐ If this project was helpful, leave a star on GitHub!**

**📝 Developed with ❤️ for the developer community**

*Last update: December 1, 2025*
