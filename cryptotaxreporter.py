from datetime import date

import portfolio
from csvparser.trades_parser import parse_from_csv
from csvprinter.sales_printer import print_to_csv
from portfolio.sale import Sale

tax_year = date.today().year - 1
print('Starting reporting for tax year', tax_year)
print('\nProcessing trades...\n')
trades = parse_from_csv()
total_profit = 0
total_sale_price = 0
total_buy_price = 0
sales = []

for trade in trades:
    profit = portfolio.add_trade(trade)
    if trade.amount < 0:
        sale_price = abs(trade.amount) * trade.price
        total_sale_price = total_sale_price + sale_price
        buy_price = sale_price - profit
        if buy_price == 0:
            buy_price = 0
        total_buy_price = total_buy_price + buy_price
        sales.append(Sale(trade.ticker, trade.date, buy_price, sale_price))
    total_profit = total_profit + profit
print_to_csv(sales)
print('Total buy price: {}'.format(total_buy_price))
print('Total sales price: {}'.format(total_sale_price))
print('Total profit: {}'.format(total_profit))
