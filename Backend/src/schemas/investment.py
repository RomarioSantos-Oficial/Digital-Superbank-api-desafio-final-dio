"""
Schemas para investimentos
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from src.models.investment import AssetType, AssetCategory


class AssetResponse(BaseModel):
    """Schema para resposta de ativo"""
    id: int
    symbol: str
    name: str
    asset_type: AssetType
    category: AssetCategory
    current_price: float
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BuyAssetRequest(BaseModel):
    """Schema para compra de ativo"""
    account_id: int
    asset_id: int
    quantity: int = Field(..., gt=0)


class BuyAssetResponse(BaseModel):
    """Schema de resposta para compra de ativo"""
    transaction_id: int
    portfolio_item_id: int
    asset_id: int
    symbol: str
    quantity_purchased: int
    price_per_unit: float
    total_cost: float
    new_average_price: float
    total_quantity: int
    created_at: datetime


class SellAssetRequest(BaseModel):
    """Schema para venda de ativo"""
    account_id: int
    asset_id: int
    quantity: int = Field(..., gt=0)


class SellAssetResponse(BaseModel):
    """Schema de resposta para venda de ativo"""
    transaction_id: int
    asset_id: int
    symbol: str
    quantity_sold: int
    price_per_unit: float
    total_value: float
    remaining_quantity: int
    created_at: datetime


class PortfolioItemResponse(BaseModel):
    """Schema para item do portfólio"""
    portfolio_item_id: int
    asset_id: int
    symbol: str
    name: str
    asset_type: AssetType
    category: AssetCategory
    quantity: int
    average_price: float
    current_price: float
    total_invested: float
    current_value: float
    profit_loss: float
    profit_loss_percent: float
    purchased_at: datetime


class PortfolioSummaryResponse(BaseModel):
    """Schema para resumo do portfólio"""
    account_id: int
    total_items: int
    total_invested: float
    current_value: float
    total_profit_loss: float
    total_profit_loss_percent: float
    items: List[PortfolioItemResponse]

