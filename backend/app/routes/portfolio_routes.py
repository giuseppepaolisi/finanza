from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from services.portfolio_service import PortfolioService
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

# Schemi Pydantic per input

class InvestmentSchema(BaseModel):
    symbol: str
    quantity: float
# Dependency per ottenere il database serve per ogni endpoint che ne ha bisogno

# Permette di acquiistre un nuovo asset
@router.post("/assets")
def add_investment(data: InvestmentSchema, db: Session = Depends(get_db)):
    asset_data = {"symbol": data.symbol}
    trans_data = {"quantity": data.quantity}
    print(f"asset {asset_data}, transaction {trans_data}")
    
    return PortfolioService.add_transaction(db, asset_data, trans_data)

# Ritorna lo stato attuale del portafoglio, con possibilità di ordinare per prezzo, valore di mercato o quantità totale
@router.get("/assets/{sort_by}/{sort_order}")
def view_portfolio(sort_by: str, sort_order: str, db: Session = Depends(get_db)):
    return PortfolioService.get_portfolio_status(db, sort_by=sort_by, sort_order=sort_order)

# Ritorna tutte le transazioni per un dato asset
@router.get("/assets/{symbol}")
def get_transactions_by_symbol(symbol: str, db: Session = Depends(get_db)):
    return PortfolioService.get_transactions_by_symbol(db, symbol)

# Ritorna il valore totale del portafoglio in una data valuta
@router.get("/value/{currency}")
def get_total_portfolio_value(currency: str, db: Session = Depends(get_db)):
    return PortfolioService.get_total_portfolio_value(db, currency=currency)
