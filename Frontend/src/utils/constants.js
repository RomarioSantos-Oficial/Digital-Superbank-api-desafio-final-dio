export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Digital Superbank';
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0';
export const BANK_CODE = import.meta.env.VITE_BANK_CODE || '737';
export const BANK_NAME = import.meta.env.VITE_BANK_NAME || 'Digital Superbank';

// Account types
export const ACCOUNT_TYPES = {
  CHECKING: 'checking',
  SAVINGS: 'savings',
  BLACK: 'black',
  BUSINESS: 'business',
  INVESTMENT: 'investment',
};

export const ACCOUNT_TYPE_LABELS = {
  checking: 'Conta Corrente',
  savings: 'Conta Poupança',
  black: 'Conta Black',
  business: 'Conta Empresarial',
  investment: 'Conta Investimento',
};

// Transaction types
export const TRANSACTION_TYPES = {
  DEPOSIT: 'deposit',
  WITHDRAWAL: 'withdrawal',
  TRANSFER: 'transfer',
  PIX: 'pix',
  BILL_PAYMENT: 'bill_payment',
  PURCHASE: 'purchase',
};

export const TRANSACTION_TYPE_LABELS = {
  deposit: 'Depósito',
  withdrawal: 'Saque',
  transfer: 'Transferência',
  pix: 'PIX',
  bill_payment: 'Pagamento de Boleto',
  purchase: 'Compra',
};

// Transaction status
export const TRANSACTION_STATUS = {
  COMPLETED: 'completed',
  PENDING: 'pending',
  CANCELLED: 'cancelled',
  SCHEDULED: 'scheduled',
};

export const TRANSACTION_STATUS_LABELS = {
  completed: 'Concluído',
  pending: 'Pendente',
  cancelled: 'Cancelado',
  scheduled: 'Agendado',
};

// Card types
export const CARD_TYPES = {
  BASIC: 'basic',
  PLUS: 'plus',
  PREMIUM: 'premium',
  VIRTUAL: 'virtual',
};

export const CARD_TYPE_LABELS = {
  basic: 'Aura Basic',
  plus: 'Aura Plus',
  premium: 'Aura Premium',
  virtual: 'Cartão Virtual',
};

export const CARD_TYPE_COLORS = {
  basic: 'from-green-400 to-green-600',
  plus: 'from-blue-500 to-blue-700',
  premium: 'from-gray-800 to-black',
  virtual: 'from-purple-500 to-purple-700',
};

// Card status
export const CARD_STATUS = {
  ACTIVE: 'active',
  BLOCKED: 'blocked',
  CANCELLED: 'cancelled',
};

// Asset types
export const ASSET_TYPES = {
  STOCK: 'stock',
  REIT: 'reit',
  CRYPTO: 'crypto',
  BOND: 'bond',
  ETF: 'etf',
};

export const ASSET_TYPE_LABELS = {
  stock: 'Ação',
  reit: 'Fundo Imobiliário',
  crypto: 'Criptomoeda',
  bond: 'Título',
  etf: 'ETF',
};

// Credit score ranges
export const CREDIT_SCORE_RANGES = {
  VERY_LOW: { min: 0, max: 300, label: 'Muito Baixo', color: 'red' },
  LOW: { min: 301, max: 500, label: 'Baixo', color: 'orange' },
  MEDIUM: { min: 501, max: 700, label: 'Médio', color: 'yellow' },
  GOOD: { min: 701, max: 850, label: 'Bom', color: 'green' },
  EXCELLENT: { min: 851, max: 1000, label: 'Excelente', color: 'blue' },
};

// Pagination
export const DEFAULT_PAGE_SIZE = 20;
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

// Date formats
export const DATE_FORMAT = 'dd/MM/yyyy';
export const DATETIME_FORMAT = 'dd/MM/yyyy HH:mm';
export const TIME_FORMAT = 'HH:mm';

// Currency
export const CURRENCY = 'BRL';
export const CURRENCY_SYMBOL = 'R$';

// Validation
export const CPF_REGEX = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
export const PHONE_REGEX = /^\(\d{2}\) \d{4,5}-\d{4}$/;
export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Local storage keys
export const STORAGE_KEYS = {
  TOKEN: 'auth_token',
  USER: 'user_data',
  THEME: 'theme',
};
