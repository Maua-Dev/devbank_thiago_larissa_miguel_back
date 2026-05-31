import pytest
import inspect
from abc import ABC
from src.app.repo.transaction_repository_interface import TransactionRepository


class Test_TransactionRepositoryInterface:

    # teste para ver se a classe foi declarada como abstrata
    def test_transaction_repository_is_abstract(self):
        assert issubclass(TransactionRepository, ABC)

    # teste que garante que a TransactionRepository so possa ser usada se implementada
    def test_transaction_repository_cannot_be_used(self):
        with pytest.raises(TypeError):
            TransactionRepository()

    # teste para confirmar que o método get_all_transactions existe na interface
    def test_transaction_repository_get_all_transactions(self):
        assert hasattr(TransactionRepository, "get_all_transactions")

    # teste para confirmar que o método get_transaction existe na interface
    def test_transaction_repository_get_transaction(self):
        assert hasattr(TransactionRepository, "get_transaction")

    # teste para confirmar que o método get_history existe na interface
    def test_transaction_repository_get_history(self):
        assert hasattr(TransactionRepository, "get_history")

    # teste para confirmar que o método create_transaction existe na interface
    def test_transaction_repository_create_transaction(self):
        assert hasattr(TransactionRepository, "create_transaction")

    # teste que lista os métodos abstratos obrigatórios
    def test_transaction_repository_abstract_methods(self):
        abstract_methods = TransactionRepository.__abstractmethods__

        assert "get_all_transactions" in abstract_methods
        assert "get_transaction" in abstract_methods
        assert "create_transaction" in abstract_methods

    # get_history nao e abstrato
    def test_get_history_is_not_abstract(self):
        abstract_methods = TransactionRepository.__abstractmethods__

        assert "get_history" not in abstract_methods

    # teste que verifica a quantidade de metodos abstratos
    def test_transaction_repository_number_abstract_methods(self):
        assert len(TransactionRepository.__abstractmethods__) == 3

    # teste que verifica se o id existe na assinatura 
    def test_get_transaction_signature(self):
        sig = inspect.signature(TransactionRepository.get_transaction)

        assert "id" in sig.parameters

    # teste que verifica se o account_id existe na assinatura
    def test_get_history_signature(self):
        sig = inspect.signature(TransactionRepository.get_history)

        assert "account_id" in sig.parameters

    # teste que verifica se o transaction existe na assinatura 
    def test_create_transaction_signature(self):
        sig = inspect.signature(TransactionRepository.create_transaction)

        assert "transaction" in sig.parameters

    # teste que verifica as heranças
    def test_concrete_class_inherits(self):
        class CompleteRepo(TransactionRepository):
            def get_all_transactions(self): pass
            def get_transaction(self, id): pass
            def create_transaction(self, transaction): pass

        assert hasattr(CompleteRepo, "get_history")