from pydantic import BaseModel

class PortfolioHolding(BaseModel):
    symbol: str
    quantity: int
    averagePrice: float
    currentValue: float