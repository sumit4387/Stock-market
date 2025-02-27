import datetime
import uuid

from src.model.trade_indicator import TradeIndicator


class Trade:
    """
        Represents a trade on the stock market.
    """

    def __init__(self, quantity: int, indicator: TradeIndicator, price: float):
        self.id = uuid.uuid4()
        self.timestamp = datetime.datetime.now()
        self.quantity = quantity
        self.indicator = indicator
        self.price = price
