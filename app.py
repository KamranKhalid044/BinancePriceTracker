# app.py


from datetime import datetime
from models import Trade, Session
from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc, func, and_, exists

app = Flask(__name__)

CURRENT_PRICE_ENDPOINT = '/current_price'
HISTORICAL_DATA_ENDPOINT = '/historical_data'
STATISTICAL_ANALYSIS_ENDPOINT = '/statistical_analysis'


@app.route(CURRENT_PRICE_ENDPOINT, methods=['GET'])
def get_current_price():
    symbols = request.args.get('symbol')
    if not symbols or not symbols.strip():
        return jsonify({'error': 'Please provide a valid symbol parameter'}), 400

    symbols_list = symbols.split(',')
    if len(symbols_list) > 1:
        return jsonify({'error': 'Only one symbol parameter is allowed'}), 400

    symbol = symbols_list[0].strip()

    try:
        with Session() as session:
            symbol_exists = session.query(Trade).filter_by(symbol=symbol).first() is not None
            if not symbol_exists:
                return jsonify({'message': 'Symbol does not exist in the database'}), 404

            trade = session.query(Trade).filter_by(symbol=symbol).order_by(desc(Trade.timestamp),
                                                                           desc(Trade.id)).first()
            if trade:
                return jsonify({'symbol': trade.symbol, 'price': trade.price}), 200
            else:
                return jsonify({'message': 'Data not found for the specified symbol'}), 404
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error occurred while fetching current price: {e}'}), 500


@app.route(HISTORICAL_DATA_ENDPOINT, methods=['GET'])
def get_historical_data():
    symbol = request.args.get('symbol')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    if not symbol or not start_date_str or not end_date_str:
        return jsonify({'error': 'Please provide symbol, start_date, and end_date parameters'}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format, date format must be YYYY-MM-DD HH:MM:SS'}), 400

    if start_date >= end_date:
        return jsonify({'error': 'Start date must be earlier than the end date'}), 400

    try:
        with Session() as session:
            symbol_exists = session.query(Trade).filter_by(symbol=symbol).first() is not None
            if not symbol_exists:
                return jsonify({'message': 'Symbol does not exist in the database'}), 404

            date_range_exists = session.query(exists().where(Trade.symbol == symbol,
                                                             Trade.timestamp >= str(start_date),
                                                             Trade.timestamp <= str(end_date))).scalar()
            if not date_range_exists:
                return jsonify({'message': 'Data not found for the specified date range'}), 404

            total_items = session.query(func.count(Trade.id)).filter(Trade.symbol == symbol,
                                                                     Trade.timestamp >= str(start_date),
                                                                     Trade.timestamp <= str(end_date)).scalar()

            offset = (page - 1) * per_page

            trades = session.query(Trade).filter(Trade.symbol == symbol, Trade.timestamp >= str(start_date),
                                                 Trade.timestamp <= str(end_date)).order_by(
                desc(Trade.timestamp)).limit(per_page).offset(offset).all()

            if not trades and (page > 1 and total_items > 0):
                total_pages = (total_items + per_page - 1) // per_page
                return jsonify({'message': 'Requested page is out of range. Please provide a valid page number',
                                'total_items': total_items, 'total_pages': total_pages}), 404

            data = [{'symbol': trade.symbol, 'price': trade.price, 'timestamp': trade.timestamp} for trade in
                    trades]

            total_pages = (total_items + per_page - 1) // per_page

            return jsonify({'total_items': total_items, 'total_pages': total_pages, 'data': data}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error occurred while fetching historical data: {e}'}), 500


@app.route(STATISTICAL_ANALYSIS_ENDPOINT, methods=['GET'])
def perform_statistical_analysis():
    symbols = request.args.get('symbol')
    if not symbols or not symbols.strip():
        return jsonify({'error': 'Please provide a valid symbol parameter'}), 400

    symbols_list = symbols.split(',')
    if len(symbols_list) > 1:
        return jsonify({'error': 'Only one symbol parameter is allowed'}), 400

    symbol = symbols_list[0].strip()

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = None
    end_date = None

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid date format, date format must be YYYY-MM-DD HH:MM:SS'}), 400

        if start_date >= end_date:
            return jsonify({'error': 'Start date must be earlier than the end date'}), 400

    try:
        with Session() as session:
            symbol_exists = session.query(Trade).filter_by(symbol=symbol).first() is not None
            if not symbol_exists:
                return jsonify({'message': 'Symbol does not exist in the database'}), 404

            query = session.query(Trade.price).filter(Trade.symbol == symbol)

            if start_date and end_date:
                date_range_exists = session.query(
                    exists().where(and_(Trade.timestamp >= str(start_date), Trade.timestamp <= str(end_date)))).scalar()

                if not date_range_exists:
                    return jsonify({'message': 'Data not found for the specified date range'}), 404

                query = query.filter(and_(Trade.timestamp >= str(start_date), Trade.timestamp <= str(end_date)))

            trades = query.all()
            prices = [trade.price for trade in trades]
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

            return jsonify({'symbol': symbol, 'average_price': average_price, 'median_price': median_price,
                            'standard_deviation': standard_deviation, 'percentage_change': percentage_change}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error occurred while performing statistical analysis: {e}'}), 500


if __name__ == "__main__":
    app.run(debug=True)
