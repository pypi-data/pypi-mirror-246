"""
Generates performance reports for your stock portfolio.
"""
from argparse import ArgumentParser, Namespace
import csv
from collections import OrderedDict
import os
import requests



def main():
    """
    Entrypoint into program.
    """
    args = get_args()
    source_csv = args.source
    target_csv = args.target
    if not source_csv:
        print("No source file was entered.")
    else:
        input_file = read_portfolio(source_csv)
        market_data = get_market_data(input_file)
        calulated_data = calculate_metrics(input_file, market_data)
        save_portfolio(calulated_data, target_csv)


def read_portfolio(filename):
    """
    Returns data from a CSV file
    """
    stock_list = []
    try:
        with open(filename, newline='',encoding="utf-8") as csvfile:
            stocks = csv.reader(csvfile)
            headers = next(stocks)
            for row in stocks:
                stocksign = OrderedDict(zip(headers,row))
                stock_list.append(stocksign)
    except FileNotFoundError:
        print(f"File {filename} not found")
    return stock_list

def get_args(args=None):
    """
    Parse and return command line argument values
    """

    parser = ArgumentParser()
    parser.add_argument('--source', type=str, help='The source csv file with stock information')
    parser.add_argument('--target', type=str,
                        help='The target file to be created with updated stock information')
    parsed_args: Namespace = parser.parse_args(args)
    return parsed_args


def get_market_data(stocks_list):
    """
    Get the latest market data for the given stock symbols
    """
    market_data = []
    api_token = os.getenv('api_token')
    symbols = [item['symbol'] for item in stocks_list if 'symbol' in item]
    url = f'https://cloud.iexapis.com/stable/tops?token={api_token}&symbols={",".join(symbols)}'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            market_data.append(response.json())
        else:
            for symbol in symbols:
                failed = {"symbol": symbol,
                          "price": None, "size": None, "time": None}
                market_data.append(failed)
    except requests.RequestException as e:
        for symbol in symbols:
            exception = {"symbol": symbol, "error": f"Error: {e}"}
            market_data.append(exception)
    return market_data


def calculate_metrics(input_file, market_data):
    """
    Calculates the various metrics of each of the stocks
    """
    market_dict = {item['symbol']: item for item in market_data}

    calculated = []

    for item in input_file:
        symbol = item['symbol']
        if symbol in market_dict and market_dict[symbol]['price'] is not None:
            units = int(item['units'])
            cost = float(item['cost'])
            latest_price = float(market_dict[symbol]['price'])

            latest_price = float(market_dict[symbol]['price'])
            book_value = int(units * cost)
            market_value = int(units * latest_price)
            gain_loss = int(market_value - book_value)
            round_change = gain_loss / book_value if book_value != 0 else 0
            change = round(round_change, 3)

            target_csv = {
                'symbol': symbol,
                'units': units,
                'cost': cost,
                'latest_price': latest_price,
                'book_value': book_value,
                'market_value': market_value,
                'gain_loss': gain_loss,
                'change': change
            }
            calculated.append(target_csv)
        else:
            target_csv = {
                'symbol': f"{symbol} Market data for not found",
                'units': None,
                'cost': None,
                'latest_price': None,
                'book_value': None,
                'market_value': None,
                'gain_loss': None,
                'change': None
            }
            calculated.append(target_csv)

    return calculated

def save_portfolio(output_data, filename):
    """
    Saves data to a CSV file
    """
    try:
        if output_data:
            if not all(isinstance(item, dict)for item in output_data):
                raise ValueError("Each item should be a dictionary")

            with open (filename, 'w', encoding="utf-8", newline='') as f:
                w = csv.DictWriter(f,output_data[0].keys())
                w.writeheader()
                w.writerows(output_data)
    except ValueError as ve:
        print(f"Value error has occurred: {ve}")
    except IOError as ioe:
        print(f"An IO Error has occurred: {ioe}")

if __name__ == '__main__':
    main()
