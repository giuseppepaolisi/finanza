from .price_service import PriceService
from .currency_service import CurrencyService
from .portfolio_service import PortfolioService
from persistence import JSONStorage


def create_portfolio_service():
    """
    Factory per l'inizializzazione del servizio di portfolio.
    Crea e connette tutti i servizi necessari.
    """
    storage = JSONStorage()
    price_service = PriceService()
    currency_service = CurrencyService(price_service)
    portfolio_service = PortfolioService(storage, price_service, currency_service)
    return portfolio_service


# Istanza singleton del portfolio service
portfolio = create_portfolio_service()
