import { useState, useCallback } from 'react';
import * as transactionService from '../services/transaction.service';
import toast from 'react-hot-toast';

export const useTransactions = () => {
  const [loading, setLoading] = useState(false);
  const [transactions, setTransactions] = useState([]);

  const deposit = useCallback(async (depositData) => {
    setLoading(true);
    try {
      const result = await transactionService.deposit(depositData);
      toast.success('Depósito realizado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao realizar depósito');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const withdraw = useCallback(async (withdrawData) => {
    setLoading(true);
    try {
      const result = await transactionService.withdraw(withdrawData);
      toast.success('Saque realizado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao realizar saque');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const transfer = useCallback(async (transferData) => {
    setLoading(true);
    try {
      const result = await transactionService.transfer(transferData);
      toast.success('Transferência realizada com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao realizar transferência');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const sendPix = useCallback(async (pixData) => {
    setLoading(true);
    try {
      const result = await transactionService.sendPix(pixData);
      toast.success('PIX enviado com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao enviar PIX');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const payBill = useCallback(async (billData) => {
    setLoading(true);
    try {
      const result = await transactionService.payBill(billData);
      toast.success('Boleto pago com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao pagar boleto');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const getStatement = useCallback(async (accountId, filters) => {
    setLoading(true);
    try {
      const result = await transactionService.getStatement(accountId, filters);
      setTransactions(result.transactions || []);
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao carregar extrato');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  const scheduleTransaction = useCallback(async (transactionData) => {
    setLoading(true);
    try {
      const result = await transactionService.scheduleTransaction(transactionData);
      toast.success('Transação agendada com sucesso!');
      return { success: true, data: result };
    } catch (error) {
      toast.error(error.message || 'Erro ao agendar transação');
      return { success: false, error: error.message };
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    transactions,
    deposit,
    withdraw,
    transfer,
    sendPix,
    payBill,
    getStatement,
    scheduleTransaction,
  };
};
