from pydantic import BaseModel, field_validator 
import re

class Account(BaseModel):
    name : str
    agency: str
    account_id: str
    current_balance: float

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not re.fullmatch(r'^[A-Za-zÀ-ÿ\s]+$', value):
            raise ValueError(f"name inválido: '{value}'")
        return value

    @field_validator("agency")
    @classmethod
    def validate_agency(cls, value: str):
        if not re.fullmatch(r'^\d{4}$', value):
            raise ValueError(f"agency inválida: '{value}' (esperado 4 dígitos)")
        return value

    @field_validator("account_id")
    @classmethod
    def validate_account_id(cls, value: str):
        if not re.fullmatch(r'^\d{5}-\d{1}$', value):
            raise ValueError(f"account_id inválido: '{value}' (esperado XXXXX-X)")
        return value

    @field_validator("current_balance")
    @classmethod
    def validate_current_balance(cls, value: float):
        if value < 0:
            raise ValueError("Saldo não pode ser negativo")
        return value