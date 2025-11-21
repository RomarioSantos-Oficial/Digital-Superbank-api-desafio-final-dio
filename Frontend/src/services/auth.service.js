import api from './api';

const AUTH_PREFIX = '/api/v1/auth';

/**
 * Faz login do usuário
 */
export const login = async (credentials) => {
  // O backend espera identifier (pode ser email, CPF ou número da conta) e password
  const response = await api.post(`${AUTH_PREFIX}/login`, {
    identifier: credentials.username || credentials.email,
    password: credentials.password
  });
  
  return response.data;
};

/**
 * Registra novo usuário
 */
export const register = async (userData) => {
  const response = await api.post(`${AUTH_PREFIX}/register`, userData);
  return response.data;
};

/**
 * Obtém informações do usuário atual
 */
export const getCurrentUser = async () => {
  const response = await api.get(`${AUTH_PREFIX}/me`);
  return response.data;
};

/**
 * Atualiza informações do usuário
 */
export const updateUser = async (userId, userData) => {
  const response = await api.put(`${AUTH_PREFIX}/users/${userId}`, userData);
  return response.data;
};

/**
 * Altera senha do usuário
 */
export const changePassword = async (userId, passwordData) => {
  const response = await api.put(
    `${AUTH_PREFIX}/users/${userId}/password`,
    passwordData
  );
  return response.data;
};

/**
 * Faz logout (limpa token local)
 */
export const logout = () => {
  // O logout é feito apenas no cliente
  // Limpa token e dados do usuário no localStorage
  return Promise.resolve();
};

export default {
  login,
  register,
  getCurrentUser,
  updateUser,
  changePassword,
  logout,
};
