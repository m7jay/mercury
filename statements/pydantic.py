from datetime import date
from typing import Optional
from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_id: str
    transaction_date: date
    amount_deposited: Optional[float]
    amount_withdrawn: Optional[float]
    balance: float
    others: Optional[str]
