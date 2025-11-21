"""
Script para corrigir dados do usuário - remover cartão duplicado
"""
from src.database.connection import SessionLocal
from src.models.user import User
from src.models.credit_card import CreditCard
from src.models.account import Account

def fix_duplicate_cards():
    db = SessionLocal()
    
    try:
        # Busca usuário Romario
        user = db.query(User).filter(User.full_name.like('%Romario%')).first()
        
        if not user:
            print("❌ Usuário não encontrado")
            return
        
        print(f"\n🔍 Verificando dados do usuário: {user.full_name}")
        print(f"ID: {user.id}")
        
        # Busca todos os cartões do usuário
        cards = db.query(CreditCard).join(Account).filter(
            Account.user_id == user.id
        ).all()
        
        print(f"\n📊 Total de cartões encontrados: {len(cards)}")
        
        if len(cards) <= 1:
            print("✅ Usuário não tem cartões duplicados")
            return
        
        # Lista os cartões
        for i, card in enumerate(cards, 1):
            print(f"\n{i}. Cartão ID: {card.id}")
            print(f"   Número: {card.card_number}")
            print(f"   Conta: {card.account_id}")
            print(f"   Limite: R$ {card.credit_limit}")
            print(f"   Status: {card.status}")
        
        # Remove cartões duplicados (mantém apenas o primeiro)
        print(f"\n🗑️  Removendo {len(cards) - 1} cartão(ões) duplicado(s)...")
        
        for card in cards[1:]:  # Remove todos exceto o primeiro
            db.delete(card)
            print(f"   ❌ Removido cartão ID {card.id} - {card.card_number}")
        
        db.commit()
        print("\n✅ Cartões duplicados removidos com sucesso!")
        
        # Verifica resultado
        remaining_cards = db.query(CreditCard).join(Account).filter(
            Account.user_id == user.id
        ).count()
        
        print(f"\n📊 Cartões restantes: {remaining_cards}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Correção de Dados - Cartões Duplicados")
    print("=" * 60)
    fix_duplicate_cards()
    print("\n" + "=" * 60)
    print("✅ Script concluído!")
    print("=" * 60)
