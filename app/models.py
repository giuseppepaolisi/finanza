from pydantic import BaseModel, Field

class Stock(BaseModel):
    ticker: str
    quantity: int
    price: float = Field(..., description="prezzo unitario")
    currency: str = Field(..., description="valuta")