import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useAccounts } from '../../hooks/useAccounts';
import { IoPersonCircle, IoMenu, IoLogOut } from 'react-icons/io5';
import { formatCurrency } from '../../utils/formatters';
import NotificationBell from '../common/NotificationBell';

const Header = ({ onMenuClick }) => {
  const { user, logout } = useAuth();
  const { getTotalBalance } = useAccounts();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-40">
      <div className="px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 hover:bg-gray-700 rounded-lg text-white"
          >
            <IoMenu className="w-6 h-6" />
          </button>
          
          <Link to="/dashboard" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">DS</span>
            </div>
            <span className="font-bold text-xl text-white hidden sm:block">
              Digital Superbank
            </span>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-2 bg-gray-700 px-4 py-2 rounded-lg">
            <span className="text-sm text-gray-400">Saldo Total:</span>
            <span className="font-bold text-yellow-500">
              {formatCurrency(getTotalBalance())}
            </span>
          </div>

          <NotificationBell />

          <div className="flex items-center gap-2">
            <Link
              to="/profile"
              className="flex items-center gap-2 p-2 hover:bg-gray-700 rounded-lg"
            >
              <IoPersonCircle className="w-8 h-8 text-blue-500" />
              <span className="hidden sm:block font-medium text-white">
                {user?.name || 'Usuário'}
              </span>
            </Link>

            <button
              onClick={handleLogout}
              className="p-2 hover:bg-red-900 hover:bg-opacity-30 rounded-lg text-red-500"
              title="Sair"
            >
              <IoLogOut className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
