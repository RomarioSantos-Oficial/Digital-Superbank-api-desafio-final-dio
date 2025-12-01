"""
Script de teste para simular instalação do zero.
Remove dados de investimentos e recria.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import SessionLocal
from src.models.investment import Asset

print("\n" + "=" * 80)
print("🧪 TESTE DE INSTALAÇÃO DO ZERO")
print("=" * 80 + "\n")

# 1. Limpar dados de investimentos
print("🗑️  Removendo investimentos existentes...")
db = SessionLocal()
try:
    count = db.query(Asset).delete()
    db.commit()
    print(f"✅ {count} ativos removidos\n")
except Exception as e:
    db.rollback()
    print(f"❌ Erro ao limpar: {e}\n")
    sys.exit(1)
finally:
    db.close()

# 2. Executar generate_stocks.py
print("=" * 80)
print("📈 EXECUTANDO generate_stocks.py")
print("=" * 80 + "\n")

import subprocess
result = subprocess.run(
    [sys.executable, 'scripts/generate_stocks.py'],
    cwd=os.path.dirname(os.path.dirname(__file__)),
    capture_output=True,
    text=True
)

print(result.stdout)
if result.returncode != 0:
    print(f"❌ ERRO:\n{result.stderr}")
    sys.exit(1)

# 3. Executar generate_funds.py
print("\n" + "=" * 80)
print("🏢 EXECUTANDO generate_funds.py")
print("=" * 80 + "\n")

result = subprocess.run(
    [sys.executable, 'scripts/generate_funds.py'],
    cwd=os.path.dirname(os.path.dirname(__file__)),
    capture_output=True,
    text=True
)

print(result.stdout)
if result.returncode != 0:
    print(f"❌ ERRO:\n{result.stderr}")
    sys.exit(1)

# 4. Verificar resultado
print("\n" + "=" * 80)
print("🔍 VERIFICANDO RESULTADO")
print("=" * 80 + "\n")

db = SessionLocal()
try:
    from src.models.investment import AssetType
    
    total_stocks = db.query(Asset).filter(Asset.asset_type == AssetType.STOCK).count()
    total_funds = db.query(Asset).filter(Asset.asset_type == AssetType.FUND).count()
    
    print(f"📊 Ações criadas: {total_stocks}/30")
    print(f"📊 Fundos criados: {total_funds}/25\n")
    
    if total_stocks == 30 and total_funds == 25:
        print("=" * 80)
        print("✅ SUCESSO! Instalação do zero funcionou perfeitamente!")
        print("=" * 80 + "\n")
    else:
        print("=" * 80)
        print("❌ FALHA! Nem todos os investimentos foram criados.")
        print("=" * 80 + "\n")
        sys.exit(1)
        
finally:
    db.close()
