from fastapi.exceptions import HTTPException
import pytest
import src.app.main as main_module
from src.app.main import get_all_items, get_item, create_item, delete_item, update_item, execute_get_para_barra, deposit, withdraw, history
from src.app.repo.item_repository_mock import ItemRepositoryMock
from src.app.repo.account_repository_mock import AccountRepositoryMock
from src.app.repo.transaction_repository_mock import TransactionRepositoryMock


class Test_Main:
    EXISTING_ITEM_ID = "b11af449-22c7-43db-b0e4-dbfbbe7fdbd7"
    EXISTING_ADMIN_ITEM_ID = "b41af449-22c7-43db-b0e4-dbfbbe7fdbd7"
    EXISTING_UPDATE_ITEM_ID = "b21af449-22c7-43db-b0e4-dbfbbe7fdbd7"
    NEW_ITEM_ID = "88f0920c-0de0-4e0a-bb46-abdb3705579d"
    NOT_FOUND_ITEM_ID = "00000000-0000-0000-0000-000000000000"
    INVALID_UUID_STRING = "1"

    def setup_method(self):
    # Reset do repositorio global usado em src.app.main a cada teste
        main_module.repo = ItemRepositoryMock()
        main_module.account_repo = AccountRepositoryMock()
        main_module.transaction_repo = TransactionRepositoryMock()
        
    def teste_execute_get_para_barra(self):
        repo = AccountRepositoryMock()
        response = execute_get_para_barra()

        assert response.get("name", None) != "Vitor soller"   
        print(response.get("name", None) == "Yuri Alberto")
        assert response.get("name", None) == "Yuri Alberto"

    def test_deposito_simples(self):
        response = deposit(amount=100.0)
 
        assert response.get("current_balance") == 1600.0  
 
    def test_deposito_retorna_transaction_id(self):
        response = deposit(amount=100.0)
 
        assert response.get("transaction_id") is not None
 
    def test_deposito_retorna_timestamp(self):
        response = deposit(amount=100.0)
 
        assert response.get("timestamp") is not None
 
    def test_deposito_zero_retorna_400(self):
        with pytest.raises(HTTPException) as err:
            deposit(amount=0.0)
 
        assert err.value.status_code == 400
 
    def test_deposito_negativo_retorna_400(self):
        with pytest.raises(HTTPException) as err:
            deposit(amount=-50.0)
 
        assert err.value.status_code == 400
 
    def test_deposito_suspeito_retorna_403(self):
        with pytest.raises(HTTPException) as err:
            deposit(amount=3000.0)
 
        assert err.value.status_code == 403
        assert err.value.detail == "Depósito suspeito"
 
    def test_deposito_acima_do_dobro_retorna_403(self):
        with pytest.raises(HTTPException) as err:
            deposit(amount=3200.0)
 
        assert err.value.status_code == 403
        assert err.value.detail == "Depósito suspeito"
 
    def test_deposito_com_saldo_zero_nao_bloqueia(self):
        main_module.account_repo.update_account("10001-1", current_balance=0.0)
        response = deposit(amount=100.0)
 
        assert response.get("current_balance") == 100.0

    def test_get_all_items(self):
        repo = ItemRepositoryMock()
        response = get_all_items()
        assert all(
            [
                item_expect.to_dict() == item
                for item_expect, item in zip(repo.items, response.get("items"))
            ]
        )

    def test_get_item(self):
        repo = ItemRepositoryMock()
        response = get_item(item_id=self.EXISTING_ITEM_ID)
        expected_item = repo.get_item(self.EXISTING_ITEM_ID)
        assert response == {
            "item_id": self.EXISTING_ITEM_ID,
            "item": expected_item.to_dict(),
        }

    def test_get_item_id_is_none(self):
        with pytest.raises(HTTPException):
            get_item(item_id=None)

    def test_get_item_id_is_not_string(self):
        with pytest.raises(HTTPException):
            get_item(item_id=1)

    def test_get_item_id_is_not_uuid(self):
        with pytest.raises(ValueError):
            get_item(item_id=self.INVALID_UUID_STRING)

    def test_create_item(self):
        body = {
            "item_id": self.NEW_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        response = create_item(request=body)
        assert response == {
            "item_id": self.NEW_ITEM_ID,
            "item": {
                "item_id": self.NEW_ITEM_ID,
                "name": "test",
                "price": 1.0,
                "item_type": "TOY",
                "admin_permission": False,
            },
        }

    def test_create_item_conflict(self):
        body = {
            "item_id": self.EXISTING_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        assert err.value.status_code == 409

    def test_create_item_missing_id(self):
        body = {
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        assert err.value.status_code == 400

    def test_create_item_id_is_not_string(self):
        body = {
            "item_id": 0,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        assert err.value.status_code == 400

    def test_create_item_id_is_not_uuid(self):
        body = {
            "item_id": self.INVALID_UUID_STRING,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(ValueError):
            create_item(request=body)

    def test_create_item_missing_type(self):
        body = {
            "item_id": self.NEW_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        assert err.value.status_code == 400

    def test_create_item_item_type_is_not_string(self):
        body = {
            "item_id": self.NEW_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": 1,
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        assert err.value.status_code == 400

    def test_create_item_item_type_is_not_valid(self):
        body = {
            "item_id": self.NEW_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": "test",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            create_item(request=body)
        assert err.value.status_code == 400

    def test_delete_item(self):
        body = {"item_id": self.EXISTING_ITEM_ID}
        response = delete_item(request=body)
        assert response["item_id"] == self.EXISTING_ITEM_ID
        assert response["item"]["name"] == "Barbie"

    def test_delete_item_missing_id(self):
        with pytest.raises(HTTPException) as err:
            delete_item(request={})
        assert err.value.status_code == 400

    def test_delete_item_id_is_not_string(self):
        with pytest.raises(HTTPException) as err:
            delete_item(request={"item_id": 1})
        assert err.value.status_code == 400

    def test_delete_item_id_is_not_uuid(self):
        with pytest.raises(ValueError):
            delete_item(request={"item_id": self.INVALID_UUID_STRING})

    def test_delete_item_id_not_found(self):
        with pytest.raises(HTTPException) as err:
            delete_item(request={"item_id": self.NOT_FOUND_ITEM_ID})
        assert err.value.status_code == 404

    def test_delete_item_with_admin_flag_on_entity(self):
        body = {"item_id": self.EXISTING_ADMIN_ITEM_ID}
        response = delete_item(request=body)
        assert response["item_id"] == self.EXISTING_ADMIN_ITEM_ID
        assert response["item"]["name"] == "Super Mario Bros"

    def test_update_item(self):
        body = {
            "item_id": self.EXISTING_UPDATE_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        response = update_item(request=body)
        assert response == {
            "item_id": self.EXISTING_UPDATE_ITEM_ID,
            "item": {
                "item_id": self.EXISTING_UPDATE_ITEM_ID,
                "name": "test",
                "price": 1.0,
                "item_type": "TOY",
                "admin_permission": False,
            },
        }

    def test_update_item_missing_id(self):
        body = {
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
        assert err.value.status_code == 400

    def test_update_item_id_is_not_string(self):
        body = {
            "item_id": 1,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
        assert err.value.status_code == 400

    def test_update_item_id_is_not_uuid(self):
        body = {
            "item_id": self.INVALID_UUID_STRING,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(ValueError):
            update_item(request=body)

    def test_update_item_not_found(self):
        body = {
            "item_id": self.NOT_FOUND_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
        assert err.value.status_code == 404

    def test_update_item_with_admin_flag_on_entity(self):
        body = {
            "item_id": self.EXISTING_ADMIN_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": "TOY",
            "admin_permission": False,
        }
        response = update_item(request=body)
        assert response == {
            "item_id": self.EXISTING_ADMIN_ITEM_ID,
            "item": {
                "item_id": self.EXISTING_ADMIN_ITEM_ID,
                "name": "test",
                "price": 1.0,
                "item_type": "TOY",
                "admin_permission": False,
            },
        }

    def test_update_item_type_not_string(self):
        body = {
            "item_id": self.EXISTING_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": 1,
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
        assert err.value.status_code == 400

    def test_update_item_type_not_valid(self):
        body = {
            "item_id": self.EXISTING_ITEM_ID,
            "name": "test",
            "price": 1.0,
            "item_type": "test",
            "admin_permission": False,
        }
        with pytest.raises(HTTPException) as err:
            update_item(request=body)
        assert err.value.status_code == 400
    
    #teste do POST /withdraw
    def test_withdraw(self):
        response = withdraw(amount=100.0)
        assert response["current_balance"] == 1400.0
        assert "timestamp" in response

    def test_withdraw_multiple_bills(self):
        response = withdraw(amount=200.0)
        assert response["current_balance"] == 1300.0
        assert "timestamp" in response

    def test_withdraw_insufficient_balance(self):
        with pytest.raises(HTTPException) as err:
            withdraw(amount=2000.0)
        assert err.value.status_code == 403
        assert err.value.detail == "Saldo insuficiente para transação"

    def test_withdraw_zero_amount(self):
        with pytest.raises(HTTPException) as err:
            withdraw(amount=0)
        assert err.value.status_code == 400

    def test_withdraw_creates_transaction(self):
        transactions_before = len(main_module.transaction_repo.get_history("10001-1"))
        withdraw(amount=50.0)
        transactions_after = len(main_module.transaction_repo.get_history("10001-1"))
        assert transactions_after == transactions_before + 1

    def test_withdraw_updates_balance(self):
        withdraw(amount=100.0)
        account = main_module.account_repo.get_account("10001-1")
        assert account.current_balance == 1400.0

    
    # teste do GET /history
    

    def test_history_returns_list(self):
        response = history()
        assert "all_transactions" in response
        assert isinstance(response["all_transactions"], list)

    def test_history_correct_fields(self):
        response = history()
        for transaction in response["all_transactions"]:
            assert "type" in transaction
            assert "value" in transaction
            assert "current_balance" in transaction
            assert "timestamp" in transaction

    def test_history_type_is_string(self):
        response = history()
        for transaction in response["all_transactions"]:
            assert isinstance(transaction["type"], str)

    def test_history_value_is_float(self):
        response = history()
        for transaction in response["all_transactions"]:
            assert isinstance(transaction["value"], float)

    def test_history_current_balance_is_float(self):
        response = history()
        for transaction in response["all_transactions"]:
            assert isinstance(transaction["current_balance"], float)

    def test_history_only_account_transactions(self):
        response = history()
        assert len(response["all_transactions"]) == 3

    def test_history_reflects_new_withdraw(self):
        withdraw(amount=100.0)
        response = history()
        last = response["all_transactions"][-1]
        assert last["type"] == "withdraw"
        assert last["value"] == 100.0
        assert last["current_balance"] == 1400.0

    def test_history_reflects_new_deposit(self):
        from src.app.main import DepositRequest
        deposit(amount=200.0)
        response = history()
        last = response["all_transactions"][-1]
        assert last["type"] == "deposit"
        assert last["value"] == 200.0
        assert last["current_balance"] == 1700.0
            






