"""
🎲 SIMULADOR DE MERCADO EM TEMPO REAL
Atualiza preços dos ativos simulando flutuações de mercado
INTEGRADO COM WEBSOCKET para notificações em tempo real
"""
import sys
import time
import random
from datetime import datetime

sys.path.append('.')

from src.database.connection import SessionLocal
from src.models.investment import Asset, MarketHistory, AssetType


# Função para notificar WebSocket (importada dinamicamente)
def notify_websocket(updates):
    """Notifica clientes WebSocket sobre atualizações de preços"""
    try:
        from main import manager
        for update in updates:
            manager.broadcast_sync(update)
    except Exception as e:
        # WebSocket opcional - não bloqueia se houver erro
        pass


class MarketSimulator:
    """Simulador de mercado que atualiza preços em tempo real"""
    
    def __init__(self, update_interval: int = 10):
        """
        Args:
            update_interval: Intervalo em segundos entre atualizações (padrão: 10s)
        """
        self.update_interval = update_interval
        self.db = SessionLocal()
        self.iteration = 0
        
        # Configurações de volatilidade por tipo de ativo
        self.volatility = {
            AssetType.STOCK: 0.02,  # Ações: ±2% por atualização
            AssetType.FUND: 0.005   # Fundos: ±0.5% por atualização
        }
    
    def calculate_price_change(self, asset: Asset) -> tuple[float, float]:
        """
        Calcula nova variação de preço baseada em random walk
        
        Args:
            asset: Ativo a ser atualizado
            
        Returns:
            (novo_preço, variação_percentual)
        """
        # Obtém volatilidade do tipo de ativo
        vol = self.volatility.get(asset.asset_type, 0.01)
        
        # Random walk: movimento aleatório com tendência neutra
        # 60% chance de subir, 40% de cair (leve viés de alta)
        direction = 1 if random.random() < 0.60 else -1
        
        # Magnitude da variação (0 a volatilidade máxima)
        magnitude = random.uniform(0, vol)
        
        # Calcula variação percentual
        change_percent = direction * magnitude
        
        # Aplica ao preço atual
        new_price = asset.current_price * (1 + change_percent)
        
        # Evita preços negativos ou muito baixos
        new_price = max(new_price, 0.01)
        
        return new_price, change_percent * 100  # Retorna % em escala 0-100
    
    def simulate_volume(self, asset: Asset) -> float:
        """
        Simula volume de negociação baseado no tipo de ativo
        
        Args:
            asset: Ativo
            
        Returns:
            Volume simulado
        """
        if asset.asset_type == AssetType.STOCK:
            # Ações: volume entre 1.000 e 100.000
            return random.uniform(1000, 100000)
        else:
            # Fundos: volume menor (100 a 10.000)
            return random.uniform(100, 10000)
    
    def calculate_market_cap(self, asset: Asset, volume: float) -> float:
        """
        Calcula market cap simulado
        
        Args:
            asset: Ativo
            volume: Volume negociado
            
        Returns:
            Market cap simulado
        """
        # Simula número de ações/cotas em circulação
        if asset.asset_type == AssetType.STOCK:
            shares_outstanding = random.uniform(1000000, 10000000)
        else:
            shares_outstanding = random.uniform(100000, 1000000)
        
        return asset.current_price * shares_outstanding
    
    def update_market(self):
        """Atualiza todos os ativos do mercado"""
        try:
            # Busca todos os ativos ativos
            assets = self.db.query(Asset).filter(Asset.is_active == True).all()
            
            if not assets:
                print("⚠️  Nenhum ativo encontrado no banco de dados")
                return
            
            updates_summary = []
            websocket_updates = []  # Para notificar clientes
            
            for asset in assets:
                # Calcula novo preço
                old_price = asset.current_price
                new_price, change_percent = self.calculate_price_change(asset)
                
                # Simula volume e market cap
                volume = self.simulate_volume(asset)
                market_cap = self.calculate_market_cap(asset, volume)
                
                # Atualiza preço do ativo
                asset.current_price = new_price
                asset.updated_at = datetime.utcnow()
                
                # Registra histórico
                history = MarketHistory(
                    asset_id=asset.id,
                    price=new_price,
                    volume=volume,
                    change_percent=change_percent,
                    market_cap=market_cap,
                    timestamp=datetime.utcnow()
                )
                self.db.add(history)
                
                # Adiciona ao resumo
                emoji = "🟢" if change_percent > 0 else "🔴" if change_percent < 0 else "⚪"
                updates_summary.append(
                    f"  {emoji} {asset.symbol:6s} | R$ {old_price:8.2f} → R$ {new_price:8.2f} | "
                    f"{change_percent:+6.2f}% | Vol: {volume:,.0f}"
                )
                
                # Prepara mensagem para WebSocket
                websocket_updates.append({
                    "type": "price_update",
                    "symbol": asset.symbol,
                    "name": asset.name,
                    "price": new_price,
                    "change_percent": change_percent,
                    "volume": volume,
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Commit das mudanças
            self.db.commit()
            
            # Notifica clientes WebSocket conectados
            if websocket_updates:
                notify_websocket(websocket_updates)
            
            # Exibe resumo
            self.iteration += 1
            timestamp = datetime.utcnow().strftime("%H:%M:%S")
            print(f"\n{'='*80}")
            print(f"📊 ATUALIZAÇÃO #{self.iteration} - {timestamp}")
            print(f"{'='*80}")
            for summary in updates_summary:
                print(summary)
            print(f"{'='*80}")
            print(f"✅ {len(assets)} ativos atualizados com sucesso!")
            
        except Exception as e:
            print(f"\n❌ Erro ao atualizar mercado: {e}")
            self.db.rollback()
    
    def run(self):
        """Loop principal do simulador"""
        print("="*80)
        print("🎲 SIMULADOR DE MERCADO EM TEMPO REAL - DIGITAL SUPERBANK")
        print("="*80)
        print(f"⏱️  Intervalo de atualização: {self.update_interval} segundos")
        print(f"📈 Volatilidade das Ações:   ±{self.volatility[AssetType.STOCK]*100:.1f}%")
        print(f"📊 Volatilidade dos Fundos:  ±{self.volatility[AssetType.FUND]*100:.1f}%")
        print("="*80)
        print("⚡ Iniciando simulação... (Ctrl+C para parar)")
        print()
        
        try:
            while True:
                self.update_market()
                
                # Aguarda próxima atualização
                print(f"\n⏳ Próxima atualização em {self.update_interval} segundos...\n")
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("⛔ Simulador interrompido pelo usuário")
            print(f"📊 Total de atualizações: {self.iteration}")
            print("="*80)
        except Exception as e:
            print(f"\n\n❌ Erro fatal no simulador: {e}")
        finally:
            self.db.close()
            print("✅ Conexão com banco de dados fechada")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Simulador de Mercado em Tempo Real",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python scripts/market_simulator.py                    # Atualiza a cada 10 segundos (padrão)
  python scripts/market_simulator.py --interval 5       # Atualiza a cada 5 segundos (mais rápido)
  python scripts/market_simulator.py --interval 30      # Atualiza a cada 30 segundos (mais lento)
  python scripts/market_simulator.py --interval 1       # Atualiza a cada 1 segundo (muito rápido!)
        """
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Intervalo em segundos entre atualizações (padrão: 10)'
    )
    
    args = parser.parse_args()
    
    # Valida intervalo
    if args.interval < 1:
        print("❌ Erro: Intervalo mínimo é 1 segundo")
        return
    
    if args.interval > 300:
        print("⚠️  Aviso: Intervalo muito longo (> 5 minutos)")
    
    # Inicia simulador
    simulator = MarketSimulator(update_interval=args.interval)
    simulator.run()


if __name__ == "__main__":
    main()
