from datetime import datetime, timezone
from decimal import Decimal
import re
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, field_validator

from src.app.enums import transactionType


class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4) # geração automática de ID 
    account_id: str 
    transaction_type: transactionType # Lari/Miguel deem uma olhada na class transactionType 
    amount: Decimal # IMPORTANTE -> coloquei type Decimal 
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    """ 
    IMPORTANTE -> created_at marca o timestamp da transação, atributo essencial. 
    Se eu colocasse somente um datetime.now(timezone.utc) o Python ia executar a
    leitura uma vez e isso ia fazer com que todas as transações tivessem o mesmo 
    valor, então chamei uma lambda (tipo uma func anônima) pra que em cada instância
    o valor fosse único.
    """
    
    @field_validator("account_id")
    @classmethod
    def validate_account_id(cls, value: str):
        if not re.fullmatch(r'^\d{5}-\d{1}$', value):
            raise ValueError(f"account_id inválido: '{value}' (esperado XXXXX-X)")
        return value
    
    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Decimal):

        if value <= 0:
            raise ValueError(
                "amount deve ser maior que zero"
            )

        return value
    


