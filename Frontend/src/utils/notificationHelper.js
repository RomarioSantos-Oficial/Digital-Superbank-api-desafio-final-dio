/**
 * Helper para criar notificações de transações
 * Dispara evento customizado para o NotificationBell capturar
 */

export const createTransactionNotification = (transaction, accountNumber) => {
  // Dispara evento customizado para o NotificationBell atualizar
  const event = new CustomEvent('newTransaction', {
    detail: { transaction, accountNumber }
  });
  window.dispatchEvent(event);
};

export const notifyDeposit = (amount, accountNumber) => {
  createTransactionNotification({
    transaction_type: 'DEPOSIT',
    amount,
    created_at: new Date().toISOString(),
    description: 'Depósito'
  }, accountNumber);
};

export const notifyWithdrawal = (amount, accountNumber) => {
  createTransactionNotification({
    transaction_type: 'WITHDRAWAL',
    amount,
    created_at: new Date().toISOString(),
    description: 'Saque'
  }, accountNumber);
};

export const notifyTransfer = (amount, accountNumber, isReceived = false) => {
  createTransactionNotification({
    transaction_type: 'TRANSFER',
    amount,
    created_at: new Date().toISOString(),
    description: isReceived ? 'Transferência recebida' : 'Transferência enviada',
    to_account_id: isReceived ? 1 : null,
    from_account_id: isReceived ? null : 1
  }, accountNumber);
};

export const notifyPix = (amount, accountNumber, isReceived = false) => {
  createTransactionNotification({
    transaction_type: isReceived ? 'PIX_RECEIVE' : 'PIX_SEND',
    amount,
    created_at: new Date().toISOString(),
    description: isReceived ? 'PIX recebido' : 'PIX enviado'
  }, accountNumber);
};

export const notifyBillPayment = (amount, accountNumber, description) => {
  createTransactionNotification({
    transaction_type: 'BILL_PAYMENT',
    amount,
    created_at: new Date().toISOString(),
    description: description || 'Pagamento de boleto'
  }, accountNumber);
};
