from src.entity.stock import Stock
from src.model.stock_symbol import StockSymbol


class StockPreferred(Stock):
    """
        Represents a stock with type preferred.
    """

    def __init__(self,
                 symbol: StockSymbol,
                 last_dividend: float,
                 par_value: float,
                 fixed_dividend: float
                 ):
        super().__init__(
            symbol=symbol,
            last_dividend=last_dividend,
            par_value=par_value
        )
        self.fixed_dividend: float = fixed_dividend

    def calculate_dividend_yield(self, price: float) -> float:
        return round(self.fixed_dividend * self.par_value / price, 5)
