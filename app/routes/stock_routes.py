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
    
@router.delete("/remove/{ticker}")
async def remove_stock(ticker: str):
    try:
        st.remove_stock(ticker)
        return {"message": f"{ticker} rimosso con successo"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/clear")
async def clear_portfolio():
    st.clear_portfolio()
    return {"message": "Portafoglio svuotato con successo"}

@router.put("/update")
async def update_stock(stock: StockInput):
    try:
        st.update_stock(stock)
        return {"message": f"{stock.ticker} aggiornato con successo", "data": st.stocks[stock.ticker]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{ticker}")
async def get_stock(ticker: str):
    try:
        return st.get_stock(ticker)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# Ritorna i prezzi storici di un'azione
@router.get("/history/{ticker}")
async def get_history(ticker: str, period: str = "1mo"):
    try:
        # Ritorna un JSON con la lista dei prezzi storici per l'azione specificata
        return st.get_old_prices(ticker, period)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))