from src.entity.stock import Stock
from src.entity.trade import Trade
from src.repository.trade_repository import TradeRepository
from src.service.stock_service import StockService


class TradeService:
    def __init__(self, trade_repository: TradeRepository, stock_service: StockService):
        self.trade_repository: TradeRepository = trade_repository
        self.stock_service: StockService = stock_service

    def record_trade(self, trade: Trade, stock: Stock) -> None:
        """
        Save a trade.
         :param trade: the trade to save
         :param stock: the stock to save the trade for
        """
        self.trade_repository.record_trade(trade, stock)
