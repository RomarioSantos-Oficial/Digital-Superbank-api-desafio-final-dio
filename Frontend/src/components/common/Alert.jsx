import React from 'react';
import { motion } from 'framer-motion';
import { IoCheckmarkCircle, IoWarning, IoInformationCircle, IoCloseCircle } from 'react-icons/io5';

const Alert = ({ type = 'info', message, onClose, className = '' }) => {
  const config = {
    success: {
      icon: IoCheckmarkCircle,
      bgColor: 'bg-light-green',
      textColor: 'text-secondary-green',
      borderColor: 'border-primary-green',
    },
    error: {
      icon: IoCloseCircle,
      bgColor: 'bg-red-50',
      textColor: 'text-error',
      borderColor: 'border-error',
    },
    warning: {
      icon: IoWarning,
      bgColor: 'bg-yellow-50',
      textColor: 'text-warning',
      borderColor: 'border-warning',
    },
    info: {
      icon: IoInformationCircle,
      bgColor: 'bg-light-blue',
      textColor: 'text-primary-blue',
      borderColor: 'border-primary-blue',
    },
  };

  const { icon: Icon, bgColor, textColor, borderColor } = config[type];

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      className={`
        ${bgColor} ${textColor} border-l-4 ${borderColor}
        p-4 rounded-lg flex items-start gap-3 ${className}
      `}
    >
      <Icon className="w-6 h-6 flex-shrink-0 mt-0.5" />
      <p className="flex-1">{message}</p>
      {onClose && (
        <button
          onClick={onClose}
          className="flex-shrink-0 hover:opacity-70 transition-opacity"
        >
          <IoCloseCircle className="w-5 h-5" />
        </button>
      )}
    </motion.div>
  );
};

export default Alert;
