import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { IoNotifications, IoClose, IoCheckmark, IoTime, IoWallet, IoArrowDown, IoArrowUp } from 'react-icons/io5';
import { formatCurrency, formatDate } from '../../utils/formatters';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const NotificationBell = () => {
  const { user } = useAuth();
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [lastCheckTime, setLastCheckTime] = useState(null);

  useEffect(() => {
    if (user) {
      loadNotifications();
      // Atualizar notificações a cada 15 segundos
      const interval = setInterval(loadNotifications, 15000);
      return () => clearInterval(interval);
    }
  }, [user]);

  const loadNotifications = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token || !user) return;

      // Buscar todas as contas do usuário
      const accountsResponse = await api.get('/api/v1/accounts');
      const userAccounts = accountsResponse.data;

      // Buscar transações recentes de todas as contas (últimas 24 horas)
      const oneDayAgo = new Date();
      oneDayAgo.setDate(oneDayAgo.getDate() - 1);

      const allTransactions = [];
      for (const account of userAccounts) {
        try {
          const response = await api.get('/api/v1/transactions/statement', {
            params: { 
              account_id: account.id,
              limit: 50 
            }
          });
          if (response.data && response.data.transactions) {
            allTransactions.push(...response.data.transactions.map(t => ({
              ...t,
              accountNumber: account.account_number,
              accountType: account.account_type
            })));
          }
        } catch (err) {
          console.error(`Erro ao buscar transações da conta ${account.id}:`, err);
        }
      }

      // Filtrar transações das últimas 24 horas
      const recentTransactions = allTransactions.filter(t => {
        const transactionDate = new Date(t.created_at);
        return transactionDate >= oneDayAgo;
      });

      // Converter transações em notificações
      const transactionNotifications = recentTransactions.map(transaction => {
        const isCredit = transaction.transaction_type === 'DEPOSIT' || 
                        transaction.transaction_type === 'TRANSFER' && transaction.to_account_id;
        const isDebit = transaction.transaction_type === 'WITHDRAWAL' || 
                       transaction.transaction_type === 'TRANSFER' && transaction.from_account_id ||
                       transaction.transaction_type === 'PIX_SEND' ||
                       transaction.transaction_type === 'BILL_PAYMENT';

        let title = '';
        let message = '';
        let color = '';
        let icon = IoWallet;

        switch (transaction.transaction_type) {
          case 'DEPOSIT':
            title = 'Depósito recebido';
            message = `${formatCurrency(transaction.amount)} na conta ${transaction.accountNumber}`;
            color = 'green';
            icon = IoArrowDown;
            break;
          case 'WITHDRAWAL':
            title = 'Saque realizado';
            message = `${formatCurrency(transaction.amount)} da conta ${transaction.accountNumber}`;
            color = 'red';
            icon = IoArrowUp;
            break;
          case 'TRANSFER':
            if (isCredit) {
              title = 'Transferência recebida';
              message = `${formatCurrency(transaction.amount)} na conta ${transaction.accountNumber}`;
              color = 'green';
              icon = IoArrowDown;
            } else {
              title = 'Transferência enviada';
              message = `${formatCurrency(transaction.amount)} da conta ${transaction.accountNumber}`;
              color = 'blue';
              icon = IoArrowUp;
            }
            break;
          case 'PIX_SEND':
            title = 'PIX enviado';
            message = `${formatCurrency(transaction.amount)} da conta ${transaction.accountNumber}`;
            color = 'purple';
            icon = IoArrowUp;
            break;
          case 'PIX_RECEIVE':
            title = 'PIX recebido';
            message = `${formatCurrency(transaction.amount)} na conta ${transaction.accountNumber}`;
            color = 'green';
            icon = IoArrowDown;
            break;
          case 'BILL_PAYMENT':
            title = 'Pagamento realizado';
            message = `${formatCurrency(transaction.amount)} da conta ${transaction.accountNumber}`;
            color = 'orange';
            icon = IoCheckmark;
            break;
          default:
            title = 'Transação';
            message = `${formatCurrency(transaction.amount)}`;
            color = 'gray';
        }

        if (transaction.description && transaction.description !== 'Transferência') {
          message += ` - ${transaction.description}`;
        }

        return {
          id: `transaction-${transaction.id}`,
          type: 'transaction',
          title,
          message,
          timestamp: new Date(transaction.created_at),
          read: false,
          icon,
          color,
          transactionId: transaction.id
        };
      });

      // Carregar notificações já lidas do localStorage
      const savedNotifications = localStorage.getItem(`notifications_${user.id}`);
      const readNotificationIds = savedNotifications ? JSON.parse(savedNotifications) : [];

      // Marcar como lidas as notificações já vistas
      const notificationsWithReadStatus = transactionNotifications.map(n => ({
        ...n,
        read: readNotificationIds.includes(n.id)
      }));

      // Ordenar por data (mais recentes primeiro)
      notificationsWithReadStatus.sort((a, b) => b.timestamp - a.timestamp);

      setNotifications(notificationsWithReadStatus);
      setUnreadCount(notificationsWithReadStatus.filter(n => !n.read).length);
      
    } catch (error) {
      console.error('Erro ao carregar notificações:', error);
    }
  };

  // Função para salvar notificações lidas no localStorage
  const saveReadNotifications = (notifs) => {
    if (!user) return;
    const readIds = notifs.filter(n => n.read).map(n => n.id);
    localStorage.setItem(`notifications_${user.id}`, JSON.stringify(readIds));
  };

  const markAsRead = (id) => {
    const updated = notifications.map(notif =>
      notif.id === id ? { ...notif, read: true } : notif
    );
    setNotifications(updated);
    saveReadNotifications(updated);
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = () => {
    const updated = notifications.map(notif => ({ ...notif, read: true }));
    setNotifications(updated);
    saveReadNotifications(updated);
    setUnreadCount(0);
  };

  const deleteNotification = (id) => {
    const updated = notifications.filter(notif => notif.id !== id);
    setNotifications(updated);
    
    const notif = notifications.find(n => n.id === id);
    if (notif && !notif.read) {
      setUnreadCount(prev => Math.max(0, prev - 1));
    }
  };

  const getTimeAgo = (date) => {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    if (seconds < 60) return 'Agora';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m atrás`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h atrás`;
    return `${Math.floor(seconds / 86400)}d atrás`;
  };

  return (
    <div className="relative">
      {/* Bell Icon */}
      <button
        onClick={() => setShowNotifications(!showNotifications)}
        className="relative p-2 text-white hover:bg-white hover:bg-opacity-10 rounded-lg transition-all"
      >
        <IoNotifications className="w-6 h-6" />
        {unreadCount > 0 && (
          <motion.span
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center"
          >
            {unreadCount > 9 ? '9+' : unreadCount}
          </motion.span>
        )}
      </button>

      {/* Notifications Panel */}
      <AnimatePresence>
        {showNotifications && (
          <>
            {/* Overlay */}
            <div
              className="fixed inset-0 z-40"
              onClick={() => setShowNotifications(false)}
            />

            {/* Panel */}
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="absolute right-0 top-12 w-96 bg-gray-800 rounded-xl shadow-2xl z-50 overflow-hidden border border-gray-700"
            >
              {/* Header */}
              <div className="p-4 border-b border-gray-700 flex items-center justify-between bg-gradient-to-r from-blue-600 to-purple-600">
                <h3 className="text-lg font-bold text-white">Notificações</h3>
                {unreadCount > 0 && (
                  <button
                    onClick={markAllAsRead}
                    className="text-xs text-white hover:underline"
                  >
                    Marcar todas como lidas
                  </button>
                )}
              </div>

              {/* Notifications List */}
              <div className="max-h-96 overflow-y-auto">
                {notifications.length === 0 ? (
                  <div className="p-8 text-center">
                    <IoNotifications className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <p className="text-gray-400">Nenhuma notificação</p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-700">
                    {notifications.map((notification) => {
                      const Icon = notification.icon;
                      return (
                        <motion.div
                          key={notification.id}
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                          className={`p-4 hover:bg-gray-700 transition-colors cursor-pointer ${
                            !notification.read ? 'bg-gray-750' : ''
                          }`}
                          onClick={() => markAsRead(notification.id)}
                        >
                          <div className="flex items-start gap-3">
                            <div
                              className={`p-2 rounded-lg bg-${notification.color}-500 bg-opacity-20`}
                            >
                              <Icon className={`w-5 h-5 text-${notification.color}-500`} />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-start justify-between gap-2">
                                <p className="text-sm font-semibold text-white">
                                  {notification.title}
                                </p>
                                {!notification.read && (
                                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-1 flex-shrink-0" />
                                )}
                              </div>
                              <p className="text-xs text-gray-400 mt-1">
                                {notification.message}
                              </p>
                              <p className="text-xs text-gray-500 mt-2">
                                {getTimeAgo(notification.timestamp)}
                              </p>
                            </div>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                deleteNotification(notification.id);
                              }}
                              className="text-gray-500 hover:text-red-500 transition-colors flex-shrink-0"
                            >
                              <IoClose className="w-5 h-5" />
                            </button>
                          </div>
                        </motion.div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Footer */}
              {notifications.length > 0 && (
                <div className="p-3 border-t border-gray-700 bg-gray-750">
                  <button
                    onClick={() => {
                      const updated = notifications.map(n => ({ ...n, read: true }));
                      setNotifications(updated);
                      saveReadNotifications(updated);
                      setUnreadCount(0);
                    }}
                    className="text-xs text-gray-400 hover:text-white transition-colors w-full text-center"
                  >
                    Marcar todas como lidas
                  </button>
                </div>
              )}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};

export default NotificationBell;
