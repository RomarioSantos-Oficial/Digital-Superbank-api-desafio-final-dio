"""
Script para adicionar ativos de renda fixa ao banco de dados
CDB, LCI, LCA, Tesouro Direto, Fundos DI, etc.
"""
from src.database.connection import SessionLocal
from src.models.investment import Asset, AssetType, AssetCategory
from datetime import datetime

def add_fixed_income_assets():
    db = SessionLocal()
    
    try:
        # Lista de ativos de renda fixa para adicionar
        fixed_income_assets = [
            # CDBs
            {
                "symbol": "CDB100",
                "name": "CDB 100% CDI - Banco Digital",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 1000.00,
                "description": "CDB com liquidez diária, rendimento de 100% do CDI"
            },
            {
                "symbol": "CDB120",
                "name": "CDB 120% CDI - 12 meses",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 1000.00,
                "description": "CDB com prazo de 12 meses, rendimento de 120% do CDI"
            },
            {
                "symbol": "CDB135",
                "name": "CDB 135% CDI - 24 meses",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 1000.00,
                "description": "CDB com prazo de 24 meses, rendimento de 135% do CDI"
            },
            
            # LCI/LCA
            {
                "symbol": "LCI110",
                "name": "LCI 110% CDI - Isento IR",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 1000.00,
                "description": "Letra de Crédito Imobiliário, 110% CDI, isento de IR"
            },
            {
                "symbol": "LCA105",
                "name": "LCA 105% CDI - Isento IR",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 1000.00,
                "description": "Letra de Crédito do Agronegócio, 105% CDI, isento de IR"
            },
            
            # Tesouro Direto
            {
                "symbol": "TSELIC",
                "name": "Tesouro Selic 2027",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 10500.00,
                "description": "Título público pós-fixado, acompanha taxa Selic"
            },
            {
                "symbol": "TIPCA",
                "name": "Tesouro IPCA+ 2029",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 3200.00,
                "description": "Título público indexado à inflação + taxa fixa"
            },
            {
                "symbol": "TPREF",
                "name": "Tesouro Prefixado 2028",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 8500.00,
                "description": "Título público com taxa de juros fixa"
            },
            
            # Fundos DI
            {
                "symbol": "FUNDI",
                "name": "Fundo DI Conservador",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 150.00,
                "description": "Fundo de investimento que acompanha 100% do CDI"
            },
            {
                "symbol": "FUNDRF",
                "name": "Fundo Renda Fixa Ativo",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 120.00,
                "description": "Fundo de renda fixa com gestão ativa"
            },
            
            # Fundos Multimercado
            {
                "symbol": "FMULTI",
                "name": "Fundo Multimercado Moderado",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FINANCE,
                "current_price": 200.00,
                "description": "Fundo que investe em diversos mercados"
            },
            {
                "symbol": "FMACRO",
                "name": "Fundo Macro Estratégia",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FINANCE,
                "current_price": 180.00,
                "description": "Fundo multimercado com foco em cenários macroeconômicos"
            },
            
            # Fundos Imobiliários
            {
                "symbol": "FII01",
                "name": "FII Escritórios Premium",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FINANCE,
                "current_price": 95.00,
                "description": "Fundo de investimento em lajes corporativas"
            },
            {
                "symbol": "FII02",
                "name": "FII Shopping Centers",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FINANCE,
                "current_price": 110.00,
                "description": "Fundo de investimento em shopping centers"
            },
            {
                "symbol": "FII03",
                "name": "FII Logística",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FINANCE,
                "current_price": 105.00,
                "description": "Fundo de investimento em galpões logísticos"
            },
            
            # Debêntures
            {
                "symbol": "DEB01",
                "name": "Debênture Infraestrutura",
                "asset_type": AssetType.FUND,
                "category": AssetCategory.FIXED_INCOME,
                "current_price": 1050.00,
                "description": "Debênture incentivada, isenta de IR"
            },
        ]
        
        print("\n" + "="*70)
        print("📊 ADICIONANDO ATIVOS DE RENDA FIXA")
        print("="*70 + "\n")
        
        added_count = 0
        skipped_count = 0
        
        for asset_data in fixed_income_assets:
            # Verifica se já existe
            existing = db.query(Asset).filter(
                Asset.symbol == asset_data["symbol"]
            ).first()
            
            if existing:
                print(f"⏭️  {asset_data['symbol']:8s} - Já existe, pulando...")
                skipped_count += 1
                continue
            
            # Cria novo ativo
            asset = Asset(
                symbol=asset_data["symbol"],
                name=asset_data["name"],
                asset_type=asset_data["asset_type"],
                category=asset_data["category"],
                current_price=asset_data["current_price"],
                description=asset_data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(asset)
            print(f"✅ {asset_data['symbol']:8s} - {asset_data['name']}")
            added_count += 1
        
        # Commit
        db.commit()
        
        print("\n" + "="*70)
        print(f"✅ Adicionados: {added_count}")
        print(f"⏭️  Pulados: {skipped_count}")
        print(f"📊 Total: {added_count + skipped_count}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_fixed_income_assets()
