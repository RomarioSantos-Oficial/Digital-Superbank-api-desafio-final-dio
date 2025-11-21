# 🏦 Digital Superbank - Frontend

Frontend moderno e responsivo construído com **React + Vite** para consumir toda a API do Digital Superbank.

## 🚀 Tecnologias

- **React 18** - Framework principal
- **Vite** - Build tool
- **Tailwind CSS** - Framework CSS utility-first
- **React Router DOM** - Roteamento
- **Framer Motion** - Animações
- **React Hook Form** - Gerenciamento de formulários
- **Axios** - HTTP client
- **React Query** - Cache e state management
- **React Hot Toast** - Notificações
- **Chart.js** - Gráficos
- **date-fns** - Manipulação de datas

## 📦 Instalação

```bash
# Instalar dependências
npm install

# Copiar arquivo de ambiente
copy .env.example .env

# Iniciar servidor de desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

## 🔧 Configuração

Edite o arquivo `.env` com suas configurações:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Digital Superbank
VITE_APP_VERSION=1.0.0
```

## 📁 Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
│   ├── common/         # Componentes genéricos
│   └── layout/         # Componentes de layout
├── context/            # Context API
├── hooks/              # Custom Hooks
├── pages/              # Páginas
├── services/           # Serviços de API
├── styles/             # Estilos globais
├── utils/              # Utilitários
├── App.jsx             # Componente principal
├── main.jsx            # Entry point
└── router.jsx          # Configuração de rotas
```

## 🎨 Funcionalidades

### ✅ Autenticação
- Login e registro de usuários
- Proteção de rotas
- Gerenciamento de sessão com JWT

### ✅ Dashboard
- Visão geral de contas
- Saldo total
- Últimas transações
- Ações rápidas

### ✅ Contas
- Listagem de contas
- Criação de novas contas
- Visualização de saldo

### ✅ Transações
- Depósito
- Saque
- Transferência
- PIX
- Extrato

### ✅ Cartões
- Visualização de cartões (design 3D)
- Solicitação de novos cartões
- Bloqueio/Desbloqueio
- Gerenciamento de limite

### ✅ Investimentos
- Listagem de ativos disponíveis
- Compra e venda de ativos
- Portfólio pessoal
- Preços em tempo real (WebSocket)

### ✅ Perfil
- Edição de dados pessoais
- Visualização de score de crédito

## 🎯 Scripts Disponíveis

```bash
npm run dev        # Servidor de desenvolvimento
npm run build      # Build para produção
npm run preview    # Preview da build
npm run lint       # Lint do código
npm run format     # Formatar código
```

## 🌐 Rotas

- `/login` - Login
- `/register` - Registro
- `/dashboard` - Dashboard (protegido)
- `/accounts` - Contas (protegido)
- `/transactions` - Transações (protegido)
- `/cards` - Cartões (protegido)
- `/investments` - Investimentos (protegido)
- `/profile` - Perfil (protegido)

## 🎨 Design System

### Cores Principais
- **Primary Blue**: #0066FF
- **Primary Green**: #00D68F
- **Primary Black**: #0A0E27
- **Error Red**: #FF3B5C
- **Warning Yellow**: #FFB800

### Componentes
- Button
- Card
- Input
- Modal
- Loading
- Alert
- Badge
- Tooltip

## 📱 Responsividade

O frontend é totalmente responsivo com breakpoints:
- **sm**: 640px (Tablets pequenos)
- **md**: 768px (Tablets)
- **lg**: 1024px (Laptops)
- **xl**: 1280px (Desktops)
- **2xl**: 1536px (Desktops grandes)

## 🔒 Segurança

- JWT armazenado no localStorage
- Interceptor automático para adicionar token nas requisições
- Logout automático em caso de token inválido
- Validação de formulários
- Sanitização de inputs

## 📊 Estado Global

Gerenciado através de Context API:
- **AuthContext**: Autenticação e usuário
- **AccountContext**: Contas
- **ThemeContext**: Tema (claro/escuro)

## 🚀 Deploy

Para fazer deploy, execute:

```bash
npm run build
```

Os arquivos otimizados estarão na pasta `dist/`.

## 📝 Licença

Este projeto faz parte do Digital Superbank.

---

**Status**: ✅ **PRONTO PARA USO**

Desenvolvido com ❤️ para o Digital Superbank
