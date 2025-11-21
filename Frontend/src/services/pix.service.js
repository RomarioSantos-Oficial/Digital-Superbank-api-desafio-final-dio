import api from './api';

const PIX_PREFIX = '/api/v1/pix-keys';

/**
 * Lista todas as chaves PIX do usuário
 */
export const listPixKeys = async (accountId = null) => {
  const params = accountId ? { account_id: accountId } : {};
  const response = await api.get(PIX_PREFIX, { params });
  return response.data;
};

/**
 * Cria uma nova chave PIX
 */
export const createPixKey = async (pixKeyData) => {
  const response = await api.post(PIX_PREFIX, pixKeyData);
  return response.data;
};

/**
 * Obtém detalhes de uma chave PIX específica
 */
export const getPixKey = async (keyId) => {
  const response = await api.get(`${PIX_PREFIX}/${keyId}`);
  return response.data;
};

/**
 * Remove uma chave PIX
 */
export const deletePixKey = async (keyId) => {
  const response = await api.delete(`${PIX_PREFIX}/${keyId}`);
  return response.data;
};

export default {
  listPixKeys,
  createPixKey,
  getPixKey,
  deletePixKey,
};
