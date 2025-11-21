# 🗄️ ESTRUTURA DE BANCOS DE DADOS - DIGITAL SUPERBANK

> Sistema com **2 bancos de dados separados** para melhor organização

---

## 📊 VISÃO GERAL

### 🏦 Banco Principal: `digital_superbank.db`
**Localização:** `src/database/data/digital_superbank.db`  
**Tamanho:** ~328 KB  
**Função:** Dados bancários, usuários, transações, investimentos

### 🤖 Banco do Chatbot: `chatbot.db`
**Localização:** `src/database/data/chatbot.db`  
**Tamanho:** ~60 KB  
**Função:** Base de conhecimento, conversas, feedback

---

## 🏦 BANCO PRINCIPAL (9 tabelas)

### 👥 Usuários e Autenticação
1. **users** - Dados dos usuários
   - id, name, email, cpf, phone, password_hash
   - created_at, updated_at

2. **addresses** - Endereços dos usuários
   - id, user_id, street, number, complement, neighborhood
   - city, state, zip_code

### 💰 Contas e Transações
3. **accounts** - Contas bancárias
   - id, user_id, account_type, account_number, digit
   - balance, is_active, created_at

4. **transactions** - Histórico de transações
   - id, from_account_id, to_account_id, transaction_type
   - amount, description, timestamp

5. **scheduled_transactions** - Transações agendadas
   - id, from_account_id, to_account_id, amount
   - scheduled_date, is_executed

6. **credit_cards** - Cartões de crédito
   - id, account_id, card_number, cvv, expiry_date
   - limit, available_limit, brand

### 📈 Investimentos
7. **assets** - Ativos disponíveis (ações, fundos)
   - id, symbol, name, asset_type, category
   - current_price, is_active

8. **portfolio_items** - Portfolio dos investidores
   - id, account_id, asset_id, quantity
   - average_price, total_invested

9. **market_history** - Histórico de preços
   - id, asset_id, price, volume, timestamp

---

## 🤖 BANCO DO CHATBOT (5 tabelas)

### 📚 Base de Conhecimento
1. **knowledge_base** - Perguntas e respostas (~27 itens)
   ```sql
   - id (PK)
   - category (string) - "contas", "transacoes", "cartoes", etc
   - question (text) - Pergunta exemplo
   - answer (text) - Resposta detalhada
   - keywords (text) - Palavras-chave (separadas por vírgula)
   - intent (string) - Intenção ("saldo", "transferencia", etc)
   - confidence_threshold (float) - Limiar de confiança (0-1)
   - usage_count (integer) - Contador de uso
   - is_active (boolean)
   - created_at, updated_at
   ```

2. **question_variations** - Variações de perguntas
   ```sql
   - id (PK)
   - knowledge_id (FK) -> knowledge_base
   - variation (text) - Forma alternativa da pergunta
   - created_at
   ```

### 💬 Conversas
3. **chat_conversations** - Sessões de conversa
   ```sql
   - id (PK)
   - user_id (opcional) - Pode ser NULL (anônimo)
   - session_id (string) - UUID da sessão
   - created_at
   - ended_at (nullable)
   ```

4. **chat_messages** - Mensagens trocadas
   ```sql
   - id (PK)
   - conversation_id (FK) -> chat_conversations
   - is_user (boolean) - True=usuário, False=bot
   - message (text)
   - detected_intent (string, nullable)
   - confidence_score (float, nullable)
   - knowledge_id (FK, nullable) -> knowledge_base
   - timestamp
   ```

5. **chat_feedback** - Avaliações dos usuários
   ```sql
   - id (PK)
   - message_id (FK) -> chat_messages
   - is_helpful (boolean) - True=útil, False=não útil
   - comment (text, nullable)
   - created_at
   ```

---

## 🔌 CONEXÕES

### Banco Principal
```python
from src.database.connection import get_db, create_tables

# Criar tabelas
create_tables()

# Usar em endpoints
@app.get("/exemplo")
def exemplo(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### Banco do Chatbot
```python
from src.database.chatbot_connection import (
    get_chatbot_db, 
    create_chatbot_tables
)

# Criar tabelas do chatbot
create_chatbot_tables()

# Usar em endpoints do chatbot
@router.post("/chatbot/message")
def chat(db: Session = Depends(get_chatbot_db)):
    # Usa banco chatbot.db
    kb = db.query(KnowledgeBase).all()
    return kb
```

---

## 📈 ESTATÍSTICAS ATUAIS

### Banco Principal
- **Tabelas:** 9
- **Tamanho:** ~328 KB
- **Registros típicos:**
  - Usuários: variável
  - Transações: cresce continuamente
  - Investimentos: ~15 ativos

### Banco do Chatbot
- **Tabelas:** 5
- **Tamanho:** ~60 KB
- **Conteúdo:**
  - 27 perguntas/respostas
  - ~80 variações de perguntas
  - Conversas: cresce com uso
  - Feedback: cresce com uso

---

## 🎯 VANTAGENS DA SEPARAÇÃO

### ✅ Organização
- Dados bancários separados de dados de IA
- Facilita backup seletivo
- Melhora a manutenção

### ✅ Performance
- Queries do chatbot não afetam banco principal
- Índices otimizados independentemente
- Crescimento isolado

### ✅ Segurança
- Permissões diferentes por banco
- Chatbot pode ser público (sem dados sensíveis)
- Dados bancários sempre protegidos

### ✅ Escalabilidade
- Chatbot pode migrar para outro servidor
- Fácil replicação do conhecimento
- Deploy independente

---

## 🔧 MANUTENÇÃO

### Backup do Banco Principal
```bash
# Copia arquivo
cp src/database/data/digital_superbank.db backup/digital_superbank_$(date +%Y%m%d).db
```

### Backup do Chatbot
```bash
# Copia arquivo
cp src/database/data/chatbot.db backup/chatbot_$(date +%Y%m%d).db
```

### Resetar Banco do Chatbot
```bash
# Remove arquivo
rm src/database/data/chatbot.db

# Recria e popula
python scripts/populate_chatbot.py
```

### Visualizar Dados (SQLite Browser)
```bash
# Instalar DB Browser for SQLite
# Abrir arquivo .db no navegador
```

---

## 📝 RESUMO

```
src/database/data/
├── digital_superbank.db  (328 KB) - Banco principal
│   ├── users (2 tabelas)
│   ├── banking (4 tabelas)
│   └── investments (3 tabelas)
│
└── chatbot.db  (60 KB) - Banco do chatbot
    ├── knowledge (2 tabelas)
    └── conversations (3 tabelas)
```

**Total:** 2 arquivos SQLite, 14 tabelas, ~388 KB

---

*Atualizado em: 20 de Novembro de 2025*
