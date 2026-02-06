from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
# Assumiamo che la tua classe sia in controller.py
from controllers.stocks_manager import st
from models import Stock, StockInput

router = APIRouter(prefix="/stocks", tags=["Stocks"])
portfolio = st # Istanza del controller

@router.post("/add")
async def add_stock(stock: StockInput):
    try:
        portfolio.add_stock(stock)
        return {"message": f"{stock.ticker} aggiunto con successo", "data": portfolio.stocks[stock.ticker]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/all/{sort}")
async def get_all(sort: str = "price"):
    return portfolio.get_all_stocks(sort=sort)

@router.get("/convert/{currency}")
async def convert_portfolio(currency: str):
    try:
        return portfolio.convert_all_stocks(currency)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Errore nella conversione")