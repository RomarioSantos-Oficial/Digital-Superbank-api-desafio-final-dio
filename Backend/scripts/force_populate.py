"""
Script para forçar a população completa do banco de dados.
Use este script na primeira vez que configurar o sistema.
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import SessionLocal, engine
from src.models.investment import Asset, AssetType, AssetCategory
from src.models.user import User
from src.models.account import Account


def limpar_banco():
    """Remove todos os dados de investimentos."""
    print("=" * 80)
    print("🗑️  LIMPANDO DADOS ANTIGOS")
    print("=" * 80 + "\n")
    
    db = SessionLocal()
    try:
        # Remove ativos
        count_assets = db.query(Asset).delete()
        db.commit()
        print(f"✅ {count_assets} ativos removidos\n")
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao limpar: {e}\n")
    finally:
        db.close()


def criar_acoes():
    """Cria todas as 30 ações."""
    print("=" * 80)
    print("📈 CRIANDO 30 AÇÕES")
    print("=" * 80 + "\n")
    
    db = SessionLocal()
    
    acoes = [
        # Tecnologia (10)
        ("AETH3", "AetherNet Solutions", AssetCategory.TECHNOLOGY, 120.50),
        ("CPYTO", "CryptoNova Tech", AssetCategory.TECHNOLOGY, 85.30),
        ("BLCKCHN", "BlockChain Systems", AssetCategory.TECHNOLOGY, 156.80),
        ("QNTM4", "Quantum Computing SA", AssetCategory.TECHNOLOGY, 210.00),
        ("AIML3", "AI & Machine Learning Corp", AssetCategory.TECHNOLOGY, 178.50),
        ("CYBR4", "CyberSec Defense", AssetCategory.TECHNOLOGY, 92.40),
        ("CLOD3", "CloudNet Brasil", AssetCategory.TECHNOLOGY, 145.20),
        ("SOFT4", "SoftDev Solutions", AssetCategory.TECHNOLOGY, 67.80),
        ("DATA3", "DataAnalytics Pro", AssetCategory.TECHNOLOGY, 134.90),
        ("TECH4", "TechVision International", AssetCategory.TECHNOLOGY, 198.60),
        
        # Energia (7)
        ("SLAR3", "Solar Energy Brasil", AssetCategory.ENERGY, 45.80),
        ("WNDP4", "Wind Power SA", AssetCategory.ENERGY, 52.30),
        ("HYDR3", "Hydro Clean Energy", AssetCategory.ENERGY, 38.90),
        ("NUCL4", "Nuclear Power Tech", AssetCategory.ENERGY, 89.50),
        ("BIOF3", "BioFuel Innovation", AssetCategory.ENERGY, 41.20),
        ("GEOT4", "GeoThermal Systems", AssetCategory.ENERGY, 55.70),
        ("ENRG3", "Energy Renewables", AssetCategory.ENERGY, 73.40),
        
        # Financeiro (6)
        ("BANK4", "SuperBank Digital", AssetCategory.FINANCE, 28.90),
        ("INVE3", "InvestPro Holding", AssetCategory.FINANCE, 34.50),
        ("FINT4", "FinTech Solutions", AssetCategory.FINANCE, 42.80),
        ("CRED3", "CreditFast Brasil", AssetCategory.FINANCE, 31.20),
        ("SEGR4", "Seguros Premium SA", AssetCategory.FINANCE, 48.60),
        ("ASSE3", "Asset Management Corp", AssetCategory.FINANCE, 55.90),
        
        # Saúde (4)
        ("HLTH3", "HealthCare Plus", AssetCategory.HEALTH, 112.40),
        ("PHMA4", "Pharma Solutions", AssetCategory.HEALTH, 95.80),
        ("HOSP3", "Hospital Network SA", AssetCategory.HEALTH, 78.30),
        ("BIOT4", "BioTech Research", AssetCategory.HEALTH, 134.70),
        
        # Outros (3)
        ("RETR3", "Retail Market SA", AssetCategory.RETAIL, 25.60),
        ("AGRO4", "AgroBusiness Brasil", AssetCategory.RETAIL, 38.40),
        ("LOGX3", "Logistics Express", AssetCategory.RETAIL, 44.90),
    ]
    
    criadas = 0
    puladas = 0
    
    try:
        for i, (symbol, name, category, price) in enumerate(acoes, 1):
            # Verifica se já existe
            existing = db.query(Asset).filter(Asset.symbol == symbol).first()
            if existing:
                print(f"⚠️  {i}/30: {symbol} já existe - pulando")
                puladas += 1
                continue
            
            acao = Asset(
                symbol=symbol,
                name=name,
                asset_type=AssetType.STOCK,
                category=category,
                current_price=price,
                description=f"Empresa do setor {category.value} com foco em inovação e crescimento sustentável."
            )
            db.add(acao)
            print(f"✅ {i}/30: {symbol} - {name} (R$ {price:.2f})")
            criadas += 1
        
        db.commit()
        print(f"\n✅ {criadas} ações criadas, {puladas} já existiam\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao criar ações: {e}\n")
        raise
    finally:
        db.close()


def criar_fundos():
    """Cria todos os 25 fundos."""
    print("=" * 80)
    print("🏢 CRIANDO 25 FUNDOS IMOBILIÁRIOS")
    print("=" * 80 + "\n")
    
    db = SessionLocal()
    
    fundos = [
        # Fundos de Lajes Corporativas
        ("CORP11", "Corporate Towers FII", "Lajes Corporativas em São Paulo e Rio", 95.50),
        ("OFFC11", "Office Premium FII", "Edifícios comerciais AAA em capitais", 88.30),
        ("BIZZ11", "Business Center FII", "Centros empresariais modernos", 102.40),
        ("WORK11", "WorkSpace FII", "Coworking e escritórios flexíveis", 76.80),
        
        # Fundos de Shopping Centers
        ("MALL11", "Shopping Brasil FII", "Shopping centers em localizações premium", 112.60),
        ("SHOP11", "Retail Malls FII", "Shoppings regionais e outlets", 98.90),
        ("PLAZ11", "Plaza Shopping FII", "Complexos de varejo e lazer", 105.30),
        
        # Fundos Logísticos
        ("LOGI11", "Logistics Hub FII", "Galpões logísticos estratégicos", 118.70),
        ("WRHZ11", "Warehouse Zone FII", "Centros de distribuição modernos", 124.50),
        ("TRNS11", "Transport Log FII", "Logística e transporte integrado", 110.20),
        ("SUPZ11", "Supply Chain FII", "Cadeia de suprimentos nacional", 115.80),
        
        # Fundos de Hotéis
        ("HTLS11", "Hotels Premium FII", "Rede de hotéis executivos", 85.40),
        ("RSRT11", "Resort & Spa FII", "Resorts de alto padrão", 92.70),
        
        # Fundos de Educação
        ("EDUC11", "Education Real Estate FII", "Campi universitários e escolas", 78.90),
        ("UNIV11", "University Campus FII", "Infraestrutura educacional", 82.50),
        
        # Fundos Residenciais
        ("HOME11", "Residential FII", "Apartamentos para locação", 68.30),
        ("LIVZ11", "Living Spaces FII", "Residências multifamiliares", 72.60),
        ("APTM11", "Apartment Rental FII", "Locação residencial urbana", 65.90),
        
        # Fundos Hospitalares
        ("HOSP11", "Healthcare Real Estate FII", "Hospitais e clínicas premium", 108.40),
        ("MEDI11", "Medical Centers FII", "Centros médicos especializados", 96.80),
        
        # Fundos de Agências Bancárias
        ("BANK11", "Banking Branches FII", "Agências bancárias estratégicas", 52.30),
        ("FINA11", "Financial Centers FII", "Centros financeiros corporativos", 58.70),
        
        # Fundos Híbridos
        ("MIXD11", "Mixed Use FII", "Uso misto: comercial e residencial", 89.50),
        ("URBN11", "Urban Development FII", "Desenvolvimento urbano integrado", 94.20),
        ("CITY11", "Smart City FII", "Cidades inteligentes e sustentáveis", 101.60),
    ]
    
    criados = 0
    pulados = 0
    
    try:
        for i, (symbol, name, desc, price) in enumerate(fundos, 1):
            # Verifica se já existe
            existing = db.query(Asset).filter(Asset.symbol == symbol).first()
            if existing:
                print(f"⚠️  {i}/25: {symbol} já existe - pulando")
                pulados += 1
                continue
            
            fundo = Asset(
                symbol=symbol,
                name=name,
                asset_type=AssetType.FUND,
                category=AssetCategory.FIXED_INCOME,
                current_price=price,
                description=desc
            )
            db.add(fundo)
            print(f"✅ {i}/25: {symbol} - {name} (R$ {price:.2f})")
            criados += 1
        
        db.commit()
        print(f"\n✅ {criados} fundos criados, {pulados} já existiam\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao criar fundos: {e}\n")
        raise
    finally:
        db.close()


def verificar_resultado():
    """Verifica se todos os dados foram criados."""
    print("=" * 80)
    print("🔍 VERIFICANDO RESULTADO")
    print("=" * 80 + "\n")
    
    db = SessionLocal()
    try:
        total_stocks = db.query(Asset).filter(Asset.asset_type == AssetType.STOCK).count()
        total_funds = db.query(Asset).filter(Asset.asset_type == AssetType.FUND).count()
        
        print(f"📊 Ações no banco: {total_stocks}/30")
        print(f"📊 Fundos no banco: {total_funds}/25")
        print()
        
        if total_stocks == 30 and total_funds == 25:
            print("✅ SUCESSO! Todos os investimentos foram criados corretamente!\n")
            return True
        else:
            print("⚠️  ATENÇÃO! Alguns investimentos estão faltando.\n")
            return False
            
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Força a população completa do banco de dados'
    )
    parser.add_argument(
        '--limpar',
        action='store_true',
        help='Remove todos os dados antes de popular (CUIDADO!)'
    )
    args = parser.parse_args()
    
    print("\n")
    print("=" * 80)
    print("🚀 POPULAÇÃO FORÇADA DO BANCO DE DADOS")
    print("=" * 80)
    print()
    print("Este script irá criar TODOS os investimentos no banco de dados.")
    print("Use na primeira execução ou quando precisar repopular o banco.")
    print()
    
    if args.limpar:
        resposta = input("⚠️  Deseja REALMENTE limpar todos os dados? (sim/não): ")
        if resposta.lower() == 'sim':
            limpar_banco()
        else:
            print("❌ Operação cancelada.\n")
            sys.exit(0)
    
    print("Iniciando população...\n")
    
    try:
        criar_acoes()
        criar_fundos()
        
        if verificar_resultado():
            print("=" * 80)
            print("✅ POPULAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 80)
            print()
        else:
            print("=" * 80)
            print("⚠️  POPULAÇÃO PARCIAL - Verifique os erros acima")
            print("=" * 80)
            print()
            sys.exit(1)
            
    except Exception as e:
        print("=" * 80)
        print(f"❌ ERRO DURANTE A POPULAÇÃO: {e}")
        print("=" * 80)
        print()
        sys.exit(1)
