import api from './api';
import { objectToQueryString } from '../utils/helpers';

const INVESTMENTS_PREFIX = '/api/v1/investments';

/**
 * Lista todos os ativos disponíveis
 */
export const getAssets = async (filters = {}) => {
  const queryString = objectToQueryString(filters);
  const url = queryString 
    ? `${INVESTMENTS_PREFIX}/assets?${queryString}`
    : `${INVESTMENTS_PREFIX}/assets`;
  
  const response = await api.get(url);
  return response.data;
};

/**
 * Obtém detalhes de um ativo específico
 */
export const getAsset = async (assetId) => {
  const response = await api.get(`${INVESTMENTS_PREFIX}/assets/${assetId}`);
  return response.data;
};

/**
 * Compra ativo
 */
export const buyAsset = async (purchaseData) => {
  const response = await api.post(`${INVESTMENTS_PREFIX}/buy`, purchaseData);
  return response.data;
};

/**
 * Vende ativo
 */
export const sellAsset = async (saleData) => {
  const response = await api.post(`${INVESTMENTS_PREFIX}/sell`, saleData);
  return response.data;
};

/**
 * Obtém portfólio do usuário
 */
export const getPortfolio = async (accountId) => {
  const response = await api.get(`${INVESTMENTS_PREFIX}/portfolio?account_id=${accountId}`);
  return response.data;
};

/**
 * Obtém resumo do portfólio
 */
export const getPortfolioSummary = async (accountId) => {
  const response = await api.get(`${INVESTMENTS_PREFIX}/portfolio/summary?account_id=${accountId}`);
  return response.data;
};

/**
 * Obtém histórico de preços de um ativo
 */
export const getAssetHistory = async (symbol, days = 30) => {
  const response = await api.get(
    `${INVESTMENTS_PREFIX}/assets/${symbol}/history?days=${days}`
  );
  return response.data;
};

/**
 * Conecta ao WebSocket de preços em tempo real
 */
export const connectToMarketFeed = (onMessage, onError) => {
  const wsUrl = import.meta.env.VITE_API_BASE_URL.replace('http', 'ws');
  const ws = new WebSocket(`${wsUrl}/ws/market-feed`);
  
  ws.onopen = () => {
    console.log('📡 Conectado ao feed de mercado');
  };
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (error) {
      console.error('Erro ao processar mensagem WebSocket:', error);
    }
  };
  
  ws.onerror = (error) => {
    console.error('Erro no WebSocket:', error);
    if (onError) onError(error);
  };
  
  ws.onclose = () => {
    console.log('📡 Desconectado do feed de mercado');
  };
  
  return ws;
};

export default {
  getAssets,
  getAsset,
  buyAsset,
  sellAsset,
  getPortfolio,
  getPortfolioSummary,
  getAssetHistory,
  connectToMarketFeed,
};
