import { useState, useCallback, useEffect } from 'react';
import * as investmentService from '../services/investment.service';
import toast from 'react-hot-toast';

export const useInvestments = () => {
  const [loading, setLoading] = useState(false);
  const [assets, setAssets] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [marketFeed, setMarketFeed] = useState(null);

  const loadAssets = useCallback(async (filters) => {
    setLoading(true);
    try {
      const data = await investmentService.getAssets(filters);
      setAssets(data);
      return { success: true, data };
    } catch (error) {
      toast.error(error.message || 'Erro ao carregar ativos');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const loadPortfolio = useCallback(async (userId) => {
    setLoading(true);
    try {
      const data = await investmentService.getPortfolio(userId);
      setPortfolio(data);
      return { success: true, data };
    } catch (error) {
      toast.error(error.message || 'Erro ao carregar portfólio');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const buyAsset = useCallback(async (purchaseData) => {
    setLoading(true);
    try {
      const result = await investmentService.buyAsset(purchaseData);
      toast.success('Ativo comprado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao comprar ativo');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const sellAsset = useCallback(async (saleData) => {
    setLoading(true);
    try {
      const result = await investmentService.sellAsset(saleData);
      toast.success('Ativo vendido com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao vender ativo');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const connectToMarketFeed = useCallback(() => {
    const ws = investmentService.connectToMarketFeed(
      (data) => {
        setMarketFeed(data);
        
        // Atualiza preços dos ativos em tempo real
        if (data.type === 'price_update') {
          setAssets(prevAssets =>
            prevAssets.map(asset =>
              asset.symbol === data.symbol
                ? { ...asset, current_price: data.price }
                : asset
            )
          );
        }
      },
      (error) => {
        console.error('WebSocket error:', error);
      }
    );
    
    return ws;
  }, []);

  return {
    loading,
    assets,
    portfolio,
    marketFeed,
    loadAssets,
    loadPortfolio,
    buyAsset,
    sellAsset,
    connectToMarketFeed,
  };
};
