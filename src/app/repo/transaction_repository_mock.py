from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from ..entities.transaction import Transaction
from .transaction_repository_interface import TransactionRepository
from ..enums.transactionType import TransactionType

class TransactionRepositoryMock(TransactionRepository):

    def __init__(self):
        self.transactions = [

        # Yuri Alberto (10001-1)
            Transaction(account_id="10001-1", transaction_type=TransactionType.DEPOSIT, amount=Decimal("500.00")),
            Transaction(account_id="10001-1", transaction_type=TransactionType.DEPOSIT, amount=Decimal("200.00")),
            Transaction(account_id="10001-1", transaction_type=TransactionType.WITHDRAW, amount=Decimal("75.50")),

            # Rodrigo Garro (10002-2)
            Transaction(account_id="10002-2", transaction_type=TransactionType.DEPOSIT, amount=Decimal("320.75")),
            Transaction(account_id="10002-2", transaction_type=TransactionType.WITHDRAW, amount=Decimal("100.00")),
            Transaction(account_id="10002-2", transaction_type=TransactionType.DEPOSIT, amount=Decimal("50.00")),

            # Hugo Souza (10003-3)
            Transaction(account_id="10003-3", transaction_type=TransactionType.DEPOSIT, amount=Decimal("200.00")),
            Transaction(account_id="10003-3", transaction_type=TransactionType.WITHDRAW, amount=Decimal("150.00")),
            Transaction(account_id="10003-3", transaction_type=TransactionType.WITHDRAW, amount=Decimal("50.00")),

            # Gustavo Henrique (10004-4)
            Transaction(account_id="10004-4", transaction_type=TransactionType.DEPOSIT, amount=Decimal("5000.00")),
            Transaction(account_id="10004-4", transaction_type=TransactionType.DEPOSIT, amount=Decimal("3750.50")),
            Transaction(account_id="10004-4", transaction_type=TransactionType.WITHDRAW, amount=Decimal("1200.00")),

            # Matheus Bidu (10005-5)
            Transaction(account_id="10005-5", transaction_type=TransactionType.DEPOSIT, amount=Decimal("300.00")),
            Transaction(account_id="10005-5", transaction_type=TransactionType.WITHDRAW, amount=Decimal("100.00")),
            Transaction(account_id="10005-5", transaction_type=TransactionType.WITHDRAW, amount=Decimal("49.70")),

            # Breno Bidon (10006-6)
            Transaction(account_id="10006-6", transaction_type=TransactionType.DEPOSIT, amount=Decimal("15000.00")),
            Transaction(account_id="10006-6", transaction_type=TransactionType.DEPOSIT, amount=Decimal("10000.00")),
            Transaction(account_id="10006-6", transaction_type=TransactionType.WITHDRAW, amount=Decimal("2600.00")),
        ]


    def get_all_transactions(self) -> List[Transaction]:
        
        return self.transactions

    def get_transaction(self, id: UUID) -> Optional[Transaction]:
        
        for transaction in self.transactions:
            if transaction.id == id:
                return transaction

        return None

    def get_history(self, account_id: str) -> List[Transaction]:
        
        history = []

        for transaction in self.transactions:
            if transaction.account_id == account_id:
                history.append(transaction)

        return history
    
    def create_transaction(self, transaction: Transaction) -> Optional[Transaction]:
        
        self.transactions.append(transaction)
        return transaction