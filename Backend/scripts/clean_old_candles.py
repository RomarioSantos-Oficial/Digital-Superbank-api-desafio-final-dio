"""
Script para limpar velas antigas do banco de dados
Mantém apenas as velas mais recentes de cada intervalo
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from src.database.connection import SessionLocal
from src.models.investment import Candle, CandleInterval

def clean_old_candles():
    """Remove velas antigas, mantendo apenas as mais recentes"""
    db = SessionLocal()
    
    try:
        # Define quantas velas manter para cada intervalo
        keep_limits = {
            CandleInterval.ONE_SECOND: 120,      # 2 minutos
            CandleInterval.FIVE_SECONDS: 120,    # 10 minutos
            CandleInterval.TEN_SECONDS: 120,     # 20 minutos
            CandleInterval.THIRTY_SECONDS: 120,  # 1 hora
            CandleInterval.ONE_MINUTE: 120,      # 2 horas
            CandleInterval.FIVE_MINUTES: 120,    # 10 horas
            CandleInterval.FIFTEEN_MINUTES: 96,  # 1 dia
            CandleInterval.ONE_HOUR: 48,         # 2 dias
            CandleInterval.FOUR_HOURS: 48,       # 8 dias
            CandleInterval.ONE_DAY: 60           # 2 meses
        }
        
        total_deleted = 0
        
        for interval, keep_limit in keep_limits.items():
            # Conta quantas velas existem
            total = db.query(Candle).filter(
                Candle.interval == interval
            ).count()
            
            if total > keep_limit:
                # Busca as velas mais antigas para deletar
                candles_to_delete = db.query(Candle).filter(
                    Candle.interval == interval
                ).order_by(Candle.open_time.asc()).limit(total - keep_limit).all()
                
                for candle in candles_to_delete:
                    db.delete(candle)
                
                deleted = len(candles_to_delete)
                total_deleted += deleted
                
                print(f"✅ {interval.value}: Removidas {deleted} velas antigas (mantidas {keep_limit})")
            else:
                print(f"✓  {interval.value}: {total} velas (dentro do limite)")
        
        db.commit()
        print(f"\n🎯 Total de velas removidas: {total_deleted}")
        print("✅ Limpeza concluída!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🧹 Iniciando limpeza de velas antigas...")
    clean_old_candles()
