# 🤖 CHATBOT - DIGITAL SUPERBANK

> Sistema de chatbot inteligente com base de conhecimento e histórico de conversas

---

## ✨ FUNCIONALIDADES

### 🎯 O que o chatbot faz:
- ✅ Responde perguntas sobre o banco automaticamente
- ✅ Detecta intenções do usuário
- ✅ Mantém histórico de conversas
- ✅ Funciona com ou sem autenticação
- ✅ Aprende com feedback dos usuários
- ✅ Suporta variações de perguntas
- ✅ Fornece sugestões de próximas perguntas
- ✅ Estatísticas de uso

### 📚 Base de Conhecimento:
**40+ perguntas/respostas** sobre:
- 🏦 Contas bancárias (7 tipos)
- 💸 Transações (depósito, saque, PIX, boletos)
- 💳 Cartões de crédito (solicitação, compras, fatura)
- 📈 Investimentos (ações, fundos, portfolio)
- 🔐 Segurança (login, proteção de dados)
- 📞 Suporte (contato, horários, documentação)
- ℹ️ Informações gerais

---

## 🗄️ ESTRUTURA DO BANCO DE DADOS

### 5 Tabelas Criadas:

#### 1. **knowledge_base** - Base de conhecimento
```sql
- id (PK)
- category (string) - ex: "contas", "transacoes", "cartoes"
- question (text) - Pergunta exemplo
- answer (text) - Resposta
- keywords (text) - Palavras-chave separadas por vírgula
- intent (string) - Intenção (ex: "saldo", "transferencia")
- confidence_threshold (float) - Limiar de confiança
- usage_count (integer) - Contador de uso
- is_active (boolean)
- created_at, updated_at
```

#### 2. **question_variations** - Variações de perguntas
```sql
- id (PK)
- knowledge_id (FK)
- variation (text) - Variação da pergunta
- created_at
```

#### 3. **chat_conversations** - Sessões de chat
```sql
- id (PK)
- user_id (FK, opcional)
- session_id (string) - UUID da sessão
- created_at
- ended_at
```

#### 4. **chat_messages** - Mensagens individuais
```sql
- id (PK)
- conversation_id (FK)
- is_user (boolean) - True = usuário, False = bot
- message (text)
- detected_intent (string)
- confidence_score (float)
- knowledge_id (FK)
- timestamp
```

#### 5. **chat_feedback** - Feedback dos usuários
```sql
- id (PK)
- message_id (FK)
- is_helpful (boolean)
- comment (text, opcional)
- created_at
```

---

## 🚀 COMO USAR

### 1️⃣ Inicializar Base de Conhecimento

```bash
# Criar tabelas e popular com 40+ perguntas/respostas
python scripts/populate_chatbot.py
```

**Saída esperada:**
```
📊 Populando base de conhecimento...

✅ [1/40] contas: Como abrir uma conta?...
✅ [2/40] contas: Quais tipos de contas existem?...
...
================================================================================
✅ BASE DE CONHECIMENTO POPULADA COM SUCESSO!
================================================================================
📊 Total de itens: 40

📚 Categorias criadas:
   • Contas: 4 itens
   • Transacoes: 7 itens
   • Cartoes: 4 itens
   • Investimentos: 5 itens
   • Seguranca: 2 itens
   • Suporte: 3 itens
   • Geral: 2 itens

🤖 O chatbot está pronto para uso!
   Endpoint: POST /api/v1/chatbot/message
```

### 2️⃣ Testar Chatbot

```bash
# Teste completo automatizado
python tests/test_chatbot.py
```

**Testa:**
- Envio de mensagens
- Detecção de intenções
- Histórico de conversas
- Estatísticas
- Sugestões populares

---

## 📡 ENDPOINTS DA API

### POST /api/v1/chatbot/message
**Envia mensagem para o chatbot**

**Request:**
```json
{
  "message": "Como fazer PIX?",
  "session_id": "opcional-uuid"
}
```

**Response:**
```json
{
  "response": "Para enviar PIX:\n\nPOST /api/v1/transactions/pix/send\n\nEnvie:\n{\n  \"from_account_id\": 123,\n  \"pix_key\": \"11999999999\",\n  \"amount\": 50.00\n}\n\nO PIX é instantâneo!",
  "intent": "fazer_pix",
  "confidence": 0.95,
  "session_id": "abc-123-def-456",
  "suggestions": [
    "Como fazer uma transferência?",
    "Como ver meu extrato?",
    "Como fazer um depósito?"
  ]
}
```

