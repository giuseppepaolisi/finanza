from sqlalchemy.orm import Session
from models.models import Asset, Transaction
from services.stock_service import get_stock_service
from datetime import date
from fastapi import HTTPException

class PortfolioController:
    @staticmethod
    def add_transaction(db: Session, asset_in: dict, trans_in: dict):
        # Controlla se l'asset esiste già
        db_asset = db.query(Asset).filter(Asset.symbol == asset_in['symbol'].upper()).first()
        
        # Recupera dati live per il nuovo asset
        service = get_stock_service()
        market_data = service.get_ticker_data(asset_in['symbol'])
        # Check se esiste l'asset
        if market_data is None or market_data.get('current_value') is None:
            raise HTTPException(
                status_code=400,
                detail=f"Impossibile recuperare dati per il simbolo '{asset_in['symbol']}'."
            )
        
        if not db_asset:
            
            if market_data is None or market_data.get('current_value') is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Impossibile recuperare dati per il simbolo '{asset_in['symbol']}'. Verifica che sia corretto (es. AAPL, MSFT, GOOGL)."
                )
            
            db_asset = Asset(
                symbol=asset_in['symbol'].upper(),
                name=market_data['name'],
                market=asset_in.get('market', market_data['exchange']), # Usa il market fornito o quello recuperato
                currency=market_data['currency'],
                current_value=market_data['current_value'],
                update_date=market_data['update_date']
            )
            db.add(db_asset)
            db.flush()

        # Crea sempre la transazione
        new_trans = Transaction(
            asset_id=db_asset.id,
            quantity=trans_in['quantity'],
            purchase_price=market_data['current_value'], # Usa il prezzo attuale come prezzo di acquisto
            purchase_date=market_data['update_date'] # Usa la data dell'ultimo aggiornamento come data di acquisto
        )
        db.add(new_trans)
        db.commit()
        db.refresh(db_asset)
        return db_asset

    @staticmethod
    def get_portfolio_status(db: Session, sort_by: str = "price", sort_order: str = "asc"):
        # Recupera tutti gli asset con le relative transazioni caricate
        assets = db.query(Asset).all()
        portfolio_summary = []

        for asset in assets:
            # Aggiorna il prezzo live tramite il Service
            service = get_stock_service()
            stock_service = service.get_ticker_data(asset.symbol)
            asset.current_value = stock_service['current_value']
            asset.update_date = stock_service['update_date']
            
            # Calcola la somma delle quantità di tutte le transazioni per questo asset
            # Grazie alla relazione 'transactions' definita nel modello Asset
            total_quantity = sum(t.quantity for t in asset.transactions)
            
            # Calcola il valore totale attuale dell'investimento
            market_value = float(total_quantity) * asset.current_value

            # Costruiamo un dizionario di risposta arricchito
            portfolio_summary.append({
                "symbol": asset.symbol,
                "name": asset.name,
                "current_price": asset.current_value,
                "total_quantity": total_quantity,
                "market_value": round(market_value, 2),
                "currency": asset.currency,
                "last_update": asset.update_date,
                "purchase_date": min(t.purchase_date for t in asset.transactions) if asset.transactions else None # la prima data di acquisto tra le transazioni per questo asset
            })
        
        db.commit() # salva gli aggiornamenti dei prezzi
        
        if not sort_by in ["price", "market_value", "total_quantity"]:
            sort_by = "price"
        
        if sort_by == "price":
            portfolio_summary.sort(key=lambda x: x['current_price'], reverse=(sort_order == "desc"))
        elif sort_by == "market_value":
            portfolio_summary.sort(key=lambda x: x['market_value'], reverse=(sort_order == "desc"))
            
        return {"assets": portfolio_summary}
    
    # Ritorna il prezzo medio di carico di ogni asset
    @staticmethod
    def get_average_price(db: Session):
        assets = db.query(Asset).all()
        average_prices = {}

        for asset in assets:
            total_quantity = sum(t.quantity for t in asset.transactions)
            total_cost = sum(t.quantity * t.purchase_price for t in asset.transactions)
            average_price = total_cost / total_quantity if total_quantity > 0 else 0
            average_prices[asset.symbol] = round(average_price, 2)

        return average_prices
    
    @staticmethod
    def get_transactions_by_symbol(db: Session, symbol: str):
        asset = db.query(Asset).filter(Asset.symbol == symbol.upper()).first()
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        transactions = db.query(Transaction).filter(Transaction.asset_id == asset.id).all()
        return transactions