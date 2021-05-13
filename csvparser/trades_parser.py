import csv
import decimal
import time
from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from pycoingecko import CoinGeckoAPI

from portfolio.trade import Trade


class FieldIds:
    ticker = 'ticker'
    timestamp = 'timestamp'
    amount = 'amount'
    price = 'price'


def parse_from_csv():
    def get_coin_id_from_ticker():
        for coin in coins:
            if coin['symbol'] == str(ticker).lower():
                return coin['id']
        raise Exception("No symbol found for ticker {}".format(ticker))

    cg_api = CoinGeckoAPI()
    coins = cg_api.get_coins_list()
    trades = []
    price_cache = defaultdict(dict)
    req_count = 1
    with open('input/all.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        decimal.getcontext().prec = 16
        for row in csv_reader:
            ticker = row.get(FieldIds.ticker)
            date = datetime.strptime(row.get(FieldIds.timestamp), '%Y-%m-%d  %H:%M:%S')
            amount = Decimal(row.get(FieldIds.amount))
            price = row.get(FieldIds.price)
            if price:
                price = Decimal(price)
                date = date.strftime('%d-%m-%Y')
            else:
                coin_id = get_coin_id_from_ticker()
                date = date.strftime('%d-%m-%Y')
                if coin_id in price_cache.keys() and date in price_cache[coin_id].keys():
                    price = price_cache[coin_id][date]
                else:
                    req_count = req_count + 1
                    if req_count >= 50:
                        time.sleep(60)
                        req_count = 0
                    history = cg_api.get_coin_history_by_id(coin_id, date)
                    price = history['market_data']['current_price']['eur']
                    price_cache[coin_id][date] = price
                price = Decimal(price)
            trades.append(Trade(date, ticker, amount, price))
    return trades
