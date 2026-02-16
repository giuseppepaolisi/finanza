from abc import ABC, abstractmethod
import yfinance as yf
from datetime import date

class StockClient(ABC):
    @staticmethod
    @abstractmethod
    def get_ticker_data(symbol: str):
        pass

class StockYFinanceClient(StockClient):
    @staticmethod
    def get_ticker_data(symbol: str):
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            
            # Verifica che i dati siano validi
            last_price = info.get('lastPrice')
            if last_price is None or last_price == 0:
                return None
            
            return {
                "current_value": last_price, # Utilizzo di 'lastPrice' per ottenere il prezzo più recente
                "currency": info.get('currency', 'USD'), # Aggiunta della valuta per una migliore gestione dei dati finanziari
                "exchange": info.get('exchange', 'N/A'), # Aggiunta dell'exchange per una migliore identificazione del mercato
                "name": info.get('longName', symbol), # Aggiunta del nome completo del titolo, con fallback al simbolo se non disponibile
                "update_date": date.today()
            }
        except Exception as e:
            print(f"Errore nel recupero dati per {symbol}: {e}")
            return None

# Factory per selezionare il service
def get_stock_client() -> StockClient:
    """Factory per ottenere il servizio stock attivo"""
    return StockYFinanceClient