from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from uuid import UUID

from entities.transaction import Transaction


class TransactionRepository(ABC):

    """
    IMPORTANTE: não adicionei um método abstrato para o delete nem update pois TRANSAÇÕES NÃO PODEM SER DELETADAS/ALTERADAS.
    em transações bancárias precisamos de atomicidade, um registro imutável de operação, vou revisar isso depois
    mas por enquanto fica assim mesmo, qualquer dúvida me mandar mensagem no zap zap.
    """

    @abstractmethod
    def get_all_transactions(self) -> List[Transaction]:
         
        """
        Return all stored transactions.

        Returns:
            List[transactions]: Collection of all transactions currently persisted.
        """
        pass

    @abstractmethod
    def get_transaction(self, id: UUID) -> Optional[Transaction]:
        
        """
        Retrieve a single transaction
         by its identifier.

        Args:
            id (uuid): UUID string stored in the entity attribute `transactions.id`.

        Returns:
            Optional[Transaction]: The matching transactions when found, otherwise `None`.
        """
        pass

    def get_history(self, account_id: str) -> List[Transaction]:
        
        """

        IMPORTANTE: ESSE É O NOSSO MÉTODO RESPONSÁVEL PARA FAZERMOS A REQUISÃO DO HISTÓRICO.

        Retrieve all transactions associated with a given account.

        Args:
            account_id (str): account_id stored in the entity attribute 'transactions.account_id'.
        

        Returns:
            List[Transaction]: Collection of all transactions currently persisted.
        """

        pass

    @abstractmethod
    def create_transaction(self, transaction: Transaction) -> Optional[Transaction]:
        
        """
        Persist a new transaction.

        Args:
            transaction (Transaction): Fully validated transaction entity.

        Returns:
            Transaction: The persisted transaction.
        """
        pass
