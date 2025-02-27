import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock, patch

from src.entity.stock_common import StockCommon
from src.entity.trade import Trade
from src.model.stock_symbol import StockSymbol
from src.model.trade_indicator import TradeIndicator
from src.service.trade_service import TradeService


class MyTestCase(unittest.TestCase):
    sut: TradeService
    trade_repository_mock: MagicMock

    @classmethod
    @mock.patch('src.entity.trade.datetime')
    def setUpClass(cls, time_trades_executed):
        # trades at 20:00
        time_trades_executed.datetime.now = mock.Mock(return_value=datetime(2023, 7, 1, 20, 0, 0))
        cls.trade_pop_20 = Trade(quantity=100, indicator=TradeIndicator.SELL, price=10.0)
        # stocks
        cls.stock_pop = StockCommon(symbol=StockSymbol.POP, par_value=100.0, last_dividend=8.0)

    @classmethod
    def tearDownClass(cls) -> None:
        patch.stopall()

    def setUp(self) -> None:
        self.trade_repository_mock = MagicMock()
        self.sut = TradeService(self.trade_repository_mock, MagicMock())

    def test_record_trade(self):
        self.sut.record_trade(self.trade_pop_20, self.stock_pop)
        self.trade_repository_mock.record_trade.assert_called_once_with(self.trade_pop_20, self.stock_pop)


if __name__ == '__main__':
    unittest.main()
