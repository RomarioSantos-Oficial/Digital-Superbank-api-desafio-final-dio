"""
Script para popular banco de dados com velas históricas
Gera velas dos últimos 7 dias para todos os ativos
"""
import sys
sys.path.append('.')

from datetime import datetime, timedelta
from src.database.connection import SessionLocal
from src.models.investment import Asset, AssetType, CandleInterval
from src.services.candle_service import candle_simulator, Candle


def generate_historical_candles(days=7):
    """
    Gera velas históricas para os últimos N dias
    
    Args:
        days: Número de dias de histórico
    """
    db = SessionLocal()
    
    try:
        # Busca todas as ações ativas
        stocks = db.query(Asset).filter(
            Asset.asset_type == AssetType.STOCK,
            Asset.is_active == True
        ).all()
        
        print(f"📊 Gerando velas históricas para {len(stocks)} ações...")
        print(f"📅 Período: últimos {days} dias")
        print(f"⏱️  Intervalo: 1 minuto")
        print("="*80)
        
        total_candles = 0
        
        for stock in stocks:
            print(f"\n🔹 {stock.symbol} - {stock.name}")
            
            # Gera velas para os últimos N dias
            # 1 dia = 1440 minutos (24h * 60min)
            # Vamos simular horário comercial: 9h às 18h = 9 horas = 540 minutos/dia
            minutes_per_day = 540  # 9 horas de pregão
            total_minutes = days * minutes_per_day
            
            now = datetime.utcnow()
            current_price = stock.current_price
            candles_created = 0
            
            # Gera velas retroativas
            for i in range(total_minutes):
                # Tempo da vela (de trás para frente)
                candle_time = now - timedelta(minutes=total_minutes - i)
                
                # Pula fins de semana (sábado = 5, domingo = 6)
                if candle_time.weekday() >= 5:
                    continue
                
                # Pula fora do horário comercial (9h às 18h)
                if candle_time.hour < 9 or candle_time.hour >= 18:
                    continue
                
                # Gera dados OHLCV realistas
                candle_data = candle_simulator.generate_realistic_price_movement(
                    current_price=current_price,
                    asset_type=stock.asset_type,
                    time_elapsed=60  # 1 minuto
                )
                
                # Cria vela
                open_time = candle_time.replace(second=0, microsecond=0)
                close_time = open_time + timedelta(minutes=1)
                
                candle = Candle(
                    asset_id=stock.id,
                    interval=CandleInterval.ONE_MINUTE,
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
                
                db.add(candle)
                
                # Atualiza preço para próxima vela
                current_price = candle_data['close']
                candles_created += 1
                
                # Commit a cada 100 velas para não sobrecarregar
                if candles_created % 100 == 0:
                    db.commit()
                    print(f"  ✅ {candles_created} velas criadas...")
            
            # Commit final
            db.commit()
            
            # Atualiza preço atual do ativo
            stock.current_price = current_price
            db.commit()
            
            total_candles += candles_created
            print(f"  ✅ Total: {candles_created} velas | Preço final: R$ {current_price:.2f}")
        
        print("\n" + "="*80)
        print(f"✅ CONCLUÍDO!")
        print(f"📊 Total de velas criadas: {total_candles:,}")
        print(f"📈 Ações processadas: {len(stocks)}")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Gera velas históricas para análise técnica"
    )
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Número de dias de histórico (padrão: 7)'
    )
    
    args = parser.parse_args()
    
    print("🎲 GERADOR DE VELAS HISTÓRICAS")
    print("="*80)
    generate_historical_candles(days=args.days)
