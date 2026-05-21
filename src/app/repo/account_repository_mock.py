from typing import List, Optional
from src.app.entities.account import Account
from src.app.repo.account_repository_interface import AccountRepository


class AccountRepositoryMock(AccountRepository):

    accounts: List[Account]

    def __init__(self):

        self.accounts = [
            Account(
                name="Yuri Alberto",
                agency="0001",
                account_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                current_balance=1500.00
            ),

            Account(
                name="Rodrigo Garro",
                agency="0042",
                account_id="b2c3d4e5-f6a7-8901-bcde-f12345678901",
                current_balance=320.75
            ),

            Account(
                name="Hugo Souza",
                agency="0107",
                account_id="c3d4e5f6-a7b8-9012-cdef-123456789012",
                current_balance=0.00 
            ),

            Account(
                name="Gustavo Henrique",
                agency="0233",
                account_id="d4e5f6a7-b8c9-0123-defa-234567890123",
                current_balance=8750.50 
            ),

            Account(
                name="Matheus Bidu",
                agency="0015",
                account_id="e5f6a7b8-c9d0-1234-efab-345678901234",
                current_balance=150.30     
            ),

            Account(
                name="Breno Bidon",
                agency="0388",
                account_id="f6a7b8c9-d0e1-2345-fabc-456789012345",
                current_balance=22400.00        
            ) 
        ]

    def get_all_accounts(self) -> List[Account]:

        return self.accounts
    
    def get_account(self, account_id: str) -> Optional[Account]:
        
        for account in self.accounts: 
                if account.account_id == account_id:
                     return account
        return None
                
    def create_account(self, account: Account) -> Account:
        self.accounts.append(account)
        return account

    def delete_account(self, account_id: str) -> Optional[Account]:
        
        for account in self.accounts:
             if account.account_id == account_id:
                  self.accounts.remove(account)
                  return account
        return None
             
    def update_account( # VERIFICAR -> não deveria possuir um update_account? Ele não faz sentido se vou manipular os dados da conta com um deposit e um withdraw, além disso dados da conta devem ser restritos imagino
        self,
        account_id: str,
        name : Optional[str] = None,
        current_balance: Optional[float] = None
    ) -> Optional[Account]:
        
        for account in self.accounts:
         
            if account.account_id == account_id:
                if name is not None:
                    account.name = name
                if current_balance is not None:
                    account.current_balance = current_balance
                return account 
        return None
             


