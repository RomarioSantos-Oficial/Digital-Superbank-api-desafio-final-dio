import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  IoGrid,
  IoBusiness,
  IoSwapHorizontal,
  IoCard,
  IoTrendingUp,
  IoReceiptOutline,
  IoDocumentTextOutline,
  IoPerson,
  IoClose,
  IoKey,
} from 'react-icons/io5';

const Sidebar = ({ isOpen, onClose }) => {
  const menuItems = [
    { path: '/dashboard', icon: IoGrid, label: 'Dashboard' },
    { path: '/accounts', icon: IoBusiness, label: 'Contas' },
    { path: '/transactions', icon: IoSwapHorizontal, label: 'Transações' },
    { path: '/pix-keys', icon: IoKey, label: 'Chaves PIX' },
    { path: '/pay-bills', icon: IoReceiptOutline, label: 'Pagar Contas' },
    { path: '/statement', icon: IoDocumentTextOutline, label: 'Extrato Completo' },
    { path: '/cards', icon: IoCard, label: 'Cartões' },
    { path: '/investments', icon: IoTrendingUp, label: 'Investimentos' },
    { path: '/profile', icon: IoPerson, label: 'Perfil' },
  ];

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ x: isOpen ? 0 : -300 }}
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-64 bg-gray-800 border-r border-gray-700
          flex flex-col lg:translate-x-0
        `}
      >
        <div className="p-4 border-b border-gray-700 flex items-center justify-between lg:hidden">
          <span className="font-bold text-lg text-white">Menu</span>
          <button onClick={onClose} className="p-2 hover:bg-gray-700 rounded-lg text-white">
            <IoClose className="w-6 h-6" />
          </button>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => onClose()}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium'
                    : 'text-gray-400 hover:bg-gray-700 hover:text-white'
                }`
              }
            >
              <item.icon className="w-5 h-5" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-gray-700">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 bg-opacity-10 p-4 rounded-lg border border-blue-500 border-opacity-30">
            <p className="text-sm font-medium text-blue-400 mb-1">
              Precisa de ajuda?
            </p>
            <p className="text-xs text-gray-400">
              Converse com nosso chatbot
            </p>
          </div>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;
