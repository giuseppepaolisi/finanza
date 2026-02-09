import json
import os
from abc import ABC, abstractmethod

class PortfolioInterface(ABC):
    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def get_stocks(self):
        pass
    
    @abstractmethod
    def get_stock(self, symbol):
        pass
    
    @abstractmethod
    def get_stock_price(self, symbol):
        pass
    

class JSONStorage(PortfolioInterface):
    def __init__(self, filename="portfolio.json"):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        
    def get_stocks(self):
        data = self.load()
        return data.get("stocks", [])
    
    def get_stock(self, symbol):
        stocks = self.get_stocks()
        for stock in stocks:
            if stock.get("symbol") == symbol:
                return stock
        return None
    
    def get_stock_price(self, symbol):
        stock = self.get_stock(symbol)
        if stock:
            return stock.get("price")
        return None