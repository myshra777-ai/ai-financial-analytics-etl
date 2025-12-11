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
df["loaded_at"] = datetime.now()

# ---------------------------------
# Step 3: Load to Postgres
# ---------------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:Mishra%40123@localhost:5432/practice_db"
)

df.to_sql("transactions", con=engine, if_exists="replace", index=False)

engine.dispose()
print("Loaded rows into transactions table:", len(df))
