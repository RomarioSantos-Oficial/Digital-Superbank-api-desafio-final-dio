# Digital Superbank - Documentação do Sistema

## 📋 Informações Gerais

- **Nome do Banco**: Digital Superbank
- **Código do Banco**: 222
- **Agência Padrão**: 0001
- **Bandeiras de Cartão**: Aura | Aura Gold | Aura Platinum

## 🏦 Tipos de Conta e Dígitos Verificadores (DV)

| Tipo de Conta | Dígito (DV) | Regras de Elegibilidade |
|---------------|-------------|-------------------------|
| Conta Corrente | 1 | Todos os clientes (obrigatória) |
| Conta Poupança | 3 | A partir de 13 anos |
| Conta Salário | 4 | A partir de 16 anos |
| Conta Universitária | 5 | A partir de 16 anos |
| Conta Empresarial | 7 | A partir de 21 anos |
| Conta Black | 9 | Maiores de 18 anos com saldo ≥ R$ 50.000 |
| Conta Investimento | 8 | Maiores de 18 anos com Conta Empresarial ou Conta Black (saldo ≥ R$ 50.000) - Opcional |

**Formato do Número de Conta**: `000000-DV`

## 👥 Regras de Idade e Contas Permitidas

### 💠 Idade Mínima Geral
- **Idade mínima para criar um cliente**: 13 anos

### 🧒 Entre 13 e 15 anos
- ✔️ Conta Corrente (obrigatória)
- ✔️ Conta Poupança

### 🧑 De 16 a 17 anos
- ✔️ Conta Corrente
- ✔️ Conta Poupança
- ✔️ Conta Salário
- ✔️ Conta Universitária

### 🧑‍🦱 A partir de 18 anos
- ✔️ Todas as anteriores
- ✔️ Conta Black (se saldo ≥ R$ 50.000)
- ✔️ Conta Investimento (se tiver Conta Empresarial ou Conta Black com saldo ≥ R$ 50.000)

### 🧔 A partir de 21 anos
- ✔️ Todas as anteriores
- ✔️ Conta Empresarial

## 💰 Limites de Transação

### Saques
- **Limite diário total**: R$ 5.000,00
- **Número de saques por dia**: 3 operações
- **Valor máximo por saque**: R$ 2.000,00

## 📝 Formatos Padrão

- **Data**: DD/MM/AAAA (padrão brasileiro)
- **Moeda**: R$ (Real brasileiro)
- **CPF**: 000.000.000-00

---

## 🔧 Categorias de Funcionalidades da API

### Categoria A: Essenciais da Conta (Account Core)
Operações passivas ou de manutenção.

#### 1. Consulta de Saldo (Balance Check)
- **Descrição**: Retorna o dinheiro disponível na conta no momento exato
- **Tipo**: Leitura (GET)

#### 2. Extrato Bancário (Bank Statement)
- **Descrição**: Lista cronológica de todas as movimentações em um período
- **Tipo**: Leitura (GET) com filtros de data
- **Exemplo**: Últimos 30 dias

#### 3. Criação de Conta (Account Opening)
- **Descrição**: Cadastro do cliente (KYC básico) que gera número de agência/conta
- **Tipo**: Criação (POST)

---

### Categoria B: Movimentação Interna (On-Us Transactions)
Transações onde o dinheiro não sai do ecossistema do banco.

#### 1. Depósito (Simulado)
- **Descrição**: Injetar dinheiro "novo" em uma conta
- **Tipo**: Escrita (POST) - Crédito (+)
- **Exemplo API**: "Adicione R$ 500 na conta X"

#### 2. Saque (Simulado)
- **Descrição**: Retirar dinheiro do sistema
- **Tipo**: Escrita (POST) - Débito (-)
- **Validações**: Verificação de saldo

#### 3. Transferência Interna (P2P / TEF)
- **Descrição**: Mover dinheiro de uma conta para outra dentro do banco
- **Tipo**: Escrita (POST)
- **Desafio**: Transação atômica (garantir que o débito da Conta A e crédito na Conta B sejam executados juntos, com rollback em caso de falha)

---

