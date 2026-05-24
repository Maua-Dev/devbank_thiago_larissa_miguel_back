import pytest
import inspect
from abc import ABC
from src.app.repo.account_repository_interface import AccountRepository


class Test_AccountRepositoryInterface:

    # teste para ver se a classe foi declarada corretamente como abstrata
    def test_account_repository_is_abstract(self):
        assert issubclass(AccountRepository, ABC)

    # teste que para garantir que a AccountRepository so possa ser usada se ela for implementada
    def test_account_repository_cannot_be_used(self):
        with pytest.raises(TypeError):
            AccountRepository()

    # teste para confirmar que o metodo get existe na interface (com todas as contas)
    def test_account_repository_get_all_accounts(self):
        assert hasattr(AccountRepository, "get_all_accounts")

    # teste para confirmar que o metodo get existe na interface (com uma conta especifica)
    def test_account_repository_get_account(self):
        assert hasattr(AccountRepository, "get_account")

    # teste  para confirma que o metodo de criacao de conta existe na interface
    def test_account_repository_create_account(self):
        assert hasattr(AccountRepository, "create_account")

    # teste  para confirma que o metodo de deletar conta existe na interface
    def test_account_repository_delete_account(self):
        assert hasattr(AccountRepository, "delete_account")
    
    # teste para confirmar que o metodo de atualizar a conta existe na interface
    def test_account_repository_update_account(self):
        assert hasattr(AccountRepository, "update_account")

    # teste que lista os metodos abstratos 
    def test_account_repository_abstract_methods(self):
        abstract_methods = AccountRepository.__abstractmethods__

        assert "get_all_accounts" in abstract_methods
        assert "get_account" in abstract_methods
        assert "create_account" in abstract_methods
        assert "delete_account" in abstract_methods
        assert "update_account" in abstract_methods

    # teste que verifica se a quantidade retornada no anterior é = a que a gente criou (5)
    def test_account_repository_number_of_abstract_methods(self):
        assert len(AccountRepository.__abstractmethods__) == 5

    # teste que verifica se o account_id existe na assinatura
    def test_get_account_signature(self):
        sig = inspect.signature(AccountRepository.get_account)

        assert "account_id" in sig.parameters

    # teste que verifica se o account existe na assinatura
    def test_create_account_signature(self):
        sig = inspect.signature(AccountRepository.create_account)

        assert "account" in sig.parameters

    # teste que verifica o delete_accont na assinatura
    def test_delete_account_signature(self):
        sig = inspect.signature(AccountRepository.delete_account)

        assert "account_id" in sig.parameters

    # teste que verifica o update_account na assinatura
    def test_update_account_signature(self):
        sig = inspect.signature(AccountRepository.update_account)
        params = sig.parameters

        assert "account_id" in params
        assert "name" in params
        assert "current_balance" in params

        assert params["name"].default is None
        assert params["current_balance"].default is None

    # teste que verifica as heranças
    def test_concrete_class_inheritance(self):
        class IncompleteRepo(AccountRepository):
            def get_all_accounts(self): pass

        with pytest.raises(TypeError):
            IncompleteRepo()

    