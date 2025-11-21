# 🎨 FRONTEND - DIGITAL SUPERBANK

## 📋 VISÃO GERAL

Frontend moderno e responsivo construído com **React + Vite** para consumir toda a API do Digital Superbank.

---

## 🎨 DESIGN SYSTEM

### Paleta de Cores

```css
/* Cores Principais */
--primary-blue: #0066FF;        /* Azul vibrante */
--secondary-blue: #004DBF;      /* Azul escuro */
--light-blue: #E6F2FF;          /* Azul claro para backgrounds */
--accent-blue: #00A3FF;         /* Azul claro para highlights */

--primary-green: #00D68F;       /* Verde sucesso */
--secondary-green: #00B377;     /* Verde escuro */
--light-green: #E6FFF5;         /* Verde claro */

--primary-black: #0A0E27;       /* Preto azulado */
--secondary-black: #1A1F3A;     /* Cinza escuro */
--dark-gray: #2D3348;           /* Cinza médio */
--light-gray: #F5F7FA;          /* Cinza claro */

--white: #FFFFFF;
--error-red: #FF3B5C;
--warning-yellow: #FFB800;
--text-primary: #0A0E27;
--text-secondary: #6B7280;
```

### Tipografia

```css
/* Fontes */
font-family: 'Inter', 'Poppins', sans-serif;

/* Tamanhos */
h1: 48px (bold)
h2: 36px (bold)
h3: 28px (semibold)
h4: 24px (semibold)
body: 16px (regular)
small: 14px (regular)
```

---

## 📁 ESTRUTURA DE PASTAS

```
digital-superbank-frontend/
│
├── public/
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   │
│   ├── assets/                    # Imagens, ícones, fontes
│   │   ├── images/
│   │   │   ├── logo.svg
│   │   │   ├── hero-banking.svg
│   │   │   └── card-designs/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── components/                # Componentes reutilizáveis
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── DashboardLayout.jsx
│   │   │
│   │   ├── common/                # Componentes genéricos
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Loading.jsx
│   │   │   ├── Alert.jsx
│   │   │   ├── Badge.jsx
│   │   │   └── Tooltip.jsx
│   │   │
│   │   ├── auth/                  # Componentes de autenticação
│   │   │   ├── LoginForm.jsx
│   │   │   ├── RegisterForm.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   │
│   │   ├── dashboard/             # Dashboard
│   │   │   ├── AccountSummary.jsx
│   │   │   ├── QuickActions.jsx
│   │   │   ├── RecentTransactions.jsx
│   │   │   ├── BalanceChart.jsx
│   │   │   └── WelcomeCard.jsx
│   │   │
│   │   ├── accounts/              # Componentes de contas
│   │   │   ├── AccountCard.jsx
│   │   │   ├── AccountList.jsx
│   │   │   ├── CreateAccountModal.jsx
│   │   │   └── AccountDetails.jsx
│   │   │
│   │   ├── transactions/          # Componentes de transações
│   │   │   ├── TransactionList.jsx
│   │   │   ├── TransactionItem.jsx
│   │   │   ├── DepositModal.jsx
│   │   │   ├── WithdrawModal.jsx
│   │   │   ├── TransferModal.jsx
│   │   │   └── StatementView.jsx
│   │   │
│   │   ├── cards/                 # Componentes de cartões
│   │   │   ├── CreditCardDisplay.jsx
│   │   │   ├── CardList.jsx
│   │   │   ├── RequestCardModal.jsx
│   │   │   ├── CardDetails.jsx
│   │   │   └── VirtualCardGenerator.jsx
│   │   │
│   │   ├── investments/           # Componentes de investimentos
│   │   │   ├── AssetList.jsx
│   │   │   ├── AssetCard.jsx
│   │   │   ├── InvestmentChart.jsx
│   │   │   └── PortfolioSummary.jsx
│   │   │
│   │   └── chatbot/               # Componentes do chatbot
│   │       ├── ChatWindow.jsx
│   │       ├── ChatMessage.jsx
│   │       ├── ChatInput.jsx
│   │       └── ChatSuggestions.jsx
│   │
│   ├── pages/                     # Páginas principais
│   │   ├── auth/
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   │
│   │   ├── Dashboard.jsx          # Dashboard principal
│   │   ├── Accounts.jsx           # Minhas contas
│   │   ├── Transactions.jsx       # Transações
│   │   ├── Cards.jsx              # Meus cartões
│   │   ├── Investments.jsx        # Investimentos
│   │   ├── Profile.jsx            # Perfil do usuário
│   │   └── NotFound.jsx           # 404
│   │
│   ├── services/                  # Serviços de API
│   │   ├── api.js                 # Configuração axios
│   │   ├── auth.service.js        # Serviços de autenticação
│   │   ├── account.service.js     # Serviços de contas
│   │   ├── transaction.service.js # Serviços de transações
│   │   ├── card.service.js        # Serviços de cartões
│   │   ├── investment.service.js  # Serviços de investimentos
│   │   └── chatbot.service.js     # Serviços do chatbot
│   │
│   ├── context/                   # Context API
│   │   ├── AuthContext.jsx        # Contexto de autenticação
│   │   ├── AccountContext.jsx     # Contexto de contas
│   │   └── ThemeContext.jsx       # Contexto de tema
│   │
│   ├── hooks/                     # Custom Hooks
│   │   ├── useAuth.js
│   │   ├── useAccounts.js
│   │   ├── useTransactions.js
│   │   ├── useCards.js
│   │   └── useInvestments.js
│   │
│   ├── utils/                     # Utilitários
│   │   ├── formatters.js          # Formatação de valores, datas
│   │   ├── validators.js          # Validações
│   │   ├── constants.js           # Constantes
│   │   └── helpers.js             # Funções auxiliares
│   │
│   ├── styles/                    # Estilos globais
│   │   ├── global.css
│   │   ├── variables.css
│   │   └── animations.css
│   │
│   ├── App.jsx                    # Componente principal
│   ├── main.jsx                   # Entry point
│   └── router.jsx                 # Configuração de rotas
│
├── .env.example                   # Variáveis de ambiente
├── .gitignore
├── package.json
├── vite.config.js
├── tailwind.config.js             # Configuração Tailwind CSS
├── postcss.config.js
└── README.md
```

