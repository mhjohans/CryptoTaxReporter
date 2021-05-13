from collections import defaultdict

from portfolio.position import Position

positions = defaultdict(Position)


def add_trade(trade):
    profit = 0
    current_position = positions[trade.ticker]
    if trade.amount > 0:
        current_position.buy(trade.amount, trade.price)
    else:
        profit = current_position.sell(abs(trade.amount), trade.price)
    return profit
