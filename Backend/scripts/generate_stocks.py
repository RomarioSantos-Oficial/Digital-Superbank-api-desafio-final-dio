"""
Script para criar 30 ações para investimento.
Salva todas as informações em acao.txt
"""

import sys
import os
from datetime import datetime
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import SessionLocal
from src.models.investment import Asset, AssetType, AssetCategory


def generate_stocks(update_existing: bool = False):
    """Gera 30 ações de empresas."""
    db = SessionLocal()
    
    # 30 empresas brasileiras e internacionais
    acoes = [
        # Tecnologia (10)
        ("AETH3", "AetherNet Solutions", AssetCategory.TECHNOLOGY, 120.50, 0.35),
        ("CPYTO", "CryptoNova Tech", AssetCategory.TECHNOLOGY, 85.30, 0.40),
        ("BLCKCHN", "BlockChain Systems", AssetCategory.TECHNOLOGY, 156.80, 0.38),
        ("QNTM4", "Quantum Computing SA", AssetCategory.TECHNOLOGY, 210.00, 0.42),
        ("AIML3", "AI & Machine Learning Corp", AssetCategory.TECHNOLOGY, 178.50, 0.36),
        ("CYBR4", "CyberSec Defense", AssetCategory.TECHNOLOGY, 92.40, 0.33),
        ("CLOD3", "CloudNet Brasil", AssetCategory.TECHNOLOGY, 145.20, 0.35),
        ("SOFT4", "SoftDev Solutions", AssetCategory.TECHNOLOGY, 67.80, 0.32),
        ("DATA3", "DataAnalytics Pro", AssetCategory.TECHNOLOGY, 134.90, 0.37),
        ("TECH4", "TechVision International", AssetCategory.TECHNOLOGY, 198.60, 0.39),
        
        # Energia (7)
        ("SLAR3", "Solar Energy Brasil", AssetCategory.ENERGY, 45.80, 0.28),
        ("WNDP4", "Wind Power SA", AssetCategory.ENERGY, 52.30, 0.26),
        ("HYDR3", "Hydro Clean Energy", AssetCategory.ENERGY, 38.90, 0.25),
        ("NUCL4", "Nuclear Power Tech", AssetCategory.ENERGY, 89.50, 0.30),
        ("BIOF3", "BioFuel Innovation", AssetCategory.ENERGY, 41.20, 0.27),
        ("GEOT4", "GeoThermal Systems", AssetCategory.ENERGY, 55.70, 0.29),
        ("ENRG3", "Energy Renewables", AssetCategory.ENERGY, 73.40, 0.31),
        
        # Financeiro (6)
        ("BANK4", "SuperBank Digital", AssetCategory.FINANCE, 28.90, 0.22),
        ("INVE3", "InvestPro Holding", AssetCategory.FINANCE, 34.50, 0.24),
        ("FINT4", "FinTech Solutions", AssetCategory.FINANCE, 42.80, 0.26),
        ("CRED3", "CreditFast Brasil", AssetCategory.FINANCE, 31.20, 0.23),
        ("SEGR4", "Seguros Premium SA", AssetCategory.FINANCE, 48.60, 0.25),
        ("ASSE3", "Asset Management Corp", AssetCategory.FINANCE, 55.90, 0.27),
        
        # Saúde (4)
        ("HLTH3", "HealthCare Plus", AssetCategory.HEALTH, 112.40, 0.20),
        ("PHMA4", "Pharma Solutions", AssetCategory.HEALTH, 95.80, 0.22),
        ("HOSP3", "Hospital Network SA", AssetCategory.HEALTH, 78.30, 0.19),
        ("BIOT4", "BioTech Research", AssetCategory.HEALTH, 134.70, 0.24),
        
        # Outros (3)
        ("RETR3", "Retail Market SA", AssetCategory.RETAIL, 25.60, 0.28),
        ("AGRO4", "AgroBusiness Brasil", AssetCategory.RETAIL, 38.40, 0.26),
        ("LOGX3", "Logistics Express", AssetCategory.RETAIL, 44.90, 0.27),
    ]
    
    acoes_criadas = []
    
    print("=" * 70)
    print("📈 CRIANDO 30 AÇÕES PARA INVESTIMENTO")
    print("=" * 70 + "\n")
    
    try:
        for i, (symbol, name, category, price, volatility) in enumerate(acoes, 1):
            # Verifica se já existe
            existing = db.query(Asset).filter(Asset.symbol == symbol).first()
            if existing:
                if update_existing:
                    # Atualiza os campos relevantes
                    existing.name = name
                    existing.current_price = price
                    existing.description = f"Empresa do setor {category.value} com foco em inovação e crescimento sustentável."
                    existing.category = category
                    db.add(existing)
                    print(f"🔄 Ação {i}/30: {symbol} já existe - atualizada")
                else:
                    print(f"⚠️  Ação {i}/30: {symbol} já existe - pulando")
                    continue
            
            # Calcula variação 24h aleatória
            price_change = random.uniform(-5.0, 5.0)
            
            # Cria ação
            acao = Asset(
                symbol=symbol,
                name=name,
                asset_type=AssetType.STOCK,
                category=category,
                current_price=price,
                description=f"Empresa do setor {category.value} com foco em inovação e crescimento sustentável."
            )
            
            db.add(acao)
            
            acoes_criadas.append({
                'numero': i,
                'symbol': symbol,
                'name': name,
                'category': category.value,
                'price': price,
                'volatility': volatility,
                'change': price_change
            })
            
            print(f"✅ Ação {i}/30: {symbol} - {name}")
            print(f"   Categoria: {category.value}")
            print(f"   Preço: R$ {price:.2f}")
            print(f"   Volatilidade: {volatility * 100:.1f}%")
            print(f"   Variação 24h: {price_change:+.2f}%\n")
        
        # Commit no banco
        db.commit()
        
        # Salva no arquivo acao.txt
        arquivo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'acao.txt'
        )
        
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            f.write("═" * 80 + "\n")
            f.write("📈 DIGITAL SUPERBANK - AÇÕES DISPONÍVEIS PARA INVESTIMENTO\n")
            f.write("═" * 80 + "\n\n")
            f.write(f"Data de Criação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de Ações: 30\n\n")
            f.write("═" * 80 + "\n\n")
            
            # Agrupa por categoria
            categorias = {}
            for acao in acoes_criadas:
                cat = acao['category']
                if cat not in categorias:
                    categorias[cat] = []
                categorias[cat].append(acao)
            
            for categoria, lista_acoes in categorias.items():
                f.write(f"📊 {categoria.upper()}\n")
                f.write("─" * 80 + "\n\n")
                
                for acao in lista_acoes:
                    f.write(f"🏢 {acao['symbol']} - {acao['name']}\n")
                    f.write(f"   Preço Atual: R$ {acao['price']:>10,.2f}\n")
                    f.write(f"   Volatilidade: {acao['volatility']*100:>8.1f}%\n")
                    f.write(f"   Variação 24h: {acao['change']:>+8.2f}%\n")
                    f.write("\n")
                
                f.write("\n")
            
            f.write("═" * 80 + "\n")
            f.write("💡 DICAS DE INVESTIMENTO\n")
            f.write("═" * 80 + "\n\n")
            f.write("• Ações de TECNOLOGIA: Maior volatilidade, maior potencial de retorno\n")
            f.write("• Ações de ENERGIA: Volatilidade média, setor em crescimento\n")
            f.write("• Ações FINANCEIRAS: Menor volatilidade, dividendos regulares\n")
            f.write("• Ações de SAÚDE: Estabilidade e crescimento constante\n\n")
            
            f.write("═" * 80 + "\n")
            f.write("📋 RESUMO POR CATEGORIA\n")
            f.write("═" * 80 + "\n\n")
            
            for categoria, lista_acoes in categorias.items():
                preco_medio = sum(a['price'] for a in lista_acoes) / len(lista_acoes)
                vol_media = sum(a['volatility'] for a in lista_acoes) / len(lista_acoes)
                f.write(f"{categoria:15} | {len(lista_acoes):2} ações | ")
                f.write(f"Preço Médio: R$ {preco_medio:8,.2f} | ")
                f.write(f"Volatilidade: {vol_media*100:5.1f}%\n")
            
            f.write("\n═" * 80 + "\n")
            f.write("✅ TODAS AS AÇÕES FORAM CRIADAS COM SUCESSO!\n")
            f.write("═" * 80 + "\n")
        
        print("═" * 70)
        print(f"✅ {len(acoes_criadas)} AÇÕES CRIADAS COM SUCESSO!")
        print(f"✅ Dados salvos em: acao.txt")
        print("═" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Gerar ações de demonstração')
    parser.add_argument('--update', dest='update', action='store_true', help='Atualiza ativos existentes em vez de pular')
    args = parser.parse_args()
    generate_stocks(update_existing=args.update)
