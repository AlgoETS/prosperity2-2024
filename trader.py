from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import jsonpickle

class Trader:

    def __init__(self):
        self.ema_period = 10  # EMA period
        self.ema_values: Dict[str, float] = {}  # Stores the latest EMA values for each product

    def calculate_ema(self, prices: List[int], period: int, previous_ema: float = None) -> float:
        alpha = 2 / (period + 1)
        if previous_ema is None:  # If there's no previous EMA, use the first price as initial EMA
            return prices[0]
        else:
            current_price = prices[-1]
            return alpha * current_price + (1 - alpha) * previous_ema

    def run(self, state: TradingState):
        result = {}
        traderData = "SAMPLE"
        conversions = 0  # Assuming no conversions for simplicity

        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            
            # Calculate the EMA for the current product
            historical_prices = [trade.price for trade in state.own_trades.get(product, [])]
            if product not in self.ema_values:
                if historical_prices:
                    self.ema_values[product] = self.calculate_ema(historical_prices, self.ema_period)
            else:
                if historical_prices:
                    self.ema_values[product] = self.calculate_ema(historical_prices, self.ema_period, self.ema_values[product])
            
            current_price = None
            if order_depth.sell_orders:
                # Assuming best ask as the current price for simplicity
                current_price = min(order_depth.sell_orders.keys())
            
            if current_price:
                acceptable_quantity = 1  # Simplified logic for quantity
                
                # Buy signal: current price below EMA (indicating potential uptrend)
                if current_price < self.ema_values.get(product, 0):
                    orders.append(Order(product, current_price, acceptable_quantity))
                
                # Sell signal: current price above EMA (indicating potential downtrend)
                elif current_price > self.ema_values.get(product, 0):
                    orders.append(Order(product, current_price, -acceptable_quantity))
            
            result[product] = orders
        
        # Serialize traderData for state persistence
        traderData = jsonpickle.encode({
            "ema_values": self.ema_values
        })
        
        return result, conversions, traderData
