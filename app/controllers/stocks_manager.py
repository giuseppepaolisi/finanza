import yfinance as yf
from typing import List, Dict

class Stocks:
    def __init__(self):
        self.stocks = []

    def get_stock_price(self, ticker):
        """
        Ritorna il prezzo di un azione
        
        :param self: Description
        :param ticker: Description
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("currentPrice")

            if price is None:
                raise ValueError(f"Prezzo assente per {ticker}")
            
            currency = info.get("currency", "USD")

            return float(price), currency
        except Exception as e:
            raise ValueError("Errore nel recupero dei dati")
        
    def add_stok(self, stock):

        price, currency = self.get_stock_price(stock.ticker)

        total_value = stock.quantity * price

        stock_data = {
            'ticker': stock.ticker,
            'quantity': stock.quantity,
            'price': price,
            'currency': currency
        }

        self.stocks.append(stock_data)

    
    def get_all_stocks(self, sort = 'price'):
        stock_list = self.stocks.copy()

        if sort == 'price':
            stock_list.sort(key=lambda x: x['price'])
        elif sort == 'total':
            stock_list.sort(key=lambda x: x['price'] * x['quantity'])
        
        return stock_list

    def get_exchange(self, from_cur, to_cur):
        if from_cur == to_cur:
            return 1.0
        
        try:
            # Formato 
            forex = f"{from_cur}{to_cur}=X"
            ticker = yf.Ticker(forex)

            info = ticker.info
            rate = ticker.get("regualateMarketPrice")

            if rate is None:
                print("Tasso di cambio non disponibile")
            
            return float(rate)
        except Exception as e:
            print(f"Valore non recuperabile {e}")


    