import yfinance as yf

class Stocks:
    def __init__(self, storage_strategy):
        # Struttura: { 'AAPL': {'quantity': 10, 'currency': 'USD'} ... }
        self.storage = storage_strategy
        self.stocks = self.storage.load()

    def get_stock_price(self, ticker):
        """Recupera prezzo attuale e valuta da yfinance."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            # Alcuni ticker potrebbero non avere 'currentPrice' ma 'regularMarketPrice'
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
        # Controlla se l'azione esiste già, se sì aggiorna la quantità, altrimenti aggiungi una nuova azione
        if stock.ticker in self.stocks:
            self.stocks[stock.ticker]['quantity'] = stock.quantity
        else:
            price, currency = self.get_stock_price(stock.ticker)

            self.stocks[stock.ticker] = {
                'quantity': stock.quantity,
                #'price': price,
                'currency': currency
            }
        self.storage.save(self.stocks)

    def get_all_stocks(self, sort='price'):
        """Ritorna un dizionario dei dati, ordinato per il parametro specificato."""
        stock_dict = {}
        
        for ticker, data in self.stocks.items():
            stock_dict[ticker] = data.copy()
        
        if sort not in ['price', 'total']:
            sort = 'price'
        
        # Ordina il dizionario in base al criterio
        if sort == 'price':
            stock_dict = dict(sorted(stock_dict.items(), key=lambda x: self.get_stock_price(x[0])[0], reverse=True))
        elif sort == 'total':
            stock_dict = dict(sorted(stock_dict.items(), key=lambda x: self.get_stock_price(x[0])[0] * x[1]['quantity'], reverse=True))
        
        return stock_dict

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
                'price': self.get_stock_price(ticker)[0] * rate,
                'currency': to_cur
            }
            
        return converted_portfolio
    
    def remove_stock(self, ticker):
        """Rimuove un'azione dal portafoglio."""
        if ticker in self.stocks:
            del self.stocks[ticker]
            self.storage.save(self.stocks)
        else:
            raise ValueError(f"{ticker} non presente nel portafoglio")
        
    def clear_portfolio(self):
        """Svuota completamente il portafoglio."""
        self.stocks = {}
        self.storage.save(self.stocks)
        
    def update_stock(self, stock):
        """Aggiorna la quantità di un'azione esistente."""
        if stock.ticker in self.stocks:
            price, currency = self.get_stock_price(stock.ticker)
            self.stocks[stock.ticker] = {
                'quantity': stock.quantity,
                'currency': currency
            }
            self.storage.save(self.stocks)
        else:
            raise ValueError(f"{stock.ticker} non presente nel portafoglio")
        
    def get_stock(self, ticker):
        """Ritorna i dettagli di un'azione specifica."""
        if ticker in self.stocks:
            data = self.stocks[ticker]
            price, currency = self.get_stock_price(ticker)
            return {
                'quantity': data['quantity'],
                'price': price,
                'currency': currency
            }
        else:
            raise ValueError(f"{ticker} non presente nel portafoglio")
        
    def get_portfolio_value(self, to_cur='USD'):
        """Calcola il valore totale del portafoglio in una valuta specifica."""
        total_value = 0.0
        
        for ticker, data in self.stocks.items():
            price, currency = self.get_stock_price(ticker)
            rate = self.get_exchange(currency, to_cur)
            total_value += price * data['quantity'] * rate
            
        return total_value
    
    def get_old_prices(self, ticker, period="1mo"):
        """Ritorna una lista di oggetti {date, price} per il grafico."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            # Creiamo una lista di dizionari (formato ideale per Recharts/Chart.js)
            chart_data = []
            for date, row in hist.iterrows():
                chart_data.append({
                    # Formattiamo la data in YYYY-MM-DD per il frontend
                    "date": date.strftime('%Y-%m-%d'),
                    "price": round(float(row['Close']), 2)
                })
            return chart_data
        except Exception as e:
            raise ValueError(f"Errore nel recupero dati storici per {ticker}: {e}")

from persistence import JSONStorage
st = Stocks(storage_strategy=JSONStorage())