---

## 🗂️ PÁGINAS E FUNCIONALIDADES

### 1. 🏠 **Landing Page (Público)**
- Hero section com animações
- Apresentação dos serviços
- Testemunhos
- Call-to-action para cadastro
- Footer com links úteis

### 2. 🔐 **Login / Registro**
- Formulário de login (email ou CPF)
- Formulário de registro completo
- Validação em tempo real
- Mensagens de erro claras
- Opção "Esqueci minha senha"

### 3. 📊 **Dashboard Principal**
**Visão Geral:**
- Saldo total de todas as contas
- Gráfico de receitas vs despesas
- Últimas 5 transações
- Cards de ações rápidas (Depositar, Sacar, Transferir)
- Notificações importantes
- Atalhos para funcionalidades principais

### 4. 🏦 **Minhas Contas**
**Funcionalidades:**
- Lista de todas as contas (Corrente, Poupança, Black, Empresarial, Investimento)
- Criar nova conta (modal)
- Visualizar detalhes de cada conta
- Saldo individual por conta
- Tipo e status da conta

### 5. 💸 **Transações**
**Abas:**
- **Depósito** - Formulário para depósito
- **Saque** - Formulário para saque
- **Transferência** - Transferir entre contas ou para terceiros
- **Extrato** - Histórico completo com filtros (data, tipo, valor)

**Componentes:**
- Tabela de transações com paginação
- Filtros avançados
- Exportar extrato (PDF, CSV)
- Status visual (Completo, Pendente, Cancelado)

### 6. 💳 **Meus Cartões**
**Funcionalidades:**
- Visualização de cartões (design 3D animado)
- Solicitar novo cartão (análise automática de crédito)
- Exibir CVV temporariamente (com confirmação)
- Bloquear/Desbloquear cartão
- Ajustar limite
- Pagar fatura
- Realizar compras
- Histórico de uso

**Categorias de Cartões:**
- Aura Basic (verde claro)
- Aura Plus (azul)
- Aura Premium (preto/dourado)
- Virtual (roxo com ícone de nuvem)

### 7. 📈 **Investimentos**
**Funcionalidades:**
- Lista de ativos disponíveis (11 ativos)
- Gráficos de performance
- Simular investimento
- Portfólio pessoal
- Rentabilidade em tempo real
- Filtros por tipo de ativo

