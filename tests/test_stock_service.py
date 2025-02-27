import unittest
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import MagicMock, patch

from src.entity.stock import Stock
from src.entity.stock_common import StockCommon
from src.entity.stock_preferred import StockPreferred
from src.entity.trade import Trade
from src.exception.calculation_exception import CalculationException
from src.model.stock_symbol import StockSymbol
from src.model.trade_indicator import TradeIndicator
from src.service.stock_service import StockService


class TestStockService(unittest.TestCase):
    sut: StockService

    @classmethod
    @mock.patch('src.entity.trade.datetime')
    def setUpClass(cls, time_now_mock):
        # trades at 20:00
        time_now_mock.datetime.now.return_value = datetime(2023, 7, 1, 20, 0, 0)
        cls.trade_pop_20 = Trade(quantity=20, indicator=TradeIndicator.SELL, price=20.0)
        cls.trade_ale_20_1 = Trade(quantity=10, indicator=TradeIndicator.BUY, price=15.0)
        cls.trade_ale_20_2 = Trade(quantity=10, indicator=TradeIndicator.BUY, price=9.0)
        cls.trade_gin_20 = Trade(quantity=19, indicator=TradeIndicator.BUY, price=26.0)
        cls.trade_joe_20 = Trade(quantity=5, indicator=TradeIndicator.BUY, price=300.0)
        # trades at 21:00
        time_now_mock.datetime.now = mock.Mock(return_value=datetime(2023, 7, 1, 21, 0, 0))
        cls.trade_pop_21_1 = Trade(quantity=2, indicator=TradeIndicator.SELL, price=20.0)
        cls.trade_pop_21_2 = Trade(quantity=1, indicator=TradeIndicator.BUY, price=17.0)
        # stocks
        cls.stock_tea = StockCommon(symbol=StockSymbol.TEA, par_value=100.0, last_dividend=0.0)
        cls.stock_pop = StockCommon(symbol=StockSymbol.POP, par_value=100.0, last_dividend=8.0)
        cls.stock_gin = StockPreferred(symbol=StockSymbol.GIN, par_value=100.0, last_dividend=8.0, fixed_dividend=0.02)
        cls.stock_ale = StockCommon(symbol=StockSymbol.ALE, par_value=60.0, last_dividend=23.0)
        cls.stock_joe = StockCommon(symbol=StockSymbol.JOE, par_value=250.0, last_dividend=13.0)

    @classmethod
    def tearDownClass(cls) -> None:
        patch.stopall()

    def setUp(self) -> None:
        stock_repository = MagicMock()
        self.sut = StockService(stock_repository)

    def test_calculate_dividend_yield_common_last_dividend_0(self):
        price: float = 40.0
        result: float = self.sut.calculate_dividend_yield(self.stock_tea, price)
        self.assertEqual(0, result, 'Dividend yield wrong.')

    def test_calculate_dividend_yield_common(self):
        price: float = 31.62
        result: float = self.sut.calculate_dividend_yield(self.stock_pop, price)
        self.assertEqual(0.25300, result, 'Dividend yield wrong.')

    def test_calculate_dividend_yield_common_division_by_zero(self):
        price: float = 0.0
        with self.assertRaises(ZeroDivisionError):
            self.sut.calculate_dividend_yield(self.stock_pop, price)

    def test_calculate_dividend_yield_preferred_division_by_zero(self):
        price: float = 0.0
        with self.assertRaises(ZeroDivisionError):
            self.sut.calculate_dividend_yield(self.stock_gin, price)

    def test_calculate_dividend_yield_preferred(self):
        price: float = 16.0
        result: float = self.sut.calculate_dividend_yield(self.stock_gin, price)
        self.assertEqual(0.125, result, 'Dividend yield wrong.')

    def test_calculate_pe_ratio(self):
        price: float = 19.0
        result: float = self.sut.calculate_pe_ratio(self.stock_gin, price)
        self.assertEqual(2.375, result, 'PE ratio wrong.')

    def test_calculate_pe_ratio_division_by_zero(self):
        price: float = 19.0
        with self.assertRaises(CalculationException):
            self.sut.calculate_pe_ratio(self.stock_tea, price)

    @mock.patch('src.service.stock_service.datetime')
    def test_get_volume_weighted_stock_price(self, time_now_stock_service):
        timedelta_min = 5
        stock_pop: Stock = StockCommon(symbol=StockSymbol.POP, par_value=100.0, last_dividend=8.0)
        stock_pop.trades = [
            self.trade_pop_20,
            self.trade_pop_21_1,
            self.trade_pop_21_2
        ]

        time_now_stock_service.datetime.now.return_value = datetime(2023, 7, 1, 21, 2, 0)
        time_now_stock_service.timedelta.return_value = timedelta(minutes=timedelta_min)
        result: float = self.sut.calculate_volume_weighted_stock_price(timedelta_min, stock_pop)
        self.assertEqual(19, result, 'Volume weighted stock price is wrong.')

    def test_get_gbce_all_share_index(self):
        self.stock_pop.trades = [self.trade_pop_20, self.trade_pop_21_1, self.trade_pop_21_2]
        self.stock_ale.trades = [self.trade_ale_20_1, self.trade_ale_20_2]
        self.stock_gin.trades = [self.trade_gin_20]
        self.stock_joe.trades = [self.trade_joe_20]

        self.sut.stock_repository.get_all_stocks.return_value = [
            self.stock_tea, self.stock_pop, self.stock_ale, self.stock_gin, self.stock_joe
        ]

        result: float = self.sut.calculate_gbce_all_share_index()
        self.assertEqual(36.92887, result, 'GBCE all share index is wrong.')


if __name__ == '__main__':
    unittest.main()
