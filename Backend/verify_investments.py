"""Script para verificar dados de investimentos no banco"""
import sqlite3
import os

# Caminho do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'data', 'digital_superbank.db')

print(f"📂 Verificando banco de dados: {db_path}\n")

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Listar todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("📋 Tabelas disponíveis no banco:")
for table in tables:
    print(f"  • {table[0]}")
print()

# Verificar estrutura da tabela assets
cursor.execute("PRAGMA table_info(assets)")
columns = cursor.fetchall()
print("📋 Estrutura da tabela 'assets':")
for col in columns:
    print(f"  • {col[1]} ({col[2]})")
print()

# Contar ações (asset_type = 'STOCK')
cursor.execute("SELECT COUNT(*) FROM assets WHERE asset_type = 'STOCK'")
total_stocks = cursor.fetchone()[0]

# Contar fundos (asset_type = 'FUND')
cursor.execute("SELECT COUNT(*) FROM assets WHERE asset_type = 'FUND'")
total_funds = cursor.fetchone()[0]

# Contar outros tipos
cursor.execute("SELECT asset_type, COUNT(*) FROM assets GROUP BY asset_type")
types_count = cursor.fetchall()

print("📊 Tipos de ativos encontrados:")
for asset_type, count in types_count:
    print(f"  • {asset_type}: {count}")
print()

# Listar ações
cursor.execute("SELECT symbol, name FROM assets WHERE asset_type = 'STOCK' ORDER BY symbol")
stocks = cursor.fetchall()

# Listar fundos
cursor.execute("SELECT symbol, name FROM assets WHERE asset_type = 'FUND' ORDER BY symbol")
funds = cursor.fetchall()

print("=" * 80)
print("📊 RESUMO DE INVESTIMENTOS")
print("=" * 80)
print(f"\n✅ Total de AÇÕES: {total_stocks} (esperado: 30)")
print(f"✅ Total de FUNDOS: {total_funds} (esperado: 25)")

print("\n" + "=" * 80)
print("📈 AÇÕES CADASTRADAS")
print("=" * 80)
for symbol, name in stocks:
    print(f"  • {symbol:8} - {name}")

print("\n" + "=" * 80)
print("🏢 FUNDOS IMOBILIÁRIOS CADASTRADOS")
print("=" * 80)
for symbol, name in funds:
    print(f"  • {symbol:8} - {name}")

conn.close()

print("\n" + "=" * 80)
print("🔍 CONCLUSÃO")
print("=" * 80)
if total_stocks == 30 and total_funds == 25:
    print("✅ Todos os investimentos estão cadastrados corretamente!")
elif total_stocks == 0 and total_funds == 0:
    print("⚠️  Nenhum investimento cadastrado! Execute os scripts de população.")
else:
    print(f"⚠️  Investimentos parcialmente cadastrados:")
    print(f"    - Faltam {30 - total_stocks} ações")
    print(f"    - Faltam {25 - total_funds} fundos")
print("=" * 80)
