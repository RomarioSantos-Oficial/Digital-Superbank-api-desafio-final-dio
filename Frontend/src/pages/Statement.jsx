import React, { useState, useEffect } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import Card from '../components/common/Card';
import QuickNav from '../components/common/QuickNav';
import { useAccounts } from '../hooks/useAccounts';
import { formatCurrency } from '../utils/formatters';
import * as transactionService from '../services/transaction.service';
import { 
  IoArrowDown, 
  IoArrowUp, 
  IoSwapHorizontal,
  IoCard,
  IoTrendingUp,
  IoTrendingDown,
  IoReceipt,
  IoWallet,
  IoFilterOutline,
  IoCalendarOutline,
  IoDownloadOutline
} from 'react-icons/io5';

const Statement = () => {
  const { accounts } = useAccounts();
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [selectedAccount, setSelectedAccount] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [dateRange, setDateRange] = useState('30'); // últimos 30 dias
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);

  const transactionTypes = {
    'DEPOSIT': { label: 'Depósito', icon: IoArrowDown, color: 'green', sign: '+' },
    'WITHDRAWAL': { label: 'Saque', icon: IoArrowUp, color: 'red', sign: '-' },
    'TRANSFER': { label: 'Transferência', icon: IoSwapHorizontal, color: 'blue', sign: '-' },
    'PIX_SEND': { label: 'PIX Enviado', icon: IoSwapHorizontal, color: 'purple', sign: '-' },
    'PIX_RECEIVE': { label: 'PIX Recebido', icon: IoSwapHorizontal, color: 'green', sign: '+' },
    'BILL_PAYMENT': { label: 'Pagamento', icon: IoReceipt, color: 'orange', sign: '-' },
    'CARD_DEBIT': { label: 'Compra Débito', icon: IoCard, color: 'red', sign: '-' },
    'CARD_CREDIT': { label: 'Compra Crédito', icon: IoCard, color: 'yellow', sign: '-' },
    'INVESTMENT_BUY': { label: 'Compra Ativo', icon: IoTrendingUp, color: 'blue', sign: '-' },
    'INVESTMENT_SELL': { label: 'Venda Ativo', icon: IoTrendingDown, color: 'green', sign: '+' }
  };

  useEffect(() => {
    loadTransactions();
    
    // Auto-refresh: atualiza a cada 30 segundos
    const interval = setInterval(() => {
      loadTransactions();
    }, 30000);
    
    return () => clearInterval(interval);
  }, [accounts]);

  useEffect(() => {
    filterTransactions();
  }, [transactions, selectedAccount, selectedType, dateRange]);

  const loadTransactions = async () => {
    if (accounts.length === 0) return;
    
    setLoading(true);
    try {
      // Carrega transações de todas as contas
      const allTransactions = [];
      
      for (const account of accounts) {
        try {
          const accountTransactions = await transactionService.getTransactionHistory(account.id);
          // Adiciona info da conta a cada transação
          const transactionsWithAccount = accountTransactions.map(t => ({
            ...t,
            account_name: getAccountTypeName(account.account_type),
            account_id: account.id
          }));
          allTransactions.push(...transactionsWithAccount);
        } catch (error) {
          console.error(`Erro ao carregar transações da conta ${account.id}:`, error);
        }
      }
      
      // Ordena por data (mais recente primeiro)
      allTransactions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      
      setTransactions(allTransactions);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Erro ao carregar extrato:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterTransactions = () => {
    let filtered = [...transactions];

    // Filtro por conta
    if (selectedAccount !== 'all') {
      filtered = filtered.filter(t => t.account_id === parseInt(selectedAccount));
    }

    // Filtro por tipo
    if (selectedType !== 'all') {
      filtered = filtered.filter(t => t.transaction_type === selectedType);
    }

    // Filtro por data
    if (dateRange !== 'all') {
      const days = parseInt(dateRange);
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - days);
      filtered = filtered.filter(t => new Date(t.created_at) >= cutoffDate);
    }

    setFilteredTransactions(filtered);
  };

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

  const getTransactionIcon = (type) => {
    return transactionTypes[type]?.icon || IoWallet;
  };

  const getTransactionColor = (type) => {
    return transactionTypes[type]?.color || 'gray';
  };

  const getTransactionSign = (type) => {
    return transactionTypes[type]?.sign || '';
  };

  const calculateTotals = () => {
    const totals = {
      income: 0,
      expenses: 0,
      total: 0
    };

    filteredTransactions.forEach(t => {
      const sign = getTransactionSign(t.transaction_type);
      if (sign === '+') {
        totals.income += t.amount;
      } else if (sign === '-') {
        totals.expenses += t.amount;
      }
    });

    totals.total = totals.income - totals.expenses;
    return totals;
  };

  const totals = calculateTotals();

  const exportStatement = () => {
    // Aqui você pode implementar exportação para PDF ou CSV
    console.log('Exportar extrato', filteredTransactions);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <QuickNav />
        
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Extrato Completo</h1>
            <p className="text-gray-400 mt-2">
              Visualize todas as suas transações
              {lastUpdate && (
                <span className="text-xs text-gray-500 ml-2">
                  • Última atualização: {lastUpdate.toLocaleTimeString('pt-BR')}
                </span>
              )}
            </p>
          </div>
          <button
            onClick={exportStatement}
            className="flex items-center gap-2 px-4 py-2 bg-yellow-500 text-gray-900 rounded-lg hover:bg-yellow-600 transition-colors font-medium"
          >
            <IoDownloadOutline className="w-5 h-5" />
            Exportar
          </button>
        </div>

        {/* Resumo */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="bg-gradient-to-br from-green-600 to-green-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white font-medium opacity-90">Entradas</p>
                <p className="text-3xl font-bold mt-1 text-white">
                  {formatCurrency(totals.income)}
                </p>
              </div>
              <IoArrowDown className="w-12 h-12 text-white opacity-30" />
            </div>
          </Card>

          <Card className="bg-gradient-to-br from-red-600 to-red-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white font-medium opacity-90">Saídas</p>
                <p className="text-3xl font-bold mt-1 text-white">
                  {formatCurrency(totals.expenses)}
                </p>
              </div>
              <IoArrowUp className="w-12 h-12 text-white opacity-30" />
            </div>
          </Card>

          <Card className={`bg-gradient-to-br ${totals.total >= 0 ? 'from-blue-600 to-blue-700' : 'from-orange-600 to-orange-700'}`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white font-medium opacity-90">Saldo Período</p>
                <p className="text-3xl font-bold mt-1 text-white">
                  {formatCurrency(totals.total)}
                </p>
              </div>
              <IoWallet className="w-12 h-12 text-white opacity-30" />
            </div>
          </Card>
        </div>

        {/* Filtros */}
        <Card>
          <div className="flex items-center gap-2 mb-4">
            <IoFilterOutline className="w-5 h-5 text-yellow-500" />
            <h2 className="text-lg font-bold text-white">Filtros</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Filtro por Conta */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Conta
              </label>
              <select
                value={selectedAccount}
                onChange={(e) => setSelectedAccount(e.target.value)}
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-yellow-500"
              >
                <option value="all">Todas as Contas</option>
                {accounts.map(account => (
                  <option key={account.id} value={account.id}>
                    {getAccountTypeName(account.account_type)} - {account.account_number}
                  </option>
                ))}
              </select>
            </div>

            {/* Filtro por Tipo */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Tipo de Transação
              </label>
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-yellow-500"
              >
                <option value="all">Todos os Tipos</option>
                {Object.entries(transactionTypes).map(([key, value]) => (
                  <option key={key} value={key}>
                    {value.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Filtro por Período */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Período
              </label>
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-yellow-500"
              >
                <option value="7">Últimos 7 dias</option>
                <option value="30">Últimos 30 dias</option>
                <option value="60">Últimos 60 dias</option>
                <option value="90">Últimos 90 dias</option>
                <option value="all">Todo o período</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Lista de Transações */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-white">
              Transações ({filteredTransactions.length})
            </h2>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500 mx-auto"></div>
              <p className="text-gray-400 mt-4">Carregando transações...</p>
            </div>
          ) : filteredTransactions.length > 0 ? (
            <div className="space-y-3">
              {filteredTransactions.map((transaction, index) => {
                const Icon = getTransactionIcon(transaction.transaction_type);
                const color = getTransactionColor(transaction.transaction_type);
                const sign = getTransactionSign(transaction.transaction_type);
                const typeInfo = transactionTypes[transaction.transaction_type] || {};

                return (
                  <div
                    key={`${transaction.id}-${transaction.account_id}-${index}`}
                    className="flex items-center justify-between p-4 bg-gray-800 rounded-lg hover:bg-gray-750 transition-colors"
                  >
                    <div className="flex items-center gap-4 flex-1">
                      <div className={`w-12 h-12 bg-${color}-900 rounded-full flex items-center justify-center flex-shrink-0`}>
                        <Icon className={`w-6 h-6 text-${color}-300`} />
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="font-medium text-white truncate">
                            {typeInfo.label || transaction.transaction_type}
                          </p>
                          <span className={`text-xs px-2 py-1 rounded bg-${color}-900 text-${color}-300`}>
                            {transaction.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-400 truncate">
                          {transaction.description}
                        </p>
                        <div className="flex items-center gap-3 mt-1">
                          <span className="text-xs text-gray-500">
                            {transaction.account_name}
                          </span>
                          <span className="text-xs text-gray-500">•</span>
                          <span className="text-xs text-gray-500 flex items-center gap-1">
                            <IoCalendarOutline className="w-3 h-3" />
                            {new Date(transaction.created_at).toLocaleDateString('pt-BR', {
                              day: '2-digit',
                              month: 'short',
                              year: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="text-right flex-shrink-0">
                      <p className={`text-lg font-bold ${sign === '+' ? 'text-green-400' : 'text-red-400'}`}>
                        {sign}{formatCurrency(transaction.amount)}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-12">
              <IoReceipt className="w-16 h-16 text-gray-600 mx-auto mb-4 opacity-50" />
              <p className="text-gray-400">Nenhuma transação encontrada</p>
              <p className="text-sm text-gray-500 mt-2">
                Ajuste os filtros para ver mais resultados
              </p>
            </div>
          )}
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default Statement;
