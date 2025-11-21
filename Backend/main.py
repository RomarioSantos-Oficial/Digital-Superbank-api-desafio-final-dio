"""
Digital Superbank API
API bancária completa com FastAPI
"""
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
from typing import List
from datetime import datetime

from src.configs.settings import settings
from src.database.connection import create_tables, SessionLocal
from src.database.chatbot_connection import create_chatbot_tables
from src.api.v1.router import api_router
from src.models.investment import Asset, CandleInterval
from src.services import investment_service
from src.services.candle_service import generate_candles_for_all_stocks
import random


class ConnectionManager:
    """Gerenciador de conexões WebSocket"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Aceita nova conexão"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 Nova conexão WebSocket. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove conexão"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"📡 Conexão encerrada. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Envia mensagem para todos os clientes conectados"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # Remove conexões inativas
        for conn in disconnected:
            self.active_connections.remove(conn)
    
    def broadcast_sync(self, message: dict):
        """Versão síncrona do broadcast (para uso do simulador)"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.broadcast(message))
            else:
                loop.run_until_complete(self.broadcast(message))
        except Exception as e:
            print(f"⚠️  Erro ao enviar broadcast: {e}")


manager = ConnectionManager()

# Controle do simulador de mercado
market_simulator_task = None
market_simulator_running = False


async def market_simulator_background():
    """
    Simulador de mercado com sistema de VELAS (Candlesticks)
    Gera dados OHLCV realistas a cada 1 SEGUNDO para análise técnica
    Variação: 0.01% a 1% máximo
    """
    global market_simulator_running
    
    print("📈 Simulador de Velas (Candlesticks) iniciado")
    print("⏱️  Intervalo: 1 SEGUNDO | Dados: OHLCV (Open/High/Low/Close/Volume)")
    print("📊 Variação: 0.01% a 1% por movimento")
    
    # Contadores para cada intervalo
    interval_counters = {
        CandleInterval.ONE_SECOND: 0,
        CandleInterval.FIVE_SECONDS: 0,
        CandleInterval.TEN_SECONDS: 0,
        CandleInterval.THIRTY_SECONDS: 0,
        CandleInterval.ONE_MINUTE: 0,
        CandleInterval.FIVE_MINUTES: 0,
        CandleInterval.FIFTEEN_MINUTES: 0,
        CandleInterval.ONE_HOUR: 0,
        CandleInterval.FOUR_HOURS: 0,
        CandleInterval.ONE_DAY: 0
    }
    
    # Tempo necessário para cada intervalo (em segundos)
    interval_times = {
        CandleInterval.ONE_SECOND: 1,
        CandleInterval.FIVE_SECONDS: 5,
        CandleInterval.TEN_SECONDS: 10,
        CandleInterval.THIRTY_SECONDS: 30,
        CandleInterval.ONE_MINUTE: 60,
        CandleInterval.FIVE_MINUTES: 300,
        CandleInterval.FIFTEEN_MINUTES: 900,
        CandleInterval.ONE_HOUR: 3600,
        CandleInterval.FOUR_HOURS: 14400,
        CandleInterval.ONE_DAY: 86400
    }
    
    while market_simulator_running:
        try:
            db = SessionLocal()
            
            all_candles = []
            
            # Para cada intervalo, verifica se chegou a hora de criar vela
            for interval, required_time in interval_times.items():
                interval_counters[interval] += 1
                
                # Se atingiu o tempo necessário, cria a vela
                if interval_counters[interval] >= required_time:
                    print(f"⏰ Criando vela de {interval.value} após {interval_counters[interval]} segundos")
                    candles = generate_candles_for_all_stocks(
                        db, 
                        interval=interval,
                        time_elapsed=required_time
                    )
                    all_candles.extend(candles)
                    interval_counters[interval] = 0  # Reset contador
            
            # Envia atualizações via WebSocket
            for candle in all_candles:
                asset = db.query(Asset).filter(Asset.id == candle.asset_id).first()
                
                if asset:
                    # Calcula variação percentual
                    change_percent = ((candle.close_price - candle.open_price) / 
                                     candle.open_price) * 100
                    
                    await manager.broadcast({
                        "type": "candle_update",
                        "symbol": asset.symbol,
                        "name": asset.name,
                        "candle": {
                            "interval": candle.interval.value,
                            "open": candle.open_price,
                            "high": candle.high_price,
                            "low": candle.low_price,
                            "close": candle.close_price,
                            "volume": candle.volume,
                            "trades": candle.trades_count,
                            "change_percent": round(change_percent, 2),
                            "open_time": candle.open_time.isoformat(),
                            "close_time": candle.close_time.isoformat()
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    })
            
            db.close()
            
            # Log resumido a cada 10 velas
            if candles and len(candles) % 10 == 0:
                print(f"📊 {len(candles)} velas geradas | "
                      f"Última: {candles[-1].close_price:.2f}")
            
        except Exception as e:
            print(f"⚠️  Erro no simulador: {e}")
            import traceback
            traceback.print_exc()
        
        # Aguarda 1 SEGUNDO (velas em tempo real)
        await asyncio.sleep(1)
    
    print("📉 Simulador de Velas parado")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de inicialização e finalização"""
    global market_simulator_task, market_simulator_running
    
    # Startup
    print("🚀 Iniciando Digital Superbank API...")
    create_tables()
    print("✅ Banco de dados principal inicializado")
    create_chatbot_tables()
    print("✅ Banco de dados do chatbot inicializado")
    
    # Inicia simulador de mercado em background
    market_simulator_running = True
    market_simulator_task = asyncio.create_task(market_simulator_background())
    
    yield
    
    # Shutdown
    print("👋 Encerrando Digital Superbank API...")
    market_simulator_running = False
    if market_simulator_task:
        market_simulator_task.cancel()
        try:
            await market_simulator_task
        except asyncio.CancelledError:
            pass


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API bancária completa com contas, transações, cartões e investimentos",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global para exceções"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor",
            "error": str(exc) if settings.DEBUG else "Erro interno"
        }
    )


# Incluir rotas da API
app.include_router(api_router, prefix="/api/v1")


# Endpoints de controle do simulador de mercado
@app.post("/api/v1/market/simulator/start")
async def start_market_simulator():
    """Inicia o simulador de mercado"""
    global market_simulator_task, market_simulator_running
    
    if market_simulator_running:
        return {
            "status": "already_running",
            "message": "Simulador já está em execução"
        }
    
    market_simulator_running = True
    market_simulator_task = asyncio.create_task(market_simulator_background())
    
    return {
        "status": "started",
        "message": "Simulador de mercado iniciado com sucesso"
    }


@app.post("/api/v1/market/simulator/stop")
async def stop_market_simulator():
    """Para o simulador de mercado"""
    global market_simulator_task, market_simulator_running
    
    if not market_simulator_running:
        return {
            "status": "not_running",
            "message": "Simulador não está em execução"
        }
    
    market_simulator_running = False
    if market_simulator_task:
        market_simulator_task.cancel()
        try:
            await market_simulator_task
        except asyncio.CancelledError:
            pass
    
    return {
        "status": "stopped",
        "message": "Simulador de mercado parado com sucesso"
    }


@app.get("/api/v1/market/simulator/status")
async def get_simulator_status():
    """Obtém status do simulador de mercado"""
    return {
        "running": market_simulator_running,
        "websocket_connections": len(manager.active_connections),
        "update_interval": 10  # segundos
    }


# Rota de health check
@app.get("/")
async def root():
    """Rota raiz - Health check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "bank_code": settings.BANK_CODE,
        "bank_name": settings.BANK_NAME
    }


