import { useContext } from 'react';
import { AccountContext } from '../context/AccountContext';

export const useAccounts = () => {
  const context = useContext(AccountContext);
  
  if (!context) {
    throw new Error('useAccounts must be used within an AccountProvider');
  }
  
  return context;
};
