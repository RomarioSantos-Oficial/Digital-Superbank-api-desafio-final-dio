import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  IoGrid, IoBusiness, IoSwapHorizontal, IoCard, 
  IoTrendingUp, IoPerson, IoArrowBack 
} from 'react-icons/io5';

const QuickNav = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', icon: IoGrid, label: 'Dashboard', color: 'bg-blue-500' },
    { path: '/accounts', icon: IoBusiness, label: 'Contas', color: 'bg-green-500' },
    { path: '/transactions', icon: IoSwapHorizontal, label: 'Transações', color: 'bg-purple-500' },
    { path: '/cards', icon: IoCard, label: 'Cartões', color: 'bg-pink-500' },
    { path: '/investments', icon: IoTrendingUp, label: 'Investimentos', color: 'bg-yellow-500' },
    { path: '/profile', icon: IoPerson, label: 'Perfil', color: 'bg-gray-500' },
  ];

  const currentItem = navItems.find(item => item.path === location.pathname);
  const otherItems = navItems.filter(item => item.path !== location.pathname);

  return (
    <div className="mb-6">
      {/* Navegação para voltar */}
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-400 hover:text-yellow-500 transition-colors mb-4"
      >
        <IoArrowBack className="w-5 h-5" />
        <span>Voltar</span>
      </button>

      {/* Navegação rápida */}
      <div className="bg-gray-800 rounded-lg p-4">
        <h3 className="text-sm font-medium text-gray-400 mb-3">Acesso Rápido</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
          {otherItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className="flex flex-col items-center gap-2 p-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-all hover:scale-105 group"
            >
              <div className={`${item.color} p-2 rounded-lg text-white group-hover:scale-110 transition-transform`}>
                <item.icon className="w-5 h-5" />
              </div>
              <span className="text-xs text-gray-300 group-hover:text-white text-center">
                {item.label}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default QuickNav;
