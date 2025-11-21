import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Modal from '../components/common/Modal';
import Input from '../components/common/Input';
import QuickNav from '../components/common/QuickNav';
import CandlestickModal from '../components/investments/CandlestickModal';
import TradingToggle from '../components/common/TradingToggle';
import { useAuth } from '../hooks/useAuth';
import { useAccounts } from '../hooks/useAccounts';
import { useInvestments } from '../hooks/useInvestments';
import { formatCurrency, formatPercent } from '../utils/formatters';
import { IoTrendingUp, IoTrendingDown, IoWallet, IoStatsChart, IoRocket, IoSunny, IoMoon } from 'react-icons/io5';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';

const Investments = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { accounts } = useAccounts();
  const { assets, portfolio, loadAssets, loadPortfolio, buyAsset, sellAsset, loading } = useInvestments();
  const [activeTab, setActiveTab] = useState('stocks');
  const [showBuyModal, setShowBuyModal] = useState(false);
  const [showSellModal, setShowSellModal] = useState(false);
  const [showCandlestickModal, setShowCandlestickModal] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [selectedPortfolioItem, setSelectedPortfolioItem] = useState(null);
  
  // Filtra ativos por tipo
  const stocks = assets.filter(a => a.asset_type === 'STOCK');
  const funds = assets.filter(a => a.asset_type === 'FUND');
  
  // Filtra portfólio por tipo (backend já retorna o campo 'type')
  const stocksPortfolio = portfolio.filter(p => p.asset_type === 'STOCK');
  const fundsPortfolio = portfolio.filter(p => p.asset_type === 'FUND');
  
  const { register: registerBuy, handleSubmit: handleSubmitBuy, reset: resetBuy, watch: watchBuy } = useForm();
  const { register: registerSell, handleSubmit: handleSubmitSell, reset: resetSell, watch: watchSell } = useForm();

  const investmentAccount = accounts.find(acc => acc.account_type === 'INVESTIMENTO');

  useEffect(() => {
    loadAssets();
    if (investmentAccount?.id) {
      loadPortfolio(investmentAccount.id);
    }
    
    // Auto-refresh: atualiza preços a cada 10 segundos
    const assetsInterval = setInterval(() => {
      loadAssets();
    }, 10000);
    
    const portfolioInterval = setInterval(() => {
      if (investmentAccount?.id) {
        loadPortfolio(investmentAccount.id);
      }
    }, 10000);
    
    // Cleanup ao desmontar
    return () => {
      clearInterval(assetsInterval);
      clearInterval(portfolioInterval);
    };
  }, [investmentAccount, loadAssets, loadPortfolio]);

  const handleOpenBuy = (asset) => {
    if (!investmentAccount) {
      toast.error('Você precisa de uma Conta Investimento para comprar ativos');
      return;
    }
    setSelectedAsset(asset);
    setShowBuyModal(true);
  };

  const handleOpenSell = (portfolioItem) => {
    setSelectedPortfolioItem(portfolioItem);
    setShowSellModal(true);
  };

  const onSubmitBuy = async (data) => {
    const quantity = parseInt(data.quantity);
    
    if (!quantity || quantity <= 0) {
      toast.error('Quantidade inválida');
      return;
    }

    const result = await buyAsset({
      account_id: investmentAccount.id,
      asset_id: selectedAsset.id,
      quantity: quantity
    });

    if (result.success) {
      setShowBuyModal(false);
      resetBuy();
      loadPortfolio(investmentAccount.id);
    }
  };

  const onSubmitSell = async (data) => {
    const quantity = parseInt(data.quantity);
    
    if (!quantity || quantity <= 0) {
      toast.error('Quantidade inválida');
      return;
    }

    if (quantity > selectedPortfolioItem.quantity) {
      toast.error('Quantidade maior que o disponível');
      return;
    }

    if (!investmentAccount) {
      toast.error('Conta de investimento não encontrada');
      return;
    }

    const result = await sellAsset({
      account_id: investmentAccount.id,
      asset_id: selectedPortfolioItem.asset_id,
      quantity: quantity
    });

    if (result.success) {
      setShowSellModal(false);
      resetSell();
      loadPortfolio(investmentAccount.id);
    }
  };

  const buyQuantity = watchBuy('quantity');
  const sellQuantity = watchSell('quantity');

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <QuickNav />
        <h1 className="text-3xl font-bold text-white">Investimentos</h1>

        <div className="flex items-center justify-between border-b border-gray-700">
          <div className="flex">
            <button
              onClick={() => setActiveTab('stocks')}
              className={`px-6 py-3 border-b-2 transition-colors ${
                activeTab === 'stocks'
                  ? 'border-yellow-500 text-yellow-500 font-medium'
                  : 'border-transparent text-gray-400 hover:text-yellow-500'
              }`}
            >
              Ações
            </button>
            <button
              onClick={() => setActiveTab('funds')}
              className={`px-6 py-3 border-b-2 transition-colors ${
                activeTab === 'funds'
                  ? 'border-yellow-500 text-yellow-500 font-medium'
                  : 'border-transparent text-gray-400 hover:text-yellow-500'
              }`}
            >
              Fundos de Investimento
            </button>
            <button
              onClick={() => setActiveTab('portfolio-stocks')}
              className={`px-6 py-3 border-b-2 transition-colors ${
                activeTab === 'portfolio-stocks'
                  ? 'border-yellow-500 text-yellow-500 font-medium'
                  : 'border-transparent text-gray-400 hover:text-yellow-500'
              }`}
            >
              Minhas Ações
            </button>
            <button
              onClick={() => setActiveTab('portfolio-funds')}
              className={`px-6 py-3 border-b-2 transition-colors ${
                activeTab === 'portfolio-funds'
                  ? 'border-yellow-500 text-yellow-500 font-medium'
                  : 'border-transparent text-gray-400 hover:text-yellow-500'
              }`}
            >
              Meus Fundos
            </button>
          </div>

          {/* Botão Toggle Trading Dashboard */}
          <TradingToggle 
            onClick={() => navigate('/trading-dashboard')}
            isActive={false}
          />
        </div>

        {/* Aba de Ações Disponíveis */}
        {activeTab === 'stocks' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stocks.map((asset) => (
              <Card key={asset.id} hover>
                <div className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-xl text-white">{asset.symbol}</h3>
                      <p className="text-sm text-gray-400">{asset.name}</p>
                      <span className="text-xs bg-blue-900 text-blue-300 px-2 py-1 rounded mt-1 inline-block">
                        {asset.category}
                      </span>
                    </div>
                    {asset.change_percent >= 0 ? (
                      <IoTrendingUp className="w-6 h-6 text-green-400" />
                    ) : (
                      <IoTrendingDown className="w-6 h-6 text-red-400" />
                    )}
                  </div>

                  <div>
                    <p className="text-2xl font-bold text-blue-400">
                      {formatCurrency(asset.current_price)}
                    </p>
                    <p className={`text-sm font-medium ${asset.change_percent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {asset.change_percent >= 0 ? '+' : ''}{formatPercent(asset.change_percent)}
                    </p>
                  </div>

                  <div className="flex gap-2">
                    {/* Botão NEGOCIAR - Abre dashboard de trading com seletor */}
                    <Button 
                      variant="primary"
                      size="small"
                      onClick={() => navigate(`/trading-dashboard/${asset.id}`)}
                      className="flex items-center gap-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    >
                      <IoRocket />
                      Negociar
                    </Button>
                    
                    {/* Botão de Gráfico - Modal rápido */}
                    <Button 
                      variant="secondary" 
                      size="small"
                      onClick={() => {
                        setSelectedAsset(asset);
                        setShowCandlestickModal(true);
                      }}
                      className="flex items-center gap-1"
                    >
                      <IoStatsChart />
                    </Button>
                    
                    <Button 
                      variant="success" 
                      size="small" 
                      onClick={() => handleOpenBuy(asset)}
                    >
                      Comprar
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Aba de Fundos Disponíveis - SEM botão de gráfico */}
        {activeTab === 'funds' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {funds.map((asset) => (
              <Card key={asset.id} hover>
                <div className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-xl text-white">{asset.symbol}</h3>
                      <p className="text-sm text-gray-400">{asset.name}</p>
                      <span className="text-xs bg-green-900 text-green-300 px-2 py-1 rounded mt-1 inline-block">
                        {asset.category}
                      </span>
                      <p className="text-xs text-yellow-400 mt-2">
                        💰 Valor Fixo (não varia)
                      </p>
                    </div>
                  </div>

                  <div>
                    <p className="text-2xl font-bold text-blue-400">
                      {formatCurrency(asset.current_price)}
                    </p>
                    <p className={`text-sm font-medium ${asset.change_percent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                      {asset.change_percent >= 0 ? '+' : ''}{formatPercent(asset.change_percent)}
                    </p>
                  </div>

                  {asset.description && (
                    <p className="text-xs text-gray-500 line-clamp-2">{asset.description}</p>
                  )}

                  <div className="flex gap-2">
                    <Button 
                      variant="success" 
                      size="small" 
                      fullWidth
                      onClick={() => handleOpenBuy(asset)}
                    >
                      Comprar
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Aba de Portfólio de Ações */}
        {activeTab === 'portfolio-stocks' && (
          <div>
            {stocksPortfolio.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {stocksPortfolio.map((item) => (
                  <Card key={item.id}>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-bold text-xl text-white">{item.symbol}</h3>
                          <p className="text-sm text-gray-400">{item.name || 'Ação'}</p>
                        </div>
                        <span className="text-sm text-gray-400 bg-gray-700 px-3 py-1 rounded-full">
                          {item.quantity} unidades
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div key="avg-price">
                          <p className="text-xs text-gray-500 mb-1">Preço Médio</p>
                          <p className="text-lg font-bold text-yellow-500">
                            {formatCurrency(item.average_price)}
                          </p>
                        </div>
                        <div key="current-price">
                          <p className="text-xs text-gray-500 mb-1">Preço Atual</p>
                          <p className="text-lg font-bold text-blue-400">
                            {formatCurrency(item.current_price)}
                          </p>
                        </div>
                      </div>

                      <div className="pt-3 border-t border-gray-700">
                        <p className="text-xs text-gray-500 mb-1">Valor Total</p>
                        <p className="text-2xl font-bold text-green-400">
                          {formatCurrency(item.total_value)}
                        </p>
                        {item.profit_loss !== undefined && (
                          <p className={`text-sm mt-1 ${item.profit_loss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {item.profit_loss >= 0 ? '+' : ''}{formatCurrency(item.profit_loss)}
                            {' '}({item.profit_loss >= 0 ? '+' : ''}{formatPercent((item.profit_loss / (item.average_price * item.quantity)) * 100)})
                          </p>
                        )}
                      </div>

                      <Button 
                        variant="danger" 
                        size="small" 
                        fullWidth
                        onClick={() => handleOpenSell(item)}
                      >
                        Vender
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            ) : (
              <Card>
                <div className="text-center py-12">
                  <IoTrendingUp className="w-16 h-16 text-gray-600 mx-auto mb-4 opacity-50" />
                  <p className="text-gray-400">Você ainda não possui ações</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Compre ações na aba "Ações"
                  </p>
                </div>
              </Card>
            )}
          </div>
        )}

        {/* Aba de Portfólio de Fundos */}
        {activeTab === 'portfolio-funds' && (
          <div>
            {fundsPortfolio.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {fundsPortfolio.map((item) => (
                  <Card key={item.id}>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-bold text-xl text-white">{item.symbol}</h3>
                          <p className="text-sm text-gray-400">{item.name || 'Fundo'}</p>
                        </div>
                        <span className="text-sm text-gray-400 bg-gray-700 px-3 py-1 rounded-full">
                          {item.quantity} cotas
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div key="avg-price">
                          <p className="text-xs text-gray-500 mb-1">Preço Médio</p>
                          <p className="text-lg font-bold text-yellow-500">
                            {formatCurrency(item.average_price)}
                          </p>
                        </div>
                        <div key="current-price">
                          <p className="text-xs text-gray-500 mb-1">Preço Atual</p>
                          <p className="text-lg font-bold text-blue-400">
                            {formatCurrency(item.current_price)}
                          </p>
                        </div>
                      </div>

                      <div className="pt-3 border-t border-gray-700">
                        <p className="text-xs text-gray-500 mb-1">Valor Total</p>
                        <p className="text-2xl font-bold text-green-400">
                          {formatCurrency(item.total_value)}
                        </p>
                        {item.profit_loss !== undefined && (
                          <p className={`text-sm mt-1 ${item.profit_loss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {item.profit_loss >= 0 ? '+' : ''}{formatCurrency(item.profit_loss)}
                            {' '}({item.profit_loss >= 0 ? '+' : ''}{formatPercent((item.profit_loss / (item.average_price * item.quantity)) * 100)})
                          </p>
                        )}
                      </div>

                      <Button 
                        variant="danger" 
                        size="small" 
                        fullWidth
                        onClick={() => handleOpenSell(item)}
                      >
                        Vender
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            ) : (
              <Card>
                <div className="text-center py-12">
                  <IoTrendingUp className="w-16 h-16 text-gray-600 mx-auto mb-4 opacity-50" />
                  <p className="text-gray-400">Você ainda não possui fundos de investimento</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Compre fundos na aba "Fundos de Investimento"
                  </p>
                </div>
              </Card>
            )}
          </div>
        )}
      </div>

      {/* Modal de Compra */}
      <Modal
        isOpen={showBuyModal}
        onClose={() => {
          setShowBuyModal(false);
          resetBuy();
        }}
        title="Comprar Ativo"
      >
        {selectedAsset && (
          <form onSubmit={handleSubmitBuy(onSubmitBuy)} className="space-y-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-sm text-gray-400">Ativo</p>
              <p className="text-lg font-bold text-white">{selectedAsset.symbol}</p>
              <p className="text-sm text-gray-400">{selectedAsset.name}</p>
              <p className="text-xl font-bold text-blue-400 mt-2">
                {formatCurrency(selectedAsset.current_price)}
              </p>
            </div>

            <Input
              label="Quantidade"
              type="number"
              min="1"
              step="1"
              placeholder="0"
              icon={<IoWallet />}
              {...registerBuy('quantity', { required: true, min: 1 })}
            />

            {buyQuantity > 0 && (
              <div className="bg-gray-800 p-4 rounded-lg">
                <p className="text-sm text-gray-400">Total</p>
                <p className="text-2xl font-bold text-yellow-500">
                  {formatCurrency(selectedAsset.current_price * parseInt(buyQuantity))}
                </p>
              </div>
            )}

            <div className="flex gap-2">
              <Button
                type="button"
                variant="secondary"
                fullWidth
                onClick={() => {
                  setShowBuyModal(false);
                  resetBuy();
                }}
              >
                Cancelar
              </Button>
              <Button type="submit" fullWidth>
                Confirmar Compra
              </Button>
            </div>
          </form>
        )}
      </Modal>

      {/* Modal de Venda */}
      <Modal
        isOpen={showSellModal}
        onClose={() => {
          setShowSellModal(false);
          resetSell();
        }}
        title="Vender Ativo"
      >
        {selectedPortfolioItem && (
          <form onSubmit={handleSubmitSell(onSubmitSell)} className="space-y-4">
            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-sm text-gray-400">Ativo</p>
              <p className="text-lg font-bold text-white">{selectedPortfolioItem.symbol}</p>
              <p className="text-sm text-gray-400">{selectedPortfolioItem.name}</p>
              <p className="text-sm text-gray-400 mt-2">
                Disponível: {selectedPortfolioItem.quantity} unidades
              </p>
            </div>

            <Input
              label="Quantidade"
              type="number"
              min="1"
              max={selectedPortfolioItem.quantity}
              step="1"
              placeholder="0"
              icon={<IoWallet />}
              {...registerSell('quantity', { 
                required: true, 
                min: 1,
                max: selectedPortfolioItem.quantity
              })}
            />

            {sellQuantity > 0 && (
              <div className="bg-gray-800 p-4 rounded-lg">
                <p className="text-sm text-gray-400">Você receberá (estimado)</p>
                <p className="text-2xl font-bold text-green-400">
                  {formatCurrency(selectedPortfolioItem.current_price * parseInt(sellQuantity))}
                </p>
              </div>
            )}

            <div className="flex gap-2">
              <Button
                type="button"
                variant="secondary"
                fullWidth
                onClick={() => {
                  setShowSellModal(false);
                  resetSell();
                }}
              >
                Cancelar
              </Button>
              <Button type="submit" variant="danger" fullWidth>
                Confirmar Venda
              </Button>
            </div>
          </form>
        )}
      </Modal>

      {/* Modal de Gráfico de Velas */}
      <CandlestickModal
        isOpen={showCandlestickModal}
        onClose={() => setShowCandlestickModal(false)}
        asset={selectedAsset}
        allAssets={stocks}
      />
    </DashboardLayout>
  );
};

export default Investments;
