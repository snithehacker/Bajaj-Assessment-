from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Order(BaseModel):
    orderId: str
    symbol: str
    side: str
    orderType: str
    quantity: int
    price: Optional[float] = None
    status: str
    timestamp: datetime