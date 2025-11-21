# 🏦 Digital Superbank

Sistema bancário completo e profissional com Backend (FastAPI) e Frontend (React + Vite).

## ⭐ Funcionalidades Principais

### 💳 Sistema Bancário Completo
- ✅ **Múltiplas Contas**: Corrente, Poupança e Investimento
- ✅ **Transações**: Depósito, Saque, Transferência e PIX
- ✅ **Cartões de Crédito**: Visualização 3D, múltiplas bandeiras (Visa, Mastercard, Elo)
- ✅ **Extrato Detalhado**: Filtros por período e tipo de transação
- ✅ **Autenticação JWT**: Sistema seguro com tokens

### 📈 Sistema de Investimentos em Tempo Real
- ✅ **Gráficos de Velas (Candlestick)**: Visualização profissional com Chart.js
- ✅ **10 Intervalos de Tempo**: 1s, 5s, 10s, 30s, 1m, 5m, 15m, 1h, 4h, 1d
- ✅ **WebSocket em Tempo Real**: Atualização automática a cada 1 segundo
- ✅ **Simulador de Mercado**: Volatilidade realista (0.1% - 0.3%)
- ✅ **Compra/Venda de Ativos**: Ações e Fundos Imobiliários
- ✅ **Dashboard de Trading**: Página dedicada com fullscreen
- ✅ **Watchlist**: Acompanhe múltiplos ativos simultaneamente
- ✅ **Estatísticas**: Máxima, Mínima, Volume, Variação 24h

### 🤖 Chatbot Inteligente
- ✅ **81 Perguntas e Respostas**: Base de conhecimento completa
- ✅ **Busca Semântica**: Encontra respostas relevantes
- ✅ **Interface Moderna**: Chat em tempo real

### 🎨 Interface Premium
- ✅ **Design Moderno**: Tailwind CSS com gradientes e animações
- ✅ **Responsivo**: Funciona em desktop, tablet e mobile
- ✅ **Animações Fluidas**: Framer Motion
- ✅ **Dark Mode Ready**: Cards com glassmorphism

## 🚀 Início Rápido

### Opção 1: Script Automático (Recomendado) ⚡

Execute o script que inicia Backend e Frontend automaticamente:

```powershell
.\start.ps1
```

O script irá:
- ✅ Verificar dependências (Python e Node.js)
- ✅ Instalar dependências automaticamente
- ✅ Iniciar o Backend em http://localhost:8000
- ✅ Iniciar o Frontend em http://localhost:3000
- ✅ Exibir logs de ambos os serviços em tempo real

### Opção 2: Manual

#### Backend (FastAPI)

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

#### Frontend (React + Vite)

```powershell
cd Frontend
npm install
npm run dev
```

## 📂 Estrutura do Projeto

```
Digital Superbank/
├── Backend/                 # API FastAPI
│   ├── main.py             # Entrada da API
│   ├── requirements.txt    # Dependências Python
│   ├── src/                # Código fonte
│   │   ├── api/           # Endpoints da API
│   │   ├── models/        # Modelos de dados
│   │   ├── services/      # Lógica de negócio
│   │   ├── database/      # Configuração de BD
│   │   └── configs/       # Configurações
│   └── tests/             # Testes
│
├── Frontend/               # App React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas
│   │   ├── services/      # Serviços de API
│   │   ├── context/       # Context API
│   │   ├── hooks/         # Custom Hooks
│   │   └── utils/         # Utilitários
│   ├── package.json       # Dependências Node
│   └── vite.config.js     # Configuração Vite
│
└── start.ps1              # Script de inicialização
```

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Funcionalidades Detalhadas

### Backend (FastAPI)
- ✅ **Autenticação JWT**: Login seguro com tokens e refresh tokens
- ✅ **CRUD Completo**: Contas, Usuários, Transações, Cartões
- ✅ **Transações Bancárias**: Depósito, Saque, Transferência, PIX
- ✅ **Cartões de Crédito**: Geração automática, múltiplas bandeiras
- ✅ **Sistema de Investimentos**: 
  - Ações (STOCK) e Fundos Imobiliários (FUND)
  - Velas em 10 intervalos diferentes (1s até 1d)
  - Simulador de mercado em tempo real
  - Geração automática de OHLCV (Open, High, Low, Close, Volume)
- ✅ **Chatbot Inteligente**: 81 Q&A sobre o sistema
- ✅ **WebSocket**: Broadcast de preços a cada 1 segundo
- ✅ **Banco de Dados**: SQLite com SQLAlchemy ORM
- ✅ **Documentação**: Swagger UI e ReDoc automáticos
- ✅ **Validação**: Pydantic schemas em todos endpoints
- ✅ **CORS Configurado**: Pronto para produção

