"""
Tests I/O disk operations.
"""

from collections import OrderedDict

import pytest

import requests_mock

from portfolio import portfolio_report


# Note: the portfolio_csv argument found in the tests below
#       is a pytest "fixture". It is defined in conftest.py

# DO NOT edit the provided tests. Make them pass.

expected1 = [
        OrderedDict([
            ('symbol', 'AAPL'),
            ('units', '1000'),
            ('cost', '123.56'),
        ]),
        OrderedDict([
            ('symbol', 'AMZN'),
            ('units', '20'),
            ('cost', '2001.1')
        ])
    ]

expected_data = [
        {"symbol": "AAPL", "price": 156.23, "size": 100, "time": 1563307196175},
        {"symbol": "AMZN", "price": 1478.19, "size": 1, "time": 1563307196058}
    ]

def test_read_portfolio(portfolio_csv):
    """
    Given that the read_portfolio is called, assert that
    the data the expected data is returned.
    """
    expected = [
        OrderedDict([
            ('symbol', 'APPL'),
            ('units', '100'),
            ('cost', '154.23'),
        ]),
        OrderedDict([
            ('symbol', 'AMZN'),
            ('units', '600'),
            ('cost', '1223.43')
        ])
    ]

    assert portfolio_report.read_portfolio(portfolio_csv) == expected, (
        'Expecting to get the data stored in the portfolio_csv '
        'fixture as a Python data structure.'
    )

def test_get_args():
    """
    Testing the comand line interface portion for the --source file name and --target file name
    Tests for successful, source only entered, target only entered and nothing entered
    """

    test_args = ['--source', 'test_source.csv', '--target', 'test_target.csv']
    parsed_args = portfolio_report.get_args(test_args)

    assert parsed_args.source == 'test_source.csv'
    assert parsed_args.target == 'test_target.csv'

    source_only = ['--source', 'test_source.csv']
    source_args = portfolio_report.get_args(source_only)

    assert source_args.source == 'test_source.csv'
    assert source_args.target is None

    source_only = ['--target', 'test_target.csv']
    source_args = portfolio_report.get_args(source_only)

    assert source_args.source is None
    assert source_args.target == 'test_target.csv'

    fail_args = ['--source', '--target']
    with pytest.raises(SystemExit):
        portfolio_report.get_args(fail_args)

def test_get_market_data(monkeypatch):

    """
    Testing api messages with IEX
    """

    # Mocking the API token
    mock_api_token = 'test_token'
    monkeypatch.setenv('api_token', mock_api_token)

    #symbols = [item['symbol'] for item in expected if 'symbol' in item]
    with requests_mock.Mocker() as m:
        m.get(f'https://cloud.iexapis.com/stable/tops?token={mock_api_token}&symbols=AAPL,AMZN',
              json=[{"symbol":"AAPL","price": 156.23, "size": 100, "time": 1563307196175},
                {"symbol":"AMZN", "price": 1478.19, "size": 1, "time": 1563307196058}])

        expected_test = portfolio_report.get_market_data(expected1)

    assert expected_test[0] == expected_data

def test_calculate_metrics():
    """
    Testing calculations are done properly.
    """
    cal_test = portfolio_report.calculate_metrics(expected1, expected_data)
    cal_verify = [
        {
            'symbol': 'AAPL',
            'units': 1000,
            'cost': 123.56,
            'latest_price': 156.23,
            'book_value': 123560,
            'market_value': 156230,
            'gain_loss': 32670,
            'change': 0.264
        },
        {
            'symbol': 'AMZN',
            'units': 20,
            'cost': 2001.1,
            'latest_price': 1478.19,
            'book_value': 40022,
            'market_value': 29563,
            'gain_loss': -10459,
            'change': -0.261
        }
    ]
    assert cal_test == cal_verify



def test_save_portfolio(portfolio_csv):
    """
    Given that the save portfolio method is called with the following
    data, assert that a CSV file is written in the expected format.

    The portfolio
    """
    data = [{'symbol': 'MSFT', 'units': 10, 'cost': 99.66}]
    portfolio_report.save_portfolio(data, filename=portfolio_csv)

    expected = 'symbol,units,cost\r\nMSFT,10,99.66\r\n'
    with open(portfolio_csv, 'r', newline='', encoding="utf-8") as file:
        result = file.read()
        assert result == expected, (
            f'Expecting the file to contain: \n{result}'
        )
