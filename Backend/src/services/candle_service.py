import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.investment import Asset, Candle, CandleInterval, AssetType
import math


class CandleSimulator:
    
    def __init__(self):
        # Volatilidade por tipo de ativo (desvio padrão) - REDUZIDA
        self.volatility = {
            AssetType.STOCK: 0.003,  # 0.3% de volatilidade (0.01% a 1% máximo)
            AssetType.FUND: 0.001    # 0.1% de volatilidade (fundos variam menos)
        }
        
        # Tendência de mercado (-1 a 1)
        # -1 = bear market, 0 = neutro, 1 = bull market
        self.market_trend = 0.1  # Tendência leve
        
        # Volume base por tipo
        self.base_volume = {
            AssetType.STOCK: 50000,
            AssetType.FUND: 10000
        }
    
    def generate_realistic_price_movement(
        self, 
        current_price: float,
        asset_type: AssetType,
        time_elapsed: int = 60  # segundos
    ) -> dict:
        vol = self.volatility.get(asset_type, 0.01)
        
        # Ajusta volatilidade pelo tempo (quanto mais tempo, mais variação)
        time_factor = math.sqrt(time_elapsed / 60)  # normaliza por 1 minuto
        adjusted_vol = vol * time_factor
        
        # Gera movimentos aleatórios com tendência
        # Usa distribuição normal com viés de tendência
        movements = []
        num_ticks = max(10, int(time_elapsed / 6))  # simula ticks
        
        price = current_price
        prices = [price]
        
        for _ in range(num_ticks):
            # Random walk com tendência
            random_factor = random.gauss(0, adjusted_vol)
            trend_factor = self.market_trend * adjusted_vol * 0.1
            
            # Movimento combinado
            movement = random_factor + trend_factor
            price = price * (1 + movement)
            
            # Evita preços negativos
            price = max(price, 0.01)
            prices.append(price)
        
        # Calcula OHLC
        open_price = prices[0]
        close_price = prices[-1]
        high_price = max(prices)
        low_price = min(prices)
        
        # Simula volume realista
        base_vol = self.base_volume.get(asset_type, 10000)
        
        # Volume varia com volatilidade (mais volatilidade = mais volume)
        volatility_factor = abs(close_price - open_price) / open_price
        volume_multiplier = 1 + (volatility_factor * 10)
        
        volume = base_vol * random.uniform(0.5, 1.5) * volume_multiplier
        
        # Número de trades (proporcional ao volume)
        trades_count = int(volume / random.uniform(50, 200))
        
        return {
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': round(volume, 2),
            'trades_count': trades_count,
            'quote_volume': round(volume * close_price, 2)
        }
    
    def create_candle(
        self,
        db: Session,
        asset: Asset,
        interval: CandleInterval = CandleInterval.ONE_MINUTE,
        time_elapsed: int = None
    ) -> Candle:
        now = datetime.utcnow()
        
        # Define tempo baseado no intervalo ou usa fornecido
        if time_elapsed is None:
            interval_seconds = {
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
            time_elapsed = interval_seconds.get(interval, 60)
        
        # Busca última vela para este ativo/intervalo
        last_candle = db.query(Candle).filter(
            Candle.asset_id == asset.id,
            Candle.interval == interval
        ).order_by(Candle.close_time.desc()).first()
        
        # Define open_time e close_time
        if last_candle:
            open_time = last_candle.close_time
        else:
            # Primeira vela - alinha com o intervalo
            open_time = now.replace(second=0, microsecond=0)
        
        close_time = open_time + timedelta(seconds=time_elapsed)
        
        # Gera dados OHLCV realistas
        candle_data = self.generate_realistic_price_movement(
            current_price=asset.current_price,
            asset_type=asset.asset_type,
            time_elapsed=time_elapsed
        )
        
        # Cria vela
        candle = Candle(
            asset_id=asset.id,
            interval=interval,
            open_price=candle_data['open'],
            high_price=candle_data['high'],
            low_price=candle_data['low'],
            close_price=candle_data['close'],
            volume=candle_data['volume'],
            trades_count=candle_data['trades_count'],
            quote_volume=candle_data['quote_volume'],
            open_time=open_time,
            close_time=close_time
        )
        
        # Atualiza preço atual do ativo
        asset.current_price = candle_data['close']
        asset.updated_at = now
        
        db.add(candle)
        db.commit()
        db.refresh(candle)
        
        return candle
    
    def update_market_trend(self):
        # Tendência muda lentamente (mean reversion)
        change = random.gauss(0, 0.05)
        self.market_trend += change
        
        # Limita entre -1 e 1
        self.market_trend = max(-1, min(1, self.market_trend))


# Instância global
candle_simulator = CandleSimulator()


def generate_candles_for_all_stocks(
    db: Session,
    interval: CandleInterval = CandleInterval.ONE_MINUTE,
    time_elapsed: int = 60
):
    # Busca apenas ações (STOCK) - Fundos não variam
    stocks = db.query(Asset).filter(
        Asset.asset_type == AssetType.STOCK,
        Asset.is_active == True
    ).all()
    
    candles = []
    
    for stock in stocks:
        try:
            candle = candle_simulator.create_candle(
                db, stock, interval, time_elapsed
            )
            candles.append(candle)
        except Exception as e:
            print(f"⚠️  Erro ao criar vela para {stock.symbol}: {e}")
    
    # Atualiza tendência de mercado
    candle_simulator.update_market_trend()
    
    return candles


def get_recent_candles(
    db: Session,
    asset_id: int,
    interval: CandleInterval = CandleInterval.ONE_MINUTE,
    limit: int = 100
):
    candles = db.query(Candle).filter(
        Candle.asset_id == asset_id,
        Candle.interval == interval
    ).order_by(Candle.open_time.desc()).limit(limit).all()
    
    return list(reversed(candles))  # Retorna em ordem cronológica


def get_candles_summary(db: Session, asset_id: int, interval: CandleInterval = CandleInterval.ONE_MINUTE):
    candles = get_recent_candles(db, asset_id, interval, limit=24)  # últimas 24 velas
    
    if not candles:
        return None
    
    prices = [c.close_price for c in candles]
    volumes = [c.volume for c in candles]
    
    return {
        'asset_id': asset_id,
        'interval': interval.value,
        'total_candles': len(candles),
        'current_price': candles[-1].close_price,
        'high_24': max(c.high_price for c in candles),
        'low_24': min(c.low_price for c in candles),
        'avg_volume': sum(volumes) / len(volumes),
        'price_change_24h': ((candles[-1].close_price - candles[0].open_price) / candles[0].open_price) * 100,
        'last_update': candles[-1].close_time
    }
