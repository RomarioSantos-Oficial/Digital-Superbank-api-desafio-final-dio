import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { CURRENCY_SYMBOL } from './constants';

/**
 * Formata valor monetário para BRL
 */
export const formatCurrency = (value) => {
  if (value === null || value === undefined) return `${CURRENCY_SYMBOL} 0,00`;
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(numValue);
};

/**
 * Formata número com separadores de milhar
 */
export const formatNumber = (value, decimals = 2) => {
  if (value === null || value === undefined) return '0';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(numValue);
};

/**
 * Formata data para formato brasileiro
 */
export const formatDate = (date, formatStr = 'dd/MM/yyyy') => {
  if (!date) return '';
  
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    return format(dateObj, formatStr, { locale: ptBR });
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
};

/**
 * Formata data e hora
 */
export const formatDateTime = (date) => {
  return formatDate(date, 'dd/MM/yyyy HH:mm');
};

/**
 * Formata apenas hora
 */
export const formatTime = (date) => {
  return formatDate(date, 'HH:mm');
};

/**
 * Formata CPF
 */
export const formatCPF = (cpf) => {
  if (!cpf) return '';
  
  const cleaned = cpf.replace(/\D/g, '');
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{3})(\d{2})$/);
  
  if (match) {
    return `${match[1]}.${match[2]}.${match[3]}-${match[4]}`;
  }
  
  return cpf;
};

/**
 * Formata telefone
 */
export const formatPhone = (phone) => {
  if (!phone) return '';
  
  const cleaned = phone.replace(/\D/g, '');
  const match = cleaned.match(/^(\d{2})(\d{4,5})(\d{4})$/);
  
  if (match) {
    return `(${match[1]}) ${match[2]}-${match[3]}`;
  }
  
  return phone;
};

/**
 * Formata número de conta
 */
export const formatAccountNumber = (accountNumber) => {
  if (!accountNumber) return '';
  
  const str = String(accountNumber);
  if (str.length < 2) return str;
  
  const digit = str.slice(-1);
  const number = str.slice(0, -1);
  
  return `${number}-${digit}`;
};

/**
 * Formata número de cartão de crédito
 */
export const formatCardNumber = (cardNumber, showFull = false) => {
  if (!cardNumber) return '';
  
  const cleaned = cardNumber.replace(/\D/g, '');
  
  if (showFull) {
    const match = cleaned.match(/(\d{4})(\d{4})(\d{4})(\d{4})/);
    if (match) {
      return `${match[1]} ${match[2]} ${match[3]} ${match[4]}`;
    }
  } else {
    // Mostra apenas os últimos 4 dígitos
    const lastFour = cleaned.slice(-4);
    return `**** **** **** ${lastFour}`;
  }
  
  return cardNumber;
};

/**
 * Formata porcentagem
 */
export const formatPercent = (value, decimals = 2) => {
  if (value === null || value === undefined) return '0%';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  return `${formatNumber(numValue, decimals)}%`;
};

/**
 * Formata data relativa (ex: "há 2 horas")
 */
export const formatRelativeTime = (date) => {
  if (!date) return '';
  
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  const now = new Date();
  const diffInSeconds = Math.floor((now - dateObj) / 1000);
  
  if (diffInSeconds < 60) {
    return 'agora';
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `há ${minutes} ${minutes === 1 ? 'minuto' : 'minutos'}`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `há ${hours} ${hours === 1 ? 'hora' : 'horas'}`;
  } else if (diffInSeconds < 604800) {
    const days = Math.floor(diffInSeconds / 86400);
    return `há ${days} ${days === 1 ? 'dia' : 'dias'}`;
  } else {
    return formatDate(dateObj);
  }
};

/**
 * Abrevia números grandes (ex: 1.5K, 2.3M)
 */
export const abbreviateNumber = (value) => {
  if (value === null || value === undefined) return '0';
  
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  
  if (numValue >= 1000000000) {
    return `${(numValue / 1000000000).toFixed(1)}B`;
  } else if (numValue >= 1000000) {
    return `${(numValue / 1000000).toFixed(1)}M`;
  } else if (numValue >= 1000) {
    return `${(numValue / 1000).toFixed(1)}K`;
  }
  
  return String(numValue);
};

/**
 * Mascara dados sensíveis
 */
export const maskSensitiveData = (data, visibleChars = 4) => {
  if (!data) return '';
  
  const str = String(data);
  if (str.length <= visibleChars) return str;
  
  const visible = str.slice(-visibleChars);
  const masked = '*'.repeat(str.length - visibleChars);
  
  return masked + visible;
};
