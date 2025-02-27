import unittest

from src.entity.stock_common import StockCommon
from src.entity.stock_preferred import StockPreferred
from src.entity.trade import Trade
from src.exception.calculation_exception import CalculationException
from src.model.stock_symbol import StockSymbol
from src.model.trade_indicator import TradeIndicator
from src.repository.stock_repository import StockRepository
from src.repository.trade_repository import TradeRepository
from src.service.stock_service import StockService
from src.service.trade_service import TradeService


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stock_tea = StockCommon(symbol=StockSymbol.TEA, par_value=100.0, last_dividend=0.0)
        cls.stock_pop = StockCommon(symbol=StockSymbol.POP, par_value=100.0, last_dividend=8.0)
        cls.stock_gin = StockPreferred(symbol=StockSymbol.GIN, par_value=100.0, last_dividend=8.0, fixed_dividend=0.02)

    def setUp(self) -> None:
        stock_repository: StockRepository = StockRepository()
        self.trade_service = TradeService(TradeRepository(stock_repository), StockService(stock_repository))
        self.stock_service = StockService(stock_repository)

    def test_something(self):
        '''
        Record trades. These are used for calculation of the GPCE all share index.
        Stock ALE and JOE do not have any trades.

        VWSP:
        tea: 220
        gin: 140
        pop: 126.72727
        GCPE:
        157.44913
        '''
        self.trade_service.record_trade(
            Trade(quantity=10, indicator=TradeIndicator.BUY, price=200.0),
            self.stock_tea
        )
        self.trade_service.record_trade(
            Trade(quantity=20, indicator=TradeIndicator.BUY, price=230.0),
            self.stock_tea
        )
        self.trade_service.record_trade(
            Trade(quantity=200, indicator=TradeIndicator.BUY, price=140.0),
            self.stock_gin
        )
        self.trade_service.record_trade(
            Trade(quantity=6, indicator=TradeIndicator.BUY, price=290.0),
            self.stock_pop
        )
        self.trade_service.record_trade(
            Trade(quantity=100, indicator=TradeIndicator.BUY, price=110.0),
            self.stock_pop
        )
        self.trade_service.record_trade(
            Trade(quantity=4, indicator=TradeIndicator.BUY, price=300.0),
            self.stock_pop
        )

        '''
        Calculate dividend yield and P/E ratio.
        '''
        self.assertEqual(0, self.stock_service.calculate_dividend_yield(self.stock_tea, 200))
        self.assertEqual(0.04, self.stock_service.calculate_dividend_yield(self.stock_pop, 200))
        self.assertEqual(0.01538, self.stock_service.calculate_dividend_yield(self.stock_gin, 130))

        # division by zero handled with custom exception
        with self.assertRaises(CalculationException):
            self.assertEqual(0, self.stock_service.calculate_pe_ratio(self.stock_tea, 200))
        self.assertEqual(20, self.stock_service.calculate_pe_ratio(self.stock_gin, 160))

        '''
        Calculate volume weighted stock price based on trades in past 5 minutes for stock gin.
        '''
        stock_gin = StockPreferred(symbol=StockSymbol.GIN, par_value=100.0, last_dividend=8.0, fixed_dividend=0.02)
        stock_gin.trades = [
            Trade(quantity=200, indicator=TradeIndicator.BUY, price=140.0)
        ]
        self.assertEqual(140, self.stock_service.calculate_volume_weighted_stock_price(5, stock_gin))

        '''
        Calculate GBCE all share index.
        '''
        self.assertEqual(157.44913, self.stock_service.calculate_gbce_all_share_index())


if __name__ == '__main__':
    unittest.main()
