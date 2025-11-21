"""
Investment Service
Gerencia ativos de investimento e portfólio
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.models.investment import Asset, AssetType, AssetCategory, PortfolioItem
from src.models.account import Account, AccountType
from src.models.transaction import Transaction, TransactionType, TransactionStatus
import random


def get_all_assets(
    db: Session,
    asset_type: Optional[AssetType] = None,
    category: Optional[AssetCategory] = None,
    active_only: bool = True
) -> List[Asset]:
    """
    Listar todos os ativos disponíveis
    Filtros opcionais: tipo, categoria, apenas ativos
    """
    query = db.query(Asset)
    
    if active_only:
        query = query.filter(Asset.is_active == True)
    
    if asset_type:
        query = query.filter(Asset.asset_type == asset_type)
    
    if category:
        query = query.filter(Asset.category == category)
    
    return query.order_by(Asset.name).all()


def get_asset_by_id(db: Session, asset_id: int) -> Optional[Asset]:
    """Buscar ativo por ID"""
    return db.query(Asset).filter(Asset.id == asset_id).first()


def buy_asset(
    db: Session,
    account_id: int,
    asset_id: int,
    quantity: int
) -> tuple[PortfolioItem, Transaction]:
    """
    Comprar ativo
    Retorna: (item_portfólio, transação)
    """
    if quantity <= 0:
        raise ValueError("Quantidade deve ser positiva")
    
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Verifica se é conta de investimento
    if account.account_type != AccountType.INVESTIMENTO:
        raise ValueError(
            "Apenas contas de investimento podem comprar ativos"
        )
    
    # Busca ativo
    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise ValueError("Ativo não encontrado")
    
    if not asset.is_active:
        raise ValueError("Ativo não está disponível para negociação")
    
    # Calcula valor total
    total_cost = asset.current_price * quantity
    
    # Verifica saldo
    if account.balance < total_cost:
        raise ValueError(
            f"Saldo insuficiente. Necessário: R$ {total_cost}, "
            f"Disponível: R$ {account.balance}"
        )
    
    # Busca ou cria item no portfólio
    portfolio_item = db.query(PortfolioItem).filter(
        and_(
            PortfolioItem.account_id == account_id,
            PortfolioItem.asset_id == asset_id
        )
    ).first()
    
    if portfolio_item:
        # Atualiza quantidade e preço médio
        total_quantity = portfolio_item.quantity + quantity
        total_invested_value = (
            portfolio_item.average_price * portfolio_item.quantity +
            asset.current_price * quantity
        )
        new_average = total_invested_value / total_quantity
        
        portfolio_item.quantity = total_quantity
        portfolio_item.average_price = new_average
        portfolio_item.total_invested = total_invested_value
        portfolio_item.updated_at = datetime.utcnow()
    else:
        # Cria novo item
        portfolio_item = PortfolioItem(
            account_id=account_id,
            asset_id=asset_id,
            quantity=quantity,
            average_price=asset.current_price,
            total_invested=total_cost
        )
        db.add(portfolio_item)
    
    # Registra transação
    transaction = Transaction(
        from_account_id=account_id,
        transaction_type=TransactionType.INVESTMENT_BUY,
        amount=total_cost,
        description=(
            f"Compra {quantity} {asset.symbol} @ "
            f"R$ {asset.current_price}"
        ),
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza saldo da conta
    account.balance -= total_cost
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(portfolio_item)
    db.refresh(transaction)
    
    return portfolio_item, transaction


def sell_asset(
    db: Session,
    account_id: int,
    asset_id: int,
    quantity: int
) -> tuple[Optional[PortfolioItem], Transaction]:
    """
    Vender ativo
    Retorna: (item_portfólio_ou_None, transação)
    Se vendeu tudo, item é removido e retorna None
    """
    if quantity <= 0:
        raise ValueError("Quantidade deve ser positiva")
    
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Verifica se é conta de investimento
    if account.account_type != AccountType.INVESTIMENTO:
        raise ValueError(
            "Apenas contas de investimento podem vender ativos"
        )
    
    # Busca ativo
    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise ValueError("Ativo não encontrado")
    
    # Busca item no portfólio
    portfolio_item = db.query(PortfolioItem).filter(
        and_(
            PortfolioItem.account_id == account_id,
            PortfolioItem.asset_id == asset_id
        )
    ).first()
    
    if not portfolio_item:
        raise ValueError("Você não possui este ativo no portfólio")
    
    if portfolio_item.quantity < quantity:
        raise ValueError(
            f"Quantidade insuficiente. Disponível: {portfolio_item.quantity}"
        )
    
    # Calcula valor da venda
    total_value = asset.current_price * quantity
    
    # Atualiza ou remove item do portfólio
    if portfolio_item.quantity == quantity:
        # Vendeu tudo, remove do portfólio
        db.delete(portfolio_item)
        portfolio_item = None
    else:
        # Vendeu parcialmente
        portfolio_item.quantity -= quantity
        portfolio_item.updated_at = datetime.utcnow()
    
    # Registra transação
    transaction = Transaction(
        from_account_id=account_id,
        transaction_type=TransactionType.INVESTMENT_SELL,
        amount=total_value,
        description=(
            f"Venda {quantity} {asset.symbol} @ "
            f"R$ {asset.current_price}"
        ),
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza saldo da conta
    account.balance += total_value
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    
    if portfolio_item:
        db.refresh(portfolio_item)
    db.refresh(transaction)
    
    return portfolio_item, transaction


def get_portfolio(db: Session, account_id: int) -> List[dict]:
    """
    Obter portfólio completo com cálculos
    Retorna lista de dicts com informações detalhadas
    """
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Busca itens do portfólio
    items = db.query(PortfolioItem).filter(
        PortfolioItem.account_id == account_id
    ).all()
    
    portfolio = []
    
    for item in items:
        asset = item.asset
        
        # Cálculos
        total_invested = item.average_price * item.quantity
        current_value = asset.current_price * item.quantity
        profit_loss = current_value - total_invested
        profit_loss_percent = (
            (profit_loss / total_invested * 100) if total_invested > 0 else 0
        )
        
        portfolio.append({
            "portfolio_item_id": item.id,
            "asset_id": asset.id,
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_type": asset.asset_type,
            "category": asset.category,
            "quantity": item.quantity,
            "average_price": item.average_price,
            "current_price": asset.current_price,
            "total_invested": total_invested,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percent": profit_loss_percent,
            "purchased_at": item.created_at
        })
    
    return portfolio


def get_portfolio_summary(db: Session, account_id: int) -> dict:
    """
    Resumo do portfólio com totalizadores
    """
    portfolio = get_portfolio(db, account_id)
    
    if not portfolio:
        return {
            "account_id": account_id,
            "total_items": 0,
            "total_invested": 0.0,
            "current_value": 0.0,
            "total_profit_loss": 0.0,
            "total_profit_loss_percent": 0.0,
            "items": []
        }
    
    total_invested = sum(item["total_invested"] for item in portfolio)
    current_value = sum(item["current_value"] for item in portfolio)
    total_profit_loss = current_value - total_invested
    total_profit_loss_percent = (
        (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
    )
    
    return {
        "account_id": account_id,
        "total_items": len(portfolio),
        "total_invested": total_invested,
        "current_value": current_value,
        "total_profit_loss": total_profit_loss,
        "total_profit_loss_percent": total_profit_loss_percent,
        "items": portfolio
    }


def update_asset_prices(db: Session) -> int:
    """
    Atualizar preços dos ativos com simulação de flutuação de mercado
    Flutuação aleatória de -5% a +5%
    Retorna: número de ativos atualizados
    """
    assets = db.query(Asset).filter(Asset.is_active == True).all()
    
    updated_count = 0
    
    for asset in assets:
        # Flutuação aleatória de -5% a +5%
        fluctuation = random.uniform(-0.05, 0.05)
        new_price = asset.current_price * (1 + fluctuation)
        
        # Garante preço mínimo de R$ 0.01
        if new_price < 0.01:
            new_price = 0.01
        
        asset.current_price = round(new_price, 2)
        asset.updated_at = datetime.utcnow()
        
        updated_count += 1
    
    db.commit()
    
    return updated_count


def create_asset(
    db: Session,
    symbol: str,
    name: str,
    asset_type: AssetType,
    category: AssetCategory,
    current_price: float,
    description: Optional[str] = None
) -> Asset:
    """
    Criar novo ativo (função administrativa)
    """
    if current_price <= 0:
        raise ValueError("Preço deve ser positivo")
    
    # Verifica se símbolo já existe
    existing = db.query(Asset).filter(Asset.symbol == symbol).first()
    if existing:
        raise ValueError(f"Ativo com símbolo {symbol} já existe")
    
    asset = Asset(
        symbol=symbol,
        name=name,
        asset_type=asset_type,
        category=category,
        current_price=current_price,
        description=description,
        is_active=True
    )
    
    db.add(asset)
    db.commit()
    db.refresh(asset)
    
    return asset


def simulate_market_realtime(db: Session) -> dict:
    """
    Simula flutuação de mercado em tempo real para todos os ativos
    Retorna: dict com ativos atualizados e suas variações
    """
    assets = db.query(Asset).filter(Asset.is_active == True).all()
    
    updated_assets = []
    
    for asset in assets:
        old_price = asset.current_price
        
        # Flutuação mais realista baseada na categoria
        if asset.category == AssetCategory.TECHNOLOGY:
            # Tech é mais volátil: -7% a +7%
            fluctuation = random.uniform(-0.07, 0.07)
        elif asset.category == AssetCategory.FIXED_INCOME:
            # Renda fixa é estável: -1% a +1%
            fluctuation = random.uniform(-0.01, 0.01)
        else:
            # Outras: -5% a +5%
            fluctuation = random.uniform(-0.05, 0.05)
        
        new_price = old_price * (1 + fluctuation)
        
        # Garante preço mínimo
        if new_price < 0.01:
            new_price = 0.01
        
        asset.current_price = round(new_price, 2)
        asset.updated_at = datetime.utcnow()
        
        change_percent = ((new_price - old_price) / old_price) * 100
        
        updated_assets.append({
            "id": asset.id,
            "symbol": asset.symbol,
            "name": asset.name,
            "old_price": round(old_price, 2),
            "new_price": round(new_price, 2),
            "change_percent": round(change_percent, 2),
            "category": asset.category.value
        })
    
    db.commit()
    
    return {
        "updated_at": datetime.utcnow().isoformat(),
        "total_assets": len(updated_assets),
        "assets": updated_assets
    }
