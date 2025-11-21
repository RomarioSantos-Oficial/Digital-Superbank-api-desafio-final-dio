# 📊 Sistema de Velas (Candlesticks) em Tempo Real

## 🎯 Visão Geral

O sistema agora possui **simulação realista de mercado** com dados OHLCV (Open, High, Low, Close, Volume) para análise técnica.

### 🔑 Características Principais

✅ **Apenas AÇÕES variam** - Fundos mantêm valor fixo
✅ **Velas de 1 minuto** - Dados OHLCV completos
✅ **Gráfico interativo** - Visualização em tempo real
✅ **WebSocket** - Atualizações instantâneas
✅ **Histórico** - Últimas 100 velas disponíveis
✅ **Estatísticas** - Máxima/Mínima/Variação 24h

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Background Task (a cada 60 segundos)      │            │
│  │                                             │            │
│  │  1. Gera vela OHLCV para cada AÇÃO         │            │
│  │  2. Usa random walk realista               │            │
│  │  3. Salva no banco (tabela candles)        │            │
│  │  4. Notifica via WebSocket                 │            │
│  └────────────┬───────────────────────────────┘            │
│               │                                             │
│               ▼                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Banco de Dados SQLite                     │            │
│  │                                             │            │
│  │  • assets (ações e fundos)                 │            │
│  │  • candles (OHLCV por minuto)              │            │
│  │  • market_history (histórico)              │            │
│  └────────────┬───────────────────────────────┘            │
│               │                                             │
│               ▼                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  API Endpoints                             │            │
│  │                                             │            │
│  │  GET /candles/{asset_id}                   │            │
│  │  GET /candles/{asset_id}/summary           │            │
│  │  GET /candles/latest                       │            │
│  └────────────┬───────────────────────────────┘            │
│               │                                             │
└───────────────┼─────────────────────────────────────────────┘
                │
                │ WebSocket + REST
                ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  Página Investimentos                      │            │
│  │                                             │            │
│  │  • Ações: Botão "Gráfico" 📊              │            │
│  │  • Fundos: Sem gráfico (valor fixo)       │            │
│  └────────────┬───────────────────────────────┘            │
│               │                                             │
│               ▼                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  CandlestickModal                          │            │
│  │                                             │            │
│  │  • Gráfico interativo (Canvas)             │            │
│  │  • Estatísticas em tempo real              │            │
│  │  • Auto-refresh (60s)                      │            │
│  │  • Tooltip com detalhes OHLCV              │            │
│  └────────────┬───────────────────────────────┘            │
│               │                                             │
│               ▼                                             │
│  ┌────────────────────────────────────────────┐            │
│  │  CandlestickChart (Canvas)                 │            │
│  │                                             │            │
│  │  🟢 Verde: Close ≥ Open (alta)            │            │
│  │  🔴 Vermelho: Close < Open (baixa)        │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Como Usar

### 1. Iniciar o Backend

```powershell
cd Backend
python main.py
```

**O que acontece:**
- ✅ API inicia na porta 8000
- ✅ Simulador de velas inicia automaticamente
- ✅ A cada 60 segundos, gera velas para todas as AÇÕES
- ✅ WebSocket disponível em `ws://localhost:8000/ws/market-feed`

### 2. (Opcional) Gerar Histórico de Velas

Para análise técnica, é bom ter histórico. Execute:

```powershell
cd Backend
python scripts/generate_historical_candles.py --days 7
```

Isso gera velas dos últimos 7 dias (horário comercial 9h-18h).

### 3. Acessar Frontend

Abra o navegador e acesse `http://localhost:5173`

**Navegação:**
1. Faça login
2. Vá em **Investimentos**
3. Na aba **Ações Disponíveis**
4. Clique no botão **📊 Gráfico** de qualquer ação
5. Visualize o gráfico de velas em tempo real!

---

## 📊 Dados das Velas (OHLCV)

Cada vela contém:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `open` | Preço de abertura | 28.50 |
| `high` | Preço máximo | 28.95 |
| `low` | Preço mínimo | 28.30 |
| `close` | Preço de fechamento | 28.72 |
| `volume` | Volume negociado | 75,234 |
| `trades` | Número de negociações | 523 |
| `open_time` | Início da vela | 2025-11-20T14:23:00 |
| `close_time` | Fim da vela | 2025-11-20T14:24:00 |

---

## 🎨 Interface do Gráfico

### Componente CandlestickChart

```jsx
<CandlestickChart
  candles={candles}    // Array de velas
  symbol="PETR4"       // Símbolo do ativo
  width={900}          // Largura do canvas
  height={450}         // Altura do canvas
/>
```

### Recursos:

- ✅ **Velas verdes** (alta): `close >= open`
- ✅ **Velas vermelhas** (baixa): `close < open`
- ✅ **Tooltip interativo** ao passar o mouse
- ✅ **Grid com escala de preços**
- ✅ **Eixo X com horários**
- ✅ **Legenda explicativa**

---

