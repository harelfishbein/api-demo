from pydantic import BaseModel
from uuid import UUID, uuid4
from decimal import Decimal
from repository import *

class CustomerDTO(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    balance: Decimal
    
    def _to_customer(self):
        return Customer(
            id = self.id,
            first_name = self.first_name,
            last_name = self.last_name,
            _balance = Dollar(self.balance)
        )
        