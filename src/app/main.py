from fastapi import FastAPI, HTTPException
from mangum import Mangum

from pydantic import BaseModel

from src.app.routes import account_routes

from .environments import Environments

from .errors.entity_errors import ParamNotValidated

from .enums.item_type_enum import ItemTypeEnum

from .entities.item import Item

from decimal import Decimal

from src.app.enums.transactionType import TransactionType
from src.app.entities.transaction import Transaction  # ← adicione essa linha


app = FastAPI()

app.include_router(account_routes.router)

repo = Environments.get_item_repo()()
account_repo = Environments.get_account_repo()()    # get firts account
transaction_repo = Environments.get_transaction_repo()()

# a baixo estão as rotas da api
# elas interagem com os métodos de repositório. por exemplo a rota create item chama, não exclusivamente,
# o método repo.create_item() para criar o item no nosso repositório


# esse comando serve para um teste simples da API 
#@app.get("/")
#def root():
#    return {"message: Hello World"}

@app.get("/")# o / é aonde vai estar o endpoint ( pode ter o msm end point para metodos diferentes so tem q identificar)
def execute_get_para_barra():
    account = account_repo.get_account("10001-1") # preciso puxar um usuarioo mock (account_ did), preferi puxando so um usuario do q todos
    return account.__dict__ # tranforma diretamente para dicionario (tranforma os parametros para json)
 
class DepositRequest(BaseModel): # essa classe serve para definir o formato do body da requisição ou seja ela vai validar o json q sera passado
    amount: float

class TransactionRequest(BaseModel):
    account_id: str
    transaction_type: TransactionType  # agora sim é o Enum
    amount: float

@app.post("/deposit")
def deposit(amount: float):

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Valor inválido"
        )

    account = account_repo.get_account("10001-1") # pegar do mock esse usuario e ver o salfo

    if float(account.current_balance) > 0 and amount >= 2 * float(account.current_balance):
        raise HTTPException(
                status_code=403,
                detail="Depósito suspeito"
            )

    new_balance = float(account.current_balance) + amount # calculo do q foi depositado + oq a pessoa tinha ja

    account_repo.update_account( "10001-1", current_balance=new_balance) # salva o novo saldo da conta

    transaction = Transaction( # cria uma representaçao da transação
        account_id="10001-1",
        transaction_type=TransactionType.DEPOSIT,
        amount=Decimal(str(amount)),
        current_balance=Decimal(str(new_balance))
    )

    created_transaction = transaction_repo.create_transaction(transaction) # salva essa representação

    return { # retorna o novo saldo e o id da transação criada
        "current_balance": new_balance,
        "transaction_id": str(created_transaction.id),
        "timestamp": created_transaction.created_at.timestamp() * 1000
    }

@app.get("/items/get_all_items")
def get_all_items():
    items = repo.get_all_items()
    return {
        "items": [item.to_dict() for item in items]
    }

@app.get("/items/{item_id}")
def get_item(item_id: str):
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")
    
    return {
        "item_id": item_id,
        "item": item.to_dict()    
    }

@app.post("/items/create_item", status_code=201)
def create_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    # por exemplo, dentro da rota create item, chamamos um get_item para checar se o item ja existe
    # em nosso repositorio
    
    item = repo.get_item(item_id)
    if item is not None:
        raise HTTPException(status_code=409, detail="Item already exists")
    
    name = request.get("name")
    price = request.get("price")
    item_type = request.get("item_type")
    if item_type is None:
        raise HTTPException(status_code=400, detail="Item type is required")
    if type(item_type) != str:
        raise HTTPException(status_code=400, detail="Item type must be a string")
    if item_type not in [possible_type.value for possible_type in ItemTypeEnum]:
        raise HTTPException(status_code=400, detail="Item type is not a valid one")
    
    admin_permission = request.get("admin_permission")
    
    try:
        item = Item(
            item_id=item_id,
            name=name,
            price=price,
            item_type=ItemTypeEnum[item_type], 
            # bate a string que veio na request com todos os .values dentro do enum ItemTypeEnum.
            # ou seja, se vier uma string TOY ele vai converter para ItemTypeEnum.TOY
            admin_permission=admin_permission,
        )
    except ParamNotValidated as err:
        raise HTTPException(status_code=400, detail=err.message)
    
    item_response = repo.create_item(item)
    return {
        "item_id": item_id,
        "item": item_response.to_dict()    
    }
    
@app.delete("/items/delete_item")
def delete_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")

    item_deleted = repo.delete_item(item_id)
    
    return {
        "item_id": item_id,
        "item": item_deleted.to_dict()    
    }
    
@app.put("/items/update_item")
def update_item(request: dict):
    item_id = request.get("item_id")
    
    validation_item_id = Item.validate_item_id(item_id=item_id)
    if not validation_item_id[0]:
        raise HTTPException(status_code=400, detail=validation_item_id[1])
    
    item = repo.get_item(item_id)
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item Not found")

    name = request.get("name")
    price = request.get("price")
    admin_permission = request.get("admin_permission")

    item_type_value = request.get("item_type")
    if item_type_value != None:
        if type(item_type_value) != str:
            raise HTTPException(status_code=400, detail="Item type must be a string")
        if item_type_value not in [possible_type.value for possible_type in ItemTypeEnum]:
            raise HTTPException(status_code=400, detail="Item type is not a valid one")
        item_type = ItemTypeEnum[item_type_value]
    else:
        item_type = None
        
    item_updated = repo.update_item(item_id, name, price, item_type, admin_permission)
    
    return {
        "item_id": item_id,
        "item": item_updated.to_dict()    
    }

VALID_BILLS = {"2", "5", "10", "20", "50", "100", "200"}

@app.post("/withdraw")
def withdraw(request: dict):

    amount = sum(
        int(bill) * request.get(bill, 0)
        for bill in VALID_BILLS
    )

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Valor inválido: nenhuma cédula informada ou total zerado"
        )

    account = account_repo.get_account("10001-1")

    if float(account.current_balance) < amount:
        raise HTTPException(
            status_code=403,
            detail="Saldo insuficiente para transação"
        )

    new_balance = float(account.current_balance) - amount

    account_repo.update_account("10001-1", current_balance=new_balance)

    transaction = Transaction(
        account_id="10001-1",
        transaction_type=TransactionType.WITHDRAW,
        amount=Decimal(str(amount)),
        current_balance=Decimal(str(new_balance))
    )

    created_transaction = transaction_repo.create_transaction(transaction)

    return {
        "current_balance": new_balance,
        "timestamp": created_transaction.created_at.timestamp() * 1000
    }


@app.get("/history")
def history():
    # retorna todas as transações da conta "10001-1" em ordem cronológica
    transactions = transaction_repo.get_history("10001-1")

    return {
        "all_transactions": [
            {
                "type": t.transaction_type.value,
                "value": float(t.amount),
                "current_balance": float(t.current_balance),
                "timestamp": t.created_at.timestamp() * 1000
            }
            for t in transactions
        ]
    }
    


handler = Mangum(app, lifespan="off")
