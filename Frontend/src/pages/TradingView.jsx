import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  IoArrowBack, IoTrendingUp, IoTrendingDown, IoTime, 
  IoStatsChart, IoWallet, IoClose, IoCheckmark,
  IoRefresh, IoExpand, IoContract
} from 'react-icons/io5';
import api from '../services/api';
import toast from 'react-hot-toast';
import CandlestickChart from '../components/investments/CandlestickChart';

/**
 * Página de Trading Profissional com Gráfico de Velas
 * Similar a IQ Option / Quotex
 */
const TradingView = () => {
  const { assetId } = useParams();
  const navigate = useNavigate();
  
  // Estados
  const [asset, setAsset] = useState(null);
  const [candles, setCandles] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [fullscreen, setFullscreen] = useState(false);
  
  // Trading
  const [tradeType, setTradeType] = useState('buy'); // buy ou sell
  const [tradeAmount, setTradeAmount] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [investmentAccount, setInvestmentAccount] = useState(null);
  
  // WebSocket
  const wsRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Carrega dados do ativo
  useEffect(() => {
    loadAssetData();
    loadInvestmentAccount();
  }, [assetId]);

  // Conecta WebSocket
  useEffect(() => {
    connectWebSocket();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [assetId]);

  const loadAssetData = async () => {
    try {
      setLoading(true);

      // Busca dados do ativo
      const assetResponse = await api.get(`/api/v1/investments/assets`);
      const assetData = assetResponse.data.find(a => a.id === parseInt(assetId));
      
      if (!assetData) {
        toast.error('Ativo não encontrado');
        navigate('/investments');
        return;
      }

      setAsset(assetData);

      // Busca velas
      const candlesResponse = await api.get(
        `/api/v1/investments/candles/${assetId}`,
        { params: { interval: '1m', limit: 100 } }
      );
      setCandles(candlesResponse.data.candles || []);

      // Busca resumo
      const summaryResponse = await api.get(
        `/api/v1/investments/candles/${assetId}/summary`,
        { params: { interval: '1m' } }
      );
      setSummary(summaryResponse.data);

    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      toast.error('Erro ao carregar dados do ativo');
    } finally {
      setLoading(false);
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

  const connectWebSocket = () => {
    const wsUrl = import.meta.env.VITE_API_BASE_URL.replace('http', 'ws');
    const ws = new WebSocket(`${wsUrl}/ws/market-feed`);

    ws.onopen = () => {
      console.log('📡 WebSocket conectado');
      setConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'candle_update' && asset && data.symbol === asset.symbol) {
          // Adiciona nova vela
          setCandles(prev => {
            const updated = [...prev, data.candle];
            return updated.slice(-100); // Mantém últimas 100
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

    ws.onerror = () => {
      setConnected(false);
    };

    ws.onclose = () => {
      setConnected(false);
      // Reconecta após 3 segundos
      setTimeout(connectWebSocket, 3000);
    };

    wsRef.current = ws;
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

    try {
      const endpoint = tradeType === 'buy' 
        ? '/api/v1/investments/buy'
        : '/api/v1/investments/sell';

      await api.post(endpoint, {
        account_id: investmentAccount.id,
        asset_id: parseInt(assetId),
        quantity: parseInt(quantity)
      });

      toast.success(
        tradeType === 'buy' 
          ? '✅ Compra realizada com sucesso!' 
          : '✅ Venda realizada com sucesso!'
      );

      // Reset
      setQuantity(1);
      setTradeAmount('');

    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao executar operação');
    }
  };

  const currentPrice = summary?.current_price || asset?.current_price || 0;
  const totalValue = currentPrice * (quantity || 0);
  const priceChange = summary?.price_change_24h || 0;
  const isPositive = priceChange >= 0;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Carregando...</div>
      </div>
    );
  }

  if (!asset) {
    return null;
  }

  return (
    <div className={`min-h-screen bg-gray-900 ${fullscreen ? 'fixed inset-0 z-50' : ''}`}>
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Voltar + Info do Ativo */}
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/investments')}
                className="p-2 hover:bg-gray-700 rounded-lg transition"
              >
                <IoArrowBack className="w-6 h-6 text-gray-400" />
              </button>

              <div>
                <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                  {asset.symbol}
                  <span className={`text-lg ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                    {isPositive ? <IoTrendingUp /> : <IoTrendingDown />}
                  </span>
                </h1>
                <p className="text-sm text-gray-400">{asset.name}</p>
              </div>
            </div>

            {/* Preço Atual + Variação */}
            <div className="text-right">
              <div className="text-3xl font-bold text-white">
                R$ {currentPrice.toFixed(2)}
              </div>
              <div className={`text-sm font-medium ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
                {isPositive ? '+' : ''}{priceChange.toFixed(2)}% (24h)
              </div>
            </div>

            {/* Controles */}
            <div className="flex items-center gap-2">
              {/* Status WebSocket */}
              <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs ${
                connected ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'
              }`}>
                <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400' : 'bg-red-400'}`} />
                {connected ? 'Ao Vivo' : 'Desconectado'}
              </div>

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

              {/* Refresh */}
              <button
                onClick={loadAssetData}
                className="p-2 hover:bg-gray-700 rounded-lg transition"
              >
                <IoRefresh className="w-5 h-5 text-gray-400" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Gráfico (3/4 da tela) */}
          <div className="lg:col-span-3">
            <div className="bg-gray-800 rounded-lg p-6">
              {/* Estatísticas Rápidas */}
              <div className="grid grid-cols-4 gap-4 mb-6">
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Máxima 24h</div>
                  <div className="text-lg font-bold text-green-400">
                    R$ {summary?.high_24?.toFixed(2) || '0.00'}
                  </div>
                </div>
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Mínima 24h</div>
                  <div className="text-lg font-bold text-red-400">
                    R$ {summary?.low_24?.toFixed(2) || '0.00'}
                  </div>
                </div>
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Volume Médio</div>
                  <div className="text-lg font-bold text-blue-400">
                    {summary?.avg_volume?.toLocaleString('pt-BR') || '0'}
                  </div>
                </div>
                <div className="bg-gray-700 rounded-lg p-3">
                  <div className="text-xs text-gray-400 mb-1">Velas</div>
                  <div className="text-lg font-bold text-yellow-400">
                    {candles.length}
                  </div>
                </div>
              </div>

              {/* Gráfico de Velas */}
              {candles.length > 0 ? (
                <CandlestickChart
                  candles={candles}
                  symbol={asset.symbol}
                  width={fullscreen ? 1200 : 900}
                  height={fullscreen ? 700 : 500}
                />
              ) : (
                <div className="flex items-center justify-center h-96 text-gray-500">
                  Carregando gráfico...
                </div>
              )}
            </div>
          </div>

          {/* Painel de Trading (1/4 da tela) */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 rounded-lg p-6 sticky top-6">
              <h2 className="text-xl font-bold text-white mb-4">Negociar</h2>

              {/* Tabs: Comprar / Vender */}
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

              {/* Preço Atual */}
              <div className="bg-gray-700 rounded-lg p-4 mb-4">
                <div className="text-xs text-gray-400 mb-1">Preço Atual</div>
                <div className="text-2xl font-bold text-white">
                  R$ {currentPrice.toFixed(2)}
                </div>
              </div>

              {/* Quantidade */}
              <div className="mb-4">
                <label className="text-sm text-gray-400 mb-2 block">
                  Quantidade
                </label>
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

              {/* Botão de Executar */}
              <button
                onClick={handleTrade}
                disabled={!investmentAccount || quantity <= 0}
                className={`w-full py-4 rounded-lg font-bold text-white text-lg transition disabled:opacity-50 disabled:cursor-not-allowed ${
                  tradeType === 'buy'
                    ? 'bg-green-600 hover:bg-green-700'
                    : 'bg-red-600 hover:bg-red-700'
                }`}
              >
                {tradeType === 'buy' ? '🚀 COMPRAR AGORA' : '💰 VENDER AGORA'}
              </button>

              {!investmentAccount && (
                <p className="text-xs text-yellow-400 mt-2 text-center">
                  ⚠️ Você precisa de uma conta de investimento
                </p>
              )}

              {/* Info adicional */}
              <div className="mt-6 pt-6 border-t border-gray-700">
                <div className="text-xs text-gray-400 space-y-2">
                  <div className="flex justify-between">
                    <span>Tipo:</span>
                    <span className="text-white">{asset.asset_type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Categoria:</span>
                    <span className="text-white">{asset.category}</span>
                  </div>
                  {lastUpdate && (
                    <div className="flex justify-between">
                      <span>Última atualização:</span>
                      <span className="text-green-400">
                        {lastUpdate.toLocaleTimeString('pt-BR')}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TradingView;