### Categoria C: Movimentação Externa (Simulada)
Simulação de operações que normalmente envolvem outros bancos.

#### 1. PIX (Envio)
- **Descrição**: Enviar dinheiro instantaneamente usando chave PIX
- **Chaves aceitas**: CPF, Email, Aleatória
- **Implementação**: Debita conta do usuário e registra como "PIX Enviado"

#### 2. PIX (Recebimento / Cash-in)
- **Descrição**: Receber PIX de outro banco
- **Implementação**: Webhook simulado que credita valor e registra como "PIX Recebido"

#### 3. Pagamento de Boleto/Contas
- **Descrição**: Pagamento de contas usando código de barras fictício
- **Implementação**: Validar saldo e debitar valor

---

### Categoria D: Cartões
Implementação da bandeira "Aura".

#### 1. Compra no Crédito
- **Descrição**: Simular compra com cartão de crédito
- **Implementação**: Aumenta saldo devedor na fatura e diminui limite disponível (não debita conta corrente imediatamente)

#### 2. Compra no Débito
- **Descrição**: Compra com desconto imediato
- **Implementação**: Similar a saque, categorizado como "Compra Débito"

#### 3. Pagamento de Fatura
- **Descrição**: Usar saldo da conta corrente para pagar fatura do cartão
- **Implementação**: Transferência da conta corrente para zerar dívida do cartão

> **Nota**: Sistema usado entre usuários dentro da mesma API

---

## 💳 Regras para Cartão de Crédito (Bandeira Aura)

### 1. Pré-Requisitos do Cliente

#### Conta Corrente Existente
- Cliente deve ter conta corrente ativa no Digital Superbank
- Cartão será vinculado à conta para débitos de fatura

#### Idade Mínima
- **Mínimo**: 18 anos
- Validação via campo `birth_date` ou modelo User

### 2. Análise de Crédito (Simulada)

#### Simulação de Score de Crédito
- Baseado em dados da conta corrente
- Critérios: número de depósitos, saldo médio dos últimos 30 dias

#### Definição do Limite de Crédito

| Faixa de Score | Resultado | Limite | Categoria |
|----------------|-----------|--------|-----------|
| < 60 | Reprovado | - | - |
| 60-70 | Aprovado | R$ 500,00 | Aura Basic |
| 71-85 | Aprovado | R$ 1.500,00 | Aura Plus |
| 86-100 | Aprovado | R$ 5.000,00 | Aura Premium |

**Alternativa**: Limite baseado em percentual do saldo médio ou maior depósito

### 3. Dados do Cartão a Serem Gerados

| Campo | Descrição | Regra |
|-------|-----------|-------|
| **Número do Cartão (PAN)** | 16 dígitos | Inicia com 5XXX (Bandeira Aura) + dígitos aleatórios + Dígito Verificador (Algoritmo de Luhn) |
| **Nome do Titular** | Nome do cliente | Obtido de `owner_name` da conta |
| **Data de Validade** | Mês/Ano | 3 a 5 anos após emissão |
| **CVV** | 3 ou 4 dígitos | Gerado aleatoriamente |
| **Limite Total** | Valor aprovado | Conforme análise de crédito |
| **Limite Disponível** | Valor disponível | Igual ao Limite Total inicialmente |
| **Fatura Atual** | Valor gasto | R$ 0,00 no início |
| **Status** | Estado do cartão | Ativo, Bloqueado, Cancelado |

### 4. Política de Múltiplos Cartões
- **Recomendação inicial**: 1 cartão por conta
- **Possibilidade futura**: Múltiplos cartões (virtual, internacional, etc.)

### 5. Estrutura de Implementação

#### Schemas (`app/schemas/credit_card.py`)
- **CreditCardCreate**: Campos mínimos (a maioria é gerada automaticamente)
  - Opcional: `requested_limit`
- **CreditCardResponse**: Todos os dados exceto CVV (só retorna na criação)

#### Serviço (`app/services/credit_card_service.py`)
- Lógica de análise de crédito
- Geração de número do cartão, CVV, data de validade
- Função: `create_new_credit_card(account_id: int, db: Session)`

