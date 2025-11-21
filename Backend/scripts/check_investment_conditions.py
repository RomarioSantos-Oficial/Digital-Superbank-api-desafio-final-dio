"""
Verifica condições para criar conta de investimento
"""
from src.database.connection import SessionLocal
from src.models.user import User
from src.models.account import Account
from datetime import date

db = SessionLocal()

user = db.query(User).filter(User.full_name.like('%Romario%')).first()

print(f"\n{'='*60}")
print(f"ANÁLISE - CONTA INVESTIMENTO")
print(f"{'='*60}\n")

print(f"👤 Usuário: {user.full_name}")
age = (date.today() - user.birth_date).days // 365
print(f"🎂 Idade: {age} anos")

accounts = db.query(Account).filter(Account.user_id == user.id).all()

print(f"\n📊 Contas existentes ({len(accounts)}):")
for acc in accounts:
    print(f"  ✓ {acc.account_type.name}")

print(f"\n🔍 Verificação de Requisitos:")
print(f"  {'✅' if age >= 18 else '❌'} Idade mínima (18+): {age} anos")

has_corrente = any(a.account_type.name == "CORRENTE" for a in accounts)
print(f"  {'✅' if has_corrente else '❌'} Possui Conta Corrente: {'Sim' if has_corrente else 'Não'}")

has_investimento = any(a.account_type.name == "INVESTIMENTO" for a in accounts)
print(f"  {'✅' if not has_investimento else '❌'} Não possui Investimento: {'Sim (pode criar)' if not has_investimento else 'Não (já existe)'}")

can_create = age >= 18 and has_corrente and not has_investimento

print(f"\n{'='*60}")
if can_create:
    print("✅ PODE CRIAR CONTA INVESTIMENTO!")
else:
    print("❌ NÃO PODE CRIAR - Requisitos não atendidos")
print(f"{'='*60}\n")

db.close()
