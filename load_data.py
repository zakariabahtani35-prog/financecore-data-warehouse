import pandas as pd
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import Config

# LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# DB CONNECTION
engine = create_engine(Config.DATABASE_URL)

# LOAD CSV
try:
    df = pd.read_csv("financecore_clean.csv")
    logging.info(f"CSV loaded successfully: {df.shape}")
except Exception as e:
    logging.error(f"Error loading CSV: {e}")
    exit()

# CLEANING
df["date_transaction"] = pd.to_datetime(df["date_transaction"], errors="coerce")
df["montant"] = pd.to_numeric(df["montant"], errors="coerce")
df["score_credit_client"] = pd.to_numeric(df["score_credit_client"], errors="coerce")

# Remove invalid important rows
df = df.dropna(subset=["client_id", "transaction_id", "montant"])

# Clean text columns
text_cols = ["client_id", "segment_client", "produit", "agence", "devise", "statut", "transaction_id"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# Replace fake null strings
df["segment_client"] = df["segment_client"].replace(["nan", "Nan", "None", ""], pd.NA)
df["produit"] = df["produit"].replace(["nan", "Nan", "None", ""], pd.NA)
df["agence"] = df["agence"].replace(["nan", "Nan", "None", ""], pd.NA)
df["devise"] = df["devise"].replace(["nan", "Nan", "None", ""], pd.NA)
df["statut"] = df["statut"].replace(["nan", "Nan", "None", ""], pd.NA)

# Fill missing values
df["segment_client"] = df["segment_client"].fillna("Unknown")
df["produit"] = df["produit"].fillna("Unknown Product")
df["agence"] = df["agence"].fillna("Unknown Agency")
df["devise"] = df["devise"].fillna("Unknown")
df["statut"] = df["statut"].fillna("Unknown")

# Remove duplicate transactions
df = df.drop_duplicates(subset=["transaction_id"], keep="first")

# NORMALIZATION

# Clients
clients_df = df[["client_id", "segment_client", "score_credit_client"]].copy()
clients_df = clients_df.drop_duplicates(subset=["client_id"], keep="first")
clients_df.columns = ["client_id", "segment", "score_credit"]

# Accounts
accounts_df = df[["client_id"]].copy()
accounts_df = accounts_df.drop_duplicates(subset=["client_id"], keep="first").reset_index(drop=True)
accounts_df["account_id"] = accounts_df.index + 1
accounts_df = accounts_df[["account_id", "client_id"]]

# Add account_id to main df
df = df.merge(accounts_df, on="client_id", how="left")

# Products
products_df = df[["produit"]].copy()
products_df = products_df.drop_duplicates(subset=["produit"], keep="first").reset_index(drop=True)
products_df["product_id"] = products_df.index + 1
products_df = products_df[["product_id", "produit"]]
products_df.columns = ["product_id", "product_name"]

# Add product_id to main df
df = df.merge(
    products_df.rename(columns={"product_name": "produit"}),
    on="produit",
    how="left"
)

# Agencies
agencies_df = df[["agence"]].copy()
agencies_df = agencies_df.drop_duplicates(subset=["agence"], keep="first").reset_index(drop=True)
agencies_df["agency_id"] = agencies_df.index + 1
agencies_df = agencies_df[["agency_id", "agence"]]
agencies_df.columns = ["agency_id", "agency_name"]

# Add agency_id to main df
df = df.merge(
    agencies_df.rename(columns={"agency_name": "agence"}),
    on="agence",
    how="left"
)

# Transactions
transactions_df = df[[
    "transaction_id",
    "account_id",
    "product_id",
    "agency_id",
    "montant",
    "devise",
    "date_transaction",
    "statut"
]].copy()

transactions_df.columns = [
    "transaction_id",
    "account_id",
    "product_id",
    "agency_id",
    "amount",
    "currency",
    "transaction_date",
    "status"
]

transactions_df = transactions_df.drop_duplicates(subset=["transaction_id"], keep="first")
transactions_df = transactions_df.dropna(subset=["account_id", "product_id", "agency_id"])

transactions_df["account_id"] = transactions_df["account_id"].astype(int)
transactions_df["product_id"] = transactions_df["product_id"].astype(int)
transactions_df["agency_id"] = transactions_df["agency_id"].astype(int)

# INSERTION

def safe_insert(dataframe, table_name):
    try:
        dataframe.to_sql(table_name, engine, if_exists="append", index=False)
        logging.info(f"Inserted into {table_name}: {len(dataframe)} rows")
    except SQLAlchemyError as e:
        logging.error(f"Error inserting into {table_name}: {e}")

safe_insert(clients_df, "clients")
safe_insert(accounts_df, "accounts")
safe_insert(products_df, "products")
safe_insert(agencies_df, "agencies")
safe_insert(transactions_df, "transactions")

# INTEGRITY CHECK
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
        count = result.fetchone()[0]
        logging.info(f"Total transactions in DB: {count}")
except Exception as e:
    logging.error(f"Integrity check failed: {e}")

print("Data pipeline executed successfully.")