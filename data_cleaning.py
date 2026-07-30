import os
import pandas as pd
import numpy as np

# Create processed directory if it doesn't exist
os.makedirs("data/processed", exist_ok=True)

print("Starting Data Cleaning Process...")

# --- 1. Clean nav_history.csv ---
nav_path = "data/raw/02_nav_history.csv" if os.path.exists("data/raw/02_nav_history.csv") else "data/raw/nav_history.csv"
if os.path.exists(nav_path):
    df_nav = pd.read_csv(nav_path)
    # Parse dates
    df_nav['date'] = pd.to_datetime(df_nav['date'])
    # Sort by amfi_code and date
    df_nav = df_nav.sort_values(by=['amfi_code', 'date'])
    # Drop duplicates
    df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
    # Filter out invalid NAV values
    df_nav = df_nav[df_nav['nav'] > 0]
    # Forward fill missing NAV values for holidays/weekends per fund
    df_nav['nav'] = df_nav.groupby('amfi_code')['nav'].ffill()
    df_nav.to_csv("data/processed/02_nav_history.csv", index=False)
    print("✓ nav_history.csv cleaned and saved.")

# --- 2. Clean investor_transactions.csv ---
txn_path = "data/raw/05_investor_transactions.csv" if os.path.exists("data/raw/05_investor_transactions.csv") else "data/raw/investor_transactions.csv"
if os.path.exists(txn_path):
    df_txn = pd.read_csv(txn_path)
    # Standardize transaction_type
    txn_map = {
        'sip': 'SIP', 'SIP': 'SIP',
        'lumpsum': 'Lumpsum', 'Lump Sum': 'Lumpsum', 'Lumpsum': 'Lumpsum',
        'redemption': 'Redemption', 'Redemption': 'Redemption'
    }
    df_txn['transaction_type'] = df_txn['transaction_type'].map(lambda x: txn_map.get(str(x).strip(), x))
    # Validate amount > 0
    df_txn = df_txn[df_txn['amount'] > 0]
    # Standardize date format
    df_txn['transaction_date'] = pd.to_datetime(df_txn['transaction_date']).dt.strftime('%Y-%m-%d')
    # Validate KYC status
    valid_kyc = ['Verified', 'Pending', 'Rejected']
    df_txn['kyc_status'] = df_txn['kyc_status'].apply(lambda x: x if x in valid_kyc else 'Pending')
    df_txn.to_csv("data/processed/05_investor_transactions.csv", index=False)
    print("✓ investor_transactions.csv cleaned and saved.")

# --- 3. Clean scheme_performance.csv ---
perf_path = "data/raw/03_scheme_performance.csv" if os.path.exists("data/raw/03_scheme_performance.csv") else "data/raw/scheme_performance.csv"
if os.path.exists(perf_path):
    df_perf = pd.read_csv(perf_path)
    # Ensure numerical returns
    return_cols = [col for col in df_perf.columns if 'return' in col or 'cagr' in col]
    for col in return_cols:
        df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce').fillna(0)
    # Check expense ratio range (0.1% to 2.5%)
    if 'expense_ratio' in df_perf.columns:
        df_perf['expense_ratio'] = pd.to_numeric(df_perf['expense_ratio'], errors='coerce')
        df_perf['expense_ratio'] = df_perf['expense_ratio'].clip(0.1, 2.5)
    df_perf.to_csv("data/processed/03_scheme_performance.csv", index=False)
    print("✓ scheme_performance.csv cleaned and saved.")

# --- 4. Process Remaining Raw CSV Files ---
for filename in os.listdir("data/raw"):
    if filename.endswith(".csv") and not os.path.exists(f"data/processed/{filename}"):
        df = pd.read_csv(f"data/raw/{filename}")
        df.to_csv(f"data/processed/{filename}", index=False)
        print(f"✓ Copied {filename} to processed directory.")

print("All data cleaning tasks completed!")
