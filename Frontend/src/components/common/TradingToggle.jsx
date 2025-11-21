import React from 'react';
import { IoSunny, IoMoon } from 'react-icons/io5';

/**
 * Botão Toggle estilo Dia/Noite para ativar Trading Dashboard
 * Design inspirado em switches modernos
 */
const TradingToggle = ({ onClick, isActive = false }) => {
  return (
    <button
      onClick={onClick}
      className="group relative flex items-center gap-3 px-5 py-2.5 rounded-full transition-all duration-300 hover:scale-105"
      style={{
        background: isActive 
          ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
          : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        boxShadow: isActive
          ? '0 4px 15px 0 rgba(102, 126, 234, 0.5)'
          : '0 4px 15px 0 rgba(245, 87, 108, 0.3)'
      }}
      title={isActive ? "Trading Dashboard Ativo" : "Abrir Trading Dashboard"}
    >
      {/* Toggle Switch */}
      <div className="relative w-14 h-7 rounded-full bg-white/20 backdrop-blur-sm">
        {/* Ícones de Fundo */}
        <div className="absolute inset-0 flex items-center justify-between px-1.5">
          <IoSunny className={`w-4 h-4 transition-opacity duration-300 ${
            !isActive ? 'text-yellow-300 opacity-100' : 'text-white/40 opacity-50'
          }`} />
          <IoMoon className={`w-4 h-4 transition-opacity duration-300 ${
            isActive ? 'text-blue-200 opacity-100' : 'text-white/40 opacity-50'
          }`} />
        </div>

        {/* Botão Deslizante */}
        <div 
          className={`absolute top-0.5 w-6 h-6 rounded-full bg-white shadow-lg transform transition-all duration-300 ease-out ${
            isActive ? 'translate-x-7' : 'translate-x-0.5'
          }`}
          style={{
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)'
          }}
        >
          {/* Brilho interno */}
          <div className="absolute inset-0 rounded-full bg-gradient-to-br from-white/50 to-transparent" />
        </div>
      </div>

      {/* Texto */}
      <span className="text-white font-semibold text-sm tracking-wide">
        {isActive ? 'Trading ON' : 'Trading Mode'}
      </span>

      {/* Indicador de Status */}
      {isActive && (
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse border-2 border-white" />
      )}
    </button>
  );
};

export default TradingToggle;
