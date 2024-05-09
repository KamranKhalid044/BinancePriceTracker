# test_api_endpoints.py

import unittest
from models import Trade
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
from app import app, CURRENT_PRICE_ENDPOINT, HISTORICAL_DATA_ENDPOINT, STATISTICAL_ANALYSIS_ENDPOINT


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch('data_manager.Session')
    def test_successful_current_price(self, mock_session):
        # Mock session.query().filter_by().order_by().first()
        mock_trade = Trade(symbol='VETUSDT', price=0.03493)
        mock_session.return_value.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = mock_trade
        response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=VETUSDT')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'symbol': 'VETUSDT', 'price': 0.03493})

    def test_no_data_found_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None
            response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=BTCUSD')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_missing_symbol_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(CURRENT_PRICE_ENDPOINT)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_symbol_not_exist_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None
            response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=UNKNOWN')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_invalid_symbol_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_multiple_symbols_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=DOGEUSDT,BTCUSD')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_symbol_with_no_trades_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None
            response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=ETHUSD')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_database_error_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.side_effect = SQLAlchemyError('Database error')
            response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=BTCUSD')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json)

    def test_error_fetching_current_price(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.side_effect = Exception('Error occurred while fetching current price')
            response = self.app.get(f'{CURRENT_PRICE_ENDPOINT}?symbol=VETUSDT')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json)

    @patch('data_manager.Session')
    def test_successful_historical_data(self, mock_session):
        mock_data = [
            {"id": 178, "symbol": "VETUSDT", "price": 0.03498, "timestamp": "2024-05-08 12:57:51"},
            {"id": 179, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"id": 180, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"id": 181, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"id": 182, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"id": 183, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"id": 184, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:53"},
            {"id": 188, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:54"},
            {"id": 189, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:54"},
            {"id": 190, "symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:54"},
            {"id": 627, "symbol": "VETUSDT", "price": 0.03493, "timestamp": "2024-05-08 13:10:12"}
        ]
        mock_session.return_value.query.return_value.filter.return_value.all.return_value = mock_data

        response = self.app.get(
            f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08 12:57:51&end_date=2024-05-08 13:10:12')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['total_items'], len(mock_data))

    def test_missing_parameters_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None
            response = self.app.get(HISTORICAL_DATA_ENDPOINT)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_symbol_not_exist_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSD&start_date=2024-05-08 12:57:51&end_date=2024-05-08 13:10:12')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_valid_date_format_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(
                f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-01 00:00:00&end_date=2024-05-10 00:00:00')
            self.assertEqual(response.status_code, 200)

    def test_invalid_date_format_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08&end_date=2024-05-08')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_start_date_after_end_date_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = None
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08 13:10:12&end_date=2024-05-08 12:57:51')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_no_data_found_within_date_range_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = None
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSDT&start_date=2024-06-01 00:00:00&end_date=2024-06-10 00:00:00')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_valid_date_range_historical_data(self):
        mock_data = [
            {"symbol": "VETUSDT", "price": 0.03498, "timestamp": "2024-05-08 12:57:51"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-09 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-10 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-11 12:57:52"}
        ]

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = mock_data
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08 12:57:51&end_date=2024-05-11 12:57:52')
            self.assertEqual(response.status_code, 200)

    def test_successful_pagination_historical_data(self):
        mock_data = [{"price": 0.03493, "symbol": "VETUSDT", "timestamp": "2024-05-08 13:10:12"},
                     {"price": 0.03499, "symbol": "VETUSDT", "timestamp": "2024-05-08 12:57:54"}]

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = mock_data
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08 12:57:51&end_date=2024-05-08 13:10:12&page=1&per_page=2')
            self.assertEqual(response.status_code, 200)
            self.assertIn('total_items', response.json)
            self.assertIn('total_pages', response.json)
            self.assertIn('data', response.json)

    def test_out_of_range_page_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = None
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08 12:57:51&end_date=2024-05-08 13:10:12&page=100')

            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_database_error_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.side_effect = SQLAlchemyError('Database error')
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}symbol=VETUSDT&start_date=2024-05-08 12:57:51&end_date=2024-05-08 13:10:12')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json)

    def test_error_fetching_historical_data(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.side_effect = Exception('Error occurred while fetching historical data')
            response = self.app.get(
                f'{HISTORICAL_DATA_ENDPOINT}symbol=VETUSDT&start_date=2024-05-08 12:57:51&end_date=2024-05-08 13:10:12')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json)

    @patch('data_manager.Session')
    def test_successful_statistical_analysis(self, mock_session):
        mock_data = [
            {"symbol": "VETUSDT", "price": 0.03498, "timestamp": "2024-05-08 12:57:51"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:53"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:54"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:54"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-08 12:57:54"},
            {"symbol": "VETUSDT", "price": 0.03493, "timestamp": "2024-05-08 13:10:12"}
        ]

        # Mock session.query().filter_by().all()
        mock_session.return_value.query.return_value.filter_by.return_value.all.return_value = mock_data

        response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT')

        self.assertEqual(response.status_code, 200)

        prices = [trade['price'] for trade in mock_data]
        prices.sort()
        n = len(prices)
        median_index = n // 2
        if n % 2 == 0:
            median_price = (prices[median_index - 1] + prices[median_index]) / 2
        else:
            median_price = prices[median_index]

        average_price = round(sum(prices) / len(prices), 2)
        standard_deviation = round((sum((x - average_price) ** 2 for x in prices) / len(prices)) ** 0.5, 2)
        percentage_change = round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)

        self.assertEqual(response.json,
                         {'symbol': 'VETUSDT', 'average_price': average_price, 'median_price': median_price,
                          'standard_deviation': standard_deviation, 'percentage_change': percentage_change})

    def test_missing_symbol_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(STATISTICAL_ANALYSIS_ENDPOINT)
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_symbol_not_exist_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.all.return_value = None
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=UNKNOWN')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_invalid_symbol_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_multiple_symbols_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=DOGEUSDT,BTCUSD')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_missing_start_date_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT')
            self.assertEqual(response.status_code, 200)
            self.assertIn('average_price', response.json)
            self.assertIn('median_price', response.json)

    def test_missing_end_date_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08 12:57:51')
            self.assertEqual(response.status_code, 200)
            self.assertIn('average_price', response.json)
            self.assertIn('median_price', response.json)

    def test_valid_date_format_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(
                f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-01 00:00:00&end_date=2024-05-10 00:00:00')
            self.assertEqual(response.status_code, 200)

    def test_invalid_date_format_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(
                f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-01T00:00:00&end_date=2024-05-10T00:00:00')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_symbol_with_no_trades_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=XYZUSD')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_start_date_after_end_date_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.first.return_value = None
            response = self.app.get(
                f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-10 00:00:00&end_date=2024-05-01 00:00:00')
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', response.json)

    def test_no_data_found_within_date_range_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = None
            response = self.app.get(
                f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-06-01 00:00:00&end_date=2024-06-10 00:00:00')
            self.assertEqual(response.status_code, 404)
            self.assertIn('message', response.json)

    def test_valid_date_range_statistical_analysis(self):
        mock_data = [
            {"symbol": "VETUSDT", "price": 0.03498, "timestamp": "2024-05-08 12:57:51"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-09 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-10 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-11 12:57:52"}
        ]

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = mock_data
            response = self.app.get(
                f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-08 12:57:51&end_date=2024-05-11 12:57:52')
            self.assertEqual(response.status_code, 200)

    def test_date_range_with_no_start_date_statistical_analysis(self):
        mock_data = [
            {"symbol": "VETUSDT", "price": 0.03498, "timestamp": "2024-05-08 12:57:51"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-09 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-10 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-11 12:57:52"}
        ]

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = mock_data
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&end_date=2024-05-10 00:00:00')
            self.assertEqual(response.status_code, 200)

    def test_date_range_with_no_end_date_statistical_analysis(self):
        mock_data = [
            {"symbol": "VETUSDT", "price": 0.03498, "timestamp": "2024-05-08 12:57:51"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-09 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-10 12:57:52"},
            {"symbol": "VETUSDT", "price": 0.03499, "timestamp": "2024-05-11 12:57:52"}
        ]

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter.return_value.all.return_value = mock_data
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT&start_date=2024-05-09 00:00:00')
            self.assertEqual(response.status_code, 200)

    def test_average_price_calculation_statistical_analysis(self):
        mock_data = [{'symbol': 'VETUSDT', 'price': 0.03498, 'timestamp': '2024-05-08 12:57:51'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:53'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03493, 'timestamp': '2024-05-08 13:10:12'}]

        prices = [data['price'] for data in mock_data]

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.all.return_value = mock_data
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT')

        average_price = round(sum(prices) / len(prices), 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['average_price'], average_price)

    def test_median_price_calculation_statistical_analysis(self):
        mock_data = [{'symbol': 'VETUSDT', 'price': 0.03498, 'timestamp': '2024-05-08 12:57:51'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:53'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03493, 'timestamp': '2024-05-08 13:10:12'}]

        prices = [data['price'] for data in mock_data]
        prices.sort()

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.all.return_value = mock_data
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT')

        n = len(prices)
        median_index = n // 2
        if n % 2 == 0:
            median_price = (prices[median_index - 1] + prices[median_index]) / 2
        else:
            median_price = prices[median_index]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['median_price'], median_price)

    def test_percentage_change_calculation_statistical_analysis(self):
        mock_data = [{'symbol': 'VETUSDT', 'price': 0.03498, 'timestamp': '2024-05-08 12:57:51'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:53'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03493, 'timestamp': '2024-05-08 13:10:12'}]

        prices = [data['price'] for data in mock_data]
        prices.sort()

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.all.return_value = mock_data
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT')

        percentage_change = round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['percentage_change'], percentage_change)

    def test_standard_deviation_calculation_statistical_analysis(self):
        mock_data = [{'symbol': 'VETUSDT', 'price': 0.03498, 'timestamp': '2024-05-08 12:57:51'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:52'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:53'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03499, 'timestamp': '2024-05-08 12:57:54'},
                     {'symbol': 'VETUSDT', 'price': 0.03493, 'timestamp': '2024-05-08 13:10:12'}]

        prices = [data['price'] for data in mock_data]

        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.return_value.filter_by.return_value.all.return_value = mock_data
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT')

        average_price = round(sum(prices) / len(prices), 2)
        standard_deviation = round((sum((x - average_price) ** 2 for x in prices) / len(prices)) ** 0.5, 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['standard_deviation'], standard_deviation)

    def test_database_error_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.side_effect = Exception('Database error')
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=BTCUSD')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json)

    def test_error_fetching_statistical_analysis(self):
        with patch('data_manager.Session') as mock_session:
            mock_session.return_value.query.side_effect = Exception(
                'Error occurred while performing statistical analysis')
            response = self.app.get(f'{STATISTICAL_ANALYSIS_ENDPOINT}?symbol=VETUSDT')
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json)


if __name__ == '__main__':
    unittest.main()
