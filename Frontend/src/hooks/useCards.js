import { useState, useCallback } from 'react';
import * as cardService from '../services/card.service';
import toast from 'react-hot-toast';

export const useCards = () => {
  const [loading, setLoading] = useState(false);
  const [cards, setCards] = useState([]);

  const loadCards = useCallback(async (userId) => {
    setLoading(true);
    try {
      const data = await cardService.getCards(userId);
      setCards(data);
      return { success: true, data };
    } catch (error) {
      toast.error(error.message || 'Erro ao carregar cartões');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const requestCard = useCallback(async (cardData) => {
    setLoading(true);
    try {
      const result = await cardService.requestCard(cardData);
      toast.success('Cartão solicitado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      console.error('Error requesting card:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Erro ao solicitar cartão';
      toast.error(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  }, []);

  const blockCard = useCallback(async (cardId) => {
    setLoading(true);
    try {
      const result = await cardService.blockCard(cardId);
      toast.success('Cartão bloqueado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao bloquear cartão');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const unblockCard = useCallback(async (cardId) => {
    setLoading(true);
    try {
      const result = await cardService.unblockCard(cardId);
      toast.success('Cartão desbloqueado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao desbloquear cartão');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const adjustLimit = useCallback(async (cardId, newLimit) => {
    setLoading(true);
    try {
      const result = await cardService.adjustLimit(cardId, newLimit);
      toast.success('Limite ajustado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao ajustar limite');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const makePurchase = useCallback(async (purchaseData) => {
    setLoading(true);
    try {
      const result = await cardService.makePurchase(purchaseData);
      toast.success('Compra realizada com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao realizar compra');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const payInvoice = useCallback(async (invoiceData) => {
    setLoading(true);
    try {
      const result = await cardService.payInvoice(invoiceData);
      toast.success('Fatura paga com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao pagar fatura');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    cards,
    loadCards,
    requestCard,
    blockCard,
    unblockCard,
    adjustLimit,
    makePurchase,
    payInvoice,
  };
};
