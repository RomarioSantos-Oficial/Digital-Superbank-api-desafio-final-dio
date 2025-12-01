"""
Script para criar fundos imobiliários para investimento.
Salva todas as informações em fundo_investimento.txt
"""

import sys
import os
from datetime import datetime
import random
import argparse
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import SessionLocal
from src.models.investment import Asset, AssetType, AssetCategory


def generate_funds():
    """Gera fundos imobiliários."""
    db = SessionLocal()
    
    # Fundos Imobiliários
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
    
    fundos_criados = []
    
    print("=" * 70)
    print("🏢 CRIANDO FUNDOS IMOBILIÁRIOS")
    print("=" * 70 + "\n")
    
    try:
        for i, (symbol, name, desc, price) in enumerate(fundos, 1):
            # Verifica se já existe
            existing = db.query(Asset).filter(Asset.symbol == symbol).first()
            if existing:
                print(f"⚠️  Fundo {i}/{len(fundos)}: {symbol} já existe - pulando")
                continue
            
            # Calcula variação 24h aleatória (fundos são mais estáveis)
            price_change = random.uniform(-2.0, 2.0)
            
            # Volatilidade menor para fundos
            volatility = random.uniform(0.08, 0.15)
            
            # Cria fundo
            fundo = Asset(
                symbol=symbol,
                name=name,
                asset_type=AssetType.FUND,
                category=AssetCategory.FIXED_INCOME,
                current_price=price,
                description=desc
            )
            
            db.add(fundo)
            
            fundos_criados.append({
                'numero': i,
                'symbol': symbol,
                'name': name,
                'description': desc,
                'price': price,
                'volatility': volatility,
                'change': price_change
            })
            
            print(f"✅ Fundo {i}/{len(fundos)}: {symbol} - {name}")
            print(f"   Descrição: {desc}")
            print(f"   Preço: R$ {price:.2f}")
            print(f"   Volatilidade: {volatility * 100:.1f}%")
            print(f"   Variação 24h: {price_change:+.2f}%\n")
        
        # Commit no banco
        db.commit()
        
        # Salva no arquivo fundo_investimento.txt
        arquivo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'demo',
            'fundo_investimento.txt'
        )
        
        # Verifica se arquivo existe e cria backup
        if os.path.exists(arquivo_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = arquivo_path.replace('.txt', f'_backup_{timestamp}.txt')
            shutil.copy2(arquivo_path, backup_path)
            print(f"📦 Backup criado: {backup_path}")
        
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            f.write("═" * 80 + "\n")
            f.write("🏢 DIGITAL SUPERBANK - FUNDOS IMOBILIÁRIOS (FII)\n")
            f.write("═" * 80 + "\n\n")
            f.write(f"Data de Criação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de Fundos: {len(fundos_criados)}\n\n")
            f.write("═" * 80 + "\n\n")
            
            # Agrupa por tipo
            tipos = {
                'Lajes Corporativas': [],
                'Shopping Centers': [],
                'Logísticos': [],
                'Hotéis': [],
                'Educação': [],
                'Residenciais': [],
                'Hospitalares': [],
                'Agências Bancárias': [],
                'Híbridos': []
            }
            
            for fundo in fundos_criados:
                desc = fundo['description'].lower()
                if 'lajes' in desc or 'corporativa' in desc or 'office' in desc or 'escritório' in desc:
                    tipos['Lajes Corporativas'].append(fundo)
                elif 'shopping' in desc or 'mall' in desc or 'varejo' in desc:
                    tipos['Shopping Centers'].append(fundo)
                elif 'logística' in desc or 'galpão' in desc or 'warehouse' in desc:
                    tipos['Logísticos'].append(fundo)
                elif 'hotel' in desc or 'resort' in desc:
                    tipos['Hotéis'].append(fundo)
                elif 'educação' in desc or 'universit' in desc or 'escola' in desc:
                    tipos['Educação'].append(fundo)
                elif 'residencial' in desc or 'apartamento' in desc or 'living' in desc:
                    tipos['Residenciais'].append(fundo)
                elif 'hospital' in desc or 'clínica' in desc or 'medical' in desc:
                    tipos['Hospitalares'].append(fundo)
                elif 'agência' in desc or 'bancária' in desc or 'banking' in desc:
                    tipos['Agências Bancárias'].append(fundo)
                else:
                    tipos['Híbridos'].append(fundo)
            
            for tipo, lista_fundos in tipos.items():
                if not lista_fundos:
                    continue
                    
                f.write(f"🏢 {tipo.upper()}\n")
                f.write("─" * 80 + "\n\n")
                
                for fundo in lista_fundos:
                    f.write(f"💼 {fundo['symbol']} - {fundo['name']}\n")
                    f.write(f"   {fundo['description']}\n")
                    f.write(f"   Preço Atual: R$ {fundo['price']:>10,.2f}\n")
                    f.write(f"   Volatilidade: {fundo['volatility']*100:>8.1f}%\n")
                    f.write(f"   Variação 24h: {fundo['change']:>+8.2f}%\n")
                    f.write("\n")
                
                f.write("\n")
            
            f.write("═" * 80 + "\n")
            f.write("💡 VANTAGENS DOS FUNDOS IMOBILIÁRIOS\n")
            f.write("═" * 80 + "\n\n")
            f.write("• Renda Passiva: Receba dividendos mensais dos aluguéis\n")
            f.write("• Diversificação: Investimento em múltiplos imóveis\n")
            f.write("• Liquidez: Negociação em bolsa de valores\n")
            f.write("• Gestão Profissional: Administrado por especialistas\n")
            f.write("• Menor Volatilidade: Mais estáveis que ações\n")
            f.write("• Isenção de IR: Sobre dividendos para pessoa física\n\n")
            
            f.write("═" * 80 + "\n")
            f.write("📊 ESTATÍSTICAS GERAIS\n")
            f.write("═" * 80 + "\n\n")
            
            preco_medio = sum(f['price'] for f in fundos_criados) / len(fundos_criados)
            vol_media = sum(f['volatility'] for f in fundos_criados) / len(fundos_criados)
            preco_min = min(f['price'] for f in fundos_criados)
            preco_max = max(f['price'] for f in fundos_criados)
            
            f.write(f"Total de Fundos: {len(fundos_criados)}\n")
            f.write(f"Preço Médio: R$ {preco_medio:,.2f}\n")
            f.write(f"Preço Mínimo: R$ {preco_min:,.2f}\n")
            f.write(f"Preço Máximo: R$ {preco_max:,.2f}\n")
            f.write(f"Volatilidade Média: {vol_media*100:.1f}%\n\n")
            
            f.write("═" * 80 + "\n")
            f.write("📋 RESUMO POR TIPO\n")
            f.write("═" * 80 + "\n\n")
            
            for tipo, lista_fundos in tipos.items():
                if not lista_fundos:
                    continue
                preco_medio = sum(f['price'] for f in lista_fundos) / len(lista_fundos)
                f.write(f"{tipo:25} | {len(lista_fundos):2} fundos | ")
                f.write(f"Preço Médio: R$ {preco_medio:8,.2f}\n")
            
            f.write("\n═" * 80 + "\n")
            f.write("✅ TODOS OS FUNDOS FORAM CRIADOS COM SUCESSO!\n")
            f.write("═" * 80 + "\n")
        
        print("═" * 70)
        print(f"✅ {len(fundos_criados)} FUNDOS IMOBILIÁRIOS CRIADOS COM SUCESSO!")
        print(f"✅ Dados salvos em: fundo_investimento.txt")
        print("═" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Gera fundos imobiliários para investimento'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Atualiza arquivo existente (cria backup automático)'
    )
    args = parser.parse_args()
    
    # Verifica se arquivo já existe
    arquivo_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'demo',
        'fundo_investimento.txt'
    )
    
    if os.path.exists(arquivo_path) and not args.update:
        print("="*70)
        print("⚠️  ARQUIVO JÁ EXISTE: fundo_investimento.txt")
        print("="*70)
        print()
        print("Para evitar perda de dados, o arquivo NÃO será sobrescrito.")
        print()
        print("Opções:")
        print("  1. Execute com --update para sobrescrever (backup será criado)")
        print("  2. Renomeie o arquivo atual manualmente")
        print("  3. Delete o arquivo atual se não precisar dele")
        print()
        print("Comando: python generate_funds.py --update")
        print("="*70)
        sys.exit(0)
    
    generate_funds()
