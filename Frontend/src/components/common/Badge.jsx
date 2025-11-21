import React from 'react';

const Badge = ({ children, variant = 'default', size = 'medium', className = '' }) => {
  const variantClasses = {
    default: 'bg-gray-100 text-gray-800',
    primary: 'bg-light-blue text-primary-blue',
    success: 'bg-light-green text-secondary-green',
    warning: 'bg-yellow-100 text-warning',
    error: 'bg-red-100 text-error',
  };

  const sizeClasses = {
    small: 'px-2 py-0.5 text-xs',
    medium: 'px-2.5 py-1 text-sm',
    large: 'px-3 py-1.5 text-base',
  };

  return (
    <span
      className={`
        inline-flex items-center rounded-full font-medium
        ${variantClasses[variant]}
        ${sizeClasses[size]}
        ${className}
      `}
    >
      {children}
    </span>
  );
};

export default Badge;
