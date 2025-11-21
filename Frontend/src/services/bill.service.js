import api from './api';

const BILLS_PREFIX = '/api/v1/bills';

/**
 * Pagar conta
 */
export const payBill = async (billData) => {
  const response = await api.post(`${BILLS_PREFIX}/pay`, billData);
  return response.data;
};

/**
 * Obter histórico de pagamentos
 */
export const getBillPaymentHistory = async (accountId = null, limit = 50) => {
  const params = new URLSearchParams();
  if (accountId) params.append('account_id', accountId);
  if (limit) params.append('limit', limit);
  
  const url = `${BILLS_PREFIX}/history${params.toString() ? `?${params.toString()}` : ''}`;
  const response = await api.get(url);
  return response.data;
};

export default {
  payBill,
  getBillPaymentHistory,
};
