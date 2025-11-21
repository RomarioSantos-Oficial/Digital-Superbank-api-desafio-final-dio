import axios from 'axios';
import { API_BASE_URL, STORAGE_KEYS } from '../utils/constants';
import { storage } from '../utils/helpers';

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de requisição - adiciona token
api.interceptors.request.use(
  (config) => {
    const token = storage.get(STORAGE_KEYS.TOKEN);
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de resposta - trata erros
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Erro da API
      const { status, data } = error.response;
      
      if (status === 401) {
        // Token inválido ou expirado - fazer logout
        storage.remove(STORAGE_KEYS.TOKEN);
        storage.remove(STORAGE_KEYS.USER);
        window.location.href = '/login';
      }
      
      // Extrair mensagem de erro
      let message = 'Erro ao processar requisição';
      
      if (typeof data === 'string') {
        message = data;
      } else if (data?.detail) {
        // Pode ser string ou array de erros de validação
        if (typeof data.detail === 'string') {
          message = data.detail;
        } else if (Array.isArray(data.detail)) {
          // Erros de validação do Pydantic
          message = data.detail.map(err => {
            if (typeof err === 'string') return err;
            if (err.msg) return `${err.loc?.[1] || 'Campo'}: ${err.msg}`;
            return JSON.stringify(err);
          }).join(', ');
        }
      } else if (data?.message) {
        message = data.message;
      }
      
      // Retorna mensagem de erro da API
      return Promise.reject({
        status,
        message,
        data,
      });
    } else if (error.request) {
      // Sem resposta do servidor
      return Promise.reject({
        status: 0,
        message: 'Sem conexão com o servidor',
        data: null,
      });
    } else {
      // Erro na configuração da requisição
      return Promise.reject({
        status: 0,
        message: error.message || 'Erro desconhecido',
        data: null,
      });
    }
  }
);

export default api;
