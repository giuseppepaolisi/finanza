from fastapi import APIRouter, HTTPException
from controllers.stocks_manager import st
from models import Stock, StockInput

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.post("/add")
async def add_stock(stock: StockInput):
    try:
        st.add_stock(stock)
        return {"message": f"{stock.ticker} aggiunto con successo", "data": st.stocks[stock.ticker]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/all/{sort}")
async def get_all(sort: str = "price"):
    return st.get_all_stocks(sort=sort)

@router.get("/convert/{currency}")
async def convert_st(currency: str):
    try:
        return st.convert_all_stocks(currency)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Errore nella conversione")