### 8. 👤 **Perfil do Usuário**
**Seções:**
- Informações pessoais (nome, email, CPF, telefone)
- Editar perfil
- Alterar senha
- Foto de perfil
- Configurações de notificações
- Score de crédito atual

### 9. 🤖 **Chatbot (Widget Flutuante)**
**Funcionalidades:**
- Ícone flutuante no canto inferior direito
- Janela expansível de chat
- Histórico de conversas
- Sugestões de perguntas
- Respostas automáticas (81 Q&A)
- Feedback de satisfação
- Modo minimizado/expandido

---

## 🎨 COMPONENTES DE INTERFACE

### Header (Navbar)
```
┌─────────────────────────────────────────────────────────────┐
│ 🏦 Digital Superbank    Dashboard  Contas  Cartões  [🔔] [@]│
└─────────────────────────────────────────────────────────────┘
```

### Sidebar (Desktop)
```
┌──────────────┐
│              │
│ 📊 Dashboard │
│ 🏦 Contas    │
│ 💸 Transações│
│ 💳 Cartões   │
│ 📈 Investimen│
│ 👤 Perfil    │
│ ⚙️  Configura│
│              │
│ [🤖 Chat]    │
└──────────────┘
```

### Card de Conta
```
┌─────────────────────────────────────┐
│ Conta Corrente                   ⋮  │
│ Nº 123456-7                         │
│                                     │
│ Saldo disponível                    │
│ R$ 8.450,00                         │
│                                     │
│ [Ver extrato] [Transferir]          │
└─────────────────────────────────────┘
```

### Card de Cartão de Crédito (3D)
```
┌─────────────────────────────────────┐
│                              💳     │
│ 5814 8680 0034 3363                 │
│                                     │
│ JOÃO SILVA                          │
│ Validade: 12/28      CVV: [Ver]     │
│                                     │
│ Limite: R$ 5.000    Aura Premium    │
│ Disponível: R$ 5.000                │
│                                     │
│ [Bloquear] [Ajustar Limite] [Pagar]│
└─────────────────────────────────────┘
```

---

## 🛠️ TECNOLOGIAS E BIBLIOTECAS

### Core
- **React 18** - Framework principal
- **Vite** - Build tool
- **React Router DOM** - Roteamento

### UI/Styling
- **Tailwind CSS** - Framework CSS utility-first
- **Headless UI** - Componentes acessíveis
- **Framer Motion** - Animações
- **React Icons** - Ícones
- **Chart.js / Recharts** - Gráficos

### Estado e Dados
- **Axios** - HTTP client
- **React Query** - Cache e state management para API
- **Context API** - Estado global
- **Zustand** (opcional) - State management leve

### Formulários e Validação
- **React Hook Form** - Gerenciamento de formulários
- **Yup / Zod** - Validação de schemas

### Utilitários
- **date-fns** - Manipulação de datas
- **react-hot-toast** - Notificações
- **react-number-format** - Formatação de números
- **cpf-cnpj-validator** - Validação de CPF

### Desenvolvimendo
- **ESLint** - Linter
- **Prettier** - Formatação de código
- **Husky** - Git hooks

---

## 📱 RESPONSIVIDADE

### Breakpoints
```css
/* Mobile First */
sm: 640px   /* Tablets pequenos */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Desktops grandes */
```

### Layout Responsivo

**Mobile (< 768px)**
- Sidebar vira menu hambúrguer
- Cards em coluna única
- Gráficos simplificados
- Chatbot minimizado por padrão

**Tablet (768px - 1024px)**
- Sidebar colapsável
- Cards em 2 colunas
- Tabelas com scroll horizontal

**Desktop (> 1024px)**
- Sidebar fixa
- Cards em grid 3-4 colunas
- Tabelas completas
- Chatbot fixo

---

## 🎭 ANIMAÇÕES E TRANSIÇÕES

### Micro-interações
- Hover nos botões (escala 1.02, sombra)
- Loading skeletons
- Transições de página (fade in/out)
- Cards com flip 3D (cartões de crédito)
- Progress bars animados
- Números contando (counter animation)

### Feedback Visual
- Loading spinners
- Toast notifications (sucesso, erro, info)
- Ripple effect em botões
- Skeleton screens

---

## 🔒 SEGURANÇA

### Autenticação
- JWT armazenado no localStorage
- Refresh token automático
- Logout automático após inatividade
- Rotas protegidas