#### Rotas (`app/api/v1/endpoints/credit_cards.py`)
- `POST /api/v1/credit-cards/` - Solicitar/criar cartão
- `GET /api/v1/credit-cards/{account_id}` - Listar cartões da conta
- `POST /api/v1/credit-cards/{card_id}/block` - Bloquear cartão


---

## 📈 Módulo de Investimentos (Simulado)

### Características Gerais
- **Ativos Fictícios**: Empresas listadas (ações) e fundos (LCI, CDB)
- **Preço Base**: Cada ativo possui preço inicial
- **Flutuação**: Preços flutuam aleatoriamente para simular mercado
- **Operações**: Compra e venda de ativos
- **Portfólio**: Registro de ativos e quantidade por cliente
- **Vinculação**: Operações debitam/creditam conta corrente

### Empresas de Ações (Fictícias)

#### 💻 Tecnologia
- **NexGen Innovations**: Desenvolvimento de software e IA
- **AetherNet Solutions**: Infraestrutura de rede e nuvem
- **Quantex Data**: Análise de dados e big data

#### 🛒 Varejo/Consumo
- **UrbanPulse Retail**: Grande rede de varejo multicanal
- **Flourish Foods**: Indústria alimentícia e bebidas
- **Stellar Fashion Group**: Moda e vestuário

#### ⚡ Indústria/Energia
- **TerraNova Mining**: Mineração e recursos naturais
- **Voltix Energy**: Energia renovável e sustentabilidade
- **Proton Industries**: Manufatura avançada e automação

#### 💼 Serviços/Finanças
- **Insight Capital**: Consultoria financeira e investimentos
- **MediCare Solutions**: Saúde e bem-estar

### Fundos de Renda Fixa (Simulados)
- **Apex RF Simples (LCI/CDB)**: Fundo de Renda Fixa de baixo risco
- **Apex RF Performance (CDB Plus)**: Fundo de Renda Fixa com retorno maior

### Estrutura de Banco de Dados

#### Modelo `Asset` (Ativo)
Representa ações ou fundos disponíveis no mercado

#### Modelo `PortfolioItem`
Representa posições do cliente em ativos específicos (quantidade de ações)


---

## 🔨 Funcionalidades Adicionais

### A. Funcionalidades Financeiras Básicas

#### 1. Pagamento de Contas e Boletos
- **Descrição**: Simular pagamento de contas (água, luz, telefone) ou boletos
- **Implementação**:
  - Recebe: `bar_code`, `amount`, `due_date`
  - Valida saldo na conta
  - Debita valor e registra transação
- **Desafio**: Validar código de barras e calcular juros/multas para atrasos

#### 2. Agendamento de Pagamentos/Transferências
- **Descrição**: Agendar transferência ou pagamento futuro
- **Implementação**:
  - Modelo: `ScheduledTransaction` (account_id, target_account_id, amount, schedule_date, status)
  - Endpoints: criar e listar agendamentos
  - Mecanismo: Simular cron job para executar agendamentos
- **Status**: pending, executed, failed
- **Desafio**: Tratar falhas (saldo insuficiente na data agendada)

#### 3. Extrato Detalhado com Filtros
- **Descrição**: Extrato com filtros avançados
- **Endpoint**: `GET /accounts/{account_id}/statement?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&transaction_type=deposit&min_amount=X&max_amount=Y`
- **Desafio**: Otimizar consultas para grandes volumes

### B. Gestão de Cartões de Crédito

#### 1. Bloqueio e Desbloqueio
- **Endpoints**: 
  - `POST /credit-cards/{card_id}/block`
  - `POST /credit-cards/{card_id}/unblock`
- **Implementação**: Atualiza campo `status`

#### 2. Pagamento de Fatura
- **Endpoint**: `POST /credit-cards/{card_id}/pay-bill`
- **Implementação**:
  - Valida saldo na conta corrente
  - Debita da conta, diminui `current_bill_amount`
  - Aumenta `available_limit`

#### 3. Ajuste de Limite
- **Endpoint**: `POST /credit-cards/{card_id}/adjust-limit`
- **Implementação**: Aprovação simulada baseada no histórico de pagamentos

