"""
Modelos de Investimento
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, 
    ForeignKey, Boolean, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.connection import Base
import enum


class AssetType(str, enum.Enum):
    """Tipos de ativos"""
    STOCK = "STOCK"  # Ações
    FUND = "FUND"    # Fundos


class AssetCategory(str, enum.Enum):
    """Categorias de ativos"""
    TECHNOLOGY = "TECHNOLOGY"
    RETAIL = "RETAIL"
    ENERGY = "ENERGY"
    FINANCE = "FINANCE"
    HEALTH = "HEALTH"
    FIXED_INCOME = "FIXED_INCOME"


class Asset(Base):
    """Modelo de ativo financeiro disponível para investimento"""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    asset_type = Column(SQLEnum(AssetType), nullable=False)
    category = Column(SQLEnum(AssetCategory), nullable=False)
    current_price = Column(Float, nullable=False)
    min_investment = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio_items = relationship("PortfolioItem", back_populates="asset")
    price_history = relationship("MarketHistory", back_populates="asset", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Asset(id={self.id}, symbol={self.symbol}, name={self.name})>"


class MarketHistory(Base):
    """Modelo de histórico de preços dos ativos ao longo do tempo"""
    __tablename__ = "market_history"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float, default=0.0)  # Volume negociado (simulado)
    change_percent = Column(Float)  # Variação percentual
    market_cap = Column(Float)  # Capitalização de mercado (simulada)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    asset = relationship("Asset", back_populates="price_history")
    
    def __repr__(self):
        return f"<MarketHistory(id={self.id}, asset_id={self.asset_id}, price={self.price}, timestamp={self.timestamp})>"


class CandleInterval(str, enum.Enum):
    """Intervalos de velas (candles)"""
    ONE_SECOND = "1s"
    FIVE_SECONDS = "5s"
    TEN_SECONDS = "10s"
    THIRTY_SECONDS = "30s"
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"


class Candle(Base):
    """
    Modelo de velas (candlestick) para análise técnica
    OHLCV: Open, High, Low, Close, Volume
    """
    __tablename__ = "candles"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    interval = Column(SQLEnum(CandleInterval), nullable=False, default=CandleInterval.ONE_MINUTE)
    
    # OHLCV Data
    open_price = Column(Float, nullable=False)  # Preço de abertura
    high_price = Column(Float, nullable=False)  # Preço máximo
    low_price = Column(Float, nullable=False)   # Preço mínimo
    close_price = Column(Float, nullable=False) # Preço de fechamento
    volume = Column(Float, default=0.0)         # Volume negociado
    
    # Dados adicionais
    trades_count = Column(Integer, default=0)   # Número de negociações
    quote_volume = Column(Float, default=0.0)   # Volume em moeda cotada
    
    # Timestamps
    open_time = Column(DateTime, nullable=False, index=True)
    close_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    asset = relationship("Asset")
    
    def __repr__(self):
        return f"<Candle(asset_id={self.asset_id}, interval={self.interval}, close={self.close_price})>"
    
    def to_dict(self):
        """Converte para dicionário (útil para WebSocket)"""
        return {
            "id": self.id,
            "asset_id": self.asset_id,
            "interval": self.interval.value,
            "open": self.open_price,
            "high": self.high_price,
            "low": self.low_price,
            "close": self.close_price,
            "volume": self.volume,
            "trades_count": self.trades_count,
            "open_time": self.open_time.isoformat(),
            "close_time": self.close_time.isoformat()
        }


class PortfolioItem(Base):
    """Modelo de item no portfólio de investimentos do cliente"""
    __tablename__ = "portfolio_items"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)  # Preço médio de compra
    total_invested = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = relationship("Account", back_populates="portfolio_items")
    asset = relationship("Asset", back_populates="portfolio_items")
    
    def __repr__(self):
        return f"<PortfolioItem(id={self.id}, asset_id={self.asset_id}, quantity={self.quantity})>"
