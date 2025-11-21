import React, { useState, useEffect } from 'react';
import Modal from '../common/Modal';
import Button from '../common/Button';
import CandlestickChart from './CandlestickChart';
import { 
  IoTrendingUp, IoTrendingDown, IoReload, IoClose, 
  IoWallet, IoSearch, IoChevronDown, IoCart, IoArrowDown,
  IoStatsChart
} from 'react-icons/io5';
import api from '../../services/api';
import toast from 'react-hot-toast';

/**
 * Modal de Visualização de Velas em Tempo Real
 * Com seletor de ações, compra/venda e saldo
 */
const CandlestickModal = ({ isOpen, onClose, asset: initialAsset, allAssets = [] }) => {
  const [asset, setAsset] = useState(initialAsset);
  const [candles, setCandles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [candleInterval, setCandleInterval] = useState('1m'); // Intervalo de velas
  
  // Mapeia intervalo de velas para milissegundos de refresh
  const getRefreshInterval = (interval) => {
    const intervalMap = {
      '1s': 1000,       // 1 segundo
      '5s': 5000,       // 5 segundos
      '10s': 10000,     // 10 segundos
      '30s': 30000,     // 30 segundos
      '1m': 60000,      // 1 minuto
      '5m': 300000,     // 5 minutos
      '15m': 900000,    // 15 minutos
      '1h': 3600000,    // 1 hora
      '4h': 14400000,   // 4 horas
      '1d': 86400000    // 1 dia
    };
    return intervalMap[interval] || 60000;
  };
  
  // Seletor de ações
  const [showAssetSelector, setShowAssetSelector] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Trading
  const [tradeType, setTradeType] = useState('buy'); // 'buy' ou 'sell'
  const [quantity, setQuantity] = useState(1);
  const [investmentAccount, setInvestmentAccount] = useState(null);
  
  // Múltiplas abas
  const [watchlist, setWatchlist] = useState([]);

  // Atualiza asset quando prop muda
  useEffect(() => {
    if (initialAsset) {
      setAsset(initialAsset);
      // Adiciona à watchlist se não estiver
      if (!watchlist.find(a => a.id === initialAsset.id)) {
        setWatchlist(prev => [...prev, initialAsset]);
      }
    }
  }, [initialAsset]);

  // Carrega conta de investimento
  const loadInvestmentAccount = async () => {
    try {
      const response = await api.get('/api/v1/accounts');
      const invAccount = response.data.find(acc => acc.account_type === 'INVESTIMENTO');
      setInvestmentAccount(invAccount);
    } catch (error) {
      console.error('Erro ao carregar conta:', error);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadInvestmentAccount();
    }
  }, [isOpen]);

  // Calcula limite de velas baseado no intervalo
  const getCandleLimit = (interval) => {
    const limitMap = {
      '1s': 60,      // 1 minuto de dados (60 velas de 1s)
      '5s': 60,      // 5 minutos de dados (60 velas de 5s)
      '10s': 60,     // 10 minutos de dados (60 velas de 10s)
      '30s': 60,     // 30 minutos de dados (60 velas de 30s)
      '1m': 60,      // 1 hora de dados (60 velas de 1m)
      '5m': 60,      // 5 horas de dados (60 velas de 5m)
      '15m': 48,     // 12 horas de dados (48 velas de 15m)
      '1h': 24,      // 24 horas de dados (24 velas de 1h)
      '4h': 24,      // 4 dias de dados (24 velas de 4h)
      '1d': 30       // 30 dias de dados (30 velas de 1d)
    };
    return limitMap[interval] || 60;
  };

  // Carrega velas do backend
  const loadCandles = async () => {
    if (!asset) return;

    try {
      setLoading(true);
      
      // Busca velas com o intervalo e limite apropriado
      const response = await api.get(`/api/v1/investments/candles/${asset.id}`, {
        params: {
          interval: candleInterval,  // Usa o intervalo escolhido pelo usuário
          limit: getCandleLimit(candleInterval)  // Limite baseado no intervalo
        }
      });

      setCandles(response.data.candles || []);

      // Busca resumo estatístico
      const summaryResponse = await api.get(`/api/v1/investments/candles/${asset.id}/summary`, {
        params: {
          interval: candleInterval  // Usa o intervalo escolhido pelo usuário
        }
      });

      setSummary(summaryResponse.data);

    } catch (error) {
      console.error('Erro ao carregar velas:', error);
      toast.error('Erro ao carregar dados do gráfico');
    } finally {
      setLoading(false);
    }
  };

  // Carrega velas quando abre o modal ou muda o intervalo
  useEffect(() => {
    if (isOpen && asset) {
      loadCandles();
    }
  }, [isOpen, asset, candleInterval]);

  // Auto-refresh baseado no intervalo de velas escolhido
  useEffect(() => {
    if (!isOpen || !autoRefresh) return;

    const interval = setInterval(() => {
      loadCandles();
    }, getRefreshInterval(candleInterval));

    return () => clearInterval(interval);
  }, [isOpen, autoRefresh, asset, candleInterval]);

  // WebSocket para atualizações em tempo real
  useEffect(() => {
    if (!isOpen || !asset) return;

    const wsUrl = import.meta.env.VITE_API_BASE_URL.replace('http', 'ws');
    const ws = new WebSocket(`${wsUrl}/ws/market-feed`);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Atualiza apenas se for o ativo correto E o intervalo correto
        if (data.type === 'candle_update' && 
            data.symbol === asset.symbol &&
            data.candle.interval === candleInterval) {
          setCandles(prev => {
            const updated = [...prev, data.candle];
            // Mantém apenas o limite correto de velas
            return updated.slice(-getCandleLimit(candleInterval));
          });

          // Atualiza resumo
          if (data.candle) {
            setSummary(prev => ({
              ...prev,
              current_price: data.candle.close
            }));
          }
        }
      } catch (error) {
        console.error('Erro ao processar WebSocket:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      ws.close();
    };
  }, [isOpen, asset, candleInterval]); // Reconecta quando muda o intervalo

  // Trocar de ativo
  const handleSelectAsset = (newAsset) => {
    setAsset(newAsset);
    setShowAssetSelector(false);
    setSearchTerm('');
    
    // Adiciona à watchlist
    if (!watchlist.find(a => a.id === newAsset.id)) {
      setWatchlist(prev => [...prev, newAsset]);
    }
  };

  // Remover da watchlist
  const handleRemoveFromWatchlist = (assetId) => {
    setWatchlist(prev => prev.filter(a => a.id !== assetId));
  };

  // Executar trade
  const handleTrade = async () => {
    if (!investmentAccount) {
      toast.error('Você precisa de uma conta de investimento');
      return;
    }

    if (!quantity || quantity <= 0) {
      toast.error('Quantidade inválida');
      return;
    }

    try {
      const endpoint = tradeType === 'buy' 
        ? '/api/v1/investments/buy'
        : '/api/v1/investments/sell';

      await api.post(endpoint, {
        account_id: investmentAccount.id,
        asset_id: asset.id,
        quantity: parseInt(quantity)
      });

      toast.success(
        tradeType === 'buy' 
          ? '✅ Compra realizada!' 
          : '✅ Venda realizada!'
      );

      setQuantity(1);
      loadInvestmentAccount(); // Atualiza saldo

    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao executar operação');
    }
  };

  // Filtrar ativos para pesquisa
  const filteredAssets = allAssets.filter(a => 
    a.asset_type === 'STOCK' && (
      a.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.symbol.toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  if (!asset) return null;

  const priceChange = summary?.price_change_24h || 0;
  const isPositive = priceChange >= 0;
  const currentPrice = summary?.current_price || asset.current_price || 0;
  const totalValue = currentPrice * (quantity || 0);

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <div className="p-6 max-h-[95vh] overflow-y-auto overflow-x-hidden">
        {/* Header com Seletor */}
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1">
            {/* Seletor de Ações */}
            <div className="relative mb-2">
              <button
                onClick={() => setShowAssetSelector(!showAssetSelector)}
                className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition"
              >
                <IoStatsChart className="text-blue-600" />
                <div className="text-left">
                  <div className="font-bold text-gray-800">{asset.symbol}</div>
                  <div className="text-xs text-gray-600">{asset.name}</div>
                </div>
                <IoChevronDown className="text-gray-400 ml-2" />
              </button>

              {/* Dropdown */}
              {showAssetSelector && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-xl z-50 max-h-96 overflow-hidden">
                  {/* Pesquisa */}
                  <div className="p-3 border-b">
                    <div className="relative">
                      <IoSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Pesquisar ações..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
                        autoFocus
                      />
                    </div>
                  </div>

                  {/* Lista */}
                  <div className="overflow-y-auto max-h-80">
                    {filteredAssets.map(a => (
                      <button
                        key={a.id}
                        onClick={() => handleSelectAsset(a)}
                        className="w-full px-4 py-3 hover:bg-gray-50 transition text-left flex items-center justify-between"
                      >
                        <div>
                          <div className="font-semibold">{a.symbol}</div>
                          <div className="text-xs text-gray-600">{a.name}</div>
                        </div>
                        <div className="text-right">
                          <div className="font-bold">R$ {(a.current_price || 0).toFixed(2)}</div>
                          <div className={`text-xs ${
                            (a.price_change_percent || 0) >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {(a.price_change_percent || 0) >= 0 ? '+' : ''}{(a.price_change_percent || 0).toFixed(2)}%
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Watchlist - Abas de Ações Acompanhadas */}
            {watchlist.length > 1 && (
              <div className="flex gap-2 flex-wrap">
                {watchlist.map(a => (
                  <div
                    key={a.id}
                    className={`group relative px-3 py-1 rounded-full text-xs font-medium transition cursor-pointer ${
                      a.id === asset.id 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <span onClick={() => setAsset(a)} className="cursor-pointer">
                      {a.symbol}
                    </span>
                    {watchlist.length > 1 && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRemoveFromWatchlist(a.id);
                        }}
                        className="ml-1 opacity-0 group-hover:opacity-100 transition"
                        type="button"
                      >
                        <IoClose className="inline w-3 h-3" />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition"
          >
            <IoClose className="w-6 h-6 text-gray-500" />
          </button>
        </div>

        {/* Grid: Gráfico + Trading */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Gráfico (2/3) */}
          <div className="lg:col-span-2">
            {/* Estatísticas */}
            {summary && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-lg p-4">
                  <div className="text-xs font-medium text-blue-700 mb-1">Preço Atual</div>
                  <div className="text-2xl font-bold text-blue-900">
                    R$ {currentPrice.toFixed(2)}
                  </div>
                </div>

                <div className={`bg-gradient-to-br rounded-lg p-4 border ${
                  isPositive 
                    ? 'from-green-50 to-green-100 border-green-200' 
                    : 'from-red-50 to-red-100 border-red-200'
                }`}>
                  <div className={`text-xs font-medium mb-1 ${
                    isPositive ? 'text-green-700' : 'text-red-700'
                  }`}>Variação 24h</div>
                  <div className={`text-2xl font-bold flex items-center gap-1 ${
                    isPositive ? 'text-green-900' : 'text-red-900'
                  }`}>
                    {isPositive ? <IoTrendingUp /> : <IoTrendingDown />}
                    {priceChange.toFixed(2)}%
                  </div>
                </div>

                <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 border border-emerald-200 rounded-lg p-4">
                  <div className="text-xs font-medium text-emerald-700 mb-1">Máxima 24h</div>
                  <div className="text-2xl font-bold text-emerald-900">
                    R$ {summary.high_24?.toFixed(2) || '0.00'}
                  </div>
                </div>

                <div className="bg-gradient-to-br from-rose-50 to-rose-100 border border-rose-200 rounded-lg p-4">
                  <div className="text-xs font-medium text-rose-700 mb-1">Mínima 24h</div>
                  <div className="text-2xl font-bold text-rose-900">
                    R$ {summary.low_24?.toFixed(2) || '0.00'}
                  </div>
                </div>
              </div>
            )}

            {/* Controles */}
            <div className="mb-4 min-h-[180px]">
              {/* Seletor de Intervalo de Velas - BOTÕES GRANDES */}
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-5 border-2 border-purple-300 mb-4 shadow-lg">
                <label className="text-base font-bold text-gray-800 mb-4 flex items-center gap-2">
                  🕒 Escolha o Intervalo das Velas:
                  <span className="text-xs text-purple-600 font-normal">(Define o tamanho de cada vela)</span>
                </label>
                <div className="grid grid-cols-5 gap-3 min-h-[120px]">
                  {[
                    { label: '⚡ 1s', value: '1s' },
                    { label: '⚡ 5s', value: '5s' },
                    { label: '⚡ 10s', value: '10s' },
                    { label: '⚡ 30s', value: '30s' },
                    { label: '📊 1min', value: '1m' },
                    { label: '📊 5min', value: '5m' },
                    { label: '📊 15min', value: '15m' },
                    { label: '📊 1h', value: '1h' },
                    { label: '📊 4h', value: '4h' },
                    { label: '📊 1d', value: '1d' },
                  ].map(interval => (
                    <button
                      key={interval.value}
                      onClick={() => setCandleInterval(interval.value)}
                      className={`px-4 py-3 rounded-lg text-sm font-bold transition-all ${
                        candleInterval === interval.value
                          ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/50 scale-105 ring-4 ring-purple-400/50'
                          : 'bg-white text-gray-700 hover:bg-gray-50 hover:scale-102 border-2 border-gray-200'
                      }`}
                    >
                      {interval.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Auto-refresh e botão atualizar */}
              <div className="flex items-center justify-between">
                <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer bg-blue-50 px-4 py-2 rounded-lg border border-blue-200">
                  <input
                    type="checkbox"
                    checked={autoRefresh}
                    onChange={(e) => setAutoRefresh(e.target.checked)}
                    className="rounded"
                  />
                  <span className="font-medium">Auto-refresh</span>
                  <span className="text-xs text-blue-600">({getRefreshInterval(candleInterval) / 1000}s)</span>
                </label>

                <button
                  onClick={loadCandles}
                  disabled={loading}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                >
                  <IoReload className={loading ? 'animate-spin' : ''} />
                  Atualizar
                </button>
              </div>
            </div>

            {/* Gráfico */}
            <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
              {/* Indicador de Intervalo */}
              <div className="flex items-center justify-between mb-3 pb-3 border-b border-gray-200">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                  <span className="text-sm font-medium text-gray-700">
                    Intervalo: {
                      candleInterval === '1s' ? '1 segundo' :
                      candleInterval === '5s' ? '5 segundos' :
                      candleInterval === '10s' ? '10 segundos' :
                      candleInterval === '30s' ? '30 segundos' :
                      candleInterval === '1m' ? '1 minuto' :
                      candleInterval === '5m' ? '5 minutos' :
                      candleInterval === '15m' ? '15 minutos' :
                      candleInterval === '1h' ? '1 hora' :
                      candleInterval === '4h' ? '4 horas' :
                      candleInterval === '1d' ? '1 dia' : candleInterval
                    }
                  </span>
                </div>
                <div className="text-xs text-gray-500">
                  {candles.length} velas carregadas
                </div>
              </div>

              {loading && candles.length === 0 ? (
                <div className="flex items-center justify-center h-96">
                  <div className="text-gray-500">Carregando gráfico...</div>
                </div>
              ) : candles.length > 0 ? (
                <CandlestickChart
                  candles={candles}
                  symbol={asset.symbol}
                  width={600}
                  height={400}
                />
              ) : (
                <div className="flex items-center justify-center h-96">
                  <div className="text-gray-500">Sem dados disponíveis</div>
                </div>
              )}
            </div>
          </div>

          {/* Painel de Trading (1/3) */}
          <div className="lg:col-span-1">
            <div className="bg-gray-50 rounded-lg p-6 sticky top-6">
              {/* Saldo */}
              {investmentAccount && (
                <div className="bg-gradient-to-br from-blue-600 via-blue-700 to-purple-600 text-white rounded-xl p-5 mb-6 shadow-lg border border-blue-400/30">
                  <div className="flex items-center gap-2 mb-2">
                    <IoWallet className="w-6 h-6" />
                    <div className="text-sm font-medium opacity-95">Saldo Disponível</div>
                  </div>
                  <div className="text-3xl font-bold tracking-tight">
                    R$ {investmentAccount.balance?.toFixed(2) || '0.00'}
                  </div>
                </div>
              )}

              {/* Tabs Comprar/Vender */}
              <div className="flex gap-3 mb-6">
                <button
                  onClick={() => setTradeType('buy')}
                  className={`flex-1 py-3 rounded-lg font-bold transition-all ${
                    tradeType === 'buy'
                      ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-lg scale-105'
                      : 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 hover:from-gray-200 hover:to-gray-300'
                  }`}
                >
                  COMPRAR
                </button>
                <button
                  onClick={() => setTradeType('sell')}
                  className={`flex-1 py-3 rounded-lg font-bold transition-all ${
                    tradeType === 'sell'
                      ? 'bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-lg scale-105'
                      : 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 hover:from-gray-200 hover:to-gray-300'
                  }`}
                >
                  VENDER
                </button>
              </div>

              {/* Preço */}
              <div className="mb-4">
                <div className="text-sm text-gray-600 mb-2">Preço Unitário</div>
                <div className="text-2xl font-bold text-gray-800">
                  R$ {currentPrice.toFixed(2)}
                </div>
              </div>

              {/* Quantidade */}
              <div className="mb-4">
                <label className="text-sm text-gray-600 mb-2 block">Quantidade</label>
                <input
                  type="number"
                  min="1"
                  step="1"
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value) || 0)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg text-lg font-semibold focus:outline-none focus:border-blue-500"
                />
              </div>

              {/* Total */}
              <div className={`border-2 border-dashed rounded-lg p-4 mb-6 ${
                tradeType === 'buy' 
                  ? 'bg-green-50 border-green-300' 
                  : 'bg-red-50 border-red-300'
              }`}>
                <div className={`text-sm font-medium mb-1 ${
                  tradeType === 'buy' ? 'text-green-700' : 'text-red-700'
                }`}>Valor Total</div>
                <div className={`text-3xl font-bold ${
                  tradeType === 'buy' ? 'text-green-900' : 'text-red-900'
                }`}>
                  R$ {totalValue.toFixed(2)}
                </div>
              </div>

              {/* Botão Executar */}
              <Button
                onClick={handleTrade}
                disabled={!investmentAccount || quantity <= 0}
                variant={tradeType === 'buy' ? 'success' : 'danger'}
                fullWidth
                className="py-4 text-lg font-bold"
              >
                {tradeType === 'buy' ? (
                  <>
                    <IoCart /> COMPRAR AGORA
                  </>
                ) : (
                  <>
                    <IoArrowDown /> VENDER AGORA
                  </>
                )}
              </Button>

              {!investmentAccount && (
                <p className="text-xs text-yellow-600 mt-2 text-center">
                  ⚠️ Você precisa de uma conta de investimento
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Info */}
        <div className="mt-4 text-sm text-gray-500 text-center">
          📊 Gráfico candlestick (1min) | 🔄 Atualização em tempo real
        </div>
      </div>
    </Modal>
  );
};

export default CandlestickModal;
