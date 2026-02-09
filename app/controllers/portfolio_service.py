class PortfolioService:
    def __init__(self, storage, price_service, currency_service):
        self.storage = storage
        self.price_service = price_service
        self.currency_service = currency_service
        self.stocks = self.storage.load()

    def add_stock(self, stock):
        """
        Aggiunge o aggiorna un'azione nel dizionario annidato.
        """
        # Controlla se l'azione esiste già, se sì aggiorna la quantità, altrimenti aggiungi una nuova azione
        if stock.ticker in self.stocks:
            self.stocks[stock.ticker]['quantity'] = stock.quantity
        else:
            price, currency = self.price_service.get_stock_price(stock.ticker)

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
            stock_dict = dict(sorted(stock_dict.items(), key=lambda x: self.price_service.get_stock_price(x[0])[0], reverse=True))
        elif sort == 'total':
            stock_dict = dict(sorted(stock_dict.items(), key=lambda x: self.price_service.get_stock_price(x[0])[0] * x[1]['quantity'], reverse=True))
        
        return stock_dict

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
            price, currency = self.price_service.get_stock_price(stock.ticker)
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
            price, currency = self.price_service.get_stock_price(ticker)
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
            price, currency = self.price_service.get_stock_price(ticker)
            rate = self.currency_service.get_exchange(currency, to_cur)
            total_value += price * data['quantity'] * rate
            
        return total_value
