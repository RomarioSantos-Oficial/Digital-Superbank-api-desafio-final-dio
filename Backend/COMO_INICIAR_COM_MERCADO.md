# 📈 Como Funciona o Simulador de Mercado em Tempo Real

## ✅ NOVO: Simulador Integrado à API

**O simulador agora é gerenciado automaticamente pela API!**

### 🚀 Como Usar

1. **Inicie apenas o Backend:**

```powershell
cd Backend
python main.py
```

✅ **Pronto!** O simulador inicia automaticamente junto com a API.

---

## 📊 Controle do Simulador via API

Você pode controlar o simulador através de endpoints:

### Ver Status

```bash
GET http://localhost:8000/api/v1/market/simulator/status
```

**Resposta:**
```json
{
  "running": true,
  "websocket_connections": 2,
  "update_interval": 10
}
```

### Parar Simulador

```bash
POST http://localhost:8000/api/v1/market/simulator/stop
```

### Iniciar Simulador

```bash
POST http://localhost:8000/api/v1/market/simulator/start
```

---

## 📡 Como Funciona Agora?

```
┌─────────────────────────────────────────────────────────┐
│            ARQUITETURA INTEGRADA                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────┐              │
│  │        Backend API (FastAPI)         │              │
│  │                                      │              │
│  │  ┌────────────────────────────────┐ │              │
│  │  │  Background Task:              │ │              │
│  │  │  Simulador de Mercado          │ │              │
│  │  │  (roda a cada 10s)             │ │              │
│  │  └───────────┬────────────────────┘ │              │
│  │              │                       │              │
│  │              ▼                       │              │
│  │  ┌────────────────────────────────┐ │              │
│  │  │  Banco de Dados SQLite         │ │              │
│  │  │  (atualiza preços)             │ │              │
│  │  └───────────┬────────────────────┘ │              │
│  │              │                       │              │
│  │              ▼                       │              │
│  │  ┌────────────────────────────────┐ │              │
│  │  │  WebSocket Manager             │ │              │
│  │  │  (notifica clientes)           │ │              │
│  │  └───────────┬────────────────────┘ │              │
│  └──────────────┼──────────────────────┘              │
│                 │                                       │
│                 ▼                                       │
│  ┌────────────────────────────────────┐               │
│  │        Frontend (React)            │               │
│  │  - Recebe via WebSocket            │               │
│  │  - Polling a cada 10s (backup)     │               │
│  └────────────────────────────────────┘               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Fluxo:

1. **API inicia** → Background task do simulador começa automaticamente
2. **A cada 10 segundos**:
   - Simulador atualiza preços no banco
   - Calcula variações baseadas em volatilidade
   - Envia notificações via WebSocket
3. **Frontend recebe** atualizações em tempo real
4. **API encerra** → Simulador para automaticamente

---

## ⚙️ Configuração

### Alterar Intervalo de Atualização

Edite `main.py` linha 113:

```python
# Aguarda 10 segundos antes da próxima atualização
await asyncio.sleep(10)  # ← Altere aqui (em segundos)
```

### Desativar Simulador Automático

Se quiser que o simulador NÃO inicie automaticamente:

**Opção 1:** Remova estas linhas do `lifespan` em `main.py`:

```python
# Inicia simulador de mercado em background
market_simulator_running = True
market_simulator_task = asyncio.create_task(market_simulator_background())
```

**Opção 2:** Use o endpoint para parar:

```bash
POST http://localhost:8000/api/v1/market/simulator/stop
```

---

## 🔧 Script Standalone (Legado)

O script `scripts/market_simulator.py` ainda existe e pode ser usado separadamente se preferir:

```powershell
# Em uma janela separada
python scripts/market_simulator.py --interval 5
```

**Quando usar o script standalone:**
- ❌ NÃO recomendado - use a versão integrada
- ⚠️ Apenas para testes ou debugging
- ⚠️ Não se comunica bem com a API (pode causar conflitos)

---

## 🐛 Solução de Problemas

### Preços não atualizam?

**Verificar status:**
```bash
GET http://localhost:8000/api/v1/market/simulator/status
```

Se `"running": false`, inicie manualmente:
```bash
POST http://localhost:8000/api/v1/market/simulator/start
```

### WebSocket não conecta?

1. Verifique console do backend - deve mostrar:
   ```
   📈 Simulador de Mercado iniciado (atualiza a cada 10s)
   📊 Mercado atualizado: 10 ativos
   ```

2. Frontend deve mostrar no console:
   ```
   📡 Conectado ao feed de mercado
   ```

### Muitas atualizações?

Aumente o intervalo em `main.py`:
```python
await asyncio.sleep(30)  # 30 segundos em vez de 10
```

---

## 📝 Logs

O simulador exibe logs no console do backend:

```
🚀 Iniciando Digital Superbank API...
✅ Banco de dados principal inicializado
✅ Banco de dados do chatbot inicializado
📈 Simulador de Mercado iniciado (atualiza a cada 10s)
📊 Mercado atualizado: 10 ativos
📊 Mercado atualizado: 10 ativos
...
```

---

## 🎯 Resumo

**ANTES (processo separado):**
```powershell
# Janela 1
python main.py

# Janela 2  
python scripts/market_simulator.py
```

**AGORA (integrado):**
```powershell
# Apenas isto!
python main.py
```

✅ **Muito mais simples!**
🎉 **Tudo gerenciado pela API!**
