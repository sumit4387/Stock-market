from src.entity.stock import Stock


class StockCommon(Stock):
    """
        Represents a stock with type common.
    """

    def calculate_dividend_yield(self, price: float) -> float:
        return round(self.last_dividend / price, 5)