@app.get("/health")
async def health_check():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "database": "connected",
        "api_version": settings.APP_VERSION
    }


@app.websocket("/ws/market-feed")
async def websocket_market_feed(websocket: WebSocket):
    """
    WebSocket para streaming de preços em tempo real
    
    Conecta e recebe atualizações de preços automaticamente:
    {
        "type": "price_update",
        "symbol": "NEXG",
        "name": "NexGen Innovations",
        "price": 45.75,
        "change_percent": 0.5,
        "volume": 85000,
        "timestamp": "2025-11-20T21:00:00"
    }
    """
    await manager.connect(websocket)
    
    try:
        # Envia dados iniciais
        db = SessionLocal()
        assets = db.query(Asset).filter(Asset.is_active == True).all()
        
        await websocket.send_json({
            "type": "connected",
            "message": "Conectado ao feed de mercado",
            "assets_count": len(assets)
        })
        
        # Mantém conexão e aguarda mensagens (opcional)
        while True:
            try:
                # Cliente pode enviar mensagens (ex: subscribir símbolos específicos)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                # Aqui você pode processar comandos do cliente
            except asyncio.TimeoutError:
                # Envia update periódico
                assets = db.query(Asset).filter(Asset.is_active == True).all()
                for asset in assets:
                    await websocket.send_json({
                        "type": "price_update",
                        "symbol": asset.symbol,
                        "name": asset.name,
                        "price": asset.current_price,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                await asyncio.sleep(2)  # Atualiza a cada 2 segundos
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"❌ Erro no WebSocket: {e}")
        manager.disconnect(websocket)
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
