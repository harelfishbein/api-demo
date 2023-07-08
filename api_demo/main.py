from fastapi import FastAPI, HTTPException, Depends
from uuid import UUID, uuid4
from typing import Union
from typing_extensions import Annotated

### Model Classes
from DTO import *
from repository import Repository, ItemName

fastapi = FastAPI()

@fastapi.get("/")
async def root():
    return {"message": "hello"}

@fastapi.post("/repo")
async def repo(r: Annotated[Repository, Depends()]):
    await r.make()

@fastapi.get("/inventory/{name}")
async def get_inventory_item(name: ItemName, r: Annotated[Repository, Depends()]):
    print(r.root_path)
    i = await r.load_inventory(name)
    return i

@fastapi.post("/inventory/{name}/add")
async def add_inventory_item(name: ItemName, r: Annotated[Repository, Depends()], quantity: int = 1):
    inventory = await r.load_inventory(name)
    inventory.quantity += quantity
    await r.dump_inventory(inventory)
    return inventory.quantity
    
@fastapi.post("/inventory/{name}/price")
async def get_inventory_item(r: Annotated[Repository, Depends()], name: ItemName, price: float):
    inventory = await r.load_inventory(name)
    inventory.unit_price = price
    await r.dump_inventory(inventory)
    return True
    
@fastapi.post("/customer/")
async def add_customer(r: Annotated[Repository, Depends()], customer: CustomerDTO, id: Union[UUID, None] = None):
    my_customer = customer._to_customer()
    await r.dump_customer(my_customer)
    return my_customer.id

