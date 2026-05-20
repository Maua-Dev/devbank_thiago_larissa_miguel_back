from pydantic import BaseModel, field_validator

class Account(BaseModel):
    name : str
    agency: str
    account: str
    current_balance: float

    @field_validator("current_balance")
    @classmethod
    def validate_balance(cls, value):

        if value < 0:
            raise ValueError("Negative balance")
        
        return value
    