#### 4. Cartão Virtual
- **Descrição**: Número, CVV e validade temporários para compras online
- **Implementação**: 
  - Campo `is_virtual: bool` no modelo `CreditCard`
  - Endpoints: criar, listar e expirar cartões virtuais

### C. Segurança e Autenticação

#### 1. Autenticação de Usuários
- **Modelo User**: `email`, `password_hash`
- **JWT**: Tokens para autenticar requisições
- **Endpoints**:
  - `POST /auth/register` - Criar usuário
  - `POST /auth/login` - Fazer login
- **Implementação**: `Depends(get_current_user)` em rotas sensíveis
- **Desafio**: Hash de senhas (passlib), refresh tokens

#### 2. Autorização (Permissões)
- **Descrição**: Garantir acesso apenas aos próprios recursos
- **Validação**: `current_user.id == account.user_id`

#### 3. 2FA (Two-Factor Authentication - Simulada)
- **Endpoints**:
  - `POST /transactions/initiate` - Gera e "envia" código
  - `POST /transactions/confirm` - Valida código para finalizar transação

### D. Outras Funcionalidades

#### 1. Notificações (Simuladas)
- **Implementação**: `print()` simulando push notification ou modelo `Notification`

#### 2. Categorização de Gastos
- **Campo**: `category` no modelo `Transaction`
- **Endpoint**: Listar gastos por categoria (alimentação, transporte, lazer)

#### 3. Relatórios Financeiros
- **Descrição**: Resumos financeiros (gastos mensais, performance de investimentos)
- **Implementação**: Endpoints GET que agregam dados

#### 4. Endpoint de Auditoria/Logs
- **Descrição**: Registrar chamadas importantes à API
- **Implementação**: Middleware do FastAPI ou decorator customizado


---

## 🎯 Melhorias na Qualidade e Robustez do Código

### 1. Testes Unitários e de Integração
- **Foco**: Funcionalidades financeiras (transferências, ativos, faturas)
- **Benefício**: Garante transações atômicas e previne bugs
- **Ferramentas**: `pytest`, `pytest-alembic`, SQLAlchemy mock

### 2. Tratamento de Erros Centralizado
- **Implementação**: `exception_handlers` do FastAPI
- **Formato**: JSON padronizado `{"detail": "Mensagem de erro"}`
- **Benefício**: Melhor experiência do desenvolvedor e depuração

### 3. Logs de Auditoria Detalhados
- **Eventos**: Login, transferências, compra/venda, criação de cartão, erros
- **Implementação**: Módulo `logging` do Python
- **Destinos**: Arquivos, console ou serviço externo

### 4. Versionamento de API Consistente
- **Padrão**: `/api/v1/`
- **Benefício**: Evolução sem quebrar compatibilidade
- **Próximo passo**: Criar `/api/v2/` quando necessário

### 5. Paginação para Listagens
- **Parâmetros**: `skip`, `limit`
- **Aplicação**: Extratos, ativos, portfólio
- **Benefício**: Evita sobrecarga com grandes volumes

### 6. Otimização de Consultas SQL
- **Problema**: N+1 queries
- **Solução**: `selectinload`, `joinedload`, `lazy=False`
- **Benefício**: Melhora performance em dados relacionados

### 7. Caching (Opcional)
- **Ferramentas**: Redis ou Memcached
- **Aplicação**: Dados pouco mutáveis (lista de ativos, saldos com delay aceitável)
- **Benefício**: Reduz carga no banco e acelera respostas

### 8. Validações Avançadas com Pydantic
- **Recursos**: `Field`, `validator`, `model_validator`
- **Aplicação**: Formatos monetários, datas, regras de negócio
- **Benefício**: Código mais limpo e consistente

### 9. Documentação da API
- **Recursos**: `summary`, `description`, `response_description`, `example`
- **Benefício**: Facilita consumo da API (especialmente frontend)

### 10. Linting e Formatação
- **Ferramentas**: `flake8`, `black`, `isort`
- **Configuração**: `requirements.txt`, `pyproject.toml`, `Makefile`
- **Benefício**: Código consistente e legível


---

## 🚀 Funcionalidades Avançadas

