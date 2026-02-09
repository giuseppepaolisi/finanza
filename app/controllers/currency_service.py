import yfinance as yf


class CurrencyService:
    def __init__(self, price_service):
        self.price_service = price_service

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

    def convert_all_stocks(self, stocks, to_cur):
        """
        Restituisce un nuovo dizionario annidato con tutti i prezzi convertiti.
        """
        converted_portfolio = {}
        
        for ticker, data in stocks.items():
            rate = self.get_exchange(data['currency'], to_cur)
            
            converted_portfolio[ticker] = {
                'quantity': data['quantity'],
                'price': self.price_service.get_stock_price(ticker)[0] * rate,
                'currency': to_cur
            }
            
        return converted_portfolio
