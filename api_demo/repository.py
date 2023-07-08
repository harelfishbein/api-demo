from enum import Enum
from uuid import UUID
from dataclasses import dataclass
from currency import *



class ItemName(str, Enum):
    apple = "apple"
    orange = "orange"
    banana = "banana"


@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: ItemName
    unit_price: Dollar
    _quantity: int = 0
            
    @property
    def quantity(self): return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if value < 0: raise ValueError("quantity must not be negative")
        self._quantity = value
        
@dataclass
class Customer:
    """Class for keeping track of customer"""
    id: UUID
    first_name: str
    last_name: str
    _balance: Dollar


from aiofile import async_open as aopen
import pickle

class Repository:
    
    
    root_path = '.'
    
    async def make(self):
        from os import mkdir
            
        mkdir(rf"{self.root_path}/customer")

        
        mkdir(rf"{self.root_path}/inventory")
        
    
        for name in ItemName.__members__.values():
            inventory = InventoryItem(
                name = ItemName(name),
                unit_price = Dollar(0),
                _quantity = 0)
            await self.dump_inventory(inventory)
    
    async def load_inventory(self, name):
        async with aopen(rf"{self.root_path}/inventory/{name}.pickle", 'rb') as f:
            b = await f.read()
        return pickle.loads(b)
        
    async def dump_inventory(self, inventory: InventoryItem):
        async with aopen(rf"{self.root_path}/inventory/{inventory.name}.pickle", 'wb') as f:
            await f.write(pickle.dumps(inventory))
            
    async def load_customer(self, customer_id: UUID):
        async with aopen(rf"{self.root_path}/customer/{customer_id}.pickle", 'rb') as f:
            b = await f.read()
        return pickle.loads(b)

    async def dump_customer(self, customer: Customer):
        async with aopen(rf"{self.root_path}/customer/{customer.id}.pickle", 'wb') as f:
            await f.write(pickle.dumps(customer))