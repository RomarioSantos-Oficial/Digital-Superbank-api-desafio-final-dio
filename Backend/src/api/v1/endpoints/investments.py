"""
Investment Endpoints
Rotas para investimentos e gerenciamento de portfólio
"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.api.dependencies import get_current_user
from src.models.user import User
from src.models.investment import (
    AssetType, AssetCategory, Asset, MarketHistory, Candle, CandleInterval
)
from src.schemas.investment import (
    AssetResponse, BuyAssetRequest, BuyAssetResponse,
    SellAssetRequest, SellAssetResponse,
    PortfolioItemResponse, PortfolioSummaryResponse
)
from src.services import investment_service
from src.services.account_service import get_account_by_id
from src.services.candle_service import get_recent_candles, get_candles_summary

router = APIRouter(prefix="/investments", tags=["Investments"])


@router.get("/assets", response_model=List[AssetResponse])
def list_assets(
    asset_type: Optional[AssetType] = None,
    category: Optional[AssetCategory] = None,
    active_only: bool = Query(default=True),
    db: Session = Depends(get_db)
):
    """
    Listar ativos disponíveis para investimento
    Filtros opcionais: tipo (STOCK/FUND), categoria, apenas ativos
    """
    assets = investment_service.get_all_assets(
        db, asset_type, category, active_only
    )
    
    return [
        AssetResponse(
            id=asset.id,
            symbol=asset.symbol,
            name=asset.name,
            asset_type=asset.asset_type,
            category=asset.category,
            current_price=asset.current_price,
            description=asset.description,
            is_active=asset.is_active,
            created_at=asset.created_at,
            updated_at=asset.updated_at
        ) for asset in assets
    ]


@router.get("/assets/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """Obter detalhes de um ativo específico"""
    asset = investment_service.get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    
    return AssetResponse(
        id=asset.id,
        symbol=asset.symbol,
        name=asset.name,
        asset_type=asset.asset_type,
        category=asset.category,
        current_price=asset.current_price,
        description=asset.description,
        is_active=asset.is_active,
        created_at=asset.created_at,
        updated_at=asset.updated_at
    )


@router.post("/buy", response_model=BuyAssetResponse)
def buy_asset(
    request: BuyAssetRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Comprar ativo
    Requer conta de investimento
    """
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        portfolio_item, transaction = investment_service.buy_asset(
            db, request.account_id, request.asset_id, request.quantity
        )
        
        return BuyAssetResponse(
            transaction_id=transaction.id,
            portfolio_item_id=portfolio_item.id,
            asset_id=request.asset_id,
            symbol=portfolio_item.asset.symbol,
            quantity_purchased=request.quantity,
            price_per_unit=portfolio_item.asset.current_price,
            total_cost=transaction.amount,
            new_average_price=portfolio_item.average_price,
            total_quantity=portfolio_item.quantity,
            created_at=transaction.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sell", response_model=SellAssetResponse)
def sell_asset(
    request: SellAssetRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Vender ativo
    Requer ter o ativo no portfólio
    """
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, request.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        # Busca ativo para pegar símbolo
        asset = investment_service.get_asset_by_id(db, request.asset_id)
        if not asset:
            raise HTTPException(
                status_code=404, detail="Ativo não encontrado"
            )
        
        portfolio_item, transaction = investment_service.sell_asset(
            db, request.account_id, request.asset_id, request.quantity
        )
        
        return SellAssetResponse(
            transaction_id=transaction.id,
            asset_id=request.asset_id,
            symbol=asset.symbol,
            quantity_sold=request.quantity,
            price_per_unit=asset.current_price,
            total_value=transaction.amount,
            remaining_quantity=(
                portfolio_item.quantity if portfolio_item else 0
            ),
            created_at=transaction.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/portfolio", response_model=List[PortfolioItemResponse])
def get_portfolio(
    account_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter portfólio de investimentos de uma conta
    Mostra todos os ativos com cálculos de lucro/prejuízo
    Aceita account_id ou user_id (usa primeira conta de investimento do usuário)
    """
    # Se não forneceu account_id mas forneceu user_id
    if not account_id and user_id:
        # Verifica se o user_id é o do usuário autenticado
        if user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Busca primeira conta de investimento do usuário
        from src.services.account_service import get_accounts_by_user_id
        accounts = get_accounts_by_user_id(db, user_id)
        inv_accounts = [acc for acc in accounts if acc.account_type == "INVESTIMENTO"]
        
        if not inv_accounts:
            return []  # Retorna lista vazia se não tiver conta de investimento
        
        account_id = inv_accounts[0].id
    
    if not account_id:
        raise HTTPException(status_code=400, detail="account_id ou user_id é obrigatório")
    
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        portfolio = investment_service.get_portfolio(db, account_id)
        
        return [
            PortfolioItemResponse(
                portfolio_item_id=item["portfolio_item_id"],
                asset_id=item["asset_id"],
                symbol=item["symbol"],
                name=item["name"],
                asset_type=item["asset_type"],
                category=item["category"],
                quantity=item["quantity"],
                average_price=item["average_price"],
                current_price=item["current_price"],
                total_invested=item["total_invested"],
                current_value=item["current_value"],
                profit_loss=item["profit_loss"],
                profit_loss_percent=item["profit_loss_percent"],
                purchased_at=item["purchased_at"]
            ) for item in portfolio
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/portfolio/summary", response_model=PortfolioSummaryResponse)
def get_portfolio_summary(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resumo do portfólio com totalizadores
    Total investido, valor atual, lucro/prejuízo
    """
    # Verifica se a conta pertence ao usuário
    account = get_account_by_id(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    try:
        summary = investment_service.get_portfolio_summary(db, account_id)
        
        return PortfolioSummaryResponse(
            account_id=summary["account_id"],
            total_items=summary["total_items"],
            total_invested=summary["total_invested"],
            current_value=summary["current_value"],
            total_profit_loss=summary["total_profit_loss"],
            total_profit_loss_percent=summary["total_profit_loss_percent"],
            items=[
                PortfolioItemResponse(
                    portfolio_item_id=item["portfolio_item_id"],
                    asset_id=item["asset_id"],
                    symbol=item["symbol"],
                    name=item["name"],
                    asset_type=item["asset_type"],
                    category=item["category"],
                    quantity=item["quantity"],
                    average_price=item["average_price"],
                    current_price=item["current_price"],
                    total_invested=item["total_invested"],
                    current_value=item["current_value"],
                    profit_loss=item["profit_loss"],
                    profit_loss_percent=item["profit_loss_percent"],
                    purchased_at=item["purchased_at"]
                ) for item in summary["items"]
            ]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/assets/{symbol}/history")
def get_asset_history(
    symbol: str,
    period: str = Query(default="1D", regex="^(1D|7D|1M|3M|6M|1Y|ALL)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obter histórico de preços de um ativo
    
    Períodos disponíveis:
    - 1D: Último dia (24 horas)
    - 7D: Última semana
    - 1M: Último mês
    - 3M: Últimos 3 meses
    - 6M: Últimos 6 meses
    - 1Y: Último ano
    - ALL: Todo o histórico
    """
    # Busca ativo
    asset = db.query(Asset).filter(Asset.symbol == symbol.upper()).first()
    if not asset:
        raise HTTPException(status_code=404, detail=f"Ativo {symbol} não encontrado")
    
    # Define período
    period_map = {
        "1D": timedelta(days=1),
        "7D": timedelta(days=7),
        "1M": timedelta(days=30),
        "3M": timedelta(days=90),
        "6M": timedelta(days=180),
        "1Y": timedelta(days=365),
        "ALL": None
    }
    
    time_delta = period_map[period]
    
    # Query histórico
    query = db.query(MarketHistory).filter(MarketHistory.asset_id == asset.id)
    
    if time_delta:
        start_date = datetime.utcnow() - time_delta
        query = query.filter(MarketHistory.timestamp >= start_date)
    
    history = query.order_by(MarketHistory.timestamp.asc()).all()
    
    # Formata resposta
    return {
        "symbol": asset.symbol,
        "name": asset.name,
        "current_price": asset.current_price,
        "period": period,
        "data_points": len(history),
        "data": [
            {
                "timestamp": h.timestamp.isoformat(),
                "price": h.price,
                "volume": h.volume,
                "change_percent": h.change_percent,
                "market_cap": h.market_cap
            } for h in history
        ]
    }


@router.post("/market/simulate")
def simulate_market(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Simula flutuação de mercado em tempo real
    Atualiza preços de todos os ativos com base em volatilidade da categoria
    
    Retorna informações de todos os ativos atualizados
    """
    try:
        result = investment_service.simulate_market_realtime(db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao simular mercado: {str(e)}"
        )


@router.get("/market/status")
def get_market_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém status atual do mercado
    Mostra todos os ativos e suas variações recentes
    """
    assets = db.query(Asset).filter(Asset.is_active == True).all()
    
    market_data = []
    for asset in assets:
        # Busca último registro de histórico para calcular variação
        last_history = db.query(MarketHistory).filter(
            MarketHistory.asset_id == asset.id
        ).order_by(MarketHistory.timestamp.desc()).first()
        
        change_percent = last_history.change_percent if last_history else 0.0
        
        market_data.append({
            "id": asset.id,
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_type": asset.asset_type.value,
            "category": asset.category.value,
            "current_price": asset.current_price,
            "change_percent": round(change_percent, 2),
            "updated_at": asset.updated_at.isoformat()
        })
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "total_assets": len(market_data),
        "assets": market_data
    }


@router.get("/candles/{asset_id}")
def get_asset_candles(
    asset_id: int,
    interval: CandleInterval = Query(default=CandleInterval.ONE_MINUTE),
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém velas (candlesticks) de um ativo para análise técnica
    
    Parâmetros:
    - asset_id: ID do ativo
    - interval: Intervalo das velas (1m, 5m, 15m, 1h, 4h, 1d)
    - limit: Número máximo de velas (padrão: 100, máximo: 500)
    
    Retorna dados OHLCV (Open, High, Low, Close, Volume)
    """
    # Verifica se o ativo existe
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    
    # Busca velas
    candles = get_recent_candles(db, asset_id, interval, limit)
    
    return {
        "asset_id": asset_id,
        "symbol": asset.symbol,
        "name": asset.name,
        "interval": interval.value,
        "candles": [
            {
                "open": c.open_price,
                "high": c.high_price,
                "low": c.low_price,
                "close": c.close_price,
                "volume": c.volume,
                "trades": c.trades_count,
                "open_time": c.open_time.isoformat(),
                "close_time": c.close_time.isoformat()
            }
            for c in candles
        ],
        "total": len(candles)
    }


@router.get("/candles/{asset_id}/summary")
def get_asset_candles_summary(
    asset_id: int,
    interval: CandleInterval = Query(default=CandleInterval.ONE_MINUTE),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém resumo estatístico das velas de um ativo
    
    Retorna:
    - Preço atual
    - Alta e baixa das últimas 24 velas
    - Volume médio
    - Variação de preço (%)
    """
    # Verifica se o ativo existe
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Ativo não encontrado")
    
    # Busca resumo
    summary = get_candles_summary(db, asset_id, interval)
    
    if not summary:
        return {
            "asset_id": asset_id,
            "symbol": asset.symbol,
            "message": "Sem dados de velas disponíveis"
        }
    
    return {
        "asset_id": asset_id,
        "symbol": asset.symbol,
        "name": asset.name,
        **summary
    }


@router.get("/candles/latest")
def get_latest_candles_all_assets(
    interval: CandleInterval = Query(default=CandleInterval.ONE_MINUTE),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém a última vela de todos os ativos ativos
    Útil para dashboard em tempo real
    """
    assets = db.query(Asset).filter(
        Asset.is_active == True,
        Asset.asset_type == AssetType.STOCK
    ).all()
    
    latest_candles = []
    
    for asset in assets:
        candles = get_recent_candles(db, asset.id, interval, limit=1)
        if candles:
            c = candles[0]
            change_percent = ((c.close_price - c.open_price) / 
                            c.open_price) * 100
            
            latest_candles.append({
                "asset_id": asset.id,
                "symbol": asset.symbol,
                "name": asset.name,
                "candle": {
                    "open": c.open_price,
                    "high": c.high_price,
                    "low": c.low_price,
                    "close": c.close_price,
                    "volume": c.volume,
                    "trades": c.trades_count,
                    "change_percent": round(change_percent, 2),
                    "open_time": c.open_time.isoformat(),
                    "close_time": c.close_time.isoformat()
                }
            })
    
    return {
        "interval": interval.value,
        "timestamp": datetime.utcnow().isoformat(),
        "total": len(latest_candles),
        "candles": latest_candles
    }
