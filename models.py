from dataclasses import dataclass, field
from typing import List
import uuid
from datetime import datetime

@dataclass
class Order:
    amount: float
    description: str
    date: str = field(default_factory=lambda: datetime.now().strftime("%b %d, %Y"))
    is_paid: bool = False

    def to_dict(self):
        return {
            "amount": self.amount,
            "description": self.description,
            "date": self.date,
            "is_paid": self.is_paid
        }

    @staticmethod
    def from_dict(data):
        return Order(
            amount=float(data.get("amount", 0)),
            description=data.get("description", ""),
            date=data.get("date", ""),
            is_paid=data.get("is_paid", False)
        )

@dataclass
class Customer:
    name: str
    phone: str
    address: str = ""  # Added address field
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    orders: List[Order] = field(default_factory=list)

    def unpaid_total(self) -> float:
        return sum(order.amount for order in self.orders if not order.is_paid)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "address": self.address, # Save address
            "orders": [o.to_dict() for o in self.orders]
        }

    @staticmethod
    def from_dict(data):
        cust = Customer(
            name=data["name"],
            phone=data["phone"],
            address=data.get("address", ""), # Load address
            id=data.get("id", str(uuid.uuid4()))
        )
        cust.orders = [Order.from_dict(o) for o in data.get("orders", [])]
        return cust