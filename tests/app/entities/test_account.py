import pytest
from pydantic import ValidationError
from src.app.entities.account import Account
from src.app.repo.account_repository_mock import AccountRepositoryMock

_mock = AccountRepositoryMock()
_base = _mock.accounts[0] 

def make_account(**overrides) -> Account:
    return Account(
        name=overrides.get("name", _base.name),
        agency=overrides.get("agency", _base.agency),
        account_id=overrides.get("account_id", _base.account_id),
        current_balance=overrides.get("current_balance", _base.current_balance),
    )

class Test_Account:
    # teste para ver se os campos estao validos
    def test_create_account_valid(self):
        account = make_account()
        
        assert account.name == _base.name
        assert account.agency == _base.agency
        assert account.account_id == _base.account_id
        assert account.current_balance == _base.current_balance

    # teste para garantir que aceite o saldo zerado (so n pode ser negativo)
    def test_create_account_zero_balance(self):
        account = make_account(current_balance=0.0)

        assert account.current_balance == 0.0

    # teste para garantir que nao haja erro de tipo
    def test_create_account_balance_as_integer(self):
        account = make_account(current_balance=1000)

        assert account.current_balance == 1000.0

    # teste para ver se a string do nome nao tem numeros
    def test_validate_name_invalid_with_number(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(name="Lulu2")

        assert "name inválido" in str(exc_info.value)

    # teste para ver se a string do nome nao tem caracteres especiais
    def test_validate_name_invalid_with_special_char(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(name="L&l&")

        assert "name inválido" in str(exc_info.value)

    # teste para ver se a string do nome n esta vazia
    def test_validate_name_invalid(self):
        with pytest.raises(ValidationError):
            make_account(name="")

    # teste para ver se a string da agencia tem menos de 4 digitos
    def test_validate_agency_invalid_too_short(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(agency="042")

        assert "agency inválida" in str(exc_info.value)

    # teste para ver se a string da agencia tem mais de 4 digitos
    def test_validate_agency_invalid_too_long(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(agency="00421")

        assert "agency inválida" in str(exc_info.value)

    # teste para ver se a agencia so contem digitos
    def test_validate_agency_invalid_with_letter(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(agency="00AB")

        assert "agency inválida" in str(exc_info.value)

    # teste para ver se a string da agencia esta vazia
    def test_validate_agency_invalid(self):
        with pytest.raises(ValidationError):
            make_account(agency="")

    # teste para verificar se o id bate com o padrao xxxxx-x
    def test_validate_account_id_invalid_template(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(account_id="123456")

        assert "account_id inválido" in str(exc_info.value)

    # teste para verificar se o id tem menos de 5 digitos antes do -
    def test_validate_account_id_invalid_digits_before(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(account_id="1234-5")

        assert "account_id inválido" in str(exc_info.value)

    # teste para verificar se o id tem dois numero apos o -
    def test_validate_account_id_invalid_two_digits(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(account_id="12345-67")

        assert "account_id inválido" in str(exc_info.value)

    # teste para verificar se o id contem letra
    def test_validate_account_id_invalid_with_letter(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(account_id="1234A-5")

        assert "account_id inválido" in str(exc_info.value)

    # teste para verificar se a string ta vazia no id
    def test_validate_account_id_invalid(self):
        with pytest.raises(ValidationError):
            make_account(account_id="")

    # teste que verifica se retorna corretamente em caso de valores positivos no saldo
    def test_validate_current_balance_valid_positive(self):
        account = make_account(current_balance=250.75)
        assert account.current_balance == 250.75

    # teste que verifica se retorna erro em caso de valores negativos no saldo
    def test_validate_current_balance_negative(self):
        with pytest.raises(ValidationError) as exc_info:
            make_account(current_balance=-0.01)
        assert "Saldo não pode ser negativo" in str(exc_info.value)

    # teste que pega todos os campos invalidos 
    def test_multiple_invalid_validation_error(self):
        with pytest.raises(ValidationError) as exc_info:
            Account(
                name="N00mee&&",
                agency="AB",
                account_id="errado",
                current_balance=-100.0,
            )

        errors = exc_info.value.errors()
        fields_with_error = {e["loc"][0] for e in errors}

        assert "name" in fields_with_error
        assert "agency" in fields_with_error
        assert "account_id" in fields_with_error
        assert "current_balance" in fields_with_error