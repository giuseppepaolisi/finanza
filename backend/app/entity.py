from pydantic import BaseModel, Field

class StockInput(BaseModel):
    symbol: str # Simbolo del titolo, es. "MSFT"
    quantity: int # Quantità di azioni possedute
    name: str # Nome completo del titolo, es. "Microsoft Corporation"
    marcket: str # Mercato di riferimento, es. "NASDAQ"
    currency: str # Valuta del titolo, es. "USD"
    purchase_date: str = Field(..., example="2023-01-01") # Data di acquisto in formato YYYY-MM-DD

class Stock(StockInput):
    price: float # Prezzo attuale del titolo
    update_date: str = Field(..., example="2024-01-01") # Data dell'ultimo aggiornamento del prezzo in formato YYYY-MM-DD
    purchase_price: float # Prezzo di acquisto del titolo
    current_value: float # Valore attuale della posizione