import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import { useAuth } from '../hooks/useAuth';
import { useAccounts } from '../hooks/useAccounts';
import Card from '../components/common/Card';
import QuickNav from '../components/common/QuickNav';
import { formatCurrency } from '../utils/formatters';
import { IoTrendingUp, IoTrendingDown, IoWallet, IoCard, IoBusiness } from 'react-icons/io5';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { accounts, loading, getTotalBalance } = useAccounts();

  const totalBalance = getTotalBalance();

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

  const handleQuickAction = (action) => {
    switch(action) {
      case 'Depositar':
        navigate('/transactions', { state: { tab: 'deposit' } });
        break;
      case 'Sacar':
        navigate('/transactions', { state: { tab: 'withdraw' } });
        break;
      case 'Transferir':
        navigate('/transactions', { state: { tab: 'transfer' } });
        break;
      case 'Pagar':
        navigate('/pay-bills');
        break;
      case 'Extrato':
        navigate('/statement');
        break;
      default:
        break;
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <QuickNav />
        {/* Welcome Section */}
        <div>
          <h1 className="text-3xl font-bold text-white">
            Bem-vindo de volta, {user?.full_name?.split(' ')[0]}! 👋
          </h1>
          <p className="text-gray-400 mt-2">
            Aqui está um resumo da sua conta
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="bg-gradient-to-br from-yellow-500 to-yellow-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-900 font-medium">Saldo Total</p>
                <p className="text-3xl font-bold mt-1 text-gray-900">
                  {formatCurrency(totalBalance)}
                </p>
              </div>
              <IoWallet className="w-12 h-12 text-gray-900 opacity-30" />
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 font-medium">Contas Ativas</p>
                <p className="text-3xl font-bold mt-1 text-white">
                  {accounts.length}
                </p>
              </div>
              <IoBusiness className="w-12 h-12 text-gray-600 opacity-30" />
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 font-medium">Receitas</p>
                <p className="text-3xl font-bold mt-1 text-green-400 flex items-center gap-1">
                  <IoTrendingUp className="w-6 h-6" />
                  {formatCurrency(0)}
                </p>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400 font-medium">Despesas</p>
                <p className="text-3xl font-bold mt-1 text-red-400 flex items-center gap-1">
                  <IoTrendingDown className="w-6 h-6" />
                  {formatCurrency(0)}
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Accounts Section */}
        <Card>
          <h2 className="text-xl font-bold text-white mb-4">
            Minhas Contas
          </h2>
          
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500 mx-auto"></div>
            </div>
          ) : accounts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {accounts.map((account) => (
                <div
                  key={account.id}
                  className="p-4 border border-gray-700 rounded-lg hover:border-yellow-500 transition-colors bg-gray-750">
                  <div className="mb-3">
                    <p className="text-xs text-gray-500 mb-1">Tipo</p>
                    <p className="text-lg font-bold text-white">
                      {getAccountTypeName(account.account_type)}
                    </p>
                  </div>
                  <div className="flex items-end justify-between">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Número da Conta</p>
                      <p className="text-sm font-mono text-gray-300">
                        {account.account_number}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-500 mb-1">Saldo Disponível</p>
                      <p className="text-2xl font-bold text-yellow-500">
                        {formatCurrency(account.balance)}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400">
              Você ainda não possui contas
            </div>
          )}
        </Card>

        {/* Quick Actions */}
        <Card>
          <h2 className="text-xl font-bold text-white mb-4">
            Ações Rápidas
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {['Depositar', 'Sacar', 'Transferir', 'Pagar', 'Extrato'].map((action) => (
              <button
                key={action}
                onClick={() => handleQuickAction(action)}
                className="p-4 bg-gray-700 hover:bg-yellow-500 hover:text-gray-900 rounded-lg text-white font-medium transition-colors"
              >
                {action}
              </button>
            ))}
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;
