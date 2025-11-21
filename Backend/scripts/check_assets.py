"""
Script para verificar ativos no banco de dados
"""
from src.database.connection import SessionLocal
from src.models.investment import Asset

db = SessionLocal()

assets = db.query(Asset).filter(Asset.is_active == True).all()
stocks = [a for a in assets if a.asset_type.value == "STOCK"]
funds = [a for a in assets if a.asset_type.value == "FUND"]

print(f"\n📊 ATIVOS NO BANCO DE DADOS")
print("="*70)
print(f"Total ativos ativos: {len(assets)}")
print(f"Ações (STOCK): {len(stocks)}")
print(f"Fundos (FUND): {len(funds)}")
print("="*70)

print(f"\n📈 AÇÕES:")
for stock in stocks[:5]:
    print(f"  {stock.symbol:10s} - {stock.name}")

print(f"\n💰 FUNDOS:")
for fund in funds[:5]:
    print(f"  {fund.symbol:10s} - {fund.name}")

db.close()
