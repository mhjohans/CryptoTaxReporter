import collections
from decimal import Decimal


class Batch:
    def __init__(self, amount, price):
        self.amount = amount
        self.price = price

    def sell(self, amount, price):
        leftover_amount = amount - self.amount
        if leftover_amount >= 0:
            self.amount = 0
        else:
            leftover_amount = 0
            self.amount = self.amount - amount
        price_difference = price - self.price
        if self.price < Decimal(0.2) * price:
            price_difference = Decimal(0.8) * price
        return leftover_amount, price_difference


class Position:
    def __init__(self):
        self.batches = collections.deque()

    def buy(self, amount, price):
        self.batches.append(Batch(amount, price))

    def sell(self, amount, price):
        profit = 0
        leftover_amount = amount
        while leftover_amount > 0:
            sell_amount = leftover_amount
            if len(self.batches) > 0:
                leftover_amount, price_difference = self.batches[0].sell(sell_amount, price)
            else:
                leftover_amount, price_difference = 0, Decimal(0.8) * price
            sell_amount = sell_amount - leftover_amount
            profit = profit + sell_amount * price_difference
            if leftover_amount > 0:
                self.batches.popleft()
        return profit