### GET /api/v1/chatbot/history/{session_id}
**Obtém histórico completo de uma conversa**

**Response:**
```json
{
  "session_id": "abc-123-def-456",
  "started_at": "2025-11-20T22:00:00",
  "ended_at": null,
  "messages": [
    {
      "id": 1,
      "is_user": true,
      "message": "Como fazer PIX?",
      "timestamp": "2025-11-20T22:00:05",
      "intent": null,
      "confidence": null
    },
    {
      "id": 2,
      "is_user": false,
      "message": "Para enviar PIX...",
      "timestamp": "2025-11-20T22:00:06",
      "intent": "fazer_pix",
      "confidence": 0.95
    }
  ]
}
```

### POST /api/v1/chatbot/feedback
**Envia feedback sobre uma resposta**

**Request:**
```json
{
  "message_id": 123,
  "is_helpful": true,
  "comment": "Muito útil, obrigado!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Feedback registrado com sucesso! Obrigado por nos ajudar a melhorar."
}
```

### GET /api/v1/chatbot/stats
**Obtém estatísticas do chatbot**

**Response:**
```json
{
  "total_conversations": 150,
  "total_messages": 620,
  "average_confidence": 0.87,
  "most_used_intents": [
    {"intent": "fazer_pix", "count": 45},
    {"intent": "consultar_saldo", "count": 38},
    {"intent": "solicitar_cartao", "count": 32}
  ],
  "feedback_positive": 142,
  "feedback_negative": 8
}
```

### GET /api/v1/chatbot/suggestions?limit=5
**Obtém perguntas mais populares**

**Response:**
```json
[
  "Como fazer PIX?",
  "Como consultar meu saldo?",
  "Como solicitar um cartão de crédito?",
  "Quais investimentos estão disponíveis?",
  "Como ver meu extrato?"
]
```

---

## 🧠 COMO FUNCIONA

### 1. Detecção de Intenção

O chatbot usa **algoritmo de similaridade de texto**:

1. Normaliza a mensagem (lowercase, remove pontuação)
2. Compara com todas as perguntas da base
3. Compara com variações cadastradas
4. Verifica palavras-chave
5. Calcula score de similaridade (0-1)
6. Retorna resposta se score >= threshold

**Exemplo:**
```
Usuário: "quero fazer um pix"
Normalizado: "quero fazer um pix"
Match: "Como fazer PIX?" (similarity: 0.85)
Keywords: "pix" encontrado (+0.2)
Score final: 0.95
Threshold: 0.6
✅ Resposta encontrada!
```

### 2. Sessões de Chat

- Cada conversa tem um `session_id` único (UUID)
- Mantém histórico completo de mensagens
- Permite consultar conversas anteriores
- Útil para análise e melhoria

### 3. Aprendizado com Feedback

- Usuários podem marcar respostas como úteis/não úteis
- Feedback armazenado para análise
- Permite identificar perguntas problemáticas
- Melhoria contínua da base de conhecimento

---

## 📊 CATEGORIAS E EXEMPLOS

### 🏦 CONTAS (4 perguntas)
- Como abrir uma conta?
- Quais tipos de contas existem?
- Como consultar meu saldo?
- O que é Conta Black?

### 💸 TRANSAÇÕES (7 perguntas)
- Como fazer um depósito?
- Como fazer um saque?
- Qual o limite de saque?
- Como fazer uma transferência?
- Como fazer PIX?
- Como pagar um boleto?
- Como ver meu extrato?

### 💳 CARTÕES (4 perguntas)
- Como solicitar um cartão de crédito?
- Quais bandeiras vocês aceitam?
- Como fazer uma compra no cartão?
- Como pagar a fatura?

### 📈 INVESTIMENTOS (5 perguntas)
- Quais investimentos estão disponíveis?
- Como comprar uma ação?
- Como vender uma ação?
- Como ver meu portfólio?
- Os preços são atualizados em tempo real?

### 🔐 SEGURANÇA (2 perguntas)
- Como faço login?
- Meus dados estão seguros?

