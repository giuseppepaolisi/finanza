from controllers.portfolio_factory import portfolio
from models import StockInput

portfolio.add_stock(StockInput(ticker="MSFT", quantity=5))
portfolio.add_stock(StockInput(ticker="GOOG", quantity=1))
portfolio.add_stock(StockInput(ticker="AAPL", quantity=7))

print(portfolio.currency_service.get_exchange("USD", "EUR"))
print(portfolio.currency_service.convert_all_stocks(portfolio.stocks, "EUR"))

print(portfolio.price_service.get_old_prices("MSFT", period="5mo"))