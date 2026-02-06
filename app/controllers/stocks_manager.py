import yfinance as yf
class Stocks:
    def __init__(self):
        # Struttura: { 'AAPL': {'quantity': 10, 'price': 150.0, 'currency': 'USD'}, ... }
        self.stocks = {}

    def get_stock_price(self, ticker):
        """Recupera prezzo attuale e valuta da yfinance."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("currentPrice") or info.get("regularMarketPrice")

            if price is None:
                raise ValueError(f"Prezzo assente per {ticker}")
            
            currency = info.get("currency", "USD")
            return float(price), currency
        except Exception as e:
            raise ValueError(f"Errore nel recupero dati per {ticker}: {e}")

    def add_stock(self, stock):
        """
        Aggiunge o aggiorna un'azione nel dizionario annidato.
        """
        price, currency = self.get_stock_price(stock.ticker)

        self.stocks[stock.ticker] = {
            'quantity': stock.quantity,
            'price': price,
            'currency': currency
        }

    def get_all_stocks(self, sort = 'price'):
        """Ritorna la lista dei dati, includendo il ticker nel dizionario."""
        stock_list = []
        for ticker, data in self.stocks.items():
            item = data.copy()
            item['ticker'] = ticker
            stock_list.append(item)

        if sort == 'price':
            stock_list.sort(key=lambda x: x['price'])
        elif sort == 'total':
            stock_list.sort(key=lambda x: x['price'] * x['quantity'])
        
        return stock_list

    def get_exchange(self, from_cur, to_cur):
        """Recupera il tasso di cambio tra due valute."""
        if from_cur == to_cur:
            return 1.0
        
        try:
            # forex_ticker è nel formato "USDEUR=X" per il cambio USD/EUR
            forex_ticker = f"{from_cur}{to_cur}=X"
            ticker = yf.Ticker(forex_ticker)
            rate = ticker.info.get('regularMarketPrice')
            
            if rate is None:
                print(f"Tasso non trovato per {from_cur}/{to_cur}")
                            
            return float(rate)
        except Exception as e:
            print(f"Errore cambio valuta: {e}")
            return 1.0

    def convert_all_stocks(self, to_cur):
        """
        Restituisce un nuovo dizionario annidato con tutti i prezzi convertiti.
        """
        converted_portfolio = {}
        
        for ticker, data in self.stocks.items():
            rate = self.get_exchange(data['currency'], to_cur)
            
            converted_portfolio[ticker] = {
                'quantity': data['quantity'],
                'price': data['price'] * rate,
                'currency': to_cur
            }
            
        return converted_portfolio
    
st = Stocks()