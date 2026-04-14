# FinanceCore 🏦

> A production-grade financial data pipeline and analytics system — from raw transactional CSV to a normalized PostgreSQL database, complete with SQL-driven risk intelligence.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen?style=flat-square)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-orange?style=flat-square)

---

## Overview

**FinanceCore** is a structured financial data engineering system designed to ingest, clean, normalize, and analyze large volumes of banking transaction data. It transforms flat, denormalized CSV exports into a fully relational PostgreSQL schema — enabling rich analytical queries across clients, accounts, products, agencies, and transactions.

The system addresses a core challenge faced by financial teams and data engineers: raw transactional data is messy, flat, and difficult to query meaningfully. FinanceCore solves this by implementing a clean ETL pipeline that produces a normalized, query-optimized relational model ready for BI tooling, dashboards, or downstream ML pipelines.

**Who is this for?**
- Data engineers building banking or fintech data platforms
- Financial analysts who need reliable, structured transactional data
- Backend engineers integrating financial data into applications
- Portfolio projects demonstrating production-level data engineering skills

---

## Key Features

- **End-to-end ETL pipeline** — Ingest raw CSV, clean and validate data, normalize into 5 relational tables, and load into PostgreSQL in a single command
- **Robust data cleaning** — Handles type coercion, null imputation, fake-null strings, duplicate removal, and invalid record filtering
- **Normalized relational schema** — Star-schema-inspired design with Clients, Accounts, Products, Agencies, and Transactions tables, enforced foreign keys, and cascading deletes
- **Anomaly and risk tracking** — The dataset includes pre-computed anomaly flags, risk categories, and rejection rates per client segment
- **Analytics-ready SQL queries** — Prebuilt analytical queries covering agency performance, product averages, monthly trends, below-average client segmentation, and risk failure rates
- **Integrity verification** — Post-load integrity checks confirm row counts and pipeline success
- **Config-driven architecture** — All database credentials are externalized to `.env` via `python-dotenv`, never hardcoded
- **SQLAlchemy ORM** — Full ORM model definitions with relationships, indexes, and cascade rules for maintainability and portability

---

## Demo / Preview

> Screenshots and dashboard previews coming soon.

| View | Description |
|---|---|
| `financecore_clean.csv` | Source dataset — 2,000 transactions across French banking clients |
| PostgreSQL schema | 5 normalized tables with FK constraints and composite indexes |
| Analytics queries | Prebuilt SQL for agency totals, product averages, risk segmentation |

To explore the data interactively, connect any SQL client (e.g., DBeaver, TablePlus, psql) to your local PostgreSQL instance after running the pipeline.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.x |
| **Data Processing** | Pandas 2.x |
| **Config Management** | python-dotenv |
| **Query Layer** | Raw SQL (PostgreSQL dialect) |
| **Environment** | `.env` file + `venv` |

---

## Project Architecture

FinanceCore follows a clean, layered ETL architecture:

```
Raw CSV
   │
   ▼
load_data.py          ← Ingestion, cleaning, normalization, insertion
   │
   ├── config.py      ← Reads .env and exposes DATABASE_URL
   ├── database_setup.py  ← Defines ORM models and creates tables
   │
   ▼
PostgreSQL Database
   ├── clients
   ├── accounts
   ├── products
   ├── agencies
   └── transactions
         │
         ▼
analytics_queries.sql    ← Business intelligence queries
integrity_checks.sql     ← Post-load validation
```

**Data flow:**
1. `config.py` reads credentials from `.env` and constructs the database URL
2. `database_setup.py` defines the ORM schema and runs `CREATE TABLE` on startup
3. `load_data.py` loads the CSV, cleans it, normalizes it into dimension/fact tables, and inserts each table in dependency order
4. SQL scripts are run post-load against the populated database for analytics and validation

---

## Project Structure

```
financecore/
├── financecore_clean.csv       # Source transaction dataset (2,000 rows)
├── config.py                   # Database configuration via environment variables
├── database_setup.py           # SQLAlchemy ORM models + table creation
├── load_data.py                # Full ETL pipeline: clean → normalize → insert
├── analytics_queries.sql       # Business analytics SQL queries
├── integrity_checks.sql        # Post-load data integrity validation
├── .gitignore                  # Ignores .env, __pycache__, venv
├── .env                        # ⚠️ Not committed — see Configuration section
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 15 running locally or remotely
- `pip` and `venv`

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/zakariabahtani35-prog/financecore-data-warehouse
cd financecore

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install sqlalchemy psycopg2-binary pandas python-dotenv

# 4. Configure environment variables (see Configuration section)
cp .env.example .env
# Edit .env with your database credentials

# 5. Create the database in PostgreSQL
psql -U postgres -c "CREATE DATABASE financecore;"

# 6. Create tables
python database_setup.py

# 7. Run the ETL pipeline
python load_data.py
```

---

## Configuration

Create a `.env` file at the project root. **Never commit this file.**

```dotenv
# .env — Database credentials
# PostgreSQL connection settings

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost          # Default: localhost
DB_PORT=5432               # Default: 5432
DB_NAME=financecore
```

`config.py` reads these values at runtime and assembles the `DATABASE_URL`:

```
postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
```

The `.gitignore` is already configured to exclude `.env`, `venv/`, and `__pycache__/`.

---

## Usage

### Run the full pipeline

```bash
python load_data.py
```

Expected output:
```
2025-xx-xx INFO - CSV loaded successfully: (2000, 35)
2025-xx-xx INFO - Inserted into clients: 100 rows
2025-xx-xx INFO - Inserted into accounts: 100 rows
2025-xx-xx INFO - Inserted into products: 7 rows
2025-xx-xx INFO - Inserted into agencies: N rows
2025-xx-xx INFO - Inserted into transactions: 2000 rows
2025-xx-xx INFO - Total transactions in DB: 2000
Data pipeline executed successfully.
```

### Run analytics queries

Connect to your PostgreSQL database and execute:

```bash
psql -U your_db_user -d financecore -f analytics_queries.sql
```

### Run integrity checks

```bash
psql -U your_db_user -d financecore -f integrity_checks.sql
```

---

## Example Use Cases

**Agency performance reporting**
Identify which branches process the highest transaction volumes — useful for resource allocation and performance reviews.

**Product-level profitability analysis**
Compare average transaction amounts across products (Compte Épargne, PEA, Crédit Consommation, etc.) to assess product line health.

**Client risk segmentation**
Segment clients by risk tier (Standard, Premium, Risque) and compute rejection rates per segment — a core input for credit risk models.

**Below-average client detection**
Automatically identify clients whose average transaction falls below the global mean — useful for churn prediction or targeted outreach.

**Monthly trend analysis**
Aggregate total transaction volume by month to detect seasonal patterns and revenue cycles.

---

## Database Schema

### `clients`
| Column | Type | Notes |
|---|---|---|
| `client_id` | String | Primary key |
| `segment` | String | Standard / Premium / Risque |
| `score_credit` | Float | Credit score |

### `accounts`
| Column | Type | Notes |
|---|---|---|
| `account_id` | Integer | Primary key (auto-assigned) |
| `client_id` | String | FK → clients |

### `products`
| Column | Type | Notes |
|---|---|---|
| `product_id` | Integer | Primary key |
| `product_name` | String | e.g. PEA, Compte Épargne |

### `agencies`
| Column | Type | Notes |
|---|---|---|
| `agency_id` | Integer | Primary key |
| `agency_name` | String | e.g. Lyon-Part-Dieu |

### `transactions`
| Column | Type | Notes |
|---|---|---|
| `transaction_id` | String | Primary key |
| `account_id` | Integer | FK → accounts |
| `product_id` | Integer | FK → products |
| `agency_id` | Integer | FK → agencies |
| `amount` | Float | Transaction amount |
| `currency` | String | EUR, GBP, etc. |
| `transaction_date` | DateTime | Indexed |
| `status` | String | Complete / Rejete / Unknown |

---

## Analytics Queries

Five prebuilt queries are included:

| Query | Description |
|---|---|
| Agency totals | `SUM(amount)` grouped by agency, descending |
| Product averages | `AVG(amount)` per product |
| Monthly trends | `DATE_TRUNC('month', ...)` aggregation |
| Below-average clients | Subquery with `HAVING AVG < global AVG` |
| Risk segmentation | Rejection rate per client segment |

---

## Performance & Scalability

- **Indexed columns** — `transaction_date`, `account_id`, `agency_id`, and `segment` are all indexed for fast analytical queries
- **Bulk insert via Pandas** — `DataFrame.to_sql()` with `if_exists="append"` performs batch inserts, significantly faster than row-by-row ORM inserts
- **Dependency-ordered insertion** — Tables are inserted in correct FK dependency order (clients → accounts → products → agencies → transactions) to prevent constraint violations
- **Deduplication at load time** — Duplicate `transaction_id` values are dropped before insertion, ensuring idempotent reloads
- **Cascade deletes** — The schema supports safe parent-record deletion without orphaned child rows

---

## Security

- All credentials are stored in `.env` and never hardcoded
- `.gitignore` explicitly excludes `.env` from version control
- SQLAlchemy parameterizes all queries, eliminating SQL injection risk at the ORM layer
- Foreign key constraints with `ondelete="CASCADE"` prevent referential integrity violations
- No external API keys or tokens are required

---

## Roadmap

### Current
- [x] Full ETL pipeline (CSV → PostgreSQL)
- [x] Normalized 5-table relational schema
- [x] Prebuilt analytics and integrity SQL
- [x] Logging and error handling throughout pipeline

### Next
- [ ] Alembic migrations for schema versioning
- [ ] Pytest test suite with mock database fixtures
- [ ] Streamlit or Metabase dashboard for visual analytics
- [ ] Support for incremental loads (upsert logic)

### Future
- [ ] Airflow DAG for scheduled pipeline runs
- [ ] REST API layer (FastAPI) to expose analytics endpoints
- [ ] Docker Compose setup for zero-config local deployment
- [ ] Multi-currency normalization to EUR at load time

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository and create a feature branch: `git checkout -b feature/your-feature`
2. Commit with clear, descriptive messages
3. Ensure your code follows existing style conventions and does not break existing pipeline behavior
4. Open a pull request with a clear description of the change and its motivation

For major changes, open an issue first to discuss the proposed approach.

---

## Testing

Integrity validation is built into the pipeline via `integrity_checks.sql`. To verify the database state after loading:

```bash
psql -U your_db_user -d financecore -f integrity_checks.sql
```

A formal test suite using `pytest` with an in-memory SQLite backend is planned for a future release.

---

## License

This project is licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

---

## Author

**[Your Name]**

[![GitHub](https://img.shields.io/badge/GitHub-your--username-181717?style=flat-square&logo=github)](https://github.com/zakariabahtani35-prog)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-your--profile-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/zakaria-bahtani-b64251390/)
[![Portfolio](https://img.shields.io/badge/Portfolio-your--site-FF5733?style=flat-square)](https://your-portfolio.com)

---

## Acknowledgments

- Dataset structure inspired by real-world North African banking transaction systems
- SQLAlchemy documentation and community for ORM best practices
- Pandas development team for the robust data processing toolchain

---

> *FinanceCore demonstrates that a clean data pipeline is the foundation of every reliable financial system. Good data in — reliable analytics out.*
