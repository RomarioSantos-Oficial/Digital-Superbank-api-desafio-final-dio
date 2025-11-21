# 🔧 Scripts - Digital Superbank

Esta pasta contém scripts utilitários para gerenciar e operar a aplicação.

## 📋 Scripts Disponíveis

### `init_db.py`
**Inicialização do banco de dados**

Cria as tabelas e popula o banco com dados iniciais:
- 📈 **11 ativos de investimento** (9 ações + 2 fundos)
- 💼 Categorias: Tecnologia, Varejo, Energia, Finanças, Saúde
- 💰 Preços variados e realistas

**Como executar:**
```bash
python scripts/init_db.py
```

**Ativos criados:**

| Símbolo | Nome | Tipo | Categoria | Preço |
|---------|------|------|-----------|-------|
| NEXG | NexGen Innovations | Ação | Tecnologia | R$ 45,50 |
| AETH | AetherNet Solutions | Ação | Tecnologia | R$ 72,30 |
| QTXD | Quantex Data | Ação | Tecnologia | R$ 38,90 |
| URBP | UrbanPulse Retail | Ação | Varejo | R$ 28,75 |
| FLSH | Flourish Foods | Ação | Varejo | R$ 52,40 |
| TNVM | TerraNova Mining | Ação | Energia | R$ 95,20 |
| VLTX | Voltix Energy | Ação | Energia | R$ 68,15 |
| INSC | Insight Capital | Ação | Finanças | R$ 81,30 |
| MDCR | MediCare Solutions | Ação | Saúde | R$ 105,60 |
| APXRF | Apex RF Simples | Fundo | Renda Fixa | R$ 100,00 |
| APXRFP | Apex RF Performance | Fundo | Renda Fixa | R$ 100,00 |

---

### `market_simulator.py`
**Simulador de mercado em tempo real**

Atualiza preços dos ativos simulando flutuações de mercado:
- ⏱️ Atualização configurável (padrão: 10 segundos)
- 📊 Volatilidade realista (Ações ±2%, Fundos ±0.5%)
- 💾 Salva histórico no banco de dados
- 🔌 **INTEGRADO com WebSocket** - notifica clientes em tempo real

**Como executar:**
```bash
# Intervalo padrão (10 segundos)
python scripts/market_simulator.py

# Intervalo personalizado
python scripts/market_simulator.py --interval 5   # Mais rápido
python scripts/market_simulator.py --interval 30  # Mais lento
python scripts/market_simulator.py --interval 1   # Muito rápido!
```

**Características:**
- ✅ Random walk com viés de alta (60% up / 40% down)
- ✅ Volume de negociação simulado
- ✅ Market cap calculado
- ✅ Preços salvos no banco (tabela `market_history`)
- ✅ **Notificações WebSocket automáticas** para clientes conectados

**Output esperado:**
```
================================================================================
📊 ATUALIZAÇÃO #1 - 21:30:15
================================================================================
  🟢 NEXG   | R$    45.50 → R$    45.82 | +0.70% | Vol: 45,230
  🔴 AETH   | R$    72.30 → R$    71.98 | -0.44% | Vol: 78,912
  🟢 QTXD   | R$    38.90 → R$    39.15 | +0.64% | Vol: 32,145
================================================================================
✅ 11 ativos atualizados com sucesso!
```

**Integração com WebSocket:**
Quando o simulador atualiza os preços:
1. 💾 Salva no banco de dados
2. 📡 Notifica o WebSocket manager
3. 🔥 Clientes conectados recebem instantaneamente

---

### `check_database.py`
**Verificação do banco de dados**

Analisa e exibe informações sobre o estado do banco:
- 📊 Estatísticas de ativos
- 📈 Histórico de preços
- 💰 Contas criadas
- 👥 Usuários registrados

**Como executar:**
```bash
python scripts/check_database.py
```

**Informações exibidas:**
- Total de ativos por tipo e categoria
- Faixa de preços (mínimo/máximo)
- Pontos de histórico salvos
- Data da última atualização
- Estatísticas de contas e usuários

---

## 🚀 Fluxo de Trabalho Recomendado

### 1️⃣ **Primeira Vez (Setup Inicial)**
```bash
# Cria banco e popula com ativos
python scripts/init_db.py
```

### 2️⃣ **Iniciar Aplicação**
```bash
# Terminal 1: API
uvicorn main:app --reload

# Terminal 2: Simulador de Mercado
python scripts/market_simulator.py --interval 5
```

### 3️⃣ **Verificar Estado**
```bash
# Analisar banco de dados
python scripts/check_database.py
```

---

## 📊 Arquitetura do Simulador

```
┌─────────────────────┐
│ market_simulator.py │  (Processo separado)
└──────────┬──────────┘
           │
           │ 1. Atualiza banco de dados (SQLite)
           │ 2. Notifica WebSocket manager
           ▼
┌─────────────────────┐
│   main.py (API)     │
│  ┌───────────────┐  │
│  │ WebSocket     │  │
│  │ Manager       │  │
│  └───────┬───────┘  │
└──────────┼──────────┘
           │
           │ 3. Broadcast para clientes
           ▼
    ┌──────────────┐
    │ Clientes WS  │  Recebem atualização INSTANTÂNEA
    └──────────────┘
```

---

## 🔧 Configurações

### Volatilidade (market_simulator.py)
```python
self.volatility = {
    AssetType.STOCK: 0.02,  # Ações: ±2%
    AssetType.FUND: 0.005   # Fundos: ±0.5%
}
```

### Intervalo de Atualização
```bash
--interval <segundos>  # Min: 1, recomendado: 5-10
```

---

## 📝 Notas Importantes

- ⚠️ O simulador deve rodar em **processo separado** da API
- ✅ É **seguro** rodar 24/7 - não sobrecarrega o banco
- 🔌 WebSocket funciona **com ou sem** o simulador (mas fica mais legal com!)
- 💾 Histórico é mantido indefinidamente (implementar limpeza futura se necessário)
- 🎯 Ideal para **desenvolvimento** e **demonstrações** - não use em produção com dados reais