### Frontend (React + Vite)
- ✅ **Interface Premium**: Design moderno com Tailwind CSS
- ✅ **Dashboard Interativo**: Visão geral de contas e saldo
- ✅ **Gerenciamento de Contas**: Criar, visualizar, editar
- ✅ **Módulo de Transações**: 
  - Formulários intuitivos
  - Histórico completo
  - Filtros avançados
- ✅ **Cartões 3D**: Visualização realista com flip animation
- ✅ **Investimentos Profissionais**:
  - Gráficos de velas (Candlestick Chart)
  - 10 intervalos de tempo
  - Trading modal com compra/venda
  - Dashboard dedicado com fullscreen
  - Watchlist de ativos
  - WebSocket em tempo real
- ✅ **Chatbot**: Interface de chat fluida
- ✅ **Perfil do Usuário**: Edição de dados pessoais
- ✅ **Animações**: Framer Motion para transições suaves
- ✅ **Responsivo**: Mobile-first design
- ✅ **Performance**: Vite para build ultra-rápido

## 📋 Pré-requisitos

- **Python** 3.8 ou superior
- **Node.js** 16 ou superior
- **npm** ou **yarn**

## 🛠️ Tecnologias

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- WebSocket
- SQLite

### Frontend
- React 18
- Vite
- Tailwind CSS
- Framer Motion
- React Router DOM
- Axios
- React Query
- React Hook Form
- Chart.js

## 📚 Documentação

- [Backend README](./Backend/README.md)
- [Frontend README](./Frontend/README.md)
- [Instalação Frontend](./Frontend/INSTALACAO.md)

## 🔧 Desenvolvimento

### Backend

```powershell
# Ativar ambiente virtual
cd Backend
.\.venv\Scripts\Activate.ps1

# Executar com reload automático
uvicorn main:app --reload

# Executar testes
pytest
```

### Frontend

```powershell
cd Frontend

# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

## 🧪 Testes

### Backend

```powershell
cd Backend
pytest
```

### Frontend

```powershell
cd Frontend
npm run test
```

## 📦 Build para Produção

### Backend

```powershell
cd Backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```powershell
cd Frontend
npm run build
# Arquivos em: Frontend/dist/
```

## 🔒 Segurança

- JWT Authentication
- Senhas hasheadas com bcrypt
- Validação de dados com Pydantic
- CORS configurado
- Sanitização de inputs

## 🗂️ Scripts Úteis

### Limpar Banco de Dados
```powershell
cd Backend
python scripts/clear_personal_data.py
```

### Limpar Velas Antigas
```powershell
cd Backend
python scripts/clean_old_candles.py
```

### Inicializar Banco
```powershell
cd Backend
python scripts/init_db.py
```

### Popular Chatbot
```powershell
cd Backend
python scripts/populate_chatbot.py
```

## 🐛 Troubleshooting

### Backend não inicia

1. Verifique se o Python está instalado: `python --version`
2. Verifique se está na versão 3.8+
3. Ative o ambiente virtual: `.\.venv\Scripts\Activate.ps1`
4. Reinstale dependências: `pip install -r requirements.txt`
5. Verifique se a porta 8000 está livre

### Frontend não inicia

1. Verifique se o Node.js está instalado: `node --version`
2. Verifique se está na versão 16+
3. Delete `node_modules` e reinstale: `rm -r node_modules; npm install`
4. Limpe o cache: `npm cache clean --force`
5. Verifique se a porta 3000 está livre

### WebSocket não conecta

1. Certifique-se que o Backend está rodando
2. Verifique o console do navegador para erros
3. Confirme que está acessando http://localhost:3000

### Gráficos não aparecem

1. Abra o DevTools (F12) e verifique erros
2. Verifique se há velas no banco de dados
3. Aguarde alguns segundos para o simulador gerar velas
4. Recarregue a página

### Erro de CORS

Já configurado! Se persistir:
1. Verifique se o Backend está em http://localhost:8000
2. Verifique se o Frontend está em http://localhost:3000

## 📊 Estrutura de Dados

### Velas (Candles)
- **Intervalos**: 1s, 5s, 10s, 30s, 1m, 5m, 15m, 1h, 4h, 1d
- **Campos**: Open, High, Low, Close, Volume, Timestamp
- **Atualização**: Tempo real via WebSocket

### Investimentos
- **Tipos**: STOCK (Ações), FUND (Fundos Imobiliários)
- **Categorias**: TECHNOLOGY, REAL_ESTATE, FINANCE, etc.
- **Dados**: Preço atual, variação 24h, volume, volatilidade

## 📝 Licença

Este projeto é parte do Digital Superbank.

## 👨‍💻 Desenvolvimento

Desenvolvido com ❤️ usando FastAPI e React.

---

**Para iniciar rapidamente, execute: `.\start.ps1`** 🚀
#   D i g i t a l - S u p e r b a n k - a p i - d e s a f i o - f i n a l - d i o  
 