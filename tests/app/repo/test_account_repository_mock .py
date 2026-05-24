import pytest
from src.app.entities.account import Account
from src.app.repo.account_repository_mock import AccountRepositoryMock
 
 
class Test_AccountRepositoryMock:
    FIRST_ACCOUNT_ID   = "10001-1"
    NOT_FOUND_ACCOUNT_ID = "00000-0"
    CREATED_ACCOUNT_ID   = "99999-9"
 
    # teste para verificar se todos os acconts do repositorios sao retornados
    def test_get_all_accounts(self):
        repo = AccountRepositoryMock()
        accounts = repo.get_all_accounts()

        assert len(accounts) == len(repo.accounts)
        assert all([account_expect == account for account_expect, account in zip(repo.accounts, accounts)])
 
    # teste para verificar o retorno de uma conta especifica
    def test_get_account(self):
        repo = AccountRepositoryMock()
        account = repo.get_account(account_id=self.FIRST_ACCOUNT_ID)

        assert account is not None
        assert account.account_id == self.FIRST_ACCOUNT_ID
 
    # teste para quando o usuario nao é encontrado
    def test_get_account_not_found(self):
        repo = AccountRepositoryMock()
        account = repo.get_account(account_id=self.NOT_FOUND_ACCOUNT_ID)

        assert account is None

    # teste de criacao de um novo usuario
    def test_create_account(self):
        repo = AccountRepositoryMock()
        len_before = len(repo.accounts)

        account = Account(
            account_id=self.CREATED_ACCOUNT_ID,
            name="Ana banana",
            agency="0999",
            current_balance=500.00,
        )

        repo.create_account(account=account)
        len_after = len(repo.accounts)
 
        assert len_after == len_before + 1
        assert repo.accounts[-1].account_id == account.account_id
        assert repo.accounts[-1].account_id == self.CREATED_ACCOUNT_ID
        assert repo.accounts[-1].agency == "0999"
        assert repo.accounts[-1].name == "Ana banana"
        assert repo.accounts[-1].current_balance == 500.00
 
    # teste para ver se foi criado a conta corretamente
    def test_create_account_correctly(self):
        repo = AccountRepositoryMock()

        account = Account(
            account_id=self.CREATED_ACCOUNT_ID,
            name="Ana banana",
            agency="0999",
            current_balance=500.00,
        )

        returned = repo.create_account(account=account)
        assert returned == account
 
    # teste para ver se esta deletando uma conta corretamente
    def test_delete_account(self):
        repo = AccountRepositoryMock()
        account_expected_to_be_deleted = repo.get_account(self.FIRST_ACCOUNT_ID)
        len_before = len(repo.accounts)
        account = repo.delete_account(account_id=self.FIRST_ACCOUNT_ID)
        len_after = len(repo.accounts)

        assert len_after == len_before - 1
        assert account == account_expected_to_be_deleted
        assert repo.get_account(self.FIRST_ACCOUNT_ID) is None
        assert account_expected_to_be_deleted not in repo.accounts
 
    # teste para ver se responde corretamente ao tentar deletar um usuario que nao existe
    def test_delete_account_not_found(self):
        repo = AccountRepositoryMock()
        len_before = len(repo.accounts)
        account = repo.delete_account(account_id=self.NOT_FOUND_ACCOUNT_ID)

        assert account is None
        assert len(repo.accounts) == len_before
 
    # teste para tentar atualizar a conta (atualizar o saldo)
    def test_update_account_current_balance(self):
        repo = AccountRepositoryMock()
        name_before = repo.get_account(self.FIRST_ACCOUNT_ID).name
        current_balance = 777.77
        account_updated = repo.update_account(account_id=self.FIRST_ACCOUNT_ID, current_balance=current_balance)
 
        assert account_updated is not None
        assert account_updated.current_balance == current_balance
        assert repo.get_account(self.FIRST_ACCOUNT_ID).current_balance == current_balance
 
    # teste de quando o usuario nao é encontrado e tentam atualizar algo
    def test_update_account_not_found(self):
        repo = AccountRepositoryMock()

        account_updated = repo.update_account(
            account_id=self.NOT_FOUND_ACCOUNT_ID,
            current_balance=0.0,
        ) 

        assert account_updated is None
 
    # teste de tentar modificar os dados da conta porem sem nenhuma real alteracao
    def test_update_account_without_changes(self):
        
        repo = AccountRepositoryMock()
        account_before = repo.get_account(self.FIRST_ACCOUNT_ID)
        updated = repo.update_account(account_id=self.FIRST_ACCOUNT_ID)

        assert updated == account_before