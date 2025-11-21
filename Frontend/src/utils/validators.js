import { cpf as cpfValidator } from 'cpf-cnpj-validator';

/**
 * Valida CPF
 */
export const validateCPF = (cpf) => {
  if (!cpf) return false;
  
  const cleaned = cpf.replace(/\D/g, '');
  return cpfValidator.isValid(cleaned);
};

/**
 * Valida email
 */
export const validateEmail = (email) => {
  if (!email) return false;
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Valida telefone
 */
export const validatePhone = (phone) => {
  if (!phone) return false;
  
  const cleaned = phone.replace(/\D/g, '');
  return cleaned.length === 10 || cleaned.length === 11;
};

/**
 * Valida senha forte
 */
export const validatePassword = (password) => {
  if (!password || password.length < 8) return false;
  
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
  return hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar;
};

/**
 * Obtém mensagem de força da senha
 */
export const getPasswordStrength = (password) => {
  if (!password) return { strength: 0, label: 'Muito fraca', color: 'red' };
  
  let strength = 0;
  
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  if (/[A-Z]/.test(password)) strength++;
  if (/[a-z]/.test(password)) strength++;
  if (/\d/.test(password)) strength++;
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
  
  if (strength <= 2) return { strength, label: 'Muito fraca', color: 'red' };
  if (strength <= 3) return { strength, label: 'Fraca', color: 'orange' };
  if (strength <= 4) return { strength, label: 'Média', color: 'yellow' };
  if (strength <= 5) return { strength, label: 'Forte', color: 'green' };
  return { strength, label: 'Muito forte', color: 'blue' };
};

/**
 * Valida valor monetário
 */
export const validateAmount = (amount, min = 0, max = Infinity) => {
  if (amount === null || amount === undefined) return false;
  
  const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
  
  if (isNaN(numAmount)) return false;
  if (numAmount < min) return false;
  if (numAmount > max) return false;
  
  return true;
};

/**
 * Valida data
 */
export const validateDate = (date) => {
  if (!date) return false;
  
  const dateObj = date instanceof Date ? date : new Date(date);
  return !isNaN(dateObj.getTime());
};

/**
 * Valida se data é futura
 */
export const validateFutureDate = (date) => {
  if (!validateDate(date)) return false;
  
  const dateObj = date instanceof Date ? date : new Date(date);
  return dateObj > new Date();
};

/**
 * Valida número de cartão de crédito (Luhn algorithm)
 */
export const validateCardNumber = (cardNumber) => {
  if (!cardNumber) return false;
  
  const cleaned = cardNumber.replace(/\D/g, '');
  
  if (cleaned.length < 13 || cleaned.length > 19) return false;
  
  let sum = 0;
  let isEven = false;
  
  for (let i = cleaned.length - 1; i >= 0; i--) {
    let digit = parseInt(cleaned[i], 10);
    
    if (isEven) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    
    sum += digit;
    isEven = !isEven;
  }
  
  return sum % 10 === 0;
};

/**
 * Valida CVV
 */
export const validateCVV = (cvv) => {
  if (!cvv) return false;
  
  const cleaned = cvv.replace(/\D/g, '');
  return cleaned.length === 3 || cleaned.length === 4;
};

/**
 * Valida campos obrigatórios
 */
export const validateRequired = (value) => {
  if (value === null || value === undefined) return false;
  if (typeof value === 'string' && value.trim() === '') return false;
  return true;
};

/**
 * Valida tamanho mínimo
 */
export const validateMinLength = (value, minLength) => {
  if (!value) return false;
  return String(value).length >= minLength;
};

/**
 * Valida tamanho máximo
 */
export const validateMaxLength = (value, maxLength) => {
  if (!value) return true;
  return String(value).length <= maxLength;
};
