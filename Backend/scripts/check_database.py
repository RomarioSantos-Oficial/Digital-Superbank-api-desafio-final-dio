"""
Script para verificar os dados salvos no banco de dados
"""
from src.database.connection import SessionLocal
from src.models.user import User
from src.models.account import Account
from src.models.investment import Asset, PortfolioItem
from src.models.transaction import Transaction
from src.models.credit_card import CreditCard

def main():
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("      ANÁLISE DO BANCO DE DADOS - DIGITAL SUPERBANK")
        print("=" * 60)
        
        # Contadores
        total_users = db.query(User).count()
        total_accounts = db.query(Account).count()
        total_transactions = db.query(Transaction).count()
        total_assets = db.query(Asset).count()
        total_portfolios = db.query(PortfolioItem).count()
        total_cards = db.query(CreditCard).count()
        
        print(f"\n📊 RESUMO GERAL:")
        print(f"   • Usuários cadastrados:     {total_users}")
        print(f"   • Contas bancárias:         {total_accounts}")
        print(f"   • Transações realizadas:    {total_transactions}")
        print(f"   • Ativos disponíveis:       {total_assets}")
        print(f"   • Portfólios ativos:        {total_portfolios}")
        print(f"   • Cartões de crédito:       {total_cards}")
        
        # Detalhes dos Usuários
        if total_users > 0:
            print(f"\n👥 USUÁRIOS CADASTRADOS (mostrando até 3):")
            for u in db.query(User).limit(3).all():
                print(f"   ID: {u.id:3d} | Nome: {u.full_name:30s} | CPF: {u.cpf}")
        
        # Detalhes das Contas
        if total_accounts > 0:
            print(f"\n💰 CONTAS BANCÁRIAS (mostrando até 5):")
            for a in db.query(Account).limit(5).all():
                print(f"   ID: {a.id:3d} | Nº: {a.account_number:15s} | Tipo: {a.account_type.value:15s} | Saldo: R$ {a.balance:12,.2f}")
        
        # Detalhes dos Ativos
        if total_assets > 0:
            print(f"\n📈 ATIVOS DE INVESTIMENTO (mostrando até 11):")
            for ast in db.query(Asset).all():
                print(f"   ID: {ast.id:2d} | {ast.symbol:6s} - {ast.name:35s} | Preço: R$ {ast.current_price:8.2f} | Tipo: {ast.asset_type.value}")
        
        # Detalhes das Transações
        if total_transactions > 0:
            print(f"\n💸 ÚLTIMAS TRANSAÇÕES (mostrando até 5):")
            for t in db.query(Transaction).order_by(Transaction.created_at.desc()).limit(5).all():
                print(f"   ID: {t.id:3d} | Tipo: {t.transaction_type.value:20s} | Valor: R$ {t.amount:10,.2f} | Status: {t.status.value}")
        
        # Detalhes dos Portfólios
        if total_portfolios > 0:
            print(f"\n🎯 PORTFÓLIOS DE INVESTIMENTO (mostrando até 5):")
            for p in db.query(PortfolioItem).limit(5).all():
                asset = db.query(Asset).filter(Asset.id == p.asset_id).first()
                if asset:
                    current_value = p.quantity * asset.current_price
                    profit_loss = current_value - p.total_invested
                    print(f"   Conta: {p.account_id} | Ativo: {asset.symbol:6s} | Qtd: {p.quantity:8.2f} | Investido: R$ {p.total_invested:10,.2f} | Atual: R$ {current_value:10,.2f} | L/P: R$ {profit_loss:+10,.2f}")
        
        # Detalhes dos Cartões
        if total_cards > 0:
            print(f"\n💳 CARTÕES DE CRÉDITO (mostrando até 5):")
            for c in db.query(CreditCard).limit(5).all():
                print(f"   ID: {c.id:3d} | Nº: {c.card_number[-4:]:>4s} | Categoria: {c.card_category:15s} | Limite: R$ {c.credit_limit:10,.2f} | Status: {c.status}")
        
        print("\n" + "=" * 60)
        print("✅ Análise concluída com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao analisar banco de dados: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
