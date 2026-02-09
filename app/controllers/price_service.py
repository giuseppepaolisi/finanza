import yfinance as yf


class PriceService:
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
