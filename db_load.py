import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# Database setup
db_name = "bluestock_mf.db"
engine = create_engine(f"sqlite:///{db_name}")

# Execute schema definition
if os.path.exists("sql/schema.sql"):
    with open("sql/schema.sql", "r") as f:
        schema_script = f.read()
    conn = sqlite3.connect(db_name)
    conn.executescript(schema_script)
    conn.close()
    print("✓ SQLite schema created successfully.")

# Map processed CSV files to SQLite tables
table_mappings = {
    "01_fund_master.csv": "dim_fund",
    "02_nav_history.csv": "fact_nav",
    "07_scheme_performance.csv": "fact_performance",
    "08_investor_transactions.csv": "fact_transactions"
}

for csv_file, table_name in table_mappings.items():
    file_path = f"data/processed/{csv_file}"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        
        # Verify row counts match
        row_count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table_name}", engine).iloc[0]['count']
        print(f"✓ Table '{table_name}' loaded. CSV rows: {len(df)} | DB rows: {row_count}")

print("Database ingestion complete!")
