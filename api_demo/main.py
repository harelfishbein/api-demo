from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4


from typing import *

### Model Classes
from DTO import *
from repository import ItemName
import repository

fastapi = FastAPI()

@fastapi.get("/")
async def root():
    repository.Repository()
    return {"message": "Repository initilized"}

@fastapi.get("/inventory/{name}")
async def get_inventory_item(name: ItemName):
    return repository.Repository.load_inventory(name)

@fastapi.post("/inventory/{name}/add")
async def add_inventory_item(name: ItemName, quantity: int = 1):
    inventory = repository.Repository.load_inventory(name)
    inventory.quantity += quantity
    repository.Repository.dump_inventory(inventory)
    
@fastapi.post("/inventory/{name}/price")
async def get_inventory_item(name: ItemName, price : float):
    inventory = repository.Repository.load_inventory(name)
    inventory.unit_price = price
    repository.Repository.dump_inventory(inventory)
    
@fastapi.post("/customer/")
async def add_customer(customer: CustomerDTO, id: Union[UUID, None] = None):
    inventory = repository.Repository.dump_customer(customer._to_customer())

