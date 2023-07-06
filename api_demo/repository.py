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

class Repository:
    from pickle import dump, load
    
    root_path = '.'
    
    def __init__(self):
        from os import mkdir
        try:
            mkdir(rf"{self.root_path}/customer")
            mkdir(rf"{self.root_path}/inventory")
            for name in ItemName.__members__.values():
                inventory = InventoryItem(
                    name = ItemName(name),
                    unit_price = Dollar('NaN'),
                    _quantity = 0)
                Repository.dump_inventory(inventory)
        except: pass
    
    @classmethod
    def load_inventory(cls, name):
        with open(rf"{cls.root_path}/inventory/{name}.pickle", 'rb') as f:
            inventory = cls.load(f)
            return inventory

    @classmethod
    def dump_inventory(cls, inventory: InventoryItem):
        with open(rf"{cls.root_path}/inventory/{inventory.name}.pickle", 'wb') as f:
            cls.dump(inventory, f)
            
    @classmethod
    def load_customer(cls, customer_id: UUID):
        with open(rf"{cls.root_path}/customer/{customer_id}.pickle", 'rb') as f:
            customer = cls.load(f)
            return customer
    
    @classmethod
    def dump_customer(cls, customer: Customer):
        with open(rf"{cls.root_path}/customer/{customer.id}.pickle", 'wb') as f:
            cls.dump(customer, f)