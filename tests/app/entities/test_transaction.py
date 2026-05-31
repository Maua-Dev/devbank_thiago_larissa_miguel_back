import pytest
from decimal import Decimal
from uuid import UUID
from pydantic import ValidationError

from src.app.entities.transaction import Transaction
from src.app.enums.transactionType import TransactionType


def make_transaction(**overrides) -> Transaction:
    return Transaction(
        account_id=overrides.get("account_id", "12345-6"),
        transaction_type=overrides.get("transaction_type", TransactionType.DEPOSIT),
        amount=overrides.get("amount", Decimal("100.00")),
    )


class Test_Transaction:
    # teste para ver se cria transacao valida
    def test_create_transaction_valid(self):
        Transaction = make_transaction()

        assert Transaction.account_id == "12345-6"
        assert Transaction.transaction_type == TransactionType.DEPOSIT
        assert Transaction.amount == Decimal("100.00")

    # teste para ver se o id é criado automaticamente
    def test_create_transaction_auto_id(self):
        Transaction = make_transaction()

        assert isinstance(Transaction.id, UUID)

    # teste para ver se duas transaçao diferente tem id diferente tambem
    def test_create_transaction_unique_ids(self):
        Transaction1 = make_transaction()
        Transaction2 = make_transaction()

        assert Transaction1.id != Transaction2.id

    # teste para ver se esta no formato correto
    def test_validate_account_id_valid(self):
        Transaction = make_transaction(account_id="00001-0")

        assert Transaction.account_id == "00001-0"

    # teste para ver se recusa sem o hifem
    def test_validate_account_no_dash(self):
        with pytest.raises(ValidationError) as exc_info:
            make_transaction(account_id="123456")

        assert "account_id inválido" in str(exc_info.value)

    # teste se tiver menos de 5 numeros antes do hifem
    def test_validate_account_short_before_dash(self):
        with pytest.raises(ValidationError) as exc_info:
            make_transaction(account_id="1234-5")

        assert "account_id inválido" in str(exc_info.value)

    # teste se tiver mais de 5 numeros depois do hifem
    def test_validate_account_long_before_dash(self):
        with pytest.raises(ValidationError) as exc_info:
            make_transaction(account_id="123456-5")

        assert "account_id inválido" in str(exc_info.value)

    # teste se tiver mais de um digito depois do hifem
    def test_validate_account_two_digits_after_dash(self):
        with pytest.raises(ValidationError) as exc_info:
            make_transaction(account_id="12345-67")

        assert "account_id inválido" in str(exc_info.value)

    # teste para ver se recusa letras
    def test_validate_account_with_letter(self):
        with pytest.raises(ValidationError) as exc_info:
            make_transaction(account_id="1234A-5")

        assert "account_id inválido" in str(exc_info.value)

    # teste para ver se recusa se o campo estiver vazio
    def test_validate_account_empty(self):
        with pytest.raises(ValidationError):
            make_transaction(account_id="")

    # teste se aprova valor positivo
    def test_validate_amount_valid(self):
        Transaction = make_transaction(amount=Decimal("500"))

        assert Transaction.amount == Decimal("500")

    # teste para ver se aprova positivos com virgula
    def test_validate_amount_decimal(self):
        Transaction = make_transaction(amount=Decimal("0.01"))

        assert Transaction.amount == Decimal("0.01")

    # teste para ver se reprova se o valor for 0
    def test_validate_amount_zero(self):
        with pytest.raises(ValidationError) as exc_info:
            make_transaction(amount=Decimal("0"))

        assert "amount deve ser maior que zero" in str(exc_info.value)

    # teste para ver se reprova se o valor for negativo
    def test_validate_amount_negative(self):
        with pytest.raises(ValidationError) as exc_info:
            make_transaction(amount=Decimal("-0.01"))

        assert "amount deve ser maior que zero" in str(exc_info.value)
