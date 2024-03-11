import jsonpickle
from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import numpy as np

class EnhancedTrader:

    def __init__(self):
        self.fast_ema_period = 5
        self.slow_ema_period = 10
        self.rsi_period = 14
        self.ema_values: Dict[str, Dict[str, float]] = {}
        self.rsi_values: Dict[str, float] = {}

    def calculate_ema(self, prices: List[int], period: int, previous_ema: float = None) -> float:
        if not prices:
            return previous_ema if previous_ema else 0
        alpha = 2 / (period + 1)
        ema = prices[0] if previous_ema is None else previous_ema
        for price in prices:
            ema = alpha * price + (1 - alpha) * ema
        return ema

    def calculate_rsi(self, prices: List[int], period: int) -> float:
        if len(prices) < period:
            return 50  # Neutral RSI value if not enough data
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100./(1.+rs)
        return rsi[-1]

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            # Initialize storage for EMA and RSI values
            if product not in self.ema_values:
                self.ema_values[product] = {'fast': None, 'slow': None}
            if product not in self.rsi_values:
                self.rsi_values[product] = None
            # Historical prices from trades
            historical_prices = [trade.price for trade in state.own_trades.get(product, [])] + [trade.price for trade in state.market_trades.get(product, [])]
            # Calculate indicators
            if historical_prices:
                fast_ema = self.calculate_ema(historical_prices, self.fast_ema_period, self.ema_values[product].get('fast'))
                slow_ema = self.calculate_ema(historical_prices, self.slow_ema_period, self.ema_values[product].get('slow'))
                rsi = self.calculate_rsi(historical_prices, self.rsi_period)
                self.ema_values[product] = {'fast': fast_ema, 'slow': slow_ema}
                self.rsi_values[product] = rsi
                # Determine trading signals
                current_position = state.position.get(product, 0)
                # Buy signal conditions
                if fast_ema > slow_ema and rsi < 30 and current_position < 10:
                    orders.append(Order(product, min(order_depth.sell_orders.keys()), 1))  # Dynamic sizing could be added
                # Sell signal conditions
                elif fast_ema < slow_ema and rsi > 70 and current_position > -10:
                    orders.append(Order(product, max(order_depth.buy_orders.keys()), -1))  # Dynamic sizing could be added
            result[product] = orders
        traderData = jsonpickle.encode({
            "ema_values": self.ema_values,
            "rsi_values": self.rsi_values
        })
        return result, conversions, traderData
