import api from './api';

const CHATBOT_PREFIX = '/api/v1/chatbot';

/**
 * Envia mensagem para o chatbot
 */
export const sendMessage = async (message, sessionId = null) => {
  const response = await api.post(`${CHATBOT_PREFIX}/message`, {
    message,
    session_id: sessionId
  });
  return response.data;
};

/**
 * Obtém histórico de uma conversa
 */
export const getChatHistory = async (sessionId) => {
  const response = await api.get(`${CHATBOT_PREFIX}/history/${sessionId}`);
  return response.data;
};

/**
 * Envia feedback sobre uma resposta
 */
export const submitFeedback = async (messageId, isHelpful, comment = null) => {
  const response = await api.post(`${CHATBOT_PREFIX}/feedback`, {
    message_id: messageId,
    is_helpful: isHelpful,
    comment
  });
  return response.data;
};

/**
 * Obtém perguntas populares/sugestões
 */
export const getPopularQuestions = async (limit = 5) => {
  const response = await api.get(`${CHATBOT_PREFIX}/suggestions`, {
    params: { limit }
  });
  return response.data;
};

/**
 * Obtém estatísticas do chatbot
 */
export const getChatbotStats = async () => {
  const response = await api.get(`${CHATBOT_PREFIX}/stats`);
  return response.data;
};

export default {
  sendMessage,
  getChatHistory,
  submitFeedback,
  getPopularQuestions,
  getChatbotStats,
};
