# 📋 INSTRUÇÕES DE INSTALAÇÃO E EXECUÇÃO

## Frontend - Digital Superbank

### Pré-requisitos
- Node.js 16+ instalado
- npm ou yarn

### 📦 Passo 1: Instalar Dependências

Abra o PowerShell no diretório do Frontend e execute:

```powershell
# Navegar para o diretório do Frontend
cd "c:\Users\limar\Desktop\final dio py\Digital Superbank\Frontend"

# Instalar todas as dependências
npm install
```

### ⚙️ Passo 2: Configurar Variáveis de Ambiente

O arquivo `.env` já está criado com as configurações padrão:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Digital Superbank
VITE_APP_VERSION=1.0.0
```

**Se o backend estiver rodando em outra porta**, edite o arquivo `.env`.

### 🚀 Passo 3: Iniciar o Servidor de Desenvolvimento

```powershell
npm run dev
```

O frontend estará disponível em: **http://localhost:3000**

### 📊 Passo 4: Garantir que o Backend está Rodando

Antes de usar o frontend, certifique-se de que o backend está rodando:

```powershell
# Em outro terminal, navegue para o Backend
cd "c:\Users\limar\Desktop\final dio py\Digital Superbank\Backend"

# Ative o ambiente virtual (se necessário)
.\.venv\Scripts\Activate.ps1

# Execute o backend
python main.py
```

O backend deve estar rodando em: **http://localhost:8000**

### ✅ Passo 5: Acessar a Aplicação

1. Abra o navegador em: **http://localhost:3000**
2. Você verá a página de login
3. Cadastre um novo usuário ou faça login com credenciais existentes

### 🎯 Funcionalidades Disponíveis

#### Autenticação
- ✅ Login
- ✅ Registro de novos usuários
- ✅ Logout

#### Dashboard
- ✅ Visão geral das contas
- ✅ Saldo total
- ✅ Resumo financeiro

#### Contas
- ✅ Listar todas as contas
- ✅ Criar nova conta
- ✅ Ver detalhes da conta
- ✅ Consultar saldo

#### Transações
- ✅ Depósito
- ✅ Saque
- ✅ Transferência entre contas
- ✅ PIX (enviar e receber)
- ✅ Pagamento de boletos
- ✅ Extrato com filtros

#### Cartões
- ✅ Solicitar novo cartão
- ✅ Visualizar cartões (design 3D)
- ✅ Bloquear/Desbloquear cartão
- ✅ Ajustar limite
- ✅ Pagar fatura
- ✅ Realizar compras

#### Investimentos
- ✅ Listar ativos disponíveis
- ✅ Comprar ativos
- ✅ Vender ativos
- ✅ Ver portfólio
- ✅ Acompanhar preços em tempo real (WebSocket)

#### Perfil
- ✅ Editar informações pessoais
- ✅ Ver score de crédito
- ✅ Alterar senha

### 🛠️ Scripts Úteis

```powershell
# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview

# Lint do código
npm run lint

# Formatar código
npm run format
```

### 📱 Teste de Responsividade

O frontend é totalmente responsivo. Teste em:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

Use o DevTools do navegador (F12) para testar diferentes resoluções.

### 🔍 Debugging

Se encontrar erros:

1. **Erro de conexão com API**
   - Verifique se o backend está rodando
   - Confirme a URL no arquivo `.env`

2. **Erro ao instalar dependências**
   - Delete a pasta `node_modules`
   - Delete o arquivo `package-lock.json`
   - Execute `npm install` novamente

3. **Erro de CORS**
   - Verifique as configurações de CORS no backend
   - O backend já está configurado para aceitar requisições de todas as origens

### 📊 Estrutura de Dados

O frontend consome as seguintes APIs:

- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registro
- `GET /api/v1/auth/me` - Usuário atual
- `GET /api/v1/accounts` - Listar contas
- `POST /api/v1/accounts` - Criar conta
- `POST /api/v1/transactions/deposit` - Depósito
- `POST /api/v1/transactions/withdraw` - Saque
- `POST /api/v1/transactions/transfer` - Transferência
- `POST /api/v1/cards` - Solicitar cartão
- `GET /api/v1/cards` - Listar cartões
- `GET /api/v1/investments/assets` - Listar ativos
- `POST /api/v1/investments/buy` - Comprar ativo
- `WS /ws/market-feed` - Feed de mercado em tempo real

### 🎨 Customização

Para customizar cores, edite:
```
src/styles/global.css
tailwind.config.js
```

### 📝 Notas Importantes

1. O frontend faz **proxy automático** para o backend através do Vite
2. O **token JWT** é armazenado no localStorage
3. O **logout automático** ocorre se o token for inválido
4. Todas as requisições passam por **interceptors do Axios**

### ✅ Checklist de Verificação

- [ ] Node.js instalado
- [ ] Dependências instaladas (`npm install`)
- [ ] Backend rodando (porta 8000)
- [ ] Frontend rodando (porta 3000)
- [ ] Navegador aberto em http://localhost:3000
- [ ] Cadastro de usuário funcionando
- [ ] Login funcionando
- [ ] Dashboard carregando

### 🚀 Próximos Passos

Após a instalação:

1. **Cadastre um usuário** na tela de registro
2. **Faça login** com as credenciais
3. **Crie uma conta** no módulo de contas
4. **Faça um depósito** para adicionar saldo
5. **Explore** as demais funcionalidades

### 💡 Dicas

- Use **Ctrl + Shift + I** para abrir o DevTools
- Use a aba **Network** para ver as requisições
- Use a aba **Console** para ver logs
- Use **React DevTools** para debug de componentes

---

**Frontend criado com sucesso!** 🎉

Se tiver dúvidas, consulte o README.md ou a documentação do código.
