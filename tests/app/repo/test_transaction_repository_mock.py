import pytest
from decimal import Decimal
from src.app.entities.transaction import Transaction
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock
from src.app.enums.transactionType import TransactionType


class Test_TransactionRepositoryMock:
    EXISTING_ACCOUNT_ID  = "10001-1"
    NOT_FOUND_ACCOUNT_ID = "00000-0"

    # teste que verificar se todas as transactions 
    def test_get_all_transactions(self):
        repo = TransactionRepositoryMock()
        transactions = repo.get_all_transactions()

        assert len(transactions) == len(repo.transactions)
        assert all([t_expect == t for t_expect, t in zip(repo.transactions, transactions)])

    # teste que verificar o retorno 
    def test_get_transaction(self):
        repo = TransactionRepositoryMock()
        target = repo.transactions[0]
        result = repo.get_transaction(id=target.id)

        assert result is not None
        assert result.id == target.id

    # teste para quando nao encontra a transacao
    def test_get_transaction_not_found(self):
        from uuid import uuid4
        repo = TransactionRepositoryMock()
        result = repo.get_transaction(id=uuid4())

        assert result is None

    # teste que retorna as transacao
    def test_get_history(self):
        repo = TransactionRepositoryMock()
        history = repo.get_history(account_id=self.EXISTING_ACCOUNT_ID)

        assert len(history) > 0
        assert all(t.account_id == self.EXISTING_ACCOUNT_ID for t in history)

    # teste para quando nao encontra transacao no historico
    def test_get_history_not_found(self):
        repo = TransactionRepositoryMock()
        history = repo.get_history(account_id=self.NOT_FOUND_ACCOUNT_ID)

        assert history == []

    # teste para criacao de transacao
    def test_create_transaction(self):
        repo = TransactionRepositoryMock()
        len_before = len(repo.transactions)

        transaction = Transaction(
            account_id="10001-1",
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("250.00"),
        )

        repo.create_transaction(transaction=transaction)
        len_after = len(repo.transactions)

        assert len_after == len_before + 1
        assert repo.transactions[-1].id == transaction.id
        assert repo.transactions[-1].account_id == "10001-1"
        assert repo.transactions[-1].transaction_type == TransactionType.DEPOSIT
        assert repo.transactions[-1].amount == Decimal("250.00")

    # teste para ver o retorno da transacao criada
    def test_create_transaction_return(self):
        repo = TransactionRepositoryMock()

        transaction = Transaction(
            account_id="10001-1",
            transaction_type=TransactionType.WITHDRAW,
            amount=Decimal("99.99"),
        )

        returned = repo.create_transaction(transaction=transaction)
        assert returned == transaction

    # teste para ver se aparece no historico a transacao criada
    def test_create_transaction_history(self):
        repo = TransactionRepositoryMock()

        transaction = Transaction(
            account_id="10001-1",
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("111.00"),
        )

        repo.create_transaction(transaction=transaction)
        history = repo.get_history(account_id="10001-1")

        assert transaction in history
