# 🎯 Simulador de Mercado - Guia Rápido

## ✅ O QUE MUDOU?

**ANTES:** Você precisava rodar 2 processos separados
**AGORA:** Tudo integrado! Apenas rode `python main.py`

---

## 🚀 Como Usar

### Iniciar o Sistema

```powershell
cd Backend
python main.py
```

**O que acontece:**
1. ✅ API inicia na porta 8000
2. ✅ Simulador de mercado inicia automaticamente
3. ✅ Preços começam a atualizar a cada 10 segundos
4. ✅ WebSocket disponível em `ws://localhost:8000/ws/market-feed`

---

## 🎮 Controle via API

### Ver Status do Simulador

```http
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

### Parar o Simulador

```http
POST http://localhost:8000/api/v1/market/simulator/stop
```

**Resposta:**
```json
{
  "status": "stopped",
  "message": "Simulador de mercado parado com sucesso"
}
```

### Iniciar o Simulador (se estiver parado)

```http
POST http://localhost:8000/api/v1/market/simulator/start
```

**Resposta:**
```json
{
  "status": "started",
  "message": "Simulador de mercado iniciado com sucesso"
}
```

---

## 📊 Logs do Console

Quando o simulador está rodando, você verá:

```
🚀 Iniciando Digital Superbank API...
✅ Banco de dados principal inicializado
✅ Banco de dados do chatbot inicializado
📈 Simulador de Mercado iniciado (atualiza a cada 10s)
INFO:     Application startup complete.
📊 Mercado atualizado: 10 ativos
📊 Mercado atualizado: 10 ativos
📊 Mercado atualizado: 10 ativos
...
```

---

## ⚙️ Configuração

### Alterar Intervalo de Atualização

Edite `Backend/main.py` na linha ~113:

```python
# De:
await asyncio.sleep(10)  # 10 segundos

# Para (exemplo - 5 segundos):
await asyncio.sleep(5)  # 5 segundos
```

### Desativar Início Automático

Edite `Backend/main.py` na função `lifespan`, comente estas linhas:

```python
# Inicia simulador de mercado em background
# market_simulator_running = True
# market_simulator_task = asyncio.create_task(market_simulator_background())
```

---

## 🔧 Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/v1/market/simulator/status` | GET | Status do simulador |
| `/api/v1/market/simulator/start` | POST | Inicia simulador |
| `/api/v1/market/simulator/stop` | POST | Para simulador |
| `/ws/market-feed` | WebSocket | Feed de preços em tempo real |

---

## 📡 Como o Frontend Recebe Atualizações?

### 1. WebSocket (Tempo Real)

O frontend conecta em `ws://localhost:8000/ws/market-feed`:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market-feed');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  // update = {
  //   type: "price_update",
  //   symbol: "PETR4",
  //   name: "Petrobras PN",
  //   price: 28.72,
  //   change_percent: 0.77,
  //   timestamp: "2025-11-20T14:23:45.123456"
  // }
};
```

### 2. Polling (Backup)

Se WebSocket falhar, o frontend faz polling a cada 10s:

```javascript
setInterval(() => {
  loadAssets(); // Busca ativos do banco
}, 10000);
```

---

## 🐛 Troubleshooting

### Preços não atualizam?

**1. Verifique o status:**
```bash
curl http://localhost:8000/api/v1/market/simulator/status
```

**2. Se `running: false`, inicie:**
```bash
curl -X POST http://localhost:8000/api/v1/market/simulator/start
```

**3. Verifique logs no console do backend**

### WebSocket não conecta?

**1. Teste no navegador (console):**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market-feed');
ws.onopen = () => console.log('✅ Conectado!');
ws.onerror = (e) => console.log('❌ Erro:', e);
```

**2. Verifique CORS** - deve estar permitido no `main.py`

**3. Certifique-se que a API está rodando** na porta 8000

---

## 📂 Arquivos Importantes

```
Backend/
├── main.py                                    ← Simulador integrado aqui!
├── src/
│   └── services/
│       └── investment_service.py              ← Lógica de simulação
├── scripts/
│   └── market_simulator.py                    ← Script standalone (legado)
└── SIMULADOR_README.md                        ← Este arquivo
```

---

## 🎉 Vantagens da Nova Abordagem

| Antes | Agora |
|-------|-------|
| ❌ 2 processos separados | ✅ 1 único processo |
| ❌ Precisa lembrar de iniciar manualmente | ✅ Inicia automaticamente |
| ❌ Script PowerShell complexo | ✅ Simples `python main.py` |
| ❌ Difícil controlar | ✅ API endpoints para controle |
| ❌ Logs em janelas separadas | ✅ Tudo no mesmo console |

---

## 💡 Dicas

- **Desenvolvimento:** Use intervalo menor (5s) para testar rapidamente
- **Produção:** Use intervalo maior (30s ou 60s) para economizar recursos
- **Debug:** Pare o simulador e rode apenas a API
- **Teste WebSocket:** Use ferramentas como [Postman](https://www.postman.com/) ou [websocat](https://github.com/vi/websocat)

---

## 📞 Suporte

Se tiver problemas:

1. ✅ Verifique logs do console
2. ✅ Teste endpoint `/api/v1/market/simulator/status`
3. ✅ Abra `/docs` no navegador e teste manualmente
4. ✅ Verifique se tem ativos no banco de dados

---

**🎯 Resumo:** Agora é só rodar `python main.py` e tudo funciona! 🚀
