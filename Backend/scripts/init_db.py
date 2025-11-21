"""
Script para popular o banco de dados com dados iniciais de teste
"""
import sys
import random
from datetime import date, timedelta

# Adiciona o diretório raiz ao path
sys.path.append('.')

from src.database.connection import SessionLocal, create_tables
from src.models.investment import Asset, AssetType, AssetCategory, MarketHistory


def create_sample_assets():
    """Cria ativos de investimento de exemplo"""
    db = SessionLocal()
    
    try:
        # Verifica se já existem ativos
        existing = db.query(Asset).first()
        if existing:
            print("⚠️  Ativos já existem no banco de dados")
            return
        
        assets = [
            # Ações de Tecnologia
            Asset(
                symbol="NEXG",
                name="NexGen Innovations",
                description="Desenvolvimento de software e IA",
                asset_type=AssetType.STOCK,
                category=AssetCategory.TECHNOLOGY,
                current_price=45.50,
                min_investment=1.0
            ),
            Asset(
                symbol="AETH",
                name="AetherNet Solutions",
                description="Infraestrutura de rede e nuvem",
                asset_type=AssetType.STOCK,
                category=AssetCategory.TECHNOLOGY,
                current_price=72.30,
                min_investment=1.0
            ),
            Asset(
                symbol="QTXD",
                name="Quantex Data",
                description="Análise de dados e big data",
                asset_type=AssetType.STOCK,
                category=AssetCategory.TECHNOLOGY,
                current_price=38.90,
                min_investment=1.0
            ),
            
            # Ações de Varejo
            Asset(
                symbol="URBP",
                name="UrbanPulse Retail",
                description="Grande rede de varejo multicanal",
                asset_type=AssetType.STOCK,
                category=AssetCategory.RETAIL,
                current_price=28.75,
                min_investment=1.0
            ),
            Asset(
                symbol="FLSH",
                name="Flourish Foods",
                description="Indústria alimentícia e bebidas",
                asset_type=AssetType.STOCK,
                category=AssetCategory.RETAIL,
                current_price=52.40,
                min_investment=1.0
            ),
            
            # Ações de Energia
            Asset(
                symbol="TNVM",
                name="TerraNova Mining",
                description="Mineração e recursos naturais",
                asset_type=AssetType.STOCK,
                category=AssetCategory.ENERGY,
                current_price=95.20,
                min_investment=1.0
            ),
            Asset(
                symbol="VLTX",
                name="Voltix Energy",
                description="Energia renovável e sustentabilidade",
                asset_type=AssetType.STOCK,
                category=AssetCategory.ENERGY,
                current_price=68.15,
                min_investment=1.0
            ),
            
            # Ações de Finanças e Saúde
            Asset(
                symbol="INSC",
                name="Insight Capital",
                description="Consultoria financeira e investimentos",
                asset_type=AssetType.STOCK,
                category=AssetCategory.FINANCE,
                current_price=81.30,
                min_investment=1.0
            ),
            Asset(
                symbol="MDCR",
                name="MediCare Solutions",
                description="Saúde e bem-estar",
                asset_type=AssetType.STOCK,
                category=AssetCategory.HEALTH,
                current_price=105.60,
                min_investment=1.0
            ),
            
            # Fundos de Renda Fixa
            Asset(
                symbol="APXRF",
                name="Apex RF Simples",
                description="Fundo de Renda Fixa de baixo risco (LCI/CDB)",
                asset_type=AssetType.FUND,
                category=AssetCategory.FIXED_INCOME,
                current_price=100.00,
                min_investment=100.0
            ),
            Asset(
                symbol="APXRFP",
                name="Apex RF Performance",
                description="Fundo de Renda Fixa com retorno maior (CDB Plus)",
                asset_type=AssetType.FUND,
                category=AssetCategory.FIXED_INCOME,
                current_price=100.00,
                min_investment=500.0
            ),
        ]
        
        for asset in assets:
            db.add(asset)
        
        db.commit()
        print(f"✅ {len(assets)} ativos criados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao criar ativos: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Função principal"""
    print("🚀 Inicializando banco de dados...")
    
    # Cria as tabelas
    create_tables()
    print("✅ Tabelas criadas")
    
    # Popula com ativos de exemplo
    print("\n📈 Criando ativos de investimento...")
    create_sample_assets()
    
    print("\n✨ Inicialização concluída!")
    print("\n📝 Próximos passos:")
    print("1. Execute: python main.py")
    print("2. Acesse: http://localhost:8000/docs")
    print("3. Registre um usuário em /api/v1/auth/register")
    print("4. Faça login em /api/v1/auth/login")


if __name__ == "__main__":
    main()
