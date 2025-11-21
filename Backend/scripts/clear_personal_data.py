"""
Script para limpar dados pessoais do banco de dados.
Remove todos os usuários, contas, transações e dados relacionados.
Mantém apenas a estrutura do banco e dados de investimentos.
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import SessionLocal
from src.models.user import User
from src.models.account import Account
from src.models.transaction import Transaction
from src.models.credit_card import CreditCard
from src.models.investment import Asset, PortfolioItem, Candle


def clear_personal_data():
    """Remove todos os dados pessoais do banco."""
    db = SessionLocal()
    
    try:
        print("🗑️  Iniciando limpeza de dados pessoais...\n")
        
        # 1. Limpar investimentos dos usuários
        portfolio_items = db.query(PortfolioItem).count()
        if portfolio_items > 0:
            db.query(PortfolioItem).delete()
            print(f"✅ Removidos {portfolio_items} itens de portfólio")
        
        # 2. Limpar cartões de crédito
        credit_cards = db.query(CreditCard).count()
        if credit_cards > 0:
            db.query(CreditCard).delete()
            print(f"✅ Removidos {credit_cards} cartões de crédito")
        
        # 3. Limpar transações
        transactions = db.query(Transaction).count()
        if transactions > 0:
            db.query(Transaction).delete()
            print(f"✅ Removidas {transactions} transações")
        
        # 4. Limpar contas bancárias
        accounts = db.query(Account).count()
        if accounts > 0:
            db.query(Account).delete()
            print(f"✅ Removidas {accounts} contas bancárias")
        
        # 5. Limpar usuários
        users = db.query(User).count()
        if users > 0:
            db.query(User).delete()
            print(f"✅ Removidos {users} usuários")
        
        # Commit das alterações
        db.commit()
        
        print("\n" + "="*60)
        print("✅ Limpeza de dados pessoais concluída com sucesso!")
        print("="*60)
        print("\n📊 Dados mantidos:")
        
        # Verifica dados que foram mantidos
        assets = db.query(Asset).count()
        print(f"   • {assets} ativos de investimento (ações/fundos)")
        
        candles = db.query(Candle).count()
        print(f"   • {candles} velas (candlesticks)")
        
        print("\n💡 O sistema está pronto para novos usuários!")
        print("   Estrutura do banco: MANTIDA ✓")
        print("   Ativos de investimento: MANTIDOS ✓")
        print("   Velas (candlesticks): MANTIDAS ✓")
        print("   Dados pessoais: REMOVIDOS ✓")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao limpar dados: {str(e)}")
        raise
    finally:
        db.close()


def clear_all_data():
    """Remove TODOS os dados do banco, incluindo investimentos."""
    db = SessionLocal()
    
    try:
        print("⚠️  ATENÇÃO: Limpeza TOTAL do banco de dados...\n")
        
        # Limpar tudo na ordem correta (por causa das foreign keys)
        tables_to_clear = [
            (PortfolioItem, "itens de portfólio"),
            (CreditCard, "cartões de crédito"),
            (Transaction, "transações"),
            (Account, "contas bancárias"),
            (User, "usuários"),
            (Candle, "velas (candlesticks)"),
            (Asset, "ativos de investimento"),
        ]
        
        for model, name in tables_to_clear:
            count = db.query(model).count()
            if count > 0:
                db.query(model).delete()
                print(f"✅ Removidos {count} {name}")
        
        db.commit()
        
        print("\n" + "="*60)
        print("✅ Limpeza TOTAL concluída!")
        print("="*60)
        print("\n⚠️  Banco de dados completamente vazio!")
        print("   Execute os scripts de inicialização:")
        print("   1. python scripts/init_db.py")
        print("   2. python scripts/populate_chatbot.py")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao limpar dados: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🗑️  SCRIPT DE LIMPEZA DE DADOS")
    print("="*60 + "\n")
    
    print("Escolha uma opção:")
    print("1. Limpar apenas dados pessoais (RECOMENDADO)")
    print("   - Remove: usuários, contas, transações, cartões")
    print("   - Mantém: estrutura, ativos, velas\n")
    print("2. Limpar TUDO (incluindo investimentos e velas)")
    print("   - Remove: TUDO do banco de dados")
    print("   - Requer reinicialização completa\n")
    
    choice = input("Digite 1 ou 2: ").strip()
    
    if choice == "1":
        confirm = input("\n⚠️  Confirma limpeza de dados pessoais? (s/N): ").strip().lower()
        if confirm == 's':
            clear_personal_data()
        else:
            print("❌ Operação cancelada.")
    elif choice == "2":
        confirm = input("\n⚠️⚠️⚠️  CONFIRMA LIMPEZA TOTAL DO BANCO? (s/N): ").strip().lower()
        if confirm == 's':
            clear_all_data()
        else:
            print("❌ Operação cancelada.")
    else:
        print("❌ Opção inválida.")
