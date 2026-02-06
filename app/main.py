from controllers.stocks_manager import Stocks
from models import Stock

stoks = Stocks()

stoks.add_stok(Stock(ticker="MSFT", quantity=5, price=0.0, currency=""))
stoks.add_stok(Stock(ticker="GOOG", quantity=1, price=0.0, currency=""))
stoks.add_stok(Stock(ticker="AAPL", quantity=7, price=0.0, currency=""))

print(stoks.get_all_stocks('price'))