from utils import print_log
from models import Trade, Session
from sqlalchemy.exc import SQLAlchemyError


def save_trade_data(symbol, price):
    session = Session()
    try:
        trade = Trade(symbol=symbol, price=price)
        session.add(trade)
        session.commit()
        print_log("Trade data saved successfully")
    except SQLAlchemyError as e:
        print_log(f"Database error occurred: {e}", level='ERROR')
        session.rollback()
    except Exception as e:
        print_log(f"Unexpected error occurred: {e}", level='ERROR')
        session.rollback()
    finally:
        session.close()
