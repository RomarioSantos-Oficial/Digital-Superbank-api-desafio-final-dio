import React, { createContext, useState, useEffect, useContext } from 'react';
import { AuthContext } from './AuthContext';
import * as accountService from '../services/account.service';
import toast from 'react-hot-toast';

export const AccountContext = createContext();

export const AccountProvider = ({ children }) => {
  const { user, isAuthenticated } = useContext(AuthContext);
  const [accounts, setAccounts] = useState([]);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated()) {
      loadAccounts();
    } else {
      setAccounts([]);
      setSelectedAccount(null);
    }
  }, [user]);

  const loadAccounts = async () => {
    setLoading(true);
    try {
      const data = await accountService.getAccounts();
      setAccounts(data);
      
      // Seleciona primeira conta por padrão
      if (data.length > 0 && !selectedAccount) {
        setSelectedAccount(data[0]);
      }
    } catch (error) {
      console.error('Error loading accounts:', error);
      toast.error('Erro ao carregar contas');
    } finally {
      setLoading(false);
    }
  };

  const createAccount = async (accountData) => {
    try {
      const newAccount = await accountService.createAccount(accountData);
      
      setAccounts([...accounts, newAccount]);
      
      toast.success('Conta criada com sucesso!');
      return { success: true, data: newAccount };
    } catch (error) {
      console.error('Error creating account:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Erro ao criar conta';
      toast.error(errorMsg);
      return { success: false, error: errorMsg };
    }
  };

  const getAccountBalance = async (accountId) => {
    try {
      const balance = await accountService.getAccountBalance(accountId);
      return { success: true, data: balance };
    } catch (error) {
      console.error('Error getting balance:', error);
      return { success: false, error: error.message };
    }
  };

  const refreshAccount = async (accountId) => {
    try {
      const updatedAccount = await accountService.getAccount(accountId);
      
      setAccounts(accounts.map(acc => 
        acc.id === accountId ? updatedAccount : acc
      ));
      
      if (selectedAccount?.id === accountId) {
        setSelectedAccount(updatedAccount);
      }
      
      return { success: true, data: updatedAccount };
    } catch (error) {
      console.error('Error refreshing account:', error);
      return { success: false, error: error.message };
    }
  };

  const getTotalBalance = () => {
    return accounts.reduce((total, account) => total + (account.balance || 0), 0);
  };

  const value = {
    accounts,
    selectedAccount,
    setSelectedAccount,
    loading,
    loadAccounts,
    createAccount,
    getAccountBalance,
    refreshAccount,
    getTotalBalance,
  };

  return <AccountContext.Provider value={value}>{children}</AccountContext.Provider>;
};
