from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.orm import declarative_base, relationship
from config import Config

Base = declarative_base()


# CLIENTS
class Client(Base):
    __tablename__ = "clients"

    client_id = Column(String, primary_key=True)
    segment = Column(String, nullable=False, index=True)
    score_credit = Column(Float)

    accounts = relationship(
        "Account",
        back_populates="client",
        cascade="all, delete"
    )


# ACCOUNTS
class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True)
    client_id = Column(
        String,
        ForeignKey("clients.client_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    client = relationship("Client", back_populates="accounts")
    transactions = relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete"
    )


# PRODUCTS
class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, unique=True, nullable=False)

    transactions = relationship("Transaction", back_populates="product")


# AGENCIES
class Agency(Base):
    __tablename__ = "agencies"

    agency_id = Column(Integer, primary_key=True)
    agency_name = Column(String, unique=True, nullable=False)

    transactions = relationship("Transaction", back_populates="agency")


# TRANSACTIONS
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)

    account_id = Column(
        Integer,
        ForeignKey("accounts.account_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    agency_id = Column(
        Integer,
        ForeignKey("agencies.agency_id"),
        nullable=False,
        index=True
    )

    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    transaction_date = Column(DateTime, index=True)
    status = Column(String)

    __table_args__ = (
        Index("idx_transaction_date", "transaction_date"),
    )

    account = relationship("Account", back_populates="transactions")
    product = relationship("Product", back_populates="transactions")
    agency = relationship("Agency", back_populates="transactions")


# DATABASE CONNECTION
engine = create_engine(Config.DATABASE_URL)


# CREATE TABLES
def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    print("🔥 Creating tables...")
    create_tables()
    print("✅ Tables created successfully.")