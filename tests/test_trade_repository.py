import unittest
from unittest.mock import MagicMock

from src.entity.stock_common import StockCommon
from src.entity.trade import Trade
from src.model.stock_symbol import StockSymbol
from src.model.trade_indicator import TradeIndicator
from src.repository.trade_repository import TradeRepository


class MyTestCase(unittest.TestCase):
    sut: TradeRepository

    @classmethod
    def setUpClass(cls):
        cls.stock_pop = StockCommon(symbol=StockSymbol.POP, par_value=100.0, last_dividend=8.0)

    def setUp(self) -> None:
        self.service_repository = MagicMock()
        self.sut = TradeRepository(self.service_repository)

    def test_record_trade(self):
        trade: Trade = Trade(quantity=100, indicator=TradeIndicator.BUY, price=10.0)

        self.sut.record_trade(trade, self.stock_pop)

        self.assertEqual(1, len(self.sut.fake_database), 'Trade was not recorded.')
        self.assertEqual(trade, self.sut.fake_database[0], 'Trade was not recorded.')
        self.service_repository.update.assert_called_once_with(self.stock_pop)


if __name__ == '__main__':
    unittest.main()