### 1. Transações Recorrentes
- **Descrição**: Pagamentos/transferências automáticas periódicas
- **Períodos**: Mensal, semanal, anual
- **Implementação**: Extensão do agendamento com campos de recorrência

### 2. Integração com Ferramentas de Análise
- **Descrição**: Exportar dados financeiros
- **Formatos**: CSV/JSON
- **Conteúdo**: Extrato, gastos por categoria

### 3. Empréstimos/Crédito Pessoal (Simulado)
- **Modelo Loan**: `amount`, `interest_rate`, `installments`, `status`
- **Funcionalidades**:
  - Lógica de aprovação simulada
  - Cálculo de parcelas
  - Débito automático da conta corrente

### 4. Geração de Relatórios (XML/PDF)
- **Descrição**: Extratos e faturas em formatos oficiais
- **Bibliotecas**: 
  - `reportlab` (PDF)
  - `lxml` (XML)

---

## 💾 Banco de Dados e Cadastro

### Banco de Dados Recomendado
- **Desenvolvimento**: SQLite (simplicidade, sem necessidade de servidor)
- **Produção**: PostgreSQL ou MySQL

### Modelo de Cadastro de Usuário

#### Tabela `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,  -- 000.000.000-00
    birth_date DATE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabela `addresses`
```sql
CREATE TABLE addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    street VARCHAR(255) NOT NULL,
    number VARCHAR(10) NOT NULL,
    complement VARCHAR(100),
    neighborhood VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,  -- SP, RJ, MG, etc.
    zip_code VARCHAR(9) NOT NULL,  -- 00000-000
    is_primary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Validações Importantes

#### CPF
- **Formato**: 000.000.000-00
- **Validação**: Algoritmo de validação de CPF (dígitos verificadores)
- **Unicidade**: Não permitir CPF duplicado

#### Endereço
- **CEP**: Validar formato 00000-000
- **Estado**: Validar siglas brasileiras (AC, AL, AP, AM, BA, etc.)

#### Email
- **Formato**: Validação regex
- **Unicidade**: Não permitir email duplicado

#### Telefone
- **Formato**: (00) 00000-0000 ou (00) 0000-0000

### Exemplo de Schema Pydantic para Cadastro

```python
from pydantic import BaseModel, Field, validator
from datetime import date
import re

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=255)
    cpf: str = Field(..., regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    birth_date: date
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: str = Field(..., regex=r'^\(\d{2}\) \d{4,5}-\d{4}$')
    password: str = Field(..., min_length=8)
    
    @validator('cpf')
    def validate_cpf(cls, v):
        # Implementar algoritmo de validação de CPF
        return v
    
    @validator('birth_date')
    def validate_age(cls, v):
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 13:
            raise ValueError('Idade mínima: 13 anos')
        return v

class AddressCreate(BaseModel):
    street: str
    number: str
    complement: str = None
    neighborhood: str
    city: str
    state: str = Field(..., regex=r'^[A-Z]{2}$')
    zip_code: str = Field(..., regex=r'^\d{5}-\d{3}$')
    is_primary: bool = False
```

---

## 📚 Resumo de Endpoints Sugeridos

### Autenticação
- `POST /auth/register` - Cadastro de usuário
- `POST /auth/login` - Login (retorna JWT)
- `POST /auth/refresh` - Renovar token

### Contas
- `POST /accounts/` - Criar conta
- `GET /accounts/{account_id}` - Consultar saldo
- `GET /accounts/{account_id}/statement` - Extrato

### Transações
- `POST /transactions/deposit` - Depósito
- `POST /transactions/withdraw` - Saque
- `POST /transactions/transfer` - Transferência interna
- `POST /transactions/pix/send` - Enviar PIX
- `POST /transactions/pix/receive` - Receber PIX
- `POST /transactions/pay-bill` - Pagar boleto

### Cartões
- `POST /credit-cards/` - Solicitar cartão
- `GET /credit-cards/{account_id}` - Listar cartões
- `POST /credit-cards/{card_id}/block` - Bloquear
- `POST /credit-cards/{card_id}/unblock` - Desbloquear
- `POST /credit-cards/{card_id}/pay-bill` - Pagar fatura

### Investimentos
- `GET /investments/assets` - Listar ativos
- `POST /investments/buy` - Comprar ativo
- `POST /investments/sell` - Vender ativo
- `GET /investments/portfolio/{account_id}` - Ver portfólio

---

*Documentação do Sistema Digital Superbank*  
*Última atualização: 20/11/2025*

Chatbot Principalmente pelo Frontend (abordagem limitada)
Se você tentasse fazer um chatbot inteiramente pelo frontend (usando apenas JavaScript no navegador), você enfrentaria grandes limitações:

Segurança: Todas as regras de negócio sensíveis (saldo, transferências, dados pessoais) estariam expostas no código do navegador, o que é um risco enorme.

Acesso a Dados: O frontend não pode acessar diretamente o banco de dados. Ele precisaria de uma API para buscar informações da conta, realizar transações, etc.

Lógica Complexa: Manter a lógica de conversação, processamento de linguagem natural (NLP) e integração com serviços externos (como o seu módulo de investimentos) no frontend se tornaria um pesadelo de manutenção e performance.

Escalabilidade: Cada usuário carregaria toda a lógica do chatbot, podendo gerar lentidão.

Chatbot Principalmente pela API (abordagem recomendada)
A melhor prática é que a lógica central do chatbot e o acesso aos dados fiquem na sua API (backend). O frontend (seja um site, aplicativo móvel ou até mesmo uma interface de terminal) se comunicaria com essa API.

Como funcionaria:

Usuário digita mensagem no Frontend: O cliente digita "Qual é o meu saldo?" no chat na página do Apex Bank.

Frontend envia mensagem para a API: O frontend faz uma requisição POST para um endpoint da sua API (ex: /api/v1/chatbot/message).

Essa requisição conteria a mensagem do usuário e talvez o token de autenticação do usuário.

API processa a mensagem:

Processamento de Linguagem Natural (NLP): A API usa alguma biblioteca ou serviço de NLP (como NLTK, SpaCy, ou até mesmo um modelo de ML mais complexo como o GPT da OpenAI se você quiser algo avançado) para entender a intenção do usuário ("ver saldo") e extrair entidades ("saldo", "minha conta").

Lógica de Negócio: Com a intenção identificada, a API chama os serviços apropriados:

Se a intenção for "ver saldo", ela chama o account_service para buscar o saldo da conta do usuário autenticado.

Se a intenção for "transferir dinheiro", ela pede os detalhes e, após confirmação, chama o transaction_service.

Geração de Resposta: A API formula uma resposta em linguagem natural (ex: "Seu saldo atual é R$ 1.500,00.")

API envia resposta de volta ao Frontend: A resposta (JSON com a mensagem do chatbot) é enviada de volta ao frontend.

Frontend exibe a resposta: O frontend apenas renderiza a resposta na interface do chat.

Componentes do Chatbot na API:
Endpoint de Chat: POST /api/v1/chatbot/message

Serviço de Chatbot (app/services/chatbot_service.py):

Módulo de NLP (seja regras simples baseadas em palavras-chave ou integração com bibliotecas/serviços).

Mapeamento de intenções para as funções dos seus outros serviços (account_service, transaction_service, investment_service, etc.).

Lógica para manter o contexto da conversação (ex: "Qual conta você quer ver o saldo?").

Modelos (Opcional): Você pode ter um modelo ChatSession para guardar o histórico da conversa ou o contexto de cada usuário, se for um chatbot mais complexo.

Vantagens da Abordagem Backend (API):
Segurança: A lógica de negócio e o acesso aos dados ficam no servidor, protegidos.

Performance: Operações pesadas (NLP, acesso a DB) são executadas no servidor, não no cliente.

Escalabilidade: Múltiplos frontends (web, mobile, WhatsApp) podem usar a mesma lógica de chatbot na API.

Manutenibilidade: É mais fácil atualizar a lógica do chatbot no backend sem precisar atualizar o frontend em todas as plataformas.

Complexidade: Facilita a integração com IA/ML para NLP avançado, já que essas bibliotecas/modelos geralmente rodam melhor no servidor.