## 🔧 Endpoints da API

### 1. Obter Velas de um Ativo

```http
GET /api/v1/investments/candles/{asset_id}?interval=1m&limit=100
```

**Parâmetros:**
- `asset_id`: ID do ativo
- `interval`: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`
- `limit`: Máximo 500 velas

**Resposta:**
```json
{
  "asset_id": 1,
  "symbol": "PETR4",
  "name": "Petrobras PN",
  "interval": "1m",
  "candles": [
    {
      "open": 28.50,
      "high": 28.95,
      "low": 28.30,
      "close": 28.72,
      "volume": 75234,
      "trades": 523,
      "open_time": "2025-11-20T14:23:00",
      "close_time": "2025-11-20T14:24:00"
    }
  ],
  "total": 100
}
```

### 2. Resumo Estatístico

```http
GET /api/v1/investments/candles/{asset_id}/summary?interval=1m
```

**Resposta:**
```json
{
  "asset_id": 1,
  "symbol": "PETR4",
  "name": "Petrobras PN",
  "interval": "1m",
  "total_candles": 24,
  "current_price": 28.72,
  "high_24": 29.15,
  "low_24": 27.85,
  "avg_volume": 68542.5,
  "price_change_24h": 2.34
}
```

### 3. Últimas Velas de Todos os Ativos

```http
GET /api/v1/investments/candles/latest?interval=1m
```

---

## 📡 WebSocket (Tempo Real)

### Conectar

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market-feed');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

### Mensagem Recebida

```json
{
  "type": "candle_update",
  "symbol": "PETR4",
  "name": "Petrobras PN",
  "candle": {
    "interval": "1m",
    "open": 28.50,
    "high": 28.95,
    "low": 28.30,
    "close": 28.72,
    "volume": 75234,
    "trades": 523,
    "change_percent": 0.77,
    "open_time": "2025-11-20T14:23:00",
    "close_time": "2025-11-20T14:24:00"
  },
  "timestamp": "2025-11-20T14:24:00"
}
```

---

## 🎲 Simulação Realista

### Volatilidade por Tipo

| Tipo | Volatilidade | Descrição |
|------|--------------|-----------|
| **STOCK** (Ações) | ±1.5% | Variação normal de mercado |
| **FUND** (Fundos) | 0% | **Valor fixo, não varia** |

### Algoritmo

1. **Random Walk** com distribuição normal
2. **Tendência de mercado** (-1 a +1)
3. **Volume proporcional** à volatilidade
4. **Horário comercial** (9h-18h em dias úteis)

---

## 📁 Arquivos Criados/Modificados

### Backend

| Arquivo | Descrição |
|---------|-----------|
| `src/models/investment.py` | Modelo `Candle` e `CandleInterval` |
| `src/services/candle_service.py` | Simulador de velas realistas |
| `src/api/v1/endpoints/investments.py` | Endpoints de velas |
| `main.py` | Background task de velas |
| `scripts/generate_historical_candles.py` | Script de histórico |

### Frontend

| Arquivo | Descrição |
|---------|-----------|
| `src/components/investments/CandlestickChart.jsx` | Gráfico Canvas |
| `src/components/investments/CandlestickModal.jsx` | Modal interativo |
| `src/pages/Investments.jsx` | Botão de gráfico (apenas ações) |

---

## 💡 Diferenças: Ações vs Fundos

### ⚡ Ações (STOCK)

- ✅ **Gera velas** a cada 1 minuto
- ✅ **Variação de preço** em tempo real
- ✅ **Botão "Gráfico"** disponível
- ✅ **Dados OHLCV** completos
- ✅ **Análise técnica** possível

### 💰 Fundos (FUND)

- ❌ **Não gera velas**
- ❌ **Preço fixo** (não varia)
- ❌ **Sem botão de gráfico**
- ⚠️ Indicador: "💰 Valor Fixo (não varia)"

---

## 🐛 Troubleshooting

### Gráfico não aparece?

1. Verifique se o backend está rodando
2. Execute o script de histórico:
   ```powershell
   python scripts/generate_historical_candles.py
   ```
3. Aguarde 1 minuto para a primeira vela ser gerada

### WebSocket não conecta?

1. Certifique-se que a API está em `http://localhost:8000`
2. Verifique console do navegador (F12)
3. Teste: `ws://localhost:8000/ws/market-feed`

### Fundos mostram gráfico?

❌ **NÃO!** Apenas ações têm gráfico. Fundos mantêm valor fixo.

---

## 🎯 Próximos Passos (Melhorias Futuras)

- [ ] Indicadores técnicos (médias móveis, RSI, MACD)
- [ ] Múltiplos intervalos (5m, 15m, 1h, 1d)
- [ ] Zoom e pan no gráfico
- [ ] Exportar dados (CSV, JSON)
- [ ] Alertas de preço
- [ ] Volume profile
- [ ] Order book simulado

---

**🎉 Pronto! Agora você tem um sistema completo de análise técnica em tempo real!**
