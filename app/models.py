from pydantic import BaseModel, Field

class StockInput(BaseModel):
    ticker: str
    quantity: int

class Stock(StockInput):
    price: float
    currency: str