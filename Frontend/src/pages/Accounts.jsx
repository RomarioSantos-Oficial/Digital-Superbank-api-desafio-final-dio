import React, { useState, useEffect } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import { useAccounts } from '../hooks/useAccounts';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Modal from '../components/common/Modal';
import Input from '../components/common/Input';
import QuickNav from '../components/common/QuickNav';
import { useForm } from 'react-hook-form';
import { formatCurrency, formatAccountNumber } from '../utils/formatters';
import { IoAdd } from 'react-icons/io5';

const Accounts = () => {
  const { accounts, loading, createAccount, loadAccounts } = useAccounts();
  const [showModal, setShowModal] = useState(false);
  const [creating, setCreating] = useState(false);
  const { register, handleSubmit, reset } = useForm();

  useEffect(() => {
    loadAccounts();
  }, []);

  const getAccountTypeName = (type) => {
    const types = {
      'CORRENTE': 'Conta Corrente',
      'POUPANCA': 'Poupança',
      'SALARIO': 'Conta Salário',
      'UNIVERSITARIA': 'Conta Universitária',
      'INVESTIMENTO': 'Investimento',
      'EMPRESARIAL': 'Empresarial',
      'BLACK': 'Black'
    };
    return types[type] || type;
  };

  const onSubmit = async (data) => {
    setCreating(true);
    
    const accountData = {
      account_type: data.account_type,
      initial_deposit: parseFloat(data.initial_deposit) || 0
    };
    
    const result = await createAccount(accountData);
    setCreating(false);

    if (result.success) {
      setShowModal(false);
      reset();
      loadAccounts();
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <QuickNav />
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-white">Minhas Contas</h1>
          <Button onClick={() => setShowModal(true)}>
            <IoAdd className="w-5 h-5" />
            Nova Conta
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500 mx-auto"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {accounts.map((account) => (
              <Card key={account.id} hover>
                <div className="space-y-4">
                  <div>
                    <span className="text-sm text-gray-500">Tipo</span>
                    <p className="text-lg font-bold text-white mt-1">
                      {getAccountTypeName(account.account_type)}
                    </p>
                  </div>
                  
                  <div>
                    <span className="text-sm text-gray-500">Número da Conta</span>
                    <p className="font-mono font-semibold text-white mt-1">
                      {account.account_number}
                    </p>
                  </div>

                  <div className="pt-4 border-t border-gray-700">
                    <span className="text-sm text-gray-500">Saldo Disponível</span>
                    <p className="text-2xl font-bold text-yellow-500 mt-1">
                      {formatCurrency(account.balance)}
                    </p>
                  </div>

                  <Button variant="secondary" fullWidth>
                    Ver Detalhes
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}

        <Modal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          title="Criar Nova Conta"
          footer={
            <div className="flex gap-2">
              <Button variant="secondary" onClick={() => setShowModal(false)}>
                Cancelar
              </Button>
              <Button onClick={handleSubmit(onSubmit)} loading={creating}>
                Criar Conta
              </Button>
            </div>
          }
        >
          <form className="space-y-4">
            {accounts.length === 0 && (
              <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3 mb-4">
                <p className="text-yellow-500 text-sm">
                  ℹ️ Sua primeira conta deve ser uma Conta Corrente
                </p>
              </div>
            )}
            
            <div>
              <label className="label">Tipo de Conta</label>
              <select className="input" {...register('account_type', { required: true })}>
                <option value="">Selecione...</option>
                <option value="CORRENTE">Conta Corrente</option>
                {accounts.length > 0 && (
                  <>
                    <option value="POUPANCA">Poupança</option>
                    <option value="SALARIO">Conta Salário</option>
                    <option value="UNIVERSITARIA">Conta Universitária</option>
                    <option value="INVESTIMENTO">Conta Investimento (18+)</option>
                    <option value="EMPRESARIAL">Conta Empresarial (21+)</option>
                    <option value="BLACK">Conta Black (18+)</option>
                  </>
                )}
              </select>
            </div>
            
            <div>
              <label className="label">Depósito Inicial (opcional)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                className="input"
                {...register('initial_deposit')}
              />
            </div>
          </form>
        </Modal>
      </div>
    </DashboardLayout>
  );
};

export default Accounts;
