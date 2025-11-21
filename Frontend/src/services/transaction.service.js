import api from './api';
import { objectToQueryString } from '../utils/helpers';

const TRANSACTIONS_PREFIX = '/api/v1/transactions';

/**
 * Realiza depósito
 */
export const deposit = async (depositData) => {
  const response = await api.post(`${TRANSACTIONS_PREFIX}/deposit`, depositData);
  return response.data;
};

/**
 * Realiza saque
 */
export const withdraw = async (withdrawData) => {
  const response = await api.post(`${TRANSACTIONS_PREFIX}/withdraw`, withdrawData);
  return response.data;
};

/**
 * Realiza transferência
 */
export const transfer = async (transferData) => {
  const response = await api.post(`${TRANSACTIONS_PREFIX}/transfer`, transferData);
  return response.data;
};

/**
 * Envia PIX
 */
export const sendPix = async (pixData) => {
  const response = await api.post(`${TRANSACTIONS_PREFIX}/pix/send`, pixData);
  return response.data;
};

/**
 * Recebe PIX
 */
export const receivePix = async (pixData) => {
  const response = await api.post(`${TRANSACTIONS_PREFIX}/pix/receive`, pixData);
  return response.data;
};

/**
 * Paga boleto
 */
export const payBill = async (billData) => {
  const response = await api.post(`${TRANSACTIONS_PREFIX}/pay-bill`, billData);
  return response.data;
};

/**
 * Obtém extrato
 */
export const getStatement = async (accountId, filters = {}) => {
  const queryString = objectToQueryString({
    account_id: accountId,
    ...filters,
  });
  
  const response = await api.get(`${TRANSACTIONS_PREFIX}/statement?${queryString}`);
  return response.data;
};

/**
 * Obtém histórico de transações de uma conta
 */
export const getTransactionHistory = async (accountId, limit = 100) => {
  const response = await api.get(`${TRANSACTIONS_PREFIX}/statement?account_id=${accountId}&limit=${limit}`);
  return response.data.transactions || [];
};

/**
 * Agenda transação
 */
export const scheduleTransaction = async (transactionData) => {
  const response = await api.post(`${TRANSACTIONS_PREFIX}/schedule`, transactionData);
  return response.data;
};

/**
 * Lista transações agendadas
 */
export const getScheduledTransactions = async (accountId) => {
  const response = await api.get(`${TRANSACTIONS_PREFIX}/scheduled?account_id=${accountId}`);
  return response.data;
};

/**
 * Cancela transação agendada
 */
export const cancelScheduledTransaction = async (transactionId) => {
  const response = await api.delete(`${TRANSACTIONS_PREFIX}/scheduled/${transactionId}`);
  return response.data;
};

export default {
  deposit,
  withdraw,
  transfer,
  sendPix,
  receivePix,
  payBill,
  getStatement,
  getTransactionHistory,
  scheduleTransaction,
  getScheduledTransactions,
  cancelScheduledTransaction,
};
