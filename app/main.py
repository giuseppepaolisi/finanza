from controllers.stocks_manager import st
from models import Stock, StockInput

st.add_stock(StockInput(ticker="MSFT", quantity=5))
st.add_stock(StockInput(ticker="GOOG", quantity=1))
st.add_stock(StockInput(ticker="AAPL", quantity=7))

print(st.get_all_stocks('price'))
print(st.get_exchange("USD", "EUR"))
print(st.convert_all_stocks("EUR"))