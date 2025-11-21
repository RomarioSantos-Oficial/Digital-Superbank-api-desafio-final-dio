"""
Transaction Service
Gerencia todas as operações de transações bancárias
"""
from datetime import datetime, date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.models.transaction import (
    Transaction, TransactionType, TransactionStatus,
    ScheduledTransaction
)
from src.models.account import Account
from src.configs.settings import settings


class TransactionLimitError(Exception):
    """Erro de limite de transação excedido"""
    pass


class InsufficientBalanceError(Exception):
    """Erro de saldo insuficiente"""
    pass


def _check_daily_withdrawal_limits(
    db: Session,
    account_id: int,
    amount: float
) -> None:
    """
    Verifica limites diários de saque:
    - Máximo R$ 2.000 por saque
    - Máximo 3 saques por dia
    - Limite total diário de R$ 5.000
    """
    # Verifica valor máximo por saque
    if amount > settings.MAX_WITHDRAWAL_AMOUNT:
        raise TransactionLimitError(
            f"Valor máximo por saque é "
            f"R$ {settings.MAX_WITHDRAWAL_AMOUNT}"
        )
    
    # Busca saques do dia
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_withdrawals = db.query(Transaction).filter(
        and_(
            Transaction.from_account_id == account_id,
            Transaction.transaction_type == TransactionType.WITHDRAWAL,
            Transaction.status == TransactionStatus.COMPLETED,
            Transaction.created_at >= today_start
        )
    ).all()
    
    # Verifica número de saques
    if len(today_withdrawals) >= settings.MAX_WITHDRAWALS_PER_DAY:
        raise TransactionLimitError(
            f"Limite de {settings.MAX_WITHDRAWALS_PER_DAY} "
            f"saques diários atingido"
        )
    
    # Verifica valor total diário
    total_today = sum(t.amount for t in today_withdrawals)
    if total_today + amount > settings.DAILY_WITHDRAWAL_LIMIT:
        raise TransactionLimitError(
            f"Limite diário total de "
            f"R$ {settings.DAILY_WITHDRAWAL_LIMIT} atingido. "
            f"Já sacou R$ {total_today} hoje"
        )


