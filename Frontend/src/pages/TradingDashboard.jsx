import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  IoArrowBack, IoTrendingUp, IoTrendingDown, IoSearch, 
  IoStatsChart, IoRefresh, IoExpand, IoContract,
  IoTime, IoClose, IoCheckmark, IoWallet
} from 'react-icons/io5';
import api from '../services/api';
import toast from 'react-hot-toast';
import CandlestickChart from '../components/investments/CandlestickChart';

/**
 * Dashboard de Trading Profissional
 * - Seleção de ações com pesquisa
 * - Atualização automática em tempo real (1s, 5s, 10s, etc)
 * - Intervalos de velas personalizados (1min, 5min, 1h, etc)
 * - Compra/Venda direto no gráfico
 */
const TradingDashboard = () => {
  const navigate = useNavigate();
  const { assetId: urlAssetId } = useParams();
  
  // Estados principais
  const [allAssets, setAllAssets] = useState([]);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [watchlist, setWatchlist] = useState([]); // Watchlist de ações acompanhadas
  const [candles, setCandles] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [fullscreen, setFullscreen] = useState(false);
  
  // Pesquisa e filtros
  const [searchTerm, setSearchTerm] = useState('');
  const [showAssetSelector, setShowAssetSelector] = useState(false);
  
  // Intervalos de atualização
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
  
  // Calcula limite de velas baseado no intervalo
  const getCandleLimit = (interval) => {
    const limitMap = {
      '1s': 60,      // 1 minuto de dados
      '5s': 60,      // 5 minutos de dados
      '10s': 60,     // 10 minutos de dados
      '30s': 60,     // 30 minutos de dados
      '1m': 60,      // 1 hora de dados
      '5m': 60,      // 5 horas de dados
      '15m': 48,     // 12 horas de dados
      '1h': 24,      // 24 horas de dados
      '4h': 24,      // 4 dias de dados
      '1d': 30       // 30 dias de dados
    };
    return limitMap[interval] || 60;
  };
  
  // Trading
  const [tradeType, setTradeType] = useState('buy');
  const [quantity, setQuantity] = useState(1);
  const [investmentAccount, setInvestmentAccount] = useState(null);
  
  // WebSocket e auto-update
  const wsRef = useRef(null);
  const updateTimerRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [autoUpdate, setAutoUpdate] = useState(true);

  // Opções de intervalo de velas
  const candleIntervals = [
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
  ];

  // Carrega todos os ativos ao iniciar
  useEffect(() => {
    loadAllAssets();
    loadInvestmentAccount();
  }, []);

  // Se tem assetId na URL, seleciona automaticamente
  useEffect(() => {
    if (urlAssetId && allAssets.length > 0) {
      const asset = allAssets.find(a => a.id === parseInt(urlAssetId));
      if (asset) {
        handleSelectAsset(asset);
      }
    }
  }, [urlAssetId, allAssets]);

  // Carrega dados quando o ativo ou intervalo muda
  useEffect(() => {
    if (selectedAsset) {
      loadAssetData();
    }
  }, [selectedAsset, candleInterval]);

  // Auto-update baseado no intervalo de velas escolhido
  useEffect(() => {
    if (!selectedAsset || !autoUpdate) return;

    const timer = setInterval(() => {
      loadAssetData(true); // true = silent update (sem loading)
    }, getRefreshInterval(candleInterval));

    updateTimerRef.current = timer;

    return () => {
      if (updateTimerRef.current) {
        clearInterval(updateTimerRef.current);
      }
    };
  }, [selectedAsset, autoUpdate, candleInterval]);

  // WebSocket
  useEffect(() => {
    if (selectedAsset) {
      connectWebSocket();
    }
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [selectedAsset, candleInterval]); // Reconecta quando muda o intervalo

  const loadAllAssets = async () => {
    try {
      const response = await api.get('/api/v1/investments/assets');
      // Filtra apenas ações (não fundos)
      const stocks = response.data.filter(a => a.asset_type === 'STOCK');
      setAllAssets(stocks);
    } catch (error) {
      console.error('Erro ao carregar ativos:', error);
      toast.error('Erro ao carregar ativos');
    }
  };

  const loadInvestmentAccount = async () => {
    try {
      const response = await api.get('/api/v1/accounts');
      const invAccount = response.data.find(acc => acc.account_type === 'INVESTIMENTO');
      setInvestmentAccount(invAccount);
    } catch (error) {
      console.error('Erro ao carregar conta:', error);
    }
  };

  const loadAssetData = async (silent = false) => {
    if (!selectedAsset) return;

    try {
      if (!silent) setLoading(true);

      // Busca velas com intervalo e limite apropriado
      const candlesResponse = await api.get(
        `/api/v1/investments/candles/${selectedAsset.id}`,
        { params: { 
          interval: candleInterval, 
          limit: getCandleLimit(candleInterval) 
        } }
      );
      setCandles(candlesResponse.data.candles || []);

      // Busca resumo
      const summaryResponse = await api.get(
        `/api/v1/investments/candles/${selectedAsset.id}/summary`,
        { params: { interval: candleInterval } }
      );
      setSummary(summaryResponse.data);

      setLastUpdate(new Date());

    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      if (!silent) {
        toast.error('Erro ao carregar dados do ativo');
      }
    } finally {
      if (!silent) setLoading(false);
    }
  };

  const connectWebSocket = () => {
    if (!selectedAsset) return;

    const wsUrl = import.meta.env.VITE_API_BASE_URL.replace('http', 'ws');
    const ws = new WebSocket(`${wsUrl}/ws/market-feed`);

    ws.onopen = () => {
      console.log('📡 WebSocket conectado');
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Atualiza apenas se for o ativo correto E o intervalo correto
        if (data.type === 'candle_update' && 
            data.symbol === selectedAsset.symbol &&
            data.candle.interval === candleInterval) {
          // Adiciona nova vela
          setCandles(prev => {
            const updated = [...prev, data.candle];
            return updated.slice(-getCandleLimit(candleInterval));
          });

          // Atualiza resumo
          setSummary(prev => ({
            ...prev,
            current_price: data.candle.close
          }));

          setLastUpdate(new Date());
        }
      } catch (error) {
        console.error('Erro ao processar WebSocket:', error);
      }
    };

    ws.onerror = () => setConnected(false);
    ws.onclose = () => {
      setConnected(false);
      setTimeout(() => connectWebSocket(), 3000);
    };

    wsRef.current = ws;
  };

  const handleSelectAsset = (asset) => {
    setSelectedAsset(asset);
    setShowAssetSelector(false);
    setSearchTerm('');
    navigate(`/trading/${asset.id}`);
    
    // Adiciona à watchlist se não estiver
    if (!watchlist.find(a => a.id === asset.id)) {
      setWatchlist(prev => [...prev, asset]);
    }
  };

  // Remover da watchlist
  const handleRemoveFromWatchlist = (assetId) => {
    setWatchlist(prev => prev.filter(a => a.id !== assetId));
    // Se remover o ativo atual, não seleciona nenhum
    if (selectedAsset?.id === assetId) {
      setSelectedAsset(null);
      navigate('/trading-dashboard');
    }
  };

  const handleTrade = async () => {
    if (!investmentAccount) {
      toast.error('Você precisa de uma conta de investimento');
      return;
    }

    if (!quantity || quantity <= 0) {
      toast.error('Quantidade inválida');
      return;
    }

    if (!selectedAsset) {
      toast.error('Selecione um ativo');
      return;
    }

    try {
      const endpoint = tradeType === 'buy' 
        ? '/api/v1/investments/buy'
        : '/api/v1/investments/sell';

      await api.post(endpoint, {
        account_id: investmentAccount.id,
        asset_id: selectedAsset.id,
        quantity: parseInt(quantity)
      });

      toast.success(
        tradeType === 'buy' 
          ? '✅ Compra realizada com sucesso!' 
          : '✅ Venda realizada com sucesso!'
      );

      setQuantity(1);

    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao executar operação');
    }
  };

  // Filtra ativos para pesquisa
  const filteredAssets = allAssets.filter(asset => 
    asset.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    asset.symbol.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const currentPrice = summary?.current_price || selectedAsset?.current_price || 0;
  const totalValue = currentPrice * (quantity || 0);
  const priceChange = summary?.price_change_24h || 0;
  const isPositive = priceChange >= 0;

  return (
    <div className={`min-h-screen bg-gray-900 ${fullscreen ? 'fixed inset-0 z-50' : ''}`}>
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between gap-4">
            {/* Voltar */}
            <button
              onClick={() => navigate('/investments')}
              className="p-2 hover:bg-gray-700 rounded-lg transition"
            >
              <IoArrowBack className="w-6 h-6 text-gray-400" />
            </button>

            {/* Watchlist - Abas de Ações Acompanhadas */}
            {watchlist.length > 0 && (
              <div className="flex items-center gap-2">
                {watchlist.map(a => (
                  <div
                    key={a.id}
                    className={`relative group flex items-center gap-2 px-4 py-2 rounded-lg transition cursor-pointer ${
                      selectedAsset?.id === a.id
                        ? 'bg-blue-600 text-white shadow-lg'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                    onClick={() => handleSelectAsset(a)}
                  >
                    <div>
                      <div className="font-semibold text-sm">{a.symbol}</div>
                      <div className="text-xs opacity-75">
                        R$ {(a.current_price || 0).toFixed(2)}
                      </div>
                    </div>
                    
                    {/* Botão Remover */}
                    {watchlist.length > 1 && (
                      <div
                        className="ml-1 opacity-0 group-hover:opacity-100 transition"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRemoveFromWatchlist(a.id);
                        }}
                      >
                        <IoClose className="w-4 h-4 hover:text-red-400" />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Seletor de Ativo */}
            <div className="flex-1 max-w-md relative">
              <button
                onClick={() => setShowAssetSelector(!showAssetSelector)}
                className="w-full bg-gray-700 hover:bg-gray-600 rounded-lg px-4 py-2 text-left transition flex items-center justify-between"
              >
                {selectedAsset ? (
                  <div className="flex items-center gap-3">
                    <IoStatsChart className="w-5 h-5 text-blue-400" />
                    <div>
                      <div className="font-bold text-white">{selectedAsset.symbol}</div>
                      <div className="text-xs text-gray-400">{selectedAsset.name}</div>
                    </div>
                  </div>
                ) : (
                  <div className="text-gray-400">Selecione uma ação...</div>
                )}
                <IoSearch className="w-5 h-5 text-gray-400" />
              </button>

              {/* Dropdown de Ativos */}
              <AnimatePresence>
                {showAssetSelector && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute top-full left-0 right-0 mt-2 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-50 max-h-96 overflow-hidden"
                  >
                    {/* Pesquisa */}
                    <div className="p-3 border-b border-gray-700">
                      <div className="relative">
                        <IoSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                        <input
                          type="text"
                          placeholder="Pesquisar ações..."
                          value={searchTerm}
                          onChange={(e) => setSearchTerm(e.target.value)}
                          className="w-full bg-gray-700 border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-white focus:outline-none focus:border-blue-500"
                          autoFocus
                        />
                      </div>
                    </div>

                    {/* Lista de Ativos */}
                    <div className="overflow-y-auto max-h-80">
                      {filteredAssets.length > 0 ? (
                        filteredAssets.map(asset => (
                          <button
                            key={asset.id}
                            onClick={() => handleSelectAsset(asset)}
                            className="w-full px-4 py-3 hover:bg-gray-700 transition text-left flex items-center justify-between"
                          >
                            <div>
                              <div className="font-semibold text-white">{asset.symbol}</div>
                              <div className="text-xs text-gray-400">{asset.name}</div>
                            </div>
                            <div className="text-right">
                              <div className="text-sm font-bold text-white">
                                R$ {(asset.current_price || 0).toFixed(2)}
                              </div>
                              <div className={`text-xs ${
                                (asset.price_change_percent || 0) >= 0 ? 'text-green-400' : 'text-red-400'
                              }`}>
                                {(asset.price_change_percent || 0) >= 0 ? '+' : ''}{(asset.price_change_percent || 0).toFixed(2)}%
                              </div>
                            </div>
                          </button>
                        ))
                      ) : (
                        <div className="p-8 text-center text-gray-500">
                          Nenhuma ação encontrada
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Preço e Variação */}
            {selectedAsset && (
              <div className="text-right">
                <div className="text-3xl font-bold text-white">
                  R$ {currentPrice.toFixed(2)}
                </div>
                <div className={`text-sm font-medium flex items-center justify-end gap-1 ${
                  isPositive ? 'text-green-400' : 'text-red-400'
                }`}>
                  {isPositive ? <IoTrendingUp /> : <IoTrendingDown />}
                  {isPositive ? '+' : ''}{priceChange.toFixed(2)}% (24h)
                </div>
              </div>
            )}

            {/* Controles */}
            <div className="flex items-center gap-2">
              {/* Status */}
              <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs ${
                connected ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'
              }`}>
                <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                {connected ? 'Ao Vivo' : 'Off'}
              </div>

              {/* Auto-Update Toggle */}
              <button
                onClick={() => setAutoUpdate(!autoUpdate)}
                className={`px-3 py-1 rounded-full text-xs font-medium transition ${
                  autoUpdate 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-400'
                }`}
              >
                Auto {autoUpdate ? 'ON' : 'OFF'}
              </button>

              {/* Fullscreen */}
              <button
                onClick={() => setFullscreen(!fullscreen)}
                className="p-2 hover:bg-gray-700 rounded-lg transition"
              >
                {fullscreen ? (
                  <IoContract className="w-5 h-5 text-gray-400" />
                ) : (
                  <IoExpand className="w-5 h-5 text-gray-400" />
                )}
              </button>

              {/* Refresh Manual */}
              <button
                onClick={() => loadAssetData()}
                className="p-2 hover:bg-gray-700 rounded-lg transition"
              >
                <IoRefresh className="w-5 h-5 text-gray-400" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      {selectedAsset ? (
        <div className={`mx-auto px-4 py-6 ${
          fullscreen ? 'max-w-full' : 'container'
        }`}>
          <div className={`grid gap-6 ${
            fullscreen ? 'grid-cols-1' : 'grid-cols-1 lg:grid-cols-4'
          }`}>
            
            {/* Gráfico (3/4) */}
            <div className={fullscreen ? 'col-span-1' : 'lg:col-span-3'}>
              <div className="bg-gray-800 rounded-lg p-6">
                
                {/* Controles de Intervalo */}
                <div className="mb-6">
                  {/* Indicador de Intervalo */}
                  <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-700">
                    <div className="flex items-center gap-3">
                      <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                      <span className="text-base font-semibold text-white">
                        Intervalo: {
                          candleInterval === '1s' ? '⚡ 1 segundo' :
                          candleInterval === '5s' ? '⚡ 5 segundos' :
                          candleInterval === '10s' ? '⚡ 10 segundos' :
                          candleInterval === '30s' ? '⚡ 30 segundos' :
                          candleInterval === '1m' ? '📊 1 minuto' :
                          candleInterval === '5m' ? '📊 5 minutos' :
                          candleInterval === '15m' ? '📊 15 minutos' :
                          candleInterval === '1h' ? '📊 1 hora' :
                          candleInterval === '4h' ? '📊 4 horas' :
                          candleInterval === '1d' ? '📊 1 dia' : candleInterval
                        }
                      </span>
                    </div>
                    <div className="flex items-center gap-4">
                      <label className="flex items-center gap-2 text-sm text-gray-300 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={autoUpdate}
                          onChange={(e) => setAutoUpdate(e.target.checked)}
                          className="rounded"
                        />
                        Auto-refresh ({getRefreshInterval(candleInterval) / 1000}s)
                      </label>
                      <div className="text-sm text-gray-400">
                        {candles.length} velas carregadas
                      </div>
                    </div>
                  </div>

                  {/* Seletor de Intervalo de Velas */}
                  <div className="bg-gray-700/50 rounded-lg p-4 border-2 border-blue-500/30">
                    <label className="text-base text-white mb-3 flex items-center gap-2 font-bold">
                      🕒 Escolha o Intervalo das Velas:
                      <span className="text-xs text-blue-400 font-normal">(Define o tamanho de cada vela)</span>
                    </label>
                    <div className="flex flex-wrap gap-3">
                      {candleIntervals.map(interval => (
                        <button
                          key={interval.value}
                          onClick={() => setCandleInterval(interval.value)}
                          className={`px-5 py-3 rounded-lg text-sm font-bold transition-all ${
                            candleInterval === interval.value
                              ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/50 scale-110 ring-4 ring-blue-400/50'
                              : 'bg-gray-600 text-gray-200 hover:bg-gray-500 hover:scale-105 border-2 border-gray-500'
                          }`}
                        >
                          {interval.label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Estatísticas */}
                <div className={`grid gap-4 mb-6 ${
                  fullscreen ? 'grid-cols-6' : 'grid-cols-5'
                }`}>
                  <div className="bg-gradient-to-br from-green-900 to-green-800 rounded-lg p-4 border border-green-700">
                    <div className="text-xs text-green-300 mb-1 font-medium">Máxima 24h</div>
                    <div className="text-xl font-bold text-green-200">
                      R$ {(summary?.high_24 || 0).toFixed(2)}
                    </div>
                  </div>
                  <div className="bg-gradient-to-br from-red-900 to-red-800 rounded-lg p-4 border border-red-700">
                    <div className="text-xs text-red-300 mb-1 font-medium">Mínima 24h</div>
                    <div className="text-xl font-bold text-red-200">
                      R$ {(summary?.low_24 || 0).toFixed(2)}
                    </div>
                  </div>
                  <div className="bg-gradient-to-br from-blue-900 to-blue-800 rounded-lg p-4 border border-blue-700">
                    <div className="text-xs text-blue-300 mb-1 font-medium">Volume</div>
                    <div className="text-xl font-bold text-blue-200">
                      {(summary?.avg_volume || 0).toLocaleString('pt-BR')}
                    </div>
                  </div>
                  <div className="bg-gradient-to-br from-yellow-900 to-yellow-800 rounded-lg p-4 border border-yellow-700">
                    <div className="text-xs text-yellow-300 mb-1 font-medium">Velas</div>
                    <div className="text-xl font-bold text-yellow-200">
                      {candles.length}
                    </div>
                  </div>
                  <div className="bg-gradient-to-br from-purple-900 to-purple-800 rounded-lg p-4 border border-purple-700">
                    <div className="text-xs text-purple-300 mb-1 font-medium">Atualizado</div>
                    <div className="text-sm font-bold text-purple-200">
                      {lastUpdate ? lastUpdate.toLocaleTimeString('pt-BR') : '--:--:--'}
                    </div>
                  </div>
                  {fullscreen && (
                    <div className="bg-gradient-to-br from-indigo-900 to-indigo-800 rounded-lg p-4 border border-indigo-700">
                      <div className="text-xs text-indigo-300 mb-1 font-medium">Refresh</div>
                      <div className="text-sm font-bold text-indigo-200">
                        {getRefreshInterval(candleInterval) / 1000}s
                      </div>
                    </div>
                  )}
                </div>

                {/* Gráfico */}
                {loading ? (
                  <div className="flex items-center justify-center h-96 text-gray-500">
                    <div className="text-center">
                      <IoRefresh className="w-12 h-12 mx-auto mb-4 animate-spin" />
                      <div>Carregando gráfico...</div>
                    </div>
                  </div>
                ) : candles.length > 0 ? (
                  <div className="w-full overflow-auto">
                    <CandlestickChart
                      candles={candles}
                      symbol={selectedAsset.symbol}
                      width={fullscreen ? window.innerWidth - 500 : 900}
                      height={fullscreen ? window.innerHeight - 300 : 500}
                    />
                  </div>
                ) : (
                  <div className="flex items-center justify-center h-96 text-gray-500">
                    Sem dados de velas disponíveis
                  </div>
                )}
              </div>
            </div>

            {/* Painel de Trading (1/4) - Esconde em fullscreen */}
            {!fullscreen && (
              <div className="lg:col-span-1">
                <div className="bg-gray-800 rounded-lg p-6 sticky top-6">
                <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                  <IoWallet />
                  Negociar
                </h2>

                {/* Tabs */}
                <div className="flex gap-2 mb-6">
                  <button
                    onClick={() => setTradeType('buy')}
                    className={`flex-1 py-3 rounded-lg font-semibold transition ${
                      tradeType === 'buy'
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                    }`}
                  >
                    COMPRAR
                  </button>
                  <button
                    onClick={() => setTradeType('sell')}
                    className={`flex-1 py-3 rounded-lg font-semibold transition ${
                      tradeType === 'sell'
                        ? 'bg-red-600 text-white'
                        : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                    }`}
                  >
                    VENDER
                  </button>
                </div>

                {/* Preço */}
                <div className="bg-gray-700 rounded-lg p-4 mb-4">
                  <div className="text-xs text-gray-400 mb-1">Preço Atual</div>
                  <div className="text-2xl font-bold text-white">
                    R$ {currentPrice.toFixed(2)}
                  </div>
                </div>

                {/* Quantidade */}
                <div className="mb-4">
                  <label className="text-sm text-gray-400 mb-2 block">Quantidade</label>
                  <input
                    type="number"
                    min="1"
                    step="1"
                    value={quantity}
                    onChange={(e) => setQuantity(parseInt(e.target.value) || 0)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white text-lg font-semibold focus:outline-none focus:border-blue-500"
                  />
                </div>

                {/* Total */}
                <div className="bg-gray-700 rounded-lg p-4 mb-6">
                  <div className="text-xs text-gray-400 mb-1">Valor Total</div>
                  <div className={`text-2xl font-bold ${
                    tradeType === 'buy' ? 'text-green-400' : 'text-red-400'
                  }`}>
                    R$ {totalValue.toFixed(2)}
                  </div>
                </div>

                {/* Botão */}
                <button
                  onClick={handleTrade}
                  disabled={!investmentAccount || quantity <= 0}
                  className={`w-full py-4 rounded-lg font-bold text-white text-lg transition disabled:opacity-50 disabled:cursor-not-allowed ${
                    tradeType === 'buy'
                      ? 'bg-green-600 hover:bg-green-700'
                      : 'bg-red-600 hover:bg-red-700'
                  }`}
                >
                  {tradeType === 'buy' ? '🚀 COMPRAR' : '💰 VENDER'}
                </button>

                {!investmentAccount && (
                  <p className="text-xs text-yellow-400 mt-2 text-center">
                    ⚠️ Conta de investimento necessária
                  </p>
                )}

                {/* Info */}
                <div className="mt-6 pt-6 border-t border-gray-700">
                  <div className="text-xs text-gray-400 space-y-2">
                    <div className="flex justify-between">
                      <span>Categoria:</span>
                      <span className="text-white">{selectedAsset.category}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Intervalo:</span>
                      <span className="text-blue-400 font-medium">{candleInterval}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Auto-Refresh:</span>
                      <span className={`font-medium ${
                        autoUpdate ? 'text-green-400' : 'text-gray-500'
                      }`}>
                        {autoUpdate ? `${getRefreshInterval(candleInterval) / 1000}s` : 'Desativado'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Conexão:</span>
                      <span className={`font-medium ${
                        connected ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {connected ? 'Conectado' : 'Desconectado'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            )}
          </div>
        </div>
      ) : (
        /* Tela Inicial - Sem Ativo Selecionado */
        <div className="flex items-center justify-center min-h-[80vh]">
          <div className="text-center">
            <IoStatsChart className="w-24 h-24 text-gray-600 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-white mb-4">
              Selecione uma Ação para Negociar
            </h2>
            <p className="text-gray-400 mb-8">
              Clique no seletor acima para escolher uma ação e começar a negociar
            </p>
            <button
              onClick={() => setShowAssetSelector(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition"
            >
              Escolher Ação
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TradingDashboard;
