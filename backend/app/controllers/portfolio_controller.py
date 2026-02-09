from entity import Stock, StockInput
from app.models.persistence import PortfolioInterface

class PortfolioController:
    """
    Gestisce un singolo portfolio
    """
    
    def __init__(self, storage: PortfolioInterface):
        self.storage = storage

    def get_stocks(self, sort_by="current_value", sort_order="asc"):
        """
        ritorna un json con tutte le stokcs ordinate per:
        - current_value
        - current_total_value
        di base ascendente, ma se viene passato un parametro "sort" con valore "desc" allora viene ordinato in modo discendente
        """
        stocks = self.storage.get_stocks()
        
        # se sort_by non è valido, default a current_value
        if sort_by not in ["current_value", "current_total_value"]:
            sort_by = "current_value"
        
        # accetto solo "asc" o "desc", altrimenti default a "asc"
        reverse = False
        if sort_order.lower() not in ["asc", "desc"]:
            sort_order = "asc"
            reverse = True
            
        # Ordina il dizionario in base al criterio
        if sort_order == 'price':
            stock_dict = dict(sorted(stocks.items(), key=lambda x: stocks.get, reverse=reverse))
        elif sort_order == 'total':
            stock_dict = dict(sorted(stocks.items(), key=lambda x: self.price_service.get_stock_price(x[0])[0] * x[1]['quantity'], reverse=reverse))

    def get_stock(self, symbol):
        return self.storage.get_stock(symbol)