def create_deposit(
    db: Session,
    account_id: int,
    amount: float,
    description: str = "Depósito"
) -> Transaction:
    """Realizar depósito em conta"""
    if amount <= 0:
        raise ValueError("Valor do depósito deve ser positivo")
    
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Cria transação
    transaction = Transaction(
        from_account_id=account_id,
        transaction_type=TransactionType.DEPOSIT,
        amount=amount,
        description=description,
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza saldo
    account.balance += amount
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


def create_withdrawal(
    db: Session,
    account_id: int,
    amount: float,
    description: str = "Saque"
) -> Transaction:
    """
    Realizar saque com validação de limites diários:
    - Máximo R$ 2.000 por saque
    - Máximo 3 saques por dia
    - Limite total diário de R$ 5.000
    """
    if amount <= 0:
        raise ValueError("Valor do saque deve ser positivo")
    
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Verifica saldo
    if account.balance < amount:
        raise InsufficientBalanceError(
            f"Saldo insuficiente. Disponível: R$ {account.balance}"
        )
    
    # Verifica limites diários
    _check_daily_withdrawal_limits(db, account_id, amount)
    
    # Cria transação
    transaction = Transaction(
        from_account_id=account_id,
        transaction_type=TransactionType.WITHDRAWAL,
        amount=amount,
        description=description,
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza saldo
    account.balance -= amount
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


def create_transfer(
    db: Session,
    from_account_id: int,
    to_account_number: str,
    amount: float,
    description: str = "Transferência"
) -> tuple[Transaction, Transaction]:
    """
    Transferência interna com transação atômica
    Retorna: (transação_débito, transação_crédito)
    """
    if amount <= 0:
        raise ValueError("Valor da transferência deve ser positivo")
    
    try:
        # Busca contas
        from_account = db.query(Account).filter(
            Account.id == from_account_id
        ).first()
        if not from_account:
            raise ValueError("Conta origem não encontrada")
        
        to_account = db.query(Account).filter(
            Account.account_number == to_account_number
        ).first()
        if not to_account:
            raise ValueError("Conta destino não encontrada")
        
        if from_account.id == to_account.id:
            raise ValueError("Não é possível transferir para a mesma conta")
        
        # Verifica saldo
        if from_account.balance < amount:
            raise InsufficientBalanceError(
                f"Saldo insuficiente. Disponível: R$ {from_account.balance}"
            )
        
        # Cria transação de débito
        debit_transaction = Transaction(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
            description=f"{description} - Para: {to_account.account_number}",
            status=TransactionStatus.COMPLETED
        )
        
        # Cria transação de crédito
        credit_transaction = Transaction(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
            description=f"{description} - De: {from_account.account_number}",
            status=TransactionStatus.COMPLETED
        )
        
        # Atualiza saldos
        from_account.balance -= amount
        from_account.updated_at = datetime.utcnow()
        
        to_account.balance += amount
        to_account.updated_at = datetime.utcnow()
        
        # Adiciona tudo em uma única transação
        db.add(debit_transaction)
        db.add(credit_transaction)
        db.commit()
        
        db.refresh(debit_transaction)
        db.refresh(credit_transaction)
        
        return debit_transaction, credit_transaction
        
    except Exception as e:
        db.rollback()
        raise e


def create_pix_send(
    db: Session,
    from_account_id: int,
    pix_key: str,
    amount: float,
    description: str = "PIX enviado"
) -> Transaction:
    """Enviar PIX (simulado - só debita da conta)"""
    if amount <= 0:
        raise ValueError("Valor do PIX deve ser positivo")
    
    # Busca conta
    account = db.query(Account).filter(Account.id == from_account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Verifica saldo
    if account.balance < amount:
        raise InsufficientBalanceError(
            f"Saldo insuficiente. Disponível: R$ {account.balance}"
        )
    
    # Cria transação
    transaction = Transaction(
        from_account_id=from_account_id,
        transaction_type=TransactionType.PIX_SEND,
        amount=amount,
        pix_key=pix_key,
        description=f"{description} - Chave: {pix_key}",
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza saldo
    account.balance -= amount
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


def create_pix_receive(
    db: Session,
    to_account_number: str,
    amount: float,
    pix_key: str,
    description: str = "PIX recebido"
) -> Transaction:
    """Receber PIX (simulado - só credita na conta)"""
    if amount <= 0:
        raise ValueError("Valor do PIX deve ser positivo")
    
    # Busca conta
    account = db.query(Account).filter(
        Account.account_number == to_account_number
    ).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Cria transação
    transaction = Transaction(
        to_account_id=account.id,
        transaction_type=TransactionType.PIX_RECEIVE,
        amount=amount,
        pix_key=pix_key,
        description=f"{description} - Chave: {pix_key}",
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza saldo
    account.balance += amount
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


def pay_bill(
    db: Session,
    account_id: int,
    bar_code: str,
    amount: float,
    description: str = "Pagamento de boleto"
) -> Transaction:
    """Pagar boleto/conta"""
    if amount <= 0:
        raise ValueError("Valor do pagamento deve ser positivo")
    
    if not bar_code or len(bar_code) < 44:
        raise ValueError(
            "Código de barras inválido (mínimo 44 dígitos)"
        )
    
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    # Verifica saldo
    if account.balance < amount:
        raise InsufficientBalanceError(
            f"Saldo insuficiente. Disponível: R$ {account.balance}"
        )
    
    # Cria transação
    transaction = Transaction(
        from_account_id=account_id,
        transaction_type=TransactionType.BILL_PAYMENT,
        amount=amount,
        bar_code=bar_code,
        description=f"{description} - Código: {bar_code[:10]}...",
        status=TransactionStatus.COMPLETED
    )
    
    # Atualiza saldo
    account.balance -= amount
    account.updated_at = datetime.utcnow()
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


def get_statement(
    db: Session,
    account_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    transaction_type: Optional[TransactionType] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    limit: int = 50,
    offset: int = 0
) -> tuple[List[Transaction], int]:
    """
    Obter extrato com filtros
    Retorna: (lista_transações, total_count)
    """
    from sqlalchemy import or_
    
    query = db.query(Transaction).filter(
        or_(
            Transaction.from_account_id == account_id,
            Transaction.to_account_id == account_id
        )
    )
    
    # Filtros
    if start_date:
        query = query.filter(Transaction.created_at >= start_date)
    if end_date:
        query = query.filter(Transaction.created_at <= end_date)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    
    # Total de registros
    total_count = query.count()
    
    # Paginação e ordenação
    transactions = query.order_by(
        Transaction.created_at.desc()
    ).limit(limit).offset(offset).all()
    
    return transactions, total_count


def schedule_transaction(
    db: Session,
    account_id: int,
    transaction_type: TransactionType,
    amount: float,
    scheduled_date: datetime,
    description: str = "",
    to_account_id: Optional[int] = None
) -> ScheduledTransaction:
    """Agendar transação futura"""
    if amount <= 0:
        raise ValueError("Valor deve ser positivo")
    
    if scheduled_date <= datetime.utcnow():
        raise ValueError("Data de agendamento deve ser futura")
    
    # Busca conta
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise ValueError("Conta não encontrada")
    
    scheduled = ScheduledTransaction(
        from_account_id=account_id,
        to_account_id=to_account_id,
        transaction_type=transaction_type,
        amount=amount,
        schedule_date=scheduled_date,
        description=description,
        status="PENDING"
    )
    
    db.add(scheduled)
    db.commit()
    db.refresh(scheduled)
    
    return scheduled


def get_scheduled_transactions(
    db: Session,
    account_id: int
) -> List[ScheduledTransaction]:
    """Listar transações agendadas"""
    return db.query(ScheduledTransaction).filter(
        and_(
            ScheduledTransaction.account_id == account_id,
            ScheduledTransaction.status == TransactionStatus.PENDING
        )
    ).order_by(ScheduledTransaction.scheduled_date).all()


def execute_scheduled_transactions(db: Session) -> int:
    """
    Executar transações agendadas que chegaram na data
    (Simula um cron job)
    Retorna: número de transações executadas
    """
    now = datetime.utcnow()
    
    pending = db.query(ScheduledTransaction).filter(
        and_(
            ScheduledTransaction.scheduled_date <= now,
            ScheduledTransaction.status == TransactionStatus.PENDING
        )
    ).all()
    
    executed_count = 0
    
    for scheduled in pending:
        try:
            # Executa conforme o tipo
            if scheduled.type == TransactionType.DEPOSIT:
                create_deposit(
                    db, scheduled.account_id,
                    scheduled.amount, scheduled.description
                )
            elif scheduled.type == TransactionType.WITHDRAWAL:
                create_withdrawal(
                    db, scheduled.account_id,
                    scheduled.amount, scheduled.description
                )
            elif scheduled.type == TransactionType.TRANSFER_OUT:
                if scheduled.destination_account:
                    create_transfer(
                        db, scheduled.account_id,
                        scheduled.destination_account,
                        scheduled.amount, scheduled.description
                    )
            elif scheduled.type == TransactionType.BILL_PAYMENT:
                if scheduled.destination_account:  # usar como bar_code
                    pay_bill(
                        db, scheduled.account_id,
                        scheduled.destination_account,
                        scheduled.amount, scheduled.description
                    )
            
            # Marca como completado
            scheduled.status = TransactionStatus.COMPLETED
            scheduled.executed_at = now
            executed_count += 1
            
        except Exception as e:
            # Marca como falha
            scheduled.status = TransactionStatus.FAILED
            scheduled.executed_at = now
            print(f"Erro ao executar agendamento {scheduled.id}: {e}")
    
    db.commit()
    return executed_count
