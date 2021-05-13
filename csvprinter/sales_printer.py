import csv


def print_to_csv(sales):
    with open('output/sales.csv', 'w+', newline='') as csv_file:
        csv_printer = csv.DictWriter(csv_file, ['ticker', 'sale_date', 'sale_price', 'buy_price'],
                                     extrasaction='ignore')
        csv_printer.writeheader()
        csv_printer.writerows(list(sale.__dict__ for sale in sales))
    print('Sales printed to', csv_file)
