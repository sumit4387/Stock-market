from src.entity.stock import Stock
from src.entity.trade import Trade
from src.repository.stock_repository import StockRepository


class TradeRepository:
    def __init__(self, stock_repository: StockRepository):
        self.fake_database: list[Trade] = []
        self.stock_repository = stock_repository

    def record_trade(self, trade: Trade, stock: Stock) -> None:
        """
        Save a trade.
        :param trade: the trade to save
        :param stock: the stock of the trade
        """
        list.append(self.fake_database, trade)
        # fake db workaround
        stock.trades.append(trade)
        self.stock_repository.update(stock)
