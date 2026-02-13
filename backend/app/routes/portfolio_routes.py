from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from services.portfolio_service import PortfolioService
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

# Schemi Pydantic per input
class TransactionSchema(BaseModel):
    quantity: float
    #purchase_price: float
    #purchase_date: date

class InvestmentSchema(BaseModel):
    symbol: str
    transaction: TransactionSchema
# Dependency per ottenere il database serve per ogni endpoint che ne ha bisogno

# Permette di acquiistre un nuovo asset
@router.post("/add")
def add_investment(data: InvestmentSchema, db: Session = Depends(get_db)):
    asset_data = {"symbol": data.symbol}
    trans_data = data.transaction.model_dump()
    
    return PortfolioService.add_transaction(db, asset_data, trans_data)

# Ritorna lo stato attuale del portafoglio, con possibilità di ordinare per prezzo, valore di mercato o quantità totale
@router.get("/status/{sort_by}/{sort_order}")
def view_portfolio(sort_by: str, sort_order: str, db: Session = Depends(get_db)):
    return PortfolioService.get_portfolio_status(db, sort_by=sort_by, sort_order=sort_order)

# Ritorna il prezzo medio di carico di ogni asset
@router.get("/means_price")
def get_average_prices(db: Session = Depends(get_db)):
    return PortfolioService.get_average_price(db)

# Ritorna tutte le transazioni per un dato asset
@router.get("/transaction/{symbol}")
def get_transactions_by_symbol(symbol: str, db: Session = Depends(get_db)):
    return PortfolioService.get_transactions_by_symbol(db, symbol)

# Ritorna il valore totale del portafoglio in una data valuta
@router.get("/value/{currency}")
def get_total_portfolio_value(currency: str, db: Session = Depends(get_db)):
    return PortfolioService.get_total_portfolio_value(db, currency=currency)

@router.get("/profit_loss/{symbol}")
def get_profit_and_loss(symbol: str, db: Session = Depends(get_db)):
    return PortfolioService.profit_and_loss(db, symbol)