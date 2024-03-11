import jsonpickle
from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import numpy as np

class Trader:

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
        for price in prices[-period:]:
            ema = alpha * price + (1 - alpha) * ema
        return ema

    def calculate_rsi(self, prices: List[int], period: int) -> float:
        if len(prices) < period:
            return 50  # Neutral RSI value if not enough data
        deltas = np.diff(prices)
        gain = np.where(deltas > 0, deltas, 0).sum() / period
        loss = np.where(deltas < 0, -deltas, 0).sum() / period

        if loss == 0:
            return 100  # Prevent division by zero
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []

            historical_prices = [trade.price for trade in state.own_trades.get(product, [])] + [trade.price for trade in state.market_trades.get(product, [])]
            if historical_prices:
                self.ema_values[product]['fast'] = self.calculate_ema(historical_prices, self.fast_ema_period, self.ema_values[product].get('fast'))
                self.ema_values[product]['slow'] = self.calculate_ema(historical_prices, self.slow_ema_period, self.ema_values[product].get('slow'))
                self.rsi_values[product] = self.calculate_rsi(historical_prices, self.rsi_period)

                fast_ema = self.ema_values[product]['fast']
                slow_ema = self.ema_values[product]['slow']
                rsi = self.rsi_values[product]
                acceptable_quantity = 1

                if fast_ema > slow_ema and rsi > 50:
                    # Modified trading logic to consider RSI
                    current_position = state.position.get(product, 0)
                    if current_position < 10 and order_depth.sell_orders:
                        lowest_sell_price = min(order_depth.sell_orders.keys())
                        orders.append(Order(product, lowest_sell_price, acceptable_quantity))
                elif fast_ema < slow_ema and rsi < 50:
                    current_position = state.position.get(product, 0)
                    if current_position > -10 and order_depth.buy_orders:
                        highest_buy_price = max(order_depth.buy_orders.keys())
                        orders.append(Order(product, highest_buy_price, -acceptable_quantity))

            result[product] = orders

        traderData = jsonpickle.encode({"ema_values": self.ema_values, "rsi_values": self.rsi_values})

        return result, conversions, traderData
