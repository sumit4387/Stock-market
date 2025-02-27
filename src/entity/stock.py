from abc import ABC, abstractmethod

from src.entity.trade import Trade
from src.exception.calculation_exception import CalculationException
from src.model.stock_symbol import StockSymbol


class Stock(ABC):
    """
        Representing a stock.
    """

    def __init__(self,
                 symbol: StockSymbol,  # is an id for the stock
                 last_dividend: float,
                 par_value: float
                 ):
        self.symbol: StockSymbol = symbol
        self.last_dividend: float = last_dividend
        self.par_value = par_value
        self.trades: list[Trade] = []

    @abstractmethod
    def calculate_dividend_yield(self, price: float) -> float:
        """
        :param price: the price used for the calculation
        :return: the dividend yield regarding the used stock and price
        """
        pass

    def calculate_pe_ratio(self, price: float) -> float:
        """
        :param price: the price used for the calculation
        :return: the P/E ratio regarding the used stock and price
        """
        try:
            return round(price / self.last_dividend, 5)
        except ZeroDivisionError:
            raise CalculationException(f'Could not calculate the P/E ratio for stock [{self.symbol}] because '
                                       f'last dividend is 0.')
