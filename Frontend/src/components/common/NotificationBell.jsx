import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { IoNotifications, IoClose, IoCheckmark, IoTime, IoWallet } from 'react-icons/io5';
import { formatCurrency, formatDate } from '../../utils/formatters';

const NotificationBell = () => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    loadNotifications();
    // Atualizar notificações a cada 30 segundos
    const interval = setInterval(loadNotifications, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadNotifications = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return;

      // Carregar notificações persistidas do localStorage
      const savedNotifications = localStorage.getItem('notifications');
      
      if (savedNotifications) {
        // Se já existem notificações salvas, usar elas
        const parsed = JSON.parse(savedNotifications);
        // Converter timestamps de string para Date
        const notificationsWithDates = parsed.map(n => ({
          ...n,
          timestamp: new Date(n.timestamp),
          icon: n.type === 'transaction' ? IoWallet : 
                n.type === 'investment' ? IoCheckmark : IoTime
        }));
        setNotifications(notificationsWithDates);
        setUnreadCount(notificationsWithDates.filter(n => !n.read).length);
      } else {
        // Primeira vez: criar notificações iniciais
        const mockNotifications = [
          {
            id: Date.now() + 1,
            type: 'transaction',
            title: 'Transferência recebida',
            message: 'Você recebeu R$ 500,00',
            timestamp: new Date(Date.now() - 1000 * 60 * 5),
            read: false,
            icon: IoWallet,
            color: 'green'
          },
          {
            id: Date.now() + 2,
            type: 'investment',
            title: 'Investimento concluído',
            message: 'Sua compra de PETR4 foi processada',
            timestamp: new Date(Date.now() - 1000 * 60 * 30),
            read: false,
            icon: IoCheckmark,
            color: 'blue'
          },
          {
            id: Date.now() + 3,
            type: 'reminder',
            title: 'Fatura próxima do vencimento',
            message: 'Sua fatura vence em 3 dias',
            timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2),
            read: false,
            icon: IoTime,
            color: 'yellow'
          }
        ];

        // Salvar no localStorage
        const toSave = mockNotifications.map(n => ({
          ...n,
          icon: undefined, // Não salvar função no localStorage
          timestamp: n.timestamp.toISOString()
        }));
        localStorage.setItem('notifications', JSON.stringify(toSave));

        setNotifications(mockNotifications);
        setUnreadCount(mockNotifications.filter(n => !n.read).length);
      }
    } catch (error) {
      console.error('Erro ao carregar notificações:', error);
    }
  };

  // Função para salvar notificações no localStorage
  const saveNotifications = (notifs) => {
    const toSave = notifs.map(n => ({
      id: n.id,
      type: n.type,
      title: n.title,
      message: n.message,
      timestamp: n.timestamp.toISOString(),
      read: n.read,
      color: n.color
    }));
    localStorage.setItem('notifications', JSON.stringify(toSave));
  };

  const markAsRead = (id) => {
    const updated = notifications.map(notif =>
      notif.id === id ? { ...notif, read: true } : notif
    );
    setNotifications(updated);
    saveNotifications(updated);
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = () => {
    const updated = notifications.map(notif => ({ ...notif, read: true }));
    setNotifications(updated);
    saveNotifications(updated);
    setUnreadCount(0);
  };

  const deleteNotification = (id) => {
    const updated = notifications.filter(notif => notif.id !== id);
    setNotifications(updated);
    saveNotifications(updated);
    
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
                      setNotifications([]);
                      setUnreadCount(0);
                      localStorage.removeItem('notifications');
                    }}
                    className="text-xs text-gray-400 hover:text-white transition-colors w-full text-center"
                  >
                    Limpar todas as notificações
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
