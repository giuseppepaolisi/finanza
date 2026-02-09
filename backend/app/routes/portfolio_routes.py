from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from controllers.portfolio_controller import PortfolioController
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

@router.post("/add")
def add_investment(data: InvestmentSchema, db: Session = Depends(get_db)):
    asset_data = {"symbol": data.symbol}
    trans_data = data.transaction.model_dump()
    
    return PortfolioController.add_transaction(db, asset_data, trans_data)

@router.get("/status")
def view_portfolio(db: Session = Depends(get_db)):
    return PortfolioController.get_portfolio_status(db)