### Validações
- Validação de CPF
- Validação de email
- Senha forte (mínimo 8 caracteres)
- Sanitização de inputs

---

## 🚀 SCRIPTS NPM

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx",
    "format": "prettier --write \"src/**/*.{js,jsx,css}\"",
    "test": "vitest"
  }
}
```

---

## 📦 PACKAGE.JSON (Resumo)

```json
{
  "name": "digital-superbank-frontend",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "@tanstack/react-query": "^5.0.0",
    "framer-motion": "^10.16.0",
    "react-hook-form": "^7.48.0",
    "yup": "^1.3.0",
    "react-hot-toast": "^2.4.1",
    "react-icons": "^4.12.0",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "date-fns": "^2.30.0",
    "cpf-cnpj-validator": "^1.0.3",
    "react-number-format": "^5.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0"
  }
}
```

---

## 🎨 EXEMPLOS DE TELAS

### 1. Dashboard
```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Logo | Dashboard | Contas | Cartões | [🔔] [@João]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Bem-vindo de volta, João! 👋                                   │
│                                                                 │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │ Saldo Total    │  │ Receitas       │  │ Despesas         │  │
│  │ R$ 25.450,00   │  │ R$ 8.000,00    │  │ R$ 2.100,00      │  │
│  │ +15% este mês  │  │ +3 transações  │  │ 7 transações     │  │
│  └────────────────┘  └────────────────┘  └─────────────────┘  │
│                                                                 │
│  📊 Gráfico de Movimentações (últimos 30 dias)                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │     █                                                    │  │
│  │   █ █     █                                              │  │
│  │ █ █ █ █ █ █ █                                            │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  🎯 Ações Rápidas                                              │
│  [💰 Depositar] [💸 Sacar] [🔄 Transferir] [💳 Pagar Fatura]  │
│                                                                 │
│  📋 Últimas Transações                                         │
│  • Depósito - R$ 5.000,00 - Hoje 10:30                        │
│  • Saque - R$ 100,00 - Hoje 09:15                             │
│  • Transferência - R$ 2.000,00 - Ontem                        │
│  [Ver todas]                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Página de Cartões
```
┌─────────────────────────────────────────────────────────────────┐
│ Meus Cartões 💳                              [+ Solicitar Novo] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🎴 CARTÃO FÍSICO                                        │  │
│  │  ┌─────────────────────────────────────┐                │  │
│  │  │ 🔵 Digital Superbank                │                │  │
│  │  │                                     │                │  │
│  │  │ 5814 8680 0034 3363                 │                │  │
│  │  │                                     │                │  │
│  │  │ JOÃO SILVA TESTE                    │                │  │
│  │  │ 12/28                    CVV [Ver]  │                │  │
│  │  │                     Aura Basic 🟢   │                │  │
│  │  └─────────────────────────────────────┘                │  │
│  │                                                          │  │
│  │  Limite: R$ 500,00                                      │  │
│  │  Disponível: R$ 500,00                                  │  │
│  │  Fatura atual: R$ 0,00                                  │  │
│  │                                                          │  │
│  │  [🔒 Bloquear] [💰 Ajustar Limite] [💳 Ver Faturas]    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  💡 Dica: Faça mais transações para aumentar seu score!        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Chatbot Widget
```
                                     ┌──────────────────────┐
                                     │ 🤖 Como posso ajudar?│
                                     ├──────────────────────┤
                                     │ João: Como fazer um  │
                                     │ depósito?            │
                                     │                      │
                                     │ Bot: Para fazer um   │
                                     │ depósito, acesse...  │
                                     │                      │
                                     │ [Digite sua pergunta]│
                                     └──────────────────────┘
```

---

## 🎯 DIFERENCIAIS DO DESIGN

### 1. **Glassmorphism**
- Cards com efeito de vidro fosco
- Background blur
- Bordas sutis

### 2. **Gradientes**
- Gradientes suaves azul → verde
- Backgrounds com gradiente
- Botões com gradiente em hover

### 3. **Sombras e Profundidade**
- Sombras suaves (elevation)
- Cartões com profundidade
- Efeito de elevação em hover

### 4. **Ícones e Ilustrações**
- Ícones modernos (React Icons)
- Ilustrações SVG customizadas
- Micro-animações nos ícones

### 5. **Dark Mode (Opcional)**
- Toggle de tema claro/escuro
- Cores adaptadas para dark mode

---

## 📊 ESTRUTURA DE ROTAS

```javascript
/                      → Landing Page
/login                 → Login
/register              → Registro

/dashboard             → Dashboard principal (protegido)
/accounts              → Minhas contas (protegido)
/transactions          → Transações (protegido)
/cards                 → Meus cartões (protegido)
/investments           → Investimentos (protegido)
/profile               → Perfil (protegido)

/404                   → Página não encontrada
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1 - Setup (1-2 dias)
- [ ] Criar projeto Vite + React
- [ ] Configurar Tailwind CSS
- [ ] Estrutura de pastas
- [ ] Configurar ESLint + Prettier
- [ ] Configurar variáveis de ambiente

### Fase 2 - Componentes Base (2-3 dias)
- [ ] Sistema de design (cores, fontes, espaçamentos)
- [ ] Componentes comuns (Button, Input, Card, Modal)
- [ ] Layout (Header, Sidebar, Footer)
- [ ] Rotas e navegação

### Fase 3 - Autenticação (2 dias)
- [ ] Serviço de API (axios)
- [ ] Context de autenticação
- [ ] Página de login
- [ ] Página de registro
- [ ] Proteção de rotas

### Fase 4 - Dashboard (2 dias)
- [ ] Dashboard principal
- [ ] Resumo de contas
- [ ] Gráficos
- [ ] Ações rápidas

### Fase 5 - Contas (2 dias)
- [ ] Listagem de contas
- [ ] Criar conta
- [ ] Detalhes da conta
- [ ] Consultar saldo

### Fase 6 - Transações (3 dias)
- [ ] Depósito
- [ ] Saque
- [ ] Transferência
- [ ] Extrato com filtros

### Fase 7 - Cartões (3 dias)
- [ ] Visualização de cartões (3D)
- [ ] Solicitar cartão
- [ ] Gerenciar cartões
- [ ] Pagar fatura

### Fase 8 - Investimentos (2 dias)
- [ ] Listagem de ativos
- [ ] Gráficos de performance
- [ ] Portfólio

### Fase 9 - Chatbot (2 dias)
- [ ] Widget flutuante
- [ ] Integração com API
- [ ] Histórico de conversas

### Fase 10 - Finalização (2 dias)
- [ ] Perfil do usuário
- [ ] Responsividade completa
- [ ] Testes
- [ ] Otimizações
- [ ] Build de produção

**Total estimado: 20-25 dias**

---

## 🚀 COMANDOS DE INSTALAÇÃO

```bash
# Criar projeto
npm create vite@latest digital-superbank-frontend -- --template react
cd digital-superbank-frontend

# Instalar dependências principais
npm install react-router-dom axios @tanstack/react-query framer-motion
npm install react-hook-form yup react-hot-toast react-icons
npm install chart.js react-chartjs-2 date-fns
npm install cpf-cnpj-validator react-number-format

# Instalar Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Instalar ferramentas de desenvolvimento
npm install -D eslint prettier

# Iniciar servidor de desenvolvimento
npm run dev
```

---

## 🎨 PRÉVIA DE CÓDIGO

### App.jsx
```javascript
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './context/AuthContext';
import { Toaster } from 'react-hot-toast';
import Router from './router';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Router />
          <Toaster position="top-right" />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

### tailwind.config.js
```javascript
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          blue: '#0066FF',
          green: '#00D68F',
          black: '#0A0E27',
        },
        secondary: {
          blue: '#004DBF',
          green: '#00B377',
          black: '#1A1F3A',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

---

## 📝 VARIÁVEIS DE AMBIENTE

### .env.example
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Digital Superbank
VITE_APP_VERSION=1.0.0
```

---

## 🎉 RESULTADO ESPERADO

Um frontend **moderno, responsivo e intuitivo** que oferece:

✅ Interface limpa e profissional  
✅ Navegação fluida  
✅ Animações suaves  
✅ Design system consistente  
✅ 100% responsivo (mobile, tablet, desktop)  
✅ Performance otimizada  
✅ Acessibilidade  
✅ Integração completa com API  
✅ Experiência de banco digital moderno  

---

**Status:** 📋 **PROPOSTA APROVADA - AGUARDANDO CONFIRMAÇÃO**

