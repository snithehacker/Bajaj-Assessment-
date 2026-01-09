from pydantic import BaseModel

class Instrument(BaseModel):
    symbol: str
    exchange: str
    instrumentType: str
    lastTradedPrice: float