import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import QuickNav from '../components/common/QuickNav';
import { useTransactions } from '../hooks/useTransactions';
import { useAccounts } from '../hooks/useAccounts';
import { useForm } from 'react-hook-form';
import { formatCurrency, formatDateTime } from '../utils/formatters';
import { IoWallet, IoArrowDown, IoArrowUp, IoSwapHorizontal, IoFlash } from 'react-icons/io5';

const Transactions = () => {
  const location = useLocation();
  const { accounts, loadAccounts } = useAccounts();
  const { deposit, withdraw, transfer, transactions, getStatement, loading } = useTransactions();
  const [activeTab, setActiveTab] = useState('deposit');
  const { register, handleSubmit, reset } = useForm();

  // Define a aba ativa baseado no state da navegação
  useEffect(() => {
    if (location.state?.tab) {
      setActiveTab(location.state.tab);
    }
  }, [location]);

  const onSubmit = async (data) => {
    let result;
    
    if (activeTab === 'deposit') {
      result = await deposit({
        account_id: parseInt(data.account_id),
        amount: parseFloat(data.amount),
      });
    } else if (activeTab === 'withdraw') {
      result = await withdraw({
        account_id: parseInt(data.account_id),
        amount: parseFloat(data.amount),
      });
    } else if (activeTab === 'transfer') {
      result = await transfer({
        from_account_id: parseInt(data.from_account_id),
        to_account_number: data.to_account_number,
        amount: parseFloat(data.amount),
      });
    } else if (activeTab === 'pix') {
      result = await transfer({
        from_account_id: parseInt(data.from_account_id),
        to_account_number: data.pix_key,
        amount: parseFloat(data.amount),
      });
    }

    if (result?.success) {
      reset();
      // Recarrega as contas para atualizar os saldos
      loadAccounts();
    }
  };

  const tabs = [
    { id: 'deposit', label: 'Depósito', icon: IoArrowDown },
    { id: 'withdraw', label: 'Saque', icon: IoArrowUp },
    { id: 'transfer', label: 'Transferência', icon: IoSwapHorizontal },
    { id: 'pix', label: 'PIX', icon: IoFlash },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <QuickNav />
        <h1 className="text-3xl font-bold text-white">Transações</h1>

        <Card>
          <div className="flex border-b border-gray-200 mb-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-3 border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-yellow-500 text-yellow-500 font-medium'
                    : 'border-transparent text-gray-400 hover:text-yellow-500'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {activeTab === 'transfer' ? (
              <>
                <div>
                  <label className="label">Conta de Origem</label>
                  <select className="input" {...register('from_account_id', { required: true })}>
                    <option value="">Selecione...</option>
                    {accounts.map((acc) => (
                      <option key={acc.id} value={acc.id}>
                        {acc.account_number} - {formatCurrency(acc.balance)}
                      </option>
                    ))}
                  </select>
                </div>

                <Input
                  label="Conta de Destino"
                  placeholder="000000-0"
                  {...register('to_account_number', { required: true })}
                />

                <Input
                  label="Valor"
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                  {...register('amount', { required: true, min: 0.01 })}
                />
              </>
            ) : activeTab === 'pix' ? (
              <>
                <div>
                  <label className="label">Conta de Origem</label>
                  <select className="input" {...register('from_account_id', { required: true })}>
                    <option value="">Selecione...</option>
                    {accounts.map((acc) => (
                      <option key={acc.id} value={acc.id}>
                        {acc.account_number} - {formatCurrency(acc.balance)}
                      </option>
                    ))}
                  </select>
                </div>

                <Input
                  label="Chave PIX"
                  placeholder="CPF, E-mail, Telefone ou Chave Aleatória"
                  {...register('pix_key', { required: true })}
                />

                <Input
                  label="Valor"
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                  {...register('amount', { required: true, min: 0.01 })}
                />
              </>
            ) : (
              <>
                <div>
                  <label className="label">Conta</label>
                  <select className="input" {...register('account_id', { required: true })}>
                    <option value="">Selecione...</option>
                    {accounts.map((acc) => (
                      <option key={acc.id} value={acc.id}>
                        {acc.account_number} - {formatCurrency(acc.balance)}
                      </option>
                    ))}
                  </select>
                </div>

                <Input
                  label="Valor"
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                  {...register('amount', { required: true, min: 0.01 })}
                />
              </>
            )}

            <Button type="submit" fullWidth loading={loading}>
              Confirmar {activeTab === 'deposit' ? 'Depósito' : activeTab === 'withdraw' ? 'Saque' : activeTab === 'pix' ? 'PIX' : 'Transferência'}
            </Button>
          </form>
        </Card>

        <Card>
          <h2 className="text-xl font-bold text-white mb-4">Histórico de Transações</h2>
          <div className="space-y-2">
            {transactions.length > 0 ? (
              transactions.map((txn, idx) => (
                <div key={idx} className="p-4 border border-gray-700 rounded-lg flex items-center justify-between bg-gray-700">
                  <div>
                    <p className="font-medium text-white">{txn.transaction_type}</p>
                    <p className="text-sm text-gray-400">{formatDateTime(txn.created_at)}</p>
                  </div>
                  <p className="text-lg font-bold text-yellow-500">
                    {formatCurrency(txn.amount)}
                  </p>
                </div>
              ))
            ) : (
              <p className="text-center py-8 text-gray-400">Nenhuma transação encontrada</p>
            )}
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default Transactions;