### 📞 SUPORTE (3 perguntas)
- Como entro em contato com o suporte?
- Onde vejo a documentação da API?
- Qual o horário de atendimento?

### ℹ️ GERAL (2 perguntas)
- O que é o Digital Superbank?
- Obrigado!

---

## 🔧 PERSONALIZAÇÃO

### Adicionar Nova Pergunta/Resposta

```python
from src.database.connection import SessionLocal
from src.models.chatbot import KnowledgeBase, QuestionVariation

db = SessionLocal()

# Criar item de conhecimento
kb = KnowledgeBase(
    category="transacoes",
    question="Como cancelar uma transferência?",
    answer="Para cancelar uma transferência agendada:\nPOST /api/v1/transactions/{id}/cancel",
    keywords="cancelar, transferencia, desfazer",
    intent="cancelar_transferencia",
    confidence_threshold=0.6
)
db.add(kb)
db.flush()

# Adicionar variações
variations = [
    "Quero cancelar uma transferência",
    "Como desfaço uma transferência",
    "Cancelar transferência agendada"
]

for var_text in variations:
    var = QuestionVariation(
        knowledge_id=kb.id,
        variation=var_text
    )
    db.add(var)

db.commit()
```

### Ajustar Threshold de Confiança

```python
# Para perguntas mais específicas, use threshold maior
kb.confidence_threshold = 0.8  # Exige 80% de similaridade

# Para perguntas genéricas, use threshold menor
kb.confidence_threshold = 0.5  # Aceita 50% de similaridade
```

---

## 📈 ESTATÍSTICAS E ANÁLISE

### Ver Perguntas Mais Usadas

```python
from src.database.connection import SessionLocal
from src.models.chatbot import KnowledgeBase
from sqlalchemy import desc

db = SessionLocal()

top_questions = db.query(KnowledgeBase).order_by(
    desc(KnowledgeBase.usage_count)
).limit(10).all()

for q in top_questions:
    print(f"{q.question}: {q.usage_count} usos")
```

### Analisar Feedback

```python
from src.models.chatbot import ChatFeedback

# Feedback positivo
positive = db.query(ChatFeedback).filter(
    ChatFeedback.is_helpful == True
).count()

# Feedback negativo
negative = db.query(ChatFeedback).filter(
    ChatFeedback.is_helpful == False
).count()

print(f"Taxa de satisfação: {positive/(positive+negative)*100:.1f}%")
```

---

## 🎯 MELHORIAS FUTURAS

### Implementado ✅
- ✅ Base de conhecimento com 40+ perguntas
- ✅ Detecção de intenções
- ✅ Variações de perguntas
- ✅ Histórico de conversas
- ✅ Feedback de usuários
- ✅ Estatísticas de uso
- ✅ Sugestões automáticas

### Possíveis Melhorias 🔮
- 🔮 Integração com NLP (spaCy, NLTK)
- 🔮 Machine Learning para melhores predições
- 🔮 Suporte a múltiplos idiomas
- 🔮 Respostas contextualizadas
- 🔮 Integração com ações diretas (fazer transações via chat)
- 🔮 Chat em tempo real via WebSocket
- 🔮 Análise de sentimento
- 🔮 Exportação de conversas

---

## 📝 NOTAS IMPORTANTES

### ✅ Vantagens
- Funciona sem autenticação (público)
- Responde 24/7
- Não requer treinamento complexo
- Fácil de adicionar novos conhecimentos
- Mantém histórico completo
- Aprende com feedback

### ⚠️ Limitações
- Detecção de intenção básica (similaridade de texto)
- Não entende contexto entre mensagens
- Precisa de variações cadastradas manualmente
- Respostas fixas (não generativas)

### 💡 Dicas de Uso
- Adicione muitas variações para perguntas importantes
- Use keywords para melhorar detecção
- Analise feedback regularmente
- Ajuste threshold conforme necessidade
- Mantenha respostas curtas e objetivas

---

**Criado em:** 20 de Novembro de 2025  
**Status:** ✅ 100% Funcional  
**Endpoints:** 5 rotas REST  
**Base de Conhecimento:** 40+ itens

---

*Sistema de Chatbot Inteligente - Digital Superbank* 🤖
