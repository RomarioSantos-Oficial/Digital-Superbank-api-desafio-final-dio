import api from './api';

const CARDS_PREFIX = '/api/v1/credit-cards/';

/**
 * Solicita novo cartão
 */
export const requestCard = async (cardData) => {
  const response = await api.post(CARDS_PREFIX, cardData);
  return response.data;
};

/**
 * Lista todos os cartões do usuário
 */
export const getCards = async (userId) => {
  const response = await api.get(`${CARDS_PREFIX}?user_id=${userId}`);
  return response.data;
};

/**
 * Obtém detalhes de um cartão específico
 */
export const getCard = async (cardId) => {
  const response = await api.get(`${CARDS_PREFIX}${cardId}`);
  return response.data;
};

/**
 * Bloqueia cartão
 */
export const blockCard = async (cardId) => {
  const response = await api.post(`${CARDS_PREFIX}${cardId}/block`);
  return response.data;
};

/**
 * Desbloqueia cartão
 */
export const unblockCard = async (cardId) => {
  const response = await api.post(`${CARDS_PREFIX}${cardId}/unblock`);
  return response.data;
};

/**
 * Cancela cartão
 */
export const cancelCard = async (cardId) => {
  const response = await api.delete(`${CARDS_PREFIX}${cardId}`);
  return response.data;
};

/**
 * Ajusta limite do cartão
 */
export const adjustLimit = async (cardId, newLimit) => {
  const response = await api.put(`${CARDS_PREFIX}${cardId}/limit`, {
    new_limit: newLimit,
  });
  return response.data;
};

/**
 * Realiza compra com cartão
 */
export const makePurchase = async (purchaseData) => {
  const response = await api.post(`${CARDS_PREFIX}/purchase`, purchaseData);
  return response.data;
};

/**
 * Paga fatura do cartão
 */
export const payInvoice = async (invoiceData) => {
  const response = await api.post(`${CARDS_PREFIX}/pay-invoice`, invoiceData);
  return response.data;
};

/**
 * Obtém histórico de uso do cartão
 */
export const getCardHistory = async (cardId) => {
  const response = await api.get(`${CARDS_PREFIX}${cardId}/history`);
  return response.data;
};

/**
 * Obtém CVV do cartão (temporário)
 */
export const getCVV = async (cardId) => {
  const response = await api.get(`${CARDS_PREFIX}${cardId}/cvv`);
  return response.data;
};

/**
 * Gera cartão virtual
 */
export const generateVirtualCard = async (userId) => {
  const response = await api.post(`${CARDS_PREFIX}/virtual`, { user_id: userId });
  return response.data;
};

export default {
  requestCard,
  getCards,
  getCard,
  blockCard,
  unblockCard,
  cancelCard,
  adjustLimit,
  makePurchase,
  payInvoice,
  getCardHistory,
  getCVV,
  generateVirtualCard,
};
