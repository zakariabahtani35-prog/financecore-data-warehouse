from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from config import Config

Base = declarative_base()

# CLIENTS
class Client(Base):
    __tablename__ = "clients"

    client_id = Column(String, primary_key=True)
    segment = Column(String, nullable=False)
    score_credit = Column(Float)


# ACCOUNTS
class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True)
    client_id = Column(String, ForeignKey("clients.client_id"), nullable=False)


# PRODUCTS
class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, unique=True, nullable=False)


# AGENCIES
class Agency(Base):
    __tablename__ = "agencies"

    agency_id = Column(Integer, primary_key=True)
    agency_name = Column(String, unique=True, nullable=False)


# TRANSACTIONS
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)

    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    agency_id = Column(Integer, ForeignKey("agencies.agency_id"), nullable=False)

    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    transaction_date = Column(DateTime)
    status = Column(String)


# CONNECTION
engine = create_engine(Config.DATABASE_URL)

# CREATE TABLES
Base.metadata.create_all(engine)

print("Tables created successfully")
