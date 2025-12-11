import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ---------------------------------
# Step 1: Extract
# ---------------------------------
csv_path = r"C:\Users\myshr\Downloads\Transactions-10000.csv"
print("Reading from:", csv_path)
df = pd.read_csv(csv_path)

print("Sample rows:")
print(df.head())
print("Columns:", df.columns)
print("Row count:", len(df))

# ---------------------------------
# Step 2: Transform
# ---------------------------------
# Rename columns to snake_case
df = df.rename(columns={
    "Index": "id",
    "Customer Id": "customer_id",
    "First Name": "first_name",
    "Last Name": "last_name",
    "Company": "company",
    "City": "city",
    "Country": "country",
    "Phone 1": "phone_primary",
    "Phone 2": "phone_secondary",
    "Email": "email",
    "Subscription Date": "subscription_date",
    "Website": "website",
})

# Parse subscription_date as proper datetime
df["subscription_date"] = pd.to_datetime(df["subscription_date"], errors="coerce")

# Add audit column
df["loaded_at"] = datetime.now()

# Basic data quality checks
print("Nulls per column:")
print(df.isnull().sum())

print("Distinct customers:", df["customer_id"].nunique())


# ---------------------------------
# Step 3: Load to Postgres
# ---------------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:Mishra%40123@localhost:5432/practice_db"
)

df.to_sql("transactions", con=engine, if_exists="replace", index=False)

engine.dispose()
print("Loaded rows into transactions table:", len(df))
