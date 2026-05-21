from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.entities.account import Account


class AccountRepository(ABC): # interface que define uma classe abstrata que será implementada no mock

    @abstractmethod
    def get_all_accounts(self) -> List[Account]: # -> significa hint, ou seja, especifica o retorno da função
        """
        Return all stored accounts.
        
        
        Returns:
            List[Account]: Collection of all accounts currently persisted.
        """
        pass # Indica ao python que essa função não ter um corpo de retorno

    @abstractmethod
    def get_account(self, account_id: str) -> Optional[Account]: # Optional: a função pode não retornar um objeto com esse id (caso ele não exista por exmeplo)
        """
        Retrieve a single account by its identifier.

        Args:
            account_id (str): Identifier stored in the entity attribute `Account._id`.

        Returns:
            Optional[Account]: The matching account when found, otherwise `None`.
        """
        pass

    @abstractmethod  
    def create_account(self, account: Account) -> Account:
        """
        Persist a new account.

        Args:
            account (Account): Fully validated account entity.

        Returns:
            Account: The persisted account.
        """
        pass

    @abstractmethod
    def delete_account(self, account_id: str) -> Optional[Account]: # Porque um delete tem retorno?
        """
        Delete an account by its identifier.

        Args:
            account_id (str): UUID string of the target account.

        Returns:
            Optional[Account]: Deleted account when found, otherwise `None`.
        """
        pass

    @abstractmethod
    def update_account( # VERIFICAR -> não deveria possuir um update_account? Ele não faz sentido se vou manipular os dados da conta com um deposit e um withdraw, além disso dados da conta devem ser restritos imagino
        self,
        account_id: str,
        name : Optional[str] = None,
        current_balance: Optional[float] = None
    ) -> Optional[Account]:
        
        """
        Update mutable fields of an existing item.

        Args:
            account_id (str): UUID string of the account to update.
            name (str, optional): New name.
            current_balance (float, optional): New current balance.

        Returns:
            Optional[Account]: Updated account when found, otherwise `None`.
        """
        pass
        