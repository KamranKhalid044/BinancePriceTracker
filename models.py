from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Index

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.now())


trade_symbol_index = Index('trade_symbol_index', Trade.symbol)

engine = create_engine('sqlite:///binance_cryptocurrency_prices.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
