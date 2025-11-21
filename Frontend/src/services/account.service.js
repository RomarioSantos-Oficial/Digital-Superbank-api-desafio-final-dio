import api from './api';

const ACCOUNTS_PREFIX = '/api/v1/accounts/';

/**
 * Cria nova conta
 */
export const createAccount = async (accountData) => {
  const response = await api.post(ACCOUNTS_PREFIX, accountData);
  return response.data;
};

/**
 * Lista todas as contas do usuário
 */
export const getAccounts = async () => {
  const response = await api.get(ACCOUNTS_PREFIX);
  return response.data;
};

/**
 * Obtém detalhes de uma conta específica
 */
export const getAccount = async (accountId) => {
  const response = await api.get(`${ACCOUNTS_PREFIX}/${accountId}`);
  return response.data;
};

/**
 * Obtém saldo de uma conta
 */
export const getAccountBalance = async (accountId) => {
  const response = await api.get(`${ACCOUNTS_PREFIX}/${accountId}/balance`);
  return response.data;
};

/**
 * Atualiza informações da conta
 */
export const updateAccount = async (accountId, accountData) => {
  const response = await api.put(`${ACCOUNTS_PREFIX}/${accountId}`, accountData);
  return response.data;
};

/**
 * Deleta uma conta
 */
export const deleteAccount = async (accountId) => {
  const response = await api.delete(`${ACCOUNTS_PREFIX}/${accountId}`);
  return response.data;
};

export default {
  createAccount,
  getAccounts,
  getAccount,
  getAccountBalance,
  updateAccount,
  deleteAccount,
};
