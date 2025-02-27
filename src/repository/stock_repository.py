from src.entity.stock import Stock
from src.entity.stock_common import StockCommon
from src.entity.stock_preferred import StockPreferred
from src.model.stock_symbol import StockSymbol


class StockRepository:
    fake_database: list[Stock]

    def __init__(self):
        self.fake_database = [
            StockCommon(symbol=StockSymbol.TEA, par_value=100.0, last_dividend=0.0),
            StockCommon(symbol=StockSymbol.POP, par_value=100.0, last_dividend=8.0),
            StockCommon(symbol=StockSymbol.ALE, par_value=60.0, last_dividend=23.0),
            StockPreferred(symbol=StockSymbol.GIN, par_value=100.0, last_dividend=8.0, fixed_dividend=0.02),
            StockCommon(symbol=StockSymbol.JOE, par_value=250.0, last_dividend=13.0)
        ]

    def get_all_stocks(self) -> list[Stock]:
        return self.fake_database

    def update(self, stock: Stock) -> None:
        for idx, item in enumerate(self.fake_database):
            if stock.symbol == item.symbol:
                self.fake_database[idx] = stock
