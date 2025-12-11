```markdown
# AI Financial Analytics ETL

Python–PostgreSQL ETL pipeline that ingests synthetic customer subscription data from CSV, cleans and standardizes it, runs basic data-quality checks, and loads it into a `transactions` table for analytics and BI dashboards. [web:270][web:336]

## Project Overview


- **Goal**: Build a simple, reproducible batch ETL pipeline as a foundation for financial analytics and customer insight dashboards. [web:270]  
- **Source**: `Transactions-10000.csv` (10k synthetic customer and subscription records).  
- **Target**: PostgreSQL database (`practice_db`) with a curated `transactions` table.  
- **Tech Stack**: Python, pandas, SQLAlchemy, PostgreSQL. [web:502][web:484]

## Data Flow

1. **Extract**
   - Read `Transactions-10000.csv` from local storage using `pandas.read_csv`. [web:502]  

2. **Transform**
   - Rename raw columns to a clean, analytics-friendly schema:
     - `Index` → `id`
     - `Customer Id` → `customer_id`
     - `First Name` → `first_name`
     - `Last Name` → `last_name`
     - `Company` → `company`
     - `City` → `city`
     - `Country` → `country`
     - `Phone 1` → `phone_primary`
     - `Phone 2` → `phone_secondary`
     - `Email` → `email`
     - `Subscription Date` → `subscription_date`
     - `Website` → `website`  
   - Parse `subscription_date` to a proper datetime column using `pd.to_datetime(..., errors="coerce")`. [web:604][web:610]  
   - Add an audit column `loaded_at` with the current timestamp for data lineage.

3. **Data Quality Checks**
   - Print null counts per column (`df.isnull().sum()`).
   - Print the number of distinct customers (`df["customer_id"].nunique()`).

4. **Load**
   - Connect to PostgreSQL (`practice_db`) via SQLAlchemy. [web:484][web:486]  
   - Write the dataframe into a `transactions` table using `DataFrame.to_sql(if_exists="replace")`. [web:487]

## Schema

Final columns in the `transactions` table:

| Column            | Type        | Description                          |
|-------------------|------------|--------------------------------------|
| id                | int         | Row identifier from the source file |
| customer_id       | text        | Unique customer identifier           |
| first_name        | text        | Customer first name                 |
| last_name         | text        | Customer last name                  |
| company           | text        | Customer company name               |
| city              | text        | City of the customer                |
| country           | text        | Country of the customer             |
| phone_primary     | text        | Primary phone number                |
| phone_secondary   | text        | Secondary phone number (optional)   |
| email             | text        | Customer email address              |
| subscription_date | timestamp   | Subscription start date             |
| website           | text        | Customer website URL                |
| loaded_at         | timestamp   | ETL load timestamp                  |

## How to Run

1. **Prerequisites**

- Python 3.10+  
- PostgreSQL with a database named `practice_db`  
- Packages: `pandas`, `sqlalchemy`, `psycopg2-binary`  

Install dependencies:

```
pip install pandas sqlalchemy psycopg2-binary
```

2. **Configure CSV path and database**

In `user_etl.py`:

```
csv_path = r"C:\Users\myshr\Downloads\Transactions-10000.csv"
```

Update if you place the CSV somewhere else.

Set the Postgres connection:

```
engine = create_engine(
    "postgresql+psycopg2://postgres:<your_password_encoded>@localhost:5432/practice_db"
)
```

If the password contains `@`, encode it as `%40` (e.g., `Mishra@123` → `Mishra%40123`). [web:484]

3. **Run the ETL**

From the project folder:

```
python user_etl.py
```

This will:

- Read the CSV.  
- Rename and clean columns, parse dates, add `loaded_at`.  
- Print basic data-quality stats.  
- Load the data into the `transactions` table in PostgreSQL.

4. **Verify in PostgreSQL**

```
SELECT * FROM transactions LIMIT 5;
SELECT COUNT(*) AS row_count,
       COUNT(DISTINCT customer_id) AS distinct_customers
FROM transactions;
``` [web:609][web:613]

## Next Steps / Roadmap

- Add derived features (e.g., `customer_tenure_days` from `subscription_date`).  
- Implement more robust validation (duplicate detection, country whitelist checks). [web:327]  
- Move the CSV into the repo under `data/transactions.csv` and parameterize the file path.  
- Connect PostgreSQL to Power BI and build a **Financial Analytics Dashboard** for customer and subscription analytics. [web